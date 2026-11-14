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
    <venv python> tools/listen.py --shard 0/4 &      # four of these (0/4 .. 3/4) hear four times as fast;
                                                     # each needs about 2.5 GB of memory. Then --report.
    <venv python> tools/listen.py --probe 'c02-s07#9#fqpa'    # settle a flag: sentence 9 of that card, the word FQPA

<venv python> is the one tools/narrate.py --setup made. What was heard is kept in <home>/heard*.json.

Every sentence is heard on its own. The recogniser now and then drops a word that is plainly in the audio
(an acronym in brackets, the last word, once a whole sentence), and hears it when the cut around the sentence
is a little wider. So a sentence that differs from the card is heard a second time on a wider cut and the
better of the two counts. Only a sentence that differs both times is flagged.

A flagged sentence is still not proof of a fault: the recogniser mishears rare words (miticide, FIFRA) and
writes numbers its own way. Look at what it heard. Words missing from the middle or the end are the real finds.
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
NOT_SOUND = re.compile(r'[^a-zA-Zæðŋɑɔəɛɜɡɪɹʃʊʌʒʤʧθ]')
AGAIN = 3          # a sentence with this many sounds different is heard a second time


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
    return NOT_SOUND.sub('', narrate.phonemize(text)[0].translate(FOLD))


def word_sounds(text):
    """[spoken word, its sounds] for every word of a card sentence, in order."""
    ph, words = narrate.phonemize(text)
    return [(w[0].strip(), NOT_SOUND.sub('', ph[w[1]:w[2]].translate(FOLD))) for w in words]


def as_heard(got):
    """What the recogniser wrote, ready to be read back. It sometimes writes a whole heading in capitals;
    read as written, every such word would be spelled out letter by letter."""
    return got.lower() if got.isupper() and len(re.findall(r'[A-Z]{4,}', got)) >= 2 else got


def heard_sound(got):
    return sound(as_heard(got))


def differ(want, got):
    """(sounds that differ, sounds of the card that are missing) for one sentence."""
    from rapidfuzz.distance import Levenshtein
    ops = Levenshtein.editops(want, heard_sound(got))
    return len(ops), sum(1 for o in ops if o.tag == 'delete')


def odd_words(shown, got):
    """(words of the card with none of their sounds in what was heard, words heard with none of their sounds
    on the card). Words of one sound are left out of the first list, and words under three sounds out of the
    second: the recogniser drops and invents "a" and "the" too often for those to mean anything."""
    from rapidfuzz.distance import Levenshtein
    ws, hs = word_sounds(shown), word_sounds(as_heard(got)) if got else []
    ops = Levenshtein.editops(''.join(x for _, x in ws), ''.join(x for _, x in hs))
    gone = {o.src_pos for o in ops if o.tag == 'delete'}
    added = {o.dest_pos for o in ops if o.tag == 'insert'}
    out = []
    for words, marks, least in ((ws, gone, 2), (hs, added, 3)):
        found, pos = [], 0
        for word, x in words:
            if len(x) >= least and all(k in marks for k in range(pos, pos + len(x))):
                found.append(word)
            pos += len(x)
        out.append(found)
    return out


UNITS = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
TEENS = {'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16,
         'seventeen': 17, 'eighteen': 18, 'nineteen': 19}
