import os
from functools import cache
from transformers import AutoTokenizer
import phonemizer
from phonemizer.separator import Separator
from whisper_normalizer.indic import (HindiNormalizer, BengaliNormalizer, GujaratiNormalizer,
KannadaNormalizer, DevanagariNormalizer, MalayalamNormalizer, PunjabiNormalizer, TamilNormalizer, TeluguNormalizer )

model_id = os.environ.get('MODEL_ID', 'google/muril-base-cased')
normalizer_map = {
    "bn": BengaliNormalizer(tts_mode=True),
    "gu": GujaratiNormalizer(tts_mode=True),
    "hi": HindiNormalizer(tts_mode=True),
    "kn": KannadaNormalizer(tts_mode=True),
    "ml": MalayalamNormalizer(tts_mode=True),
    "mr": DevanagariNormalizer(), # Marathi
    "pa": PunjabiNormalizer(tts_mode=True),
    "ta": TamilNormalizer(tts_mode=True),
    "te": TeluguNormalizer(tts_mode=True)
}

def distribute_phone(n_phone, n_word):
    phones_per_word = [0] * n_word
    for task in range(n_phone):
        min_tasks = min(phones_per_word)
        min_index = phones_per_word.index(min_tasks)
        phones_per_word[min_index] += 1
    return phones_per_word

@cache
def get_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    return tokenizer

@cache
def get_normalizer(language):
    normalizer = normalizer_map.get(language)
    return normalizer

@cache
def get_phonemizer(language):
    global_phonemizer = phonemizer.backend.EspeakBackend(language=language, preserve_punctuation=True,  with_stress=True)
    separator = Separator(phone='-', word='|')

    return global_phonemizer, separator

def text_normalize(text, language):
    normalizer = get_normalizer(language)
    return normalizer(text)

def g2p(text, language, pad_start_end=True, tokenized=None):
    global_phonemizer, separator = get_phonemizer(language)
    if tokenized is None:
        tokenizer = get_tokenizer()
        tokenized = tokenizer.tokenize(text)
    phs = []
    ph_groups = []
    for t in tokenized:
        if not t.startswith("#"):
            ph_groups.append([t])
        else:
            ph_groups[-1].append(t.replace("#", ""))
    
    phones = []
    tones = []
    word2ph = []
    for group in ph_groups:
        w = "".join(group)
        phone_len = 0
        word_len = len(group)
        r = global_phonemizer.phonemize([w], separator = separator)[0].replace('|', '')
        splitted = r.split('-')
        for s in splitted:
            if len(s):
                phones.append(s)
                if 'ˈ' in s:
                    t = 1
                else:
                    t = 0
                tones.append(t)
                phone_len += 1
        aaa = distribute_phone(phone_len, word_len)
        word2ph += aaa

    if pad_start_end:
        phones = ["_"] + phones + ["_"]
        tones = [0] + tones + [0]
        word2ph = [1] + word2ph + [1]
    return phones, tones, word2ph

def get_bert_feature(text, word2ph, device=None):
    try:
        from text import indic_bert
    except:
        from melo.text import indic_bert

    return indic_bert.get_bert_feature(text, word2ph, device=device)

if __name__ == "__main__":
    text = 'hello nama saya.'
    text = text_normalize(text)
    phones, tones, word2ph = g2p(text)
    """
    (['_',
    'h',
    'ˈɛ',
    'l',
    'o',
    'n',
    'ˈa',
    'm',
    'ə',
    's',
    'ˈa',
    'j',
    'ə',
    '.',
    '_'],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 4, 4, 4, 1, 1])
    """