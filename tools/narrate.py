#!/usr/bin/env python3
"""Record natural-voice narration for the study cards (Kokoro TTS; runs on a CPU at about 4x real time).

    python3 tools/narrate.py --setup               # one time: Python venv, voice model, word lists (about 700 MB)
    <home>/venv/bin/python tools/narrate.py        # record every card that is missing or out of date
        --chapters ch01,ch02    --cards c01-s01,c03-s02    --jobs 3    --force    --list    --new-first
        --say "LD50 is 25 mg/kg"                   # show how a sentence will be read (text, then phonemes)
        --words                                    # every word the engine had to guess, for a pronunciation check
        --check                                    # the rules still respell tools/say_cases.json as recorded there
        --files 55                                 # the Artifact "files" maps for publishing, in batches of 55 MB
        --stage DIR                                # copy the audio into DIR under its published names (for local tests)

<home> is ~/.cache/pest-study-tts, or $NARRATE_HOME.

Output:
    dist/audio/<card id>.mp3    one file per card, 24 kHz mono MP3. Not in git. Published next to the page
                                as supporting files (Artifact tool, "files": {"audio/c01-s01.mp3": ...}).
    content/narration.json      per card: hash of its text, length, start and end of every spoken line, and
                                the start of every word. In git. tools/build.py puts it inside the page.

The page plays a card's recording only if the hash of the card's text still matches, so a card whose text
changed falls back to the live voices until it is recorded again. Pronunciation rules are in say() below.
"""
import argparse
import difflib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist' / 'audio'
MANIFEST = ROOT / 'content' / 'narration.json'
HOME = pathlib.Path(os.environ.get('NARRATE_HOME', pathlib.Path.home() / '.cache' / 'pest-study-tts'))
# The v1.1 export reports how long every phoneme lasts. That is what gives each word an exact start time.
MODEL_URL = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/'
SPACY_MODEL = 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl'
MODEL, VOICES = 'kokoro-v1.0.onnx', 'voices-v1.0.bin'
SR = 24000
VOICE, SPEED, BITRATE = 'af_heart', 1.0, '40k'
RENDER = 2          # raise to record everything again after changing how audio is made
MAX_PHONEMES = 420  # the model takes 510 at most; longer lines are cut at a clause

# ---------------------------------------------------------------- spoken lines (mirrors app/template.html)

def plain(t):
    return ' '.join(str(t).replace('**', '').split())


def spoken_lines(s):
    """(kind, text as written in the content) for every sentence the page reads, in the page's order."""
    figs = {f['id']: f for f in s.get('figures', [])}
    out = []

    def fig(fid):
        f = figs[fid]
        t = f['title']
        out.append(('fig', t if re.search(r'[.!?:]$', t) else t + '.'))
        out.extend(('exp', e) for e in f.get('explain', []))

    for b in s.get('body', []):
        if b.get('h'):
            out.append(('h', b['h']))
        elif 'box' in b:
            out.append(('box', b['box']))
            for k, kind in (('p', 'p'), ('list', 'li'), ('ol', 'li')):
                out.extend((kind, t) for t in b.get(k, []))
        elif 'p' in b:
            out.extend(('p', t) for t in b['p'][:-1])
            out.extend(('pend', t) for t in b['p'][-1:])
        elif 'list' in b:
            out.extend(('li', t) for t in b['list'])
        elif 'ol' in b:
            out.extend(('li', t) for t in b['ol'])
        elif 'fig' in b:
            fig(b['fig'])
        elif 'gallery' in b:
            for fid in b['gallery']:
                fig(fid)
    return out


def display_words(t):
    """The words the page wraps in <span class="w">, in order. Same splitting as sentence() in the page."""
    out = []
    for seg in re.split(r'(\*\*[^*]+\*\*)', str(t)):
        if not seg:
            continue
        txt = seg[2:-2] if seg.startswith('**') and seg.endswith('**') else seg
        out.extend(p for p in re.split(r'\s+', txt) if p)
    return out


def fnv(text):
    """FNV-1a, 32 bit, over UTF-16 code units. The page has the same function."""
    h = 0x811c9dc5
    data = text.encode('utf-16-le')
    for i in range(0, len(data), 2):
        h ^= data[i] | (data[i + 1] << 8)
        h = (h * 0x01000193) & 0xffffffff
    return format(h, '08x')


def text_hash(lines):
    return fnv('\n'.join(plain(t) for _, t in lines))


def render_hash(lines):
    return fnv('\n'.join(say(plain(t)) for _, t in lines) + f'|{VOICE}|{SPEED}|{BITRATE}|{RENDER}')

# ---------------------------------------------------------------- how things are pronounced
# The engine (misaki) knows ordinary words, reads all-caps tokens it does not know letter by letter, and
# reads numbers, years, decimals and percentages. Everything it gets wrong for this manual is fixed here.
# Phonemes use misaki's alphabet: A=ay, I=eye, O=oh, W=ow, Y=oy, T=soft t, ᵊ=weak vowel.

