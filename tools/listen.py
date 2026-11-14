#!/usr/bin/env python3
"""Listening check for the recorded narration: a speech recogniser hears every recorded sentence, and what it
heard is compared with the card BY SOUND (both go through the same pronunciation engine, so spelling, number
style and hyphens do not count as differences).

Nobody can proof-listen eight hours of audio after every change. This finds the sentences worth a human ear:
a dropped word, a garbled word, a number read wrongly, silence.

    <venv python> tools/listen.py --setup            # one time: recogniser (pip) and its model, about 700 MB
    <venv python> tools/listen.py                    # hear every recording not heard yet, then report
    <venv python> tools/listen.py --cards c02-s07    # only these cards
    <venv python> tools/listen.py --report           # report again from what was already heard

<venv python> is the one tools/narrate.py --setup made. What was heard is kept in <home>/heard.json.
A flagged sentence is not proof of a fault: the recogniser mishears rare words (miticide, FIFRA) often.
Look at what it heard. Words missing from the middle or the end of a sentence are the real finds.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tarfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import narrate  # noqa: E402

HOME = narrate.HOME
MODEL_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8.tar.bz2'
MODEL = HOME / 'asr' / 'sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8'
HEARD = HOME / 'heard.json'
SR = 16000
FOLD = str.maketrans({'T': 't', 'ᵊ': 'ə', 'ᵻ': 'ɪ', 'ɐ': 'ə', 'ɾ': 't'})


def setup():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'sherpa-onnx', 'rapidfuzz'])
    if not (MODEL / 'tokens.txt').exists():
        (HOME / 'asr').mkdir(parents=True, exist_ok=True)
        tar = HOME / 'asr' / 'model.tar.bz2'
        subprocess.check_call(['curl', '-f', '-sS', '-L', '-o', str(tar), MODEL_URL])
        with tarfile.open(tar) as t:
            t.extractall(HOME / 'asr', filter='data')
        tar.unlink()
    print('ready')


def sound(text):
    """The sounds of a sentence as one string: stress, spaces and punctuation removed."""
    if not text:
        return ''
    return re.sub(r'[^a-zA-Zæðŋɑɔəɛɜɡɪɹʃʊʌʒʤʧθ]', '', narrate.phonemize(text)[0].translate(FOLD))


def hear(cards, threads):
    import numpy as np
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=str(MODEL / 'encoder.int8.onnx'), decoder=str(MODEL / 'decoder.int8.onnx'), joiner=str(MODEL / 'joiner.int8.onnx'),
        tokens=str(MODEL / 'tokens.txt'), num_threads=threads, model_type='nemo_transducer')
    manifest = narrate.read_manifest()
    sections = {s['id']: s for s in narrate.load_sections()}
    heard = json.loads(HEARD.read_text()) if HEARD.exists() else {}
    done = 0
    for sid, e in manifest['cards'].items():
        if (cards and sid not in cards) or sid not in sections or heard.get(sid, {}).get('p') == e['p']:
            continue
        mp3 = narrate.OUT / f'{sid}.mp3'
        lines = narrate.spoken_lines(sections[sid])
        if not mp3.exists() or narrate.text_hash(lines) != e['h']:
            continue
        pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp3), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                                           capture_output=True).stdout, dtype='<f4')
        out = []
        for i in range(len(lines)):
            a, b = e['t'][2 * i], e['t'][2 * i + 1]
            seg = pcm[max(0, int((a - 150) * SR / 1000)): int((b + 250) * SR / 1000)]
            # one sentence at a time: decoding several together garbles the short ones
            st = rec.create_stream()
            st.accept_waveform(SR, np.concatenate([np.zeros(SR // 4, dtype=np.float32), seg, np.zeros(SR // 4, dtype=np.float32)]))
            rec.decode_stream(st)
            out.append(st.result.text.strip())
        heard[sid] = {'p': e['p'], 'lines': out}
        done += 1
        if done % 5 == 0:
            HEARD.write_text(json.dumps(heard, ensure_ascii=False))
            print(done, 'cards heard', flush=True)
    HEARD.write_text(json.dumps(heard, ensure_ascii=False))
    print(done, 'cards heard now;', len(heard), 'in', HEARD)


def report(cards, cut):
    from rapidfuzz.distance import Levenshtein
    manifest = narrate.read_manifest()
    sections = {s['id']: s for s in narrate.load_sections()}
    heard = json.loads(HEARD.read_text()) if HEARD.exists() else {}
    narrate._init(1, voice=False)
    rows, total, wrong, ncards = [], 0, 0, 0
    for sid, h in heard.items():
        e = manifest['cards'].get(sid)
        if not e or e['p'] != h['p'] or sid not in sections or (cards and sid not in cards):
            continue
        ncards += 1
        for i, ((_, raw), got) in enumerate(zip(narrate.spoken_lines(sections[sid]), h['lines'])):
            shown = narrate.plain(raw)
            a, b = sound(shown), sound(got)
            ops = Levenshtein.editops(a, b)
            lost = sum(1 for o in ops if o.tag == 'delete')
            total += len(a)
            wrong += len(ops)
            if len(a) and (len(ops) / len(a) > cut and len(ops) >= 3 or lost >= 6):
                rows.append((len(ops) / len(a), sid, i, len(ops), len(a), lost, shown, got))
    missing = [sid for sid in manifest['cards'] if sid in sections and heard.get(sid, {}).get('p') != manifest['cards'][sid]['p']]
    print(f'{ncards} cards heard, sound error rate {100 * wrong / max(1, total):.2f}% ({wrong} of {total} sounds). '
          f'{len(rows)} sentences flagged. {len(missing)} recordings not heard yet.')
    for rate, sid, i, d, n, lost, shown, got in sorted(rows, reverse=True):
        print(f'\n{sid} sentence {i}: {d} of {n} sounds differ, {lost} missing')
        print('  card :', shown)
        print('  heard:', got)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--setup', action='store_true')
    ap.add_argument('--cards', default='')
    ap.add_argument('--report', action='store_true', help='do not listen, only report')
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--cut', type=float, default=0.12, help='flag a sentence when this share of its sounds differ')
    a = ap.parse_args()
    if a.setup:
        return setup()
    cards = {c.strip() for c in a.cards.split(',') if c.strip()}
    if not a.report:
        hear(cards, a.threads)
    report(cards, a.cut)


if __name__ == '__main__':
    main()