TENS = {'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90}
ORDINALS = {'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8,
            'ninth': 9, 'tenth': 10, 'eleventh': 11, 'twelfth': 12, 'thirteenth': 13, 'fourteenth': 14, 'fifteenth': 15,
            'sixteenth': 16, 'seventeenth': 17, 'eighteenth': 18, 'nineteenth': 19, 'twentieth': 20}
ROMAN = {'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6', 'X': '10'}


def numbers(text):
    """The numbers in a sentence, in order, as digit strings; number words count ("one seventy" gives 1, 70).
    Joined together they are the sentence's digits: "40 CFR Part 170" and "forty CFR part one seventy" agree."""
    text = re.sub(r'\[([^\]]*)\]\(/[^/]*/\)', r'\1', text)          # [word](/phonemes/) -> word
    text = re.sub(r'(\d)\.0+(?=\s*(?:%|percent|per cent))', r'\1', text)   # "78.00%" is read "78 percent"
    text = re.sub(r'(\d)(st|nd|rd|th)\b', r'\1', text)
    # the recogniser likes "Class I" and "Chapter X"; a lone I, V or X counts only after such a word ("O V" is not 5)
    text = re.sub(r'\b(III|II|IV|VI)\b', lambda m: ROMAN[m.group(1)], text)
    text = re.sub(r'(?i)\b(class|chapter|group|category|part|type|section)\s+(I|V|X)\b', lambda m: m.group(1) + ' ' + ROMAN[m.group(2).upper()], text)
    out, st = [], {'on': False, 'total': 0, 'cur': 0, 'last': ''}

    def flush():
        if st['on']:
            out.append(str(st['total'] + st['cur']))
        st.update(on=False, total=0, cur=0, last='')

    def start(v, kind):
        flush()
        st.update(on=True, total=0, cur=v, last=kind)

    for tok in re.findall(r'[a-z]+|\d+', text.lower()):
        after_big = st['on'] and st['last'] in ('hundred', 'thousand')
        if tok.isdigit():
            flush()
            out.append(tok)
        elif tok in UNITS:
            if st['on'] and st['last'] == 'tens' and UNITS[tok] or after_big:
                st['cur'] += UNITS[tok]
                st['last'] = 'unit+'
            else:
                start(UNITS[tok], 'unit')
        elif tok in TEENS or tok in TENS:
            v, kind = (TEENS[tok], 'teen') if tok in TEENS else (TENS[tok], 'tens')
            if after_big:
                st['cur'] += v
                st['last'] = kind
            else:
                start(v, kind)
        elif tok == 'hundred':
            if st['on'] and 1 <= st['cur'] <= 99 and st['last'] != 'hundred':
                st['cur'] *= 100
                st['last'] = 'hundred'
            else:
                start(100, 'hundred')
        elif tok == 'thousand':
            if st['on'] and st['cur'] and st['last'] != 'thousand':
                st['total'] += st['cur'] * 1000
                st['cur'] = 0
                st['last'] = 'thousand'
            else:
                start(1000, 'thousand')
        elif tok == 'and' and st['on'] and st['last'] == 'hundred':
            continue
        elif tok in ORDINALS:
            if st['on'] and st['last'] == 'tens' and ORDINALS[tok] < 10:
                st['cur'] += ORDINALS[tok]                    # "twenty first"
                flush()
            else:
                flush()
                out.append(str(ORDINALS[tok]))
        else:
            flush()
    flush()
    return out


NUMBER_CASES = [('forty CFR Part One Seventy', '40170'), ('40 CFR Part 170', '40170'), ('one hundred seventy', '170'),
                ('nineteen ninety six', '1996'), ('twenty point nine percent', '209'), ('1 8 8 8 4 2 6', '1888426'),
                ('two thousand five hundred', '2500'), ('fifty states', '50'), ('fifteen feet', '15'),
                ('a hundred and five', '105'), ('1,000 feet', '1000'), ('the 21st century', '21'),
                ('the twenty first century', '21'), ('Hazard Class I', '1'), ('Chapter X', '10'), ('78.00%', '78'),
                ('the O V cartridge', ''), ('select, I wear that', ''), ('Gasoline III, Poison VI', '36')]


def all_heard(manifest):
    """Everything heard so far, from the main file and from any shard files. When two files hold a card,
    the one that matches the current recording wins, then the one whose doubtful sentences got a second hearing."""
    out, rank = {}, {}
    for f in sorted(HOME.glob('heard*.json')):
        try:
            d = json.loads(f.read_text())
        except ValueError:
            continue
        for sid, h in d.items():
            r = (h.get('p') == manifest['cards'].get(sid, {}).get('p'), 'second' in h)
            if sid not in out or r >= rank[sid]:
                out[sid], rank[sid] = h, r
    return out


def hear(cards, threads, shard=None):
    import numpy as np
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=str(MODEL / 'encoder.int8.onnx'), decoder=str(MODEL / 'decoder.int8.onnx'), joiner=str(MODEL / 'joiner.int8.onnx'),
        tokens=str(MODEL / 'tokens.txt'), num_threads=threads, model_type='nemo_transducer')
    narrate._init(1, voice=False)
    manifest = narrate.read_manifest()
    sections = {s['id']: s for s in narrate.load_sections()}
    path = HOME / f'heard.{shard[0]}.json' if shard else HEARD
    before = all_heard(manifest)
    heard = json.loads(path.read_text()) if path.exists() else {}
    done = 0

    def decode(pcm, x0, x1):
        # one sentence at a time: decoding several together garbles the short ones
        seg = pcm[max(0, int(x0 * SR / 1000)): max(0, int(x1 * SR / 1000))]
        st = rec.create_stream()
        st.accept_waveform(SR, np.concatenate([np.zeros(SR // 4, dtype=np.float32), seg, np.zeros(SR // 4, dtype=np.float32)]))
        rec.decode_stream(st)
        return st.result.text.strip()

    for n, (sid, e) in enumerate(manifest['cards'].items()):
        if shard and n % shard[1] != shard[0]:
            continue
        old = before.get(sid) if before.get(sid, {}).get('p') == e['p'] else None
        if (cards and sid not in cards) or sid not in sections or (old and 'second' in old):
            continue
        mp3 = narrate.OUT / f'{sid}.mp3'
        lines = narrate.spoken_lines(sections[sid])
        if not mp3.exists() or narrate.text_hash(lines) != e['h']:
            continue
        pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(mp3), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                                           capture_output=True).stdout, dtype='<f4')
        first = old['lines'] if old and len(old['lines']) == len(lines) else None      # heard before, never re-checked
        out, second = [], []
        for i, (_, raw) in enumerate(lines):
            a, b = e['t'][2 * i], e['t'][2 * i + 1]
            got = first[i] if first else decode(pcm, a - 150, b + 250)
            want = sound(narrate.plain(raw))
            d = differ(want, got)[0]
            if d >= AGAIN:
                # a second hearing, on a cut that runs on to just before the next sentence
                nxt = e['t'][2 * i + 2] if i + 1 < len(lines) else e['d']
                got2 = decode(pcm, a - 300, nxt - 40)
                if differ(want, got2)[0] < d:
                    got = got2
                    second.append(i)
            out.append(got)
        heard[sid] = {'p': e['p'], 'lines': out, 'second': second}
        done += 1
        if done % 5 == 0:
            path.write_text(json.dumps(heard, ensure_ascii=False))
            print(done, 'cards heard', flush=True)
    path.write_text(json.dumps(heard, ensure_ascii=False))
    print(done, 'cards heard now;', len(heard), 'in', path)


def report(cards, cut):
    manifest = narrate.read_manifest()
    sections = {s['id']: s for s in narrate.load_sections()}
    heard = all_heard(manifest)
    narrate._init(1, voice=False)
    for text, want in NUMBER_CASES:
        assert ''.join(numbers(text)) == want, (text, numbers(text), want)
    rows, words, nums, total, wrong, ncards, nlines, twice, unchecked, numbered = [], [], [], 0, 0, 0, 0, 0, 0, 0
    for sid, h in heard.items():
        e = manifest['cards'].get(sid)
        if not e or e['p'] != h['p'] or sid not in sections or (cards and sid not in cards):
            continue
        ncards += 1
        unchecked += 'second' not in h
        for i, ((_, raw), got) in enumerate(zip(narrate.spoken_lines(sections[sid]), h['lines'])):
            shown = narrate.plain(raw)
            a = sound(shown)
            d, lost = differ(a, got)
            nlines += 1
            total += len(a)
            wrong += d
            # numbers get their own check: by sound, "fifteen" for "fifty" is one sound out
            n1, n2 = numbers(narrate.say(shown)), numbers(got)
            numbered += bool(n1)
            if ''.join(n1) != ''.join(n2):
                nums.append((sid, i, n1, n2, shown, got))
            if len(a) and (d / len(a) > cut and d >= 3 or lost >= 6):
                rows.append((d / len(a), sid, i, d, len(a), lost, shown, got))
            else:
                twice += i in h.get('second', [])
                if d >= 2:
                    gone, extra = odd_words(shown, got)
                    if gone or extra:
                        words.append((sid, i, gone, extra, shown, got))
    missing = [sid for sid in manifest['cards'] if sid in sections and (not cards or sid in cards)
               and heard.get(sid, {}).get('p') != manifest['cards'][sid]['p']]
    print(f'{ncards} cards, {nlines} sentences heard. Sound error rate {100 * wrong / max(1, total):.2f}% ({wrong} of {total} sounds). '
          f'{len(rows)} sentences flagged. {twice} more matched only on the second, wider hearing (the recogniser, not the voice). '
          f'{len(missing)} recordings not heard yet.'
          + (f' {unchecked} cards were heard before the second hearing existed: run without --report to finish them.' if unchecked else ''))
    for rate, sid, i, d, n, lost, shown, got in sorted(rows, reverse=True):
        print(f'\n{sid} sentence {i}: {d} of {n} sounds differ, {lost} missing')
        print('  card :', shown)
        print('  heard:', got)
    if words:
        print(f'\n{len(words)} more sentences are close to the card, but a whole word was not heard, or a word was heard '
              'that the card does not have. An acronym in brackets, or the first or last word, is the usual case and '
              'is the recogniser. A missing "not", a wrong number or a repeated word would matter:')
    for sid, i, gone, extra, shown, got in words:
        print(f'\n{sid} sentence {i}:' + (f' not heard: {", ".join(gone)}.' if gone else '') + (f' Heard but not on the card: {", ".join(extra)}.' if extra else ''))
        print('  card :', shown)
        print('  heard:', got)
    print(f'\nNumbers: {numbered} sentences have a number. In {len(nums)} of them the digits heard are not the digits on the card'
          + (' (a Roman numeral, a number written out its own way, or a real slip: read them):' if nums else '.'))
    for sid, i, n1, n2, shown, got in nums:
        print(f'\n{sid} sentence {i}: card {" ".join(n1) or "none"}; heard {" ".join(n2) or "none"}')
        print('  card :', shown)
        print('  heard:', got)


def probe(targets, threads, whisper):
    """A close look at single sentences, to settle a flag. A target is card#sentence, or card#sentence#word,word
    to look at those words. It prints how long and how loud each word is in the recording (a word the voice
    skipped has no length or no sound), then what is heard on the tight cut, on the wide cut, and on narrow cuts
    around the named words. A word that shows up in a narrow cut is in the audio.

    --whisper DIR adds a second recogniser's opinion. DIR holds a sherpa-onnx Whisper model, for example the
    unpacked sherpa-onnx-whisper-small.en.tar.bz2 (640 MB) from the same release page as MODEL_URL.
    Whisper guesses words it expects, so trust it for "is the word there", not for "is the word exact"."""
    import numpy as np
    import sherpa_onnx
    recs = {'parakeet': sherpa_onnx.OfflineRecognizer.from_transducer(
        encoder=str(MODEL / 'encoder.int8.onnx'), decoder=str(MODEL / 'decoder.int8.onnx'), joiner=str(MODEL / 'joiner.int8.onnx'),
        tokens=str(MODEL / 'tokens.txt'), num_threads=threads, model_type='nemo_transducer')}
    if whisper:
        first = lambda pattern: str(sorted(pathlib.Path(whisper).glob(pattern))[0])
        recs['whisper'] = sherpa_onnx.OfflineRecognizer.from_whisper(
            encoder=first('*encoder.int8.onnx'), decoder=first('*decoder.int8.onnx'), tokens=first('*tokens.txt'),
            language='en', task='transcribe', num_threads=threads)
    manifest = narrate.read_manifest()
    sections = {s['id']: s for s in narrate.load_sections()}
    quiet = np.zeros(SR // 4, dtype=np.float32)
    for target in targets:
        sid, i, *rest = target.split('#')
        i = int(i)
        names = [n.lower() for n in rest[0].split(',') if n] if rest else []
        e = manifest['cards'][sid]
        raw = narrate.spoken_lines(sections[sid])[i][1]
        pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', str(narrate.OUT / f'{sid}.mp3'), '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                                           capture_output=True).stdout, dtype='<f4')
        a, b = e['t'][2 * i], e['t'][2 * i + 1]
        nxt = e['t'][2 * i + 2] if 2 * i + 2 < len(e['t']) else e['d']

        def cut(x0, x1):
            return pcm[max(0, int(x0 * SR / 1000)): max(0, int(x1 * SR / 1000))]

        def hear(x0, x1):
            seg = cut(x0, x1)
            if len(seg) < SR // 10:
                return '(too short to hear)'
            out = []
            for name, rec in recs.items():
                st = rec.create_stream()
                st.accept_waveform(SR, np.concatenate([quiet, seg, quiet]))
                rec.decode_stream(st)
                out.append((name + ': ' if len(recs) > 1 else '') + st.result.text.strip())
            return ' | '.join(out)

        def loud(x0, x1):
            seg = cut(x0, x1).astype(np.float64)
            return float(np.sqrt((seg ** 2).mean())) if len(seg) else 0.0

        whole = loud(a, b) or 1e-6
        words, starts = narrate.display_words(raw), e['w'][i]
        ends = starts[1:] + [b - a]
        print(f'\n{sid} sentence {i}: {a} to {b} ms of the recording')
        print('  card :', narrate.plain(raw))
        print('  asked:', narrate.say(narrate.plain(raw)))
        print('  tight cut:', hear(a - 150, b + 250))
        print('  wide cut :', hear(a - 300, nxt - 40))
        hits = [k for k, w in enumerate(words) if any(n in w.lower() for n in names)]
        show = sorted({j for k in hits for j in range(max(0, k - 3), min(len(words), k + 4))}) if names else range(len(words))
        for k in show:
            print(f'   {"*" if k in hits else " "} {words[k]!r:26} {starts[k]:6} to {ends[k]:6} ms ({ends[k] - starts[k]:5} ms), '
                  f'loudness {loud(a + starts[k], a + ends[k]) / whole:.2f} of the sentence')
        for k in hits:
            for back, on in ((3, 4), (1, 2), (0, 1)):
                k0, k1 = max(0, k - back), min(len(words), k + on)
                print(f'    around "{" ".join(words[k0:k1])}": {hear(a + starts[k0] - 120, a + ends[k1 - 1] + 120)}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--setup', action='store_true')
    ap.add_argument('--cards', default='')
    ap.add_argument('--report', action='store_true', help='do not listen, only report')
    ap.add_argument('--threads', type=int, default=4)
    ap.add_argument('--cut', type=float, default=0.12, help='flag a sentence when this share of its sounds differ')
    ap.add_argument('--shard', default='', metavar='K/N', help='hear only every Nth card, starting at K (run N of these side by side)')
    ap.add_argument('--probe', nargs='+', default=[], metavar='CARD#SENTENCE[#WORD,WORD]', help='a close look at single sentences')
    ap.add_argument('--whisper', default='', metavar='DIR', help='with --probe: a sherpa-onnx Whisper model for a second opinion')
    a = ap.parse_args()
    if a.setup:
        return setup()
    if a.probe:
        return probe(a.probe, a.threads, a.whisper)
    cards = {c.strip() for c in a.cards.split(',') if c.strip()}
    if a.shard:
        k, n = (int(x) for x in a.shard.split('/'))
        return hear(cards, a.threads, (k, n))
    if not a.report:
        hear(cards, a.threads)
    report(cards, a.cut)


if __name__ == '__main__':
    main()