PHONEMES = {
    # said as words
    'FIFRA': 'fˈɪfɹə', 'NIOSH': 'nˈIɑʃ', 'CHEMTREC': 'kˈɛmtɹɛk', 'MSHA': 'ˈɛmʃə',
    'PELIGRO': 'pɛlˈiɡɹO', 'AVISO': 'ɑvˈisO', 'Cyfluthrin': 'sIflˈuθɹɪn',
    # spelled out, where the engine would say a word ("dot", "he", "lo", "ox", "me", "sigh") or wavers
    'DOT': 'dˌiˌOtˈi', 'HE': 'ˌAʧˈi', 'LO': 'ˌɛlˈO', 'OX': 'ˌOˈɛks', 'ME': 'ˌɛmˈi', 'NPIC': 'ˌɛnpˌiˌIsˈi',
    'psi': 'pˌiˌɛsˈI', 'Cs': 'sˈiz',
}
# Words the engine guesses wrong. Matched in any letter case; a plural s is added by rule.
TERMS = {
    'recordkeeping': 'ɹˈɛkəɹdkˌipɪŋ', 'miticide': 'mˈITəsˌId', 'avicide': 'ˈAvəsˌId', 'predacide': 'pɹˈɛdəsˌId',
    'thuringiensis': 'θˌʊɹɪnʤiˈɛnsɪs', 'viton': 'vˈItɑn', 'azadirachtin': 'əzˌædəɹˈæktɪn',
    'chemosterilant': 'kˌimOstˈɛɹələnt', 'chlorophenoxy': 'klˌɔɹOfənˈɑksi', 'cyfluthrin': 'sIflˈuθɹɪn',
    'dicamba': 'dIkˈæmbə', 'diethyl': 'dIˈɛθᵊl', 'di-sulfate': 'dIsˈʌlfAt', 'eductor': 'ɪdˈʌktəɹ',
    'galactothion': 'ɡəlˌæktəθˈIɑn', 'ichneumonid': 'ɪknˈumənɪd', 'phytotoxicity': 'fˌITOtɑksˈɪsəTi',
    'photodegradation': 'fˌOTOdˌɛɡɹədˈAʃən', 'preharvest': 'pɹihˈɑɹvəst', 'preplant': 'pɹiplˈænt',
    'prerinse': 'pɹiɹˈɪns', 'preslaughter': 'pɹislˈɔTəɹ', 'preslurry': 'pɹislˈɜɹi', 'prewash': 'pɹiwˈɑʃ',
    'prefilter': 'pɹifˈɪltəɹ', 'preheated': 'pɹihˈiTᵻd', 'premeasured': 'pɹimˈɛʒəɹd',
    'recertification': 'ɹˌisɜɹTəfəkˈAʃən', 'refiller': 'ɹifˈɪləɹ', 'reregistration': 'ɹˌiɹɛʤəstɹˈAʃən',
    'replanting': 'ɹiplˈæntɪŋ', 'safener': 'sˈAfənəɹ', 'acquavella': 'ˌækwəvˈɛlə',
    'peligro': 'pɛlˈiɡɹO', 'aviso': 'ɑvˈisO', 'phosphorothiate': 'fˌɑsfəɹəθˈIAt',
    'breathed': 'bɹˈiðd', 'postapplication': 'pˌOstæpləkˈAʃən',
    # words with two pronunciations that mean one thing in this manual: a tear is a rip, wind is moving air,
    # discard and decreases are verbs, records are papers
    'tear': 'tˈɛɹ', 'wind': 'wˈɪnd', 'discard': 'dəskˈɑɹd', 'arsenic': 'ˈɑɹsᵊnɪk', 'records': 'ɹˈɛkəɹdz',
    'decreases': 'dəkɹˈisᵻz', 'increases': 'ɪnkɹˈisᵻz',
}
# Words with two pronunciations where the engine picks the wrong one in a particular sentence. Each pattern
# matches just the word, in its context.
CONTEXT = [
    (r'(?<=, )read(?= the label)', 'ɹˈid'),                 # an instruction ("reed"), not the past tense
    (r'(?<=hear it )read\b', 'ɹˈɛd'),
    (r'(?<=pests )present(?= daily)', 'pɹˈɛzᵊnt'),
    (r'(?<=cleaning )presents\b', 'pɹizˈɛnts'),
    (r'(?<=settle out or )separate\b', 'sˈɛpəɹˌAt'),
    (r'(?<=clearly )separate\b', 'sˈɛpəɹˌAt'),
    (r'(?<=records or )permit\b', 'pəɹmˈɪt'),
    (r'\bRecord(?= and evaluate)', 'ɹəkˈɔɹd'),
    (r'\b[Dd]ocument(?= (?:the steps|that)\b)', 'dˈɑkjəmˌɛnt'),
    (r'\bclose(?= (?:vents|containers|all windows)\b)', 'klˈOz'),
    # "use": the noun ends in s ("yoos"), the verb in z ("yooz")
    (r'(?<=equipment to )use(?= is\b)', 'jˈuz'),
    (r'\bUse(?= integrated pest management principles)', 'jˈuz'),
    (r'(?<=clarify )use(?= instructions)', 'jˈus'),
    (r'(?<=and )use(?= (?:classification|directions)\b)', 'jˈus'),
    (r'\bUse(?= classification statement)', 'jˈus'),
    (r'(?<=sale to and )use(?= only by)', 'jˈus'),
    (r'(?<=Discontinue )use\b', 'jˈus'),
    (r'(?i)\bready-to-use\b', 'ɹˈɛditəjˈuz'),            # "ready to yooz", every time
    # noun and verb differ only in the stressed syllable: IN-crease / in-CREASE, TRANS-port / trans-PORT
    (r'(?<=and wind )increase\b', 'ɪnkɹˈis'),
    (r'(?<=Sudden )increases\b', 'ˈɪnkɹˌisᵻz'),           # the one noun; every other "increases" is a verb (see TERMS)
    (r'(?<=handle, )transport\b', 'tɹænspˈɔɹt'),
    (r'(?<=store, )transport\b', 'tɹænspˈɔɹt'),
    (r'(?<=ship or )transport\b', 'tɹænspˈɔɹt'),
    (r'(?<=pick up and )transport\b', 'tɹænspˈɔɹt'),
    (r'(?m)^Insert\b', 'ɪnsˈɜɹt'),
    (r'(?<=truck )overturns\b', 'ˌOvəɹtˈɜɹnz'),
    (r'(?<=\ba )can(?= (?:marked|of light)\b)', 'kˈæn'),   # a container, not "is able to"
]
# The sample label's Spanish sentence, word by word.
SPANISH = {'si': 'sˈi', 'usted': 'ustˈɛd', 'no': 'nˈO', 'entiende': 'ɛntjˈɛndA', 'la': 'lɑ', 'etiqueta': 'ˌɛtikˈɛtɑ',
           'busque': 'bˈuskA', 'a': 'ɑ', 'alguien': 'ˈɑlɡjɛn', 'para': 'pˈɑɹɑ', 'que': 'kA', 'se': 'sA',
           'explique': 'ɛksplˈikA', 'en': 'ɛn', 'detalle': 'dɛtˈɑjA'}


def plural(ph):
    return ph + ('s' if ph[-1] in 'ptkfθ' else 'ᵻz' if ph[-1] in 'szʃʒʧʤ' else 'z')
WORDS = {'mph': 'miles per hour', 'ppm': 'parts per million', 'ppb': 'parts per billion', 'mg': 'milligrams',
         'DANGER-POISON': 'DANGER POISON'}
ROMAN = {'I': 'one', 'II': 'two', 'III': 'three', 'IV': 'four', 'V': 'five'}
FRACTIONS = {'1/2': 'one half', '1/3': 'one third', '2/3': 'two thirds', '1/4': 'one quarter', '3/4': 'three quarters',
             '1/8': 'one eighth', '1/10': 'one tenth', '1/16': 'one sixteenth'}
UNITS = [(r'mg/kg', 'milligrams per kilogram'), (r'mg/[lL]\b', 'milligrams per liter'), (r'lb/gal', 'pounds per gallon'),
         (r'°\s?F\b', ' degrees Fahrenheit'), (r'°\s?C\b', ' degrees Celsius'), (r'°', ' degrees')]


def _code(m):
    """Registration numbers and phone numbers are read digit by digit; a plain 150-189 is a range."""
    tok = m.group(0)
    groups = tok.split('-')
    if all(g.isdigit() for g in groups) and len(groups) == 2 and len(groups[0]) < 5 and int(groups[0]) < int(groups[1]):
        return f'{groups[0]} to {groups[1]}'
    if sum(c.isdigit() for c in tok) < 5:
        return tok
    letters = lambda g: ' '.join('[A](/ˈA/)' if c == 'A' else c for c in g)       # a bare A would be read as the article
    return ', '.join(' '.join(g) if g.isdigit() else letters(g) if g.isalpha() and len(g) <= 3 else g for g in groups)


def say(text):
    """The text handed to the voice. The words shown on the card and their highlighting never use this."""
    t = text
    t = t.replace('®', '').replace('™', '').replace('’', "'").replace('‘', "'")
    t = t.replace('[', '(').replace(']', ')')                                  # square brackets mark phonemes below
    t = t.replace('β-', 'beta ').replace(' / ', ', ')
    t = t.replace('Bulletins Live!', 'Bulletins Live')                         # a name, not the end of a sentence
    # the card's note on a misprint in Table 7.1: the two words sound the same, so spell them
    t = t.replace('as Extra Course;', 'as Extra Course, spelled C O U R S E;')
    t = t.replace('it means Extra Coarse,', 'it means Extra Coarse, spelled C O [A](/ˈA/) R S E,')
    t = re.sub(r'\ba\.i\.(?=[\s),;:]|$)', '[a.i.](/ˌAˈI/)', t)                  # active ingredient: no full stop mid-sentence
    t = re.sub(r'(?<=\w)\(s\)', 's', t)                                        # ingredient(s) -> ingredients
    # a bare site name is read out; an address with a path is not
    t = re.sub(r'\b(?:https?://)?www\.([a-z0-9-]+)\.(gov|org|com|edu)(/[^\s,;)]*[^\s,;).])?',
               lambda m: 'the web address shown on the card' if m.group(3) else
               'W W W dot ' + {'epa': 'EPA', 'acrecycle': '[A](/ˈA/) C recycle'}.get(m.group(1), m.group(1)) + ' dot ' + m.group(2), t)
    # law sections: 25(b), 24(c), 2(ee), 170.240(d)(4-6)
    t = re.sub(r'\b(\d+)(?:\.(\d+))?\(([a-z]{1,2})\)(?:\((\d+)-(\d+)\))?',
               lambda m: m.group(1) + (' point ' + m.group(2) if m.group(2) else '') + ' ' + ' '.join(m.group(3).upper())
               + (f', {m.group(4)} through {m.group(5)}' if m.group(4) else ''), t)
    # the long chemical names inside the sample labels
    t = re.sub(r'(?:[^\s]*\([^\s]*\)[^\s]*|\S{28,})(?:\s+(?:[^\s]*\([^\s]*\)[^\s]*|\S{28,}))*',
               lambda m: ', a long chemical name,' if len(m.group(0)) >= 28 and re.search(r'\d', m.group(0)) else m.group(0), t)
    t = re.sub(r'\b2,4-D\b', 'two four D', t)
    t = re.sub(r'\b0,0-', 'O O ', t)
    t = re.sub(r'\bReg\.\s*No\.', 'registration number', t)
    t = re.sub(r'\bEst\.\s*No\.', 'establishment number', t)
    t = re.sub(r'\bNo\.\s*(?=[A-Z0-9])', 'number ', t)
    t = re.sub(r'\bReg\.\s*(?=\d)', 'registration number ', t)                 # "EPA Est. 56787-CO-1" has no "No."
    t = re.sub(r'\bEst\.\s*(?=\d)', 'establishment number ', t)
    t = re.sub(r'\bMI (\d{5})\b', lambda m: 'Michigan ' + ' '.join(m.group(1)), t)   # the sample label's address
    t = re.sub(r'\bTC-(\d+)([A-Z])\b', r'TC \1 \2', t)
    t = re.sub(r'\bS-(\d+)\.(\d+)\b', r'S \1 point \2', t)
    t = re.sub(r'\b(\d+):(\d+)\b', r'\1 to \2', t)                              # a 1:1 ratio
    t = re.sub(r'\b911\b', '9 1 1', t)
    t = re.sub(r'(?<![\w.,-])0\d+\b(?![.,]\d)', lambda m: ' '.join(m.group(0)), t)   # 0005 -> 0 0 0 5
    t = re.sub(r'(?<=\b[A-Z]{2} )\d{5}\b', lambda m: ' '.join(m.group(0)), t)       # a zip code
    t = re.sub(r'\b\d{3,5}(?= identifies\b)', lambda m: ' '.join(m.group(0)), t)    # the parts of a registration number
    t = re.sub(r'(?<![\w.])\.(\d+)', lambda m: 'point ' + ' '.join(m.group(1)), t)          # .04 -> point 0 4
    t = re.sub(r'(?<![\w.,-])(\d+)\.(0+)(?![\d%])', lambda m: m.group(1) + ' point ' + ' '.join(m.group(2)), t)   # 2.0 keeps its zero
    for k, v in FRACTIONS.items():
        t = re.sub(r'(?<![\w/.-])' + re.escape(k) + r'(?![\w/-])', v, t)
    t = re.sub(r'(?<![\w.-])(\d+(?:\.\d+)?)\s?[–-]\s?(\d+(?:\.\d+)?)(?=\s?(?:%|percent|°|[a-z]))',
               lambda m: f'{m.group(1)} to {m.group(2)}' if float(m.group(1)) < float(m.group(2)) else m.group(0), t)
    t = re.sub(r'(?<![\w-])[A-Z0-9]+(?:-[A-Z0-9]+)+(?![\w-])', lambda m: WORDS.get(m.group(0)) or _code(m), t)
    for pat, rep in UNITS:
        t = re.sub(pat, rep, t)
    t = t.replace(' x ', ' times ')
    t = re.sub(r'\b(Class|Classes|Categor(?:y|ies)|War)\s+(IV|III|II|I|V)\b', lambda m: m.group(1) + ' ' + ROMAN[m.group(2)], t)
    t = re.sub(r'\band/or\b', 'and or', t)
    t = t.replace('MSHA/NIOSH', 'MSHA NIOSH')                                  # one joint approval, not a choice
    t = re.sub(r'(?<=[A-Za-z])/(?=[A-Za-z])', ' or ', t)
    for k, v in WORDS.items():
        t = re.sub(r'(?<![\w.-])' + re.escape(k) + r'(?![\w-])', v, t)
    # a sentence that ends in a single capital letter or a digit ("Class A. Then", "1 4 9 2. 3 1 2 0 is") would
    # lose its full stop, because the engine takes it for an initial or a list number
    t = re.sub(r'(?<![.\w])([A-Z])\.(?=\s+[A-Z"(]|$)', r'\1 .', t)
    t = re.sub(r'(?<=\d)\.(?=\s+\S|$)', ' .', t)
    # the letter A, where the engine would say the article
    t = re.sub(r'\b((?i:category|class|type|part|group|choice|letter)) A\b', r'\1 [A](/ˈA/)', t)
    t = re.sub(r"(?<![\w.'\[-])A(?=[):]|,? (?:through|or|and) [B-Z]\b)", '[A](/ˈA/)', t)
    t = re.sub(r'\bSi [Uu]sted no entiende[^.]*', lambda m: re.sub(
        r"[A-Za-z]+", lambda w: f'[{w.group(0)}](/{SPANISH[w.group(0).lower()]}/)' if w.group(0).lower() in SPANISH else w.group(0),
        m.group(0)), t)
    for pat, ph in CONTEXT:
        t = re.sub(pat, lambda m: f'[{m.group(0)}](/{ph}/)', t)
    for k in PHONEMES:                                   # NIOSH-approved -> NIOSH approved
        t = re.sub(r'(?<![\w.\[-])(' + re.escape(k) + r')-(?=[A-Za-z])', r'\1 ', t)
        t = re.sub(r'(?<=[A-Za-z])-(' + re.escape(k) + r')(?![\w\]-])', r' \1', t)
    for k in TERMS:                                      # tear-resistant, low-wind
        t = re.sub(r'(?<![\w.\[-])((?i:' + re.escape(k) + r')s?)-(?=[A-Za-z])', r'\1 ', t)
        t = re.sub(r'(?<=[A-Za-z])-((?i:' + re.escape(k) + r')s?)(?![\w\]-])', r' \1', t)
    for k, v in PHONEMES.items():
        t = re.sub(r'(?<![\w.\[-])' + re.escape(k) + r"(?:(')?(s))?(?![\w\]-])",
                   lambda m: f'[{m.group(0)}](/{plural(v) if m.group(2) else v}/)', t)
    for k, v in TERMS.items():
        t = re.sub(r'(?<![\w.\[-])(?i:' + re.escape(k) + r")(s)?(?![\w\]-])",
                   lambda m: f'[{m.group(0)}](/{plural(v) if m.group(1) else v}/)', t)
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s+,', ',', t)
    t = re.sub(r',(?:\s*,)+', ',', t)
    return t.strip()

# ---------------------------------------------------------------- engine

_K = _G2P = None
VOWELS_ETC = 'ˈˌᵊᵻ'


def espeak_data():
    """espeak-ng ignores a data path near 160 characters and then cannot start, so keep a copy on a short path."""
    import espeakng_loader
    data = pathlib.Path(espeakng_loader.get_data_path())
    if len(str(data)) <= 120:
        return data
    short = HOME / 'espeak-ng-data'
    if len(str(short)) > 120:
        short = pathlib.Path.home() / '.cache' / 'pest-study-tts' / 'espeak-ng-data'
    if not (short / 'phontab').exists():
        shutil.copytree(data, short, dirs_exist_ok=True)
    return short


def _init(threads, voice=True):
    global _K, _G2P
    import warnings
    warnings.filterwarnings('ignore')
    if voice:
        import onnxruntime as ort
        from kokoro_onnx import Kokoro
        so = ort.SessionOptions()
        so.intra_op_num_threads = threads
        so.inter_op_num_threads = 1
        sess = ort.InferenceSession(str(HOME / MODEL), so, providers=['CPUExecutionProvider'])
        _K = Kokoro.from_session(sess, str(HOME / VOICES))
        if not _K.has_timings:
            raise SystemExit('this model file does not report timings; run --setup again (model-files-v1.1)')
    import espeakng_loader
    from phonemizer.backend.espeak.wrapper import EspeakWrapper
    from misaki import en, espeak
    EspeakWrapper.set_library(espeakng_loader.get_library_path())
    EspeakWrapper.set_data_path(str(espeak_data()))
    _G2P = en.G2P(trf=False, british=False, fallback=espeak.EspeakFallback(british=False), unk='')


def vocab():
    if _K:
        return _K.tokenizer.vocab
    from kokoro_onnx.config import DEFAULT_VOCAB
    return DEFAULT_VOCAB


def phonemize(text):
    """(phonemes, words) for one line. words: [spoken word, first phoneme index, end index, guessed]."""
    _, toks = _G2P(say(text))
    v = vocab()
    out, words, cur, a0, guess = '', [], '', None, False
    for tk in toks:
        p = ' '.join(''.join(c for c in (tk.phonemes or '') if c in v).split()).replace('ɹɹ', 'ɹ')
        if p and out.endswith(' ') and all(c in '.,;:!?' for c in p):
            out = out[:-1]                               # "A ." was split above; the voice gets "A."
        if a0 is None:
            a0 = len(out)
        out += p
        cur += tk.text
        rating = getattr(tk, 'rating', None)             # misaki puts it in either place
        if rating is None and tk._ is not None:
            rating = tk._.rating
        guess = guess or (rating is not None and rating <= 2) or tk.phonemes is None
        if tk.whitespace:
            words.append([cur, a0, len(out), guess])
            cur, a0, guess = '', None, False
            if out and not out.endswith(' '):
                out += ' '
    if cur:
        words.append([cur, a0, len(out), guess])
    out = out.rstrip()
    for w in words:
        w[1], w[2] = min(w[1], len(out)), min(w[2], len(out))
    # A sentence that ends in an abbreviation ("in 950 B.C.") comes back with no full stop, and the voice
    # then does not let its pitch fall. Put the sentence's own end mark back.
    end = re.search(r'([.!?:])["”\')\]]*$', text.strip())
    if end and out and words and (out[-1].isalpha() or out[-1] in VOWELS_ETC):
        out += end.group(1)
        words[-1][2] = len(out)
    return out, words


def pieces(ph, words):
    """Cut a line that is too long for the model into (first word, end word) runs, at a clause if possible."""
    if len(ph) <= MAX_PHONEMES:
        return [(0, len(words))]
    out, start = [], 0
    while start < len(words):
        end, best = start, None
        while end < len(words) and words[end][2] - words[start][1] <= MAX_PHONEMES:
            end += 1
            if words[end - 1][0][-1:] in '.!?;:,' and words[end - 1][2] - words[start][1] >= MAX_PHONEMES // 3:
                best = end
        if end == len(words):
            best = end
        end = best or max(end, start + 1)
        out.append((start, end))
        start = end
    return out


def speak(ph, words):
    """Audio for one line and the (start, end) time in seconds of every spoken word."""
    import numpy as np
    audio, times = [], []
    pos = 0
    runs = pieces(ph, words)
    for n, (i, j) in enumerate(runs):
        a, b = words[i][1], words[j - 1][2]
        part = ph[a:b].strip()
        if not part:
            times += [(pos / SR, pos / SR)] * (j - i)
            continue
        a += len(ph[a:b]) - len(ph[a:b].lstrip())
        wav, sr, tim = _K.create_timed(part, voice=VOICE, speed=SPEED, is_phonemes=True)
        assert sr == SR
        wav = np.asarray(wav, dtype=np.float32)
        exact = len(tim) == len(part)
        for w in words[i:j]:
            x, y = w[1] - a, w[2] - a
            if exact and 0 <= x < y <= len(tim):
                times.append((pos / SR + tim[x].start, pos / SR + tim[y - 1].end))
            else:                                   # no phonemes of its own, or timings missing: place by position
                f0, f1 = max(0, x) / max(1, len(part)), min(len(part), max(x, y)) / max(1, len(part))
                times.append((pos / SR + f0 * len(wav) / SR, pos / SR + f1 * len(wav) / SR))
        audio.append(wav)
        pos += len(wav)
        if n < len(runs) - 1:
            gap = np.zeros(int(SR * (0.3 if part[-1:] in '.!?' else 0.14)), dtype=np.float32)
            audio.append(gap)
            pos += len(gap)
    if not audio:
        return np.zeros(int(SR * 0.2), dtype=np.float32), times
    return np.concatenate(audio), times


def key(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())


def word_starts(display, spoken, times, length):
    """Start time (s) of every word shown on the card, from the times of the words actually spoken."""
    d = [(i, key(w)) for i, w in enumerate(display) if key(w)]
    s = [(j, key(w)) for j, w in enumerate(spoken) if key(w)]
    starts = [None] * len(display)
    sm = difflib.SequenceMatcher(None, [k for _, k in d], [k for _, k in s], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for n in range(i2 - i1):
                starts[d[i1 + n][0]] = times[s[j1 + n][0]][0]
        elif tag == 'replace':                      # several shown words stand for several spoken ones: share the time
            t0, t1 = times[s[j1][0]][0], times[s[j2 - 1][0]][1]
            weights = [len(d[i][1]) + 1 for i in range(i1, i2)]
            acc, total = 0, sum(weights)
            for n, i in enumerate(range(i1, i2)):
                starts[d[i][0]] = t0 + (t1 - t0) * acc / total
                acc += weights[n]
        elif tag == 'delete':                       # shown but not spoken: no time of its own
            pass
    # words with no time of their own (punctuation, symbols) take the next word's start, so they never light up alone
    nxt = length
    for i in range(len(display) - 1, -1, -1):
        if starts[i] is None:
            starts[i] = nxt
        nxt = starts[i]
    out, hi = [], 0.0
    for v in starts:
        hi = max(hi, min(v, length))
        out.append(hi)
    return out


PAUSE_MS = {'h': 650, 'box': 560, 'p': 430, 'pend': 760, 'li': 520, 'fig': 520, 'exp': 560}
LEAD_MS, TAIL_MS = 250, 450


def _narrate(job):
    import numpy as np
    sid, lines = job
    t0 = time.time()
    chunks, marks, wordms, pos, loose = [np.zeros(int(SR * LEAD_MS / 1000), dtype=np.float32)], [], [], 0, 0
    pos = len(chunks[0])
    for n, (kind, raw) in enumerate(lines):
        ph, words = phonemize(plain(raw))
        if not ph:
            ph, words = phonemize('blank')
        wav, times = speak(ph, words)
        length = len(wav) / SR
        ws = word_starts(display_words(raw), [w[0] for w in words], times, length)
        marks += [round(pos * 1000 / SR), round((pos + len(wav)) * 1000 / SR)]
        wordms.append([round(x * 1000) for x in ws])
        chunks.append(wav)
        pos += len(wav)
        gap = np.zeros(int(SR * (TAIL_MS if n == len(lines) - 1 else PAUSE_MS[kind]) / 1000), dtype=np.float32)
        chunks.append(gap)
        pos += len(gap)
    audio = np.concatenate(chunks)
    # one gain for the whole card: the loudest 0.1% of samples sit at 0.75, which leaves room for MP3 overshoot
    peak = float(np.percentile(np.abs(audio[np.abs(audio) > 0.02]), 99.9)) if np.any(np.abs(audio) > 0.02) else 1.0
    audio = np.clip(audio * min(3.0, 0.75 / max(peak, 1e-3)), -0.93, 0.93).astype('<f4')
    OUT.mkdir(parents=True, exist_ok=True)
    path, tmp = OUT / f'{sid}.mp3', OUT / f'.{sid}.tmp.mp3'
    p = subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '1', '-i', '-',
                        '-c:a', 'libmp3lame', '-b:a', BITRATE, '-ar', str(SR), '-ac', '1', str(tmp)],
                       input=audio.tobytes(), capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode()[:400])
    os.replace(tmp, path)
    # r: hash of what was asked for (text handed to the voice, voice, settings); a change means record again.
    # p: names the published file. It also covers the timings that came out, so a card recorded again
    #    (new engine version, --force, a fix to this script) gets a new name unless the result is identical,
    #    and no browser can pair an old file with new timings.
    r = render_hash(lines)
    dur = round(len(audio) * 1000 / SR)
    entry = {'h': text_hash(lines), 'r': r, 'p': fnv(r + json.dumps([dur, marks, wordms])), 'd': dur, 't': marks, 'w': wordms}
    return sid, entry, path.stat().st_size, time.time() - t0


def load_sections():
    sys.path.insert(0, str(ROOT / 'tools'))
    import build
    data = build.load()
    if build.errors:
        raise SystemExit('content does not load, nothing recorded or changed:\n' + '\n'.join(build.errors))
    return data['sections']


def read_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding='utf-8'))
    return {'v': 1, 'voice': VOICE, 'cards': {}}


def write_manifest(m):
    m['cards'] = dict(sorted(m['cards'].items()))
    tmp = MANIFEST.with_suffix('.json.tmp')
    tmp.write_text(json.dumps(m, separators=(',', ':')) + '\n', encoding='utf-8')
    os.replace(tmp, MANIFEST)          # in one step: a build running at the same time never reads half a file


def published_name(sid, entry):
    """The name a card's audio is published under. It carries the render hash, so a card that is recorded
    again gets a new address and no browser can keep playing the old file against the new timings."""
    return f'audio/{sid}.{entry["p"]}.mp3'


def recorded_cards(a, sections):
    """(card id, manifest entry) for every selected card whose recording is current and on disk."""
    manifest = read_manifest()
    want_ch = {c.strip() for c in a.chapters.split(',') if c.strip()}
    want_cards = {c.strip() for c in a.cards.split(',') if c.strip()}
    out = []
    for s in sections:
        sid = s['id']
        ch = 'ch' + sid[1:3] if re.match(r'c\d\d-', sid) else sid
        if (want_ch and ch not in want_ch) or (want_cards and sid not in want_cards):
            continue
        lines = spoken_lines(s)
        e = manifest['cards'].get(sid)
        if lines and e and e['h'] == text_hash(lines) and (OUT / f'{sid}.mp3').exists():
            out.append((sid, e))
    return out


def setup():
    HOME.mkdir(parents=True, exist_ok=True)
    venv = HOME / 'venv'
    if not (venv / 'bin' / 'python').exists():
        # spaCy (used by the pronunciation engine) has no wheels for the newest Python yet
        py = next((p for p in ('python3.12', 'python3.11') if shutil.which(p)), sys.executable)
        subprocess.check_call([py, '-m', 'venv', str(venv)])
    pip = [str(venv / 'bin' / 'pip'), 'install', '-q']
    subprocess.check_call(pip + ['kokoro-onnx==0.6.1', 'soundfile', 'misaki[en]==0.9.4'])
    subprocess.check_call(pip + [SPACY_MODEL])
    # kokoro-onnx and misaki each bring their own copy of the "phonemizer" package; keep misaki's
    subprocess.call([str(venv / 'bin' / 'pip'), 'uninstall', '-y', '-q', 'phonemizer', 'phonemizer-fork'])
    subprocess.check_call(pip + ['phonemizer-fork==3.3.2'])
    for f in (MODEL, VOICES):
        if not (HOME / f).exists() or (HOME / f).stat().st_size < 1_000_000:
            subprocess.check_call(['curl', '-f', '-sS', '-L', '-o', str(HOME / f), MODEL_URL + f])
    if not shutil.which('ffmpeg'):
        print('ffmpeg is missing: install it (apt-get install -y ffmpeg) before recording')
    print('ready. Run:', venv / 'bin' / 'python', 'tools/narrate.py')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--setup', action='store_true')
    ap.add_argument('--chapters', default='')
    ap.add_argument('--cards', default='')
    ap.add_argument('--jobs', type=int, default=3)
    ap.add_argument('--threads', type=int, default=1)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--new-first', action='store_true', help='record cards with no recording before re-recording changed ones')
    ap.add_argument('--say', default='')
    ap.add_argument('--words', action='store_true', help='list every word the engine had to guess')
    ap.add_argument('--list', action='store_true', help='show what is missing or out of date, record nothing')
    ap.add_argument('--check', action='store_true', help='test the pronunciation rules against tools/say_cases.json')
    ap.add_argument('--files', type=float, default=0, metavar='MB', help='print the Artifact "files" maps, each batch under MB')
    ap.add_argument('--stage', default='', metavar='DIR', help='copy the audio into DIR under its published names')
    a = ap.parse_args()
    if a.setup:
        return setup()
    if a.check:
        cases = json.loads((ROOT / 'tools' / 'say_cases.json').read_text(encoding='utf-8'))
        bad = [(t, want, say(t)) for t, want in cases if say(t) != want]
        for t, want, got in bad:
            print(f'FAIL {t}\n  want {want}\n  got  {got}')
        print(f'{len(cases) - len(bad)}/{len(cases)} pronunciation cases pass')
        sys.exit(1 if bad else 0)
    if a.say:
        _init(1, voice=False)
        print(say(a.say))
        print(phonemize(a.say)[0])
        return
    sections = load_sections()
    if a.files or a.stage:
        cards = recorded_cards(a, sections)
        if a.stage:
            dest = pathlib.Path(a.stage)
            (dest / 'audio').mkdir(parents=True, exist_ok=True)
            for sid, e in cards:
                shutil.copyfile(OUT / f'{sid}.mp3', dest / published_name(sid, e))
            print(f'{len(cards)} files in {dest / "audio"}')
            return
        batches, cur, size = [], {}, 0
        for sid, e in cards:
            n = (OUT / f'{sid}.mp3').stat().st_size
            if cur and (size + n > a.files * 1e6 or len(cur) >= 200):
                batches.append(cur)
                cur, size = {}, 0
            cur[published_name(sid, e)] = {'from': f'dist/audio/{sid}.mp3', 'contentType': 'audio/mpeg'}
            size += n
        if cur:
            batches.append(cur)
        for b in batches:
            print(json.dumps(b, separators=(',', ':')))
        return
    if a.words:
        _init(1, voice=False)
        seen = {}
        for s in sections:
            for _, raw in spoken_lines(s):
                ph, words = phonemize(plain(raw))
                for w, x, y, guess in words:
                    if guess:
                        seen.setdefault((key(w), ph[x:y]), [0, s['id']])[0] += 1
        for (w, ph), (n, sid) in sorted(seen.items()):
            print(f'{w}\t{ph}\t{n}\t{sid}')
        return
    manifest = read_manifest()
    want_ch = {c.strip() for c in a.chapters.split(',') if c.strip()}
    want_cards = {c.strip() for c in a.cards.split(',') if c.strip()}
    jobs = []
    live = {s['id'] for s in sections}
    for s in sections:
        sid = s['id']
        ch = 'ch' + sid[1:3] if re.match(r'c\d\d-', sid) else sid
        if (want_ch and ch not in want_ch) or (want_cards and sid not in want_cards):
            continue
        lines = spoken_lines(s)
        if not lines:
            continue
        cur = manifest['cards'].get(sid)
        ok = (cur and cur['h'] == text_hash(lines) and cur.get('r', cur.get('p')) == render_hash(lines)
              and [len(x) for x in cur['w']] == [len(display_words(t)) for _, t in lines]     # bold marks moved: word times no longer fit
              and (OUT / f'{sid}.mp3').exists())
        if not ok or a.force:
            jobs.append((sid, lines))
    if a.new_first:
        jobs.sort(key=lambda j: j[0] in manifest['cards'])
    gone = [k for k in manifest['cards'] if k not in live]
    for sid in gone:
        manifest['cards'].pop(sid)
    print(f'{len(jobs)} cards to record ({sum(len(j[1]) for j in jobs)} lines)', flush=True)
    if a.list or not jobs:
        if gone and not a.list:
            write_manifest(manifest)
        for j in jobs:
            print('  ', j[0])
        return
    espeak_data()
    import fcntl
    from concurrent.futures import ProcessPoolExecutor, as_completed
    OUT.mkdir(parents=True, exist_ok=True)
    lock = open(OUT / '.lock', 'w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise SystemExit('another recording run is going (dist/audio/.lock). Wait for it, or stop it first.')
    t0 = time.time()
    done = audio_ms = size = 0
    # A worker killed for memory, or a model that will not load, raises BrokenProcessPool here and ends the run.
    with ProcessPoolExecutor(max_workers=max(1, min(a.jobs, len(jobs))), initializer=_init, initargs=(a.threads,)) as pool:
        for fut in as_completed([pool.submit(_narrate, j) for j in jobs]):
            sid, entry, nbytes, dt = fut.result()
            manifest = read_manifest() if MANIFEST.exists() else manifest
            manifest['cards'][sid] = entry
            write_manifest(manifest)
            done += 1
            audio_ms += entry['d']
            size += nbytes
            el = time.time() - t0
            print(f'[{done}/{len(jobs)}] {sid}: {entry["d"] / 1000:.0f}s audio, {nbytes // 1024} KB, took {dt:.0f}s | '
                  f'{audio_ms / 60000:.1f} min audio, {size / 1e6:.1f} MB, in {el / 60:.1f} min ({audio_ms / 1000 / el:.1f}x)', flush=True)
    print('done')


if __name__ == '__main__':
    main()
