# punctuation = ["!", "?", "…", ",", ".", "'", "-"]
punctuation = ["!", "?", "…", ",", ".", "'", "-", "¿", "¡"]
pu_symbols = punctuation + ["SP", "UNK"]
pad = "_"

# chinese
zh_symbols = [
    "E",
    "En",
    "a",
    "ai",
    "an",
    "ang",
    "ao",
    "b",
    "c",
    "ch",
    "d",
    "e",
    "ei",
    "en",
    "eng",
    "er",
    "f",
    "g",
    "h",
    "i",
    "i0",
    "ia",
    "ian",
    "iang",
    "iao",
    "ie",
    "in",
    "ing",
    "iong",
    "ir",
    "iu",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "ong",
    "ou",
    "p",
    "q",
    "r",
    "s",
    "sh",
    "t",
    "u",
    "ua",
    "uai",
    "uan",
    "uang",
    "ui",
    "un",
    "uo",
    "v",
    "van",
    "ve",
    "vn",
    "w",
    "x",
    "y",
    "z",
    "zh",
    "AA",
    "EE",
    "OO",
]
num_zh_tones = 6

# japanese
ja_symbols = [
    "N",
    "a",
    "a:",
    "b",
    "by",
    "ch",
    "d",
    "dy",
    "e",
    "e:",
    "f",
    "g",
    "gy",
    "h",
    "hy",
    "i",
    "i:",
    "j",
    "k",
    "ky",
    "m",
    "my",
    "n",
    "ny",
    "o",
    "o:",
    "p",
    "py",
    "q",
    "r",
    "ry",
    "s",
    "sh",
    "t",
    "ts",
    "ty",
    "u",
    "u:",
    "w",
    "y",
    "z",
    "zy",
]
num_ja_tones = 1

# English
en_symbols = [
    "aa",
    "ae",
    "ah",
    "ao",
    "aw",
    "ay",
    "b",
    "ch",
    "d",
    "dh",
    "eh",
    "er",
    "ey",
    "f",
    "g",
    "hh",
    "ih",
    "iy",
    "jh",
    "k",
    "l",
    "m",
    "n",
    "ng",
    "ow",
    "oy",
    "p",
    "r",
    "s",
    "sh",
    "t",
    "th",
    "uh",
    "uw",
    "V",
    "w",
    "y",
    "z",
    "zh",
]
num_en_tones = 4

# Korean
kr_symbols = ['ᄌ', 'ᅥ', 'ᆫ', 'ᅦ', 'ᄋ', 'ᅵ', 'ᄅ', 'ᅴ', 'ᄀ', 'ᅡ', 'ᄎ', 'ᅪ', 'ᄑ', 'ᅩ', 'ᄐ', 'ᄃ', 'ᅢ', 'ᅮ', 'ᆼ', 'ᅳ', 'ᄒ', 'ᄆ', 'ᆯ', 'ᆷ', 'ᄂ', 'ᄇ', 'ᄉ', 'ᆮ', 'ᄁ', 'ᅬ', 'ᅣ', 'ᄄ', 'ᆨ', 'ᄍ', 'ᅧ', 'ᄏ', 'ᆸ', 'ᅭ', '(', 'ᄊ', ')', 'ᅲ', 'ᅨ', 'ᄈ', 'ᅱ', 'ᅯ', 'ᅫ', 'ᅰ', 'ᅤ', '~', '\\', '[', ']', '/', '^', ':', 'ㄸ', '*']
num_kr_tones = 1

# Spanish
es_symbols = [
        "N",
        "Q",
        "a",
        "b",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "ɑ",
        "æ",
        "ʃ",
        "ʑ",
        "ç",
        "ɯ",
        "ɪ",
        "ɔ",
        "ɛ",
        "ɹ",
        "ð",
        "ə",
        "ɫ",
        "ɥ",
        "ɸ",
        "ʊ",
        "ɾ",
        "ʒ",
        "θ",
        "β",
        "ŋ",
        "ɦ",
        "ɡ",
        "r",
        "ɲ",
        "ʝ",
        "ɣ",
        "ʎ",
        "ˈ",
        "ˌ",
        "ː"
    ]
num_es_tones = 1

# French 
fr_symbols = [
    "\u0303",
    "œ",
    "ø",
    "ʁ",
    "ɒ",
    "ʌ",
    "ɜ",
    "ɐ"
]
num_fr_tones = 1

# German 
de_symbols = [
    "ʏ",
    "̩"
  ]
num_de_tones = 1

# Russian 
ru_symbols = [
    "ɭ",
    "ʲ",
    "ɕ",
    "\"",
    "ɵ",
    "^",
    "ɬ"
]
num_ru_tones = 1

gu_symbols = [
    # Independent vowels (svaras)
    "અ", "આ", "ઇ", "ઈ", "ઉ", "ઊ", "ઋ", "એ", "ઐ", "ઓ", "ઔ",
    # Vowels used in loanwords
    "ઍ", "ઑ",   # ૅ (candra E) and ૉ (candra O) forms for [æ] and [ɔ]:contentReference[oaicite:4]{index=4}:contentReference[oaicite:5]{index=5}
    # Consonants (vyanjana)
    "ક", "ખ", "ગ", "ઘ", "ઙ", "ચ", "છ", "જ", "ઝ", "ઞ",
    "ટ", "ઠ", "ડ", "ઢ", "ણ", "ત", "થ", "દ", "ધ", "ન",
    "પ", "ફ", "બ", "ભ", "મ", "ય", "ર", "લ", "ળ", "વ",
    "શ", "ષ", "સ", "હ",
    # Vowel diacritics (matras) for combination with consonants
    "ા", "િ", "ી", "ુ", "ૂ", "ૃ", "ે", "ૈ", "ો", "ૌ",
    # Chandrabindu, anusvara, visarga (nasalization and aspiration markers)
    "ઁ", "ં", "ઃ",
    # Virama (suppresses inherent vowel for conjuncts)
    "્"
]
num_gu_tones = 1
hi_symbols = [
    # Independent vowels
    "अ", "आ", "इ", "ई", "उ", "ऊ", "ए", "ऐ", "ओ", "औ",
    "ऑ",    # ऑ (candra O) for /ɔ/ as in "ऑटो" (loanwords):contentReference[oaicite:15]{index=15}
    # Consonants
    "क", "ख", "ग", "घ", "ङ", "च", "छ", "ज", "झ", "ञ",
    "ट", "ठ", "ड", "ढ", "ण", "त", "थ", "द", "ध", "न",
    "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "श",
    "ष", "स", "ह",
    # Consonants with nukta (for Urdu/Persian sounds)
    "क़", "ख़", "ग़", "ज़", "फ़", "ड़", "ढ़",
    # Vowel diacritics (matras)
    "ा", "ि", "ी", "ु", "ू", "ृ", "े", "ै", "ो", "ौ", "ॉ",
    # Nasalization and other signs
    "ँ", "ं", "ः", "़",
    # Virama (halant) for suppressing the vowel
    "्"
]
num_hi_tones = 1
kn_symbols = [
    # Independent vowels
    "ಅ", "ಆ", "ಇ", "ಈ", "ಉ", "ಊ", "ಋ", "ಎ", "ಏ", "ಐ", "ಒ", "ಓ", "ಔ",
    # Consonants
    "ಕ", "ಖ", "ಗ", "ಘ", "ಙ", "ಚ", "ಛ", "ಜ", "ಝ", "ಞ",
    "ಟ", "ಠ", "ಡ", "ಢ", "ಣ", "ತ", "ಥ", "ದ", "ಧ", "ನ",
    "ಪ", "ಫ", "ಬ", "ಭ", "ಮ", "ಯ", "ರ", "ಲ", "ವ", "ಶ", "ಷ", "ಸ", "ಹ", "ಳ",
    # (Archaic letters ೞ (ḻa) and ಱ (ṟa) are omitted as they are obsolete:contentReference[oaicite:25]{index=25})
    # Vowel diacritics (matras)
    "ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ",
    # Other signs
    "ಂ", "ಃ", "್"
]
num_kn_tones = 1
ml_symbols = [
    # Independent vowels
    "അ", "ആ", "ഇ", "ഈ", "ഉ", "ഊ", "എ", "ഏ", "ഐ", "ഒ", "ഓ", "ഔ",
    # Sanskrit vowels occasionally used (short vocalic R)
    "ഋ",   # (ൠ, ഌ, ൡ are excluded – very rare and not in modern usage:contentReference[oaicite:38]{index=38}:contentReference[oaicite:39]{index=39})
    # Consonants
    "ക", "ഖ", "ഗ", "ഘ", "ങ", "ച", "ഛ", "ജ", "ഝ", "ഞ",
    "ട", "ഠ", "ഡ", "ഢ", "ണ", "ത", "ഥ", "ദ", "ധ", "ന",
    "പ", "ഫ", "ബ", "ഭ", "മ", "യ", "ര", "റ", "ല", "ള", "ഴ", "വ", "ശ", "ഷ", "സ", "ഹ",
    # (Archaic consonants ഩ (ṉa) and ഺ (ṯa) are not included:contentReference[oaicite:40]{index=40})
    # Vowel diacritics (matras)
    "ാ", "ി", "ീ", "ു", "ൂ", "ൃ", "െ", "േ", "ൈ", "ൊ", "ോ", "ൗ",
    # Other signs
    "ം", "ഃ", "്"
]
num_kn_tones = 1
ta_symbols = [
    # Independent vowels (uyir ezhuthugal)
    "அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ",
    # Consonants (mei ezhuthugal)
    "க", "ங", "ச", "ஞ", "ட", "ண", "த", "ந", "ப", "ம",
    "ய", "ர", "ல", "வ", "ழ", "ள", "ற", "ன",
    # Grantha consonants (for foreign sounds)
    "ஜ", "ஶ", "ஷ", "ஸ", "ஹ",
    # Vowel diacritics (matras)
    "ா", "ி", "ீ", "ு", "ூ", "ெ", "ே", "ை", "ொ", "ோ", "ௌ",
    # Special sign and virama
    "ஃ", "்"
]
num_ta_tones = 1
te_symbols = [
    # Independent vowels
    "అ", "ఆ", "ఇ", "ఈ", "ఉ", "ఊ", "ఎ", "ఏ", "ఐ", "ఒ", "ఓ", "ఔ",
    # Sanskrit-derived vowel (short r̥)
    "ఋ",   # (Long ౠ and vocalic ౡ, ఌ are obsolete:contentReference[oaicite:61]{index=61}:contentReference[oaicite:62]{index=62})
    # Consonants
    "క", "ఖ", "గ", "ఘ", "ఙ", "చ", "ఛ", "జ", "ఝ", "ఞ",
    "ట", "ఠ", "డ", "ఢ", "ణ", "త", "థ", "ద", "ధ", "న",
    "ప", "ఫ", "బ", "భ", "మ", "య", "ర", "ల", "వ", "శ", "ష", "స", "హ", "ళ",
    # Vowel diacritics (matras)
    "ా", "ి", "ీ", "ు", "ూ", "ృ", "ె", "ే", "ై", "ొ", "ో", "ౌ",
    # Other signs
    "ం", "ః", "్"
]
num_te_tones = 1
extra_symbols = ['ɖ', 'ˈiː', 'ɟ', 'eː', 'ˌeː', 'ʋ', 'pʰ', 'ˈɔ', 'ˈaː', 'ˈã', 'ˈeː', 'ɡʰ', 'ˈʌ', 'ˈẽː', 'ˈɛː', 'aː', 'ˈʊ', 'r.', 'ˌaː', 'ˈɪ', 'ˈoː', 'tʰ', 'ʈʰ', 'ˈuː', 'cʰ', 'ʈ', '(en)', 'ˈaɪ', '(hi)', 'ˈi', 'ɟʰ', 'ˌi', 'ˌə', 'ˌõ', 'õ', 'bʰ', 'oː', 'ɛː', 'ˌɪ', 'ĩ', 'ɛ̃', 'ˈũ', 'ɔː', 'kʰ', 'ˌʊ', 'ẽː', 'ã', 'dʰ', 'ˈɑː', 'tʃ', 'ˈeɪ', 'ˈɒ', 'əʊ', 'aɪ', 'dʒ', 'ˈa', 'ˌaɪ', 'ɳ', 'ɖʰ', 'ˈĩ', 'tː', 'ˈu', 'ˈɔː', 'ʂ', 'ˌʌ', 'ˌoː', 'ˈə', 'kː', 'uː', 'ˈõ', 'pː', 'ˌã', 'ˌu', 'ˌuː', 'ũ', 'ˌĩ', 'ˌɛ', 'ˌẽː', 'cː', 'dʰː', 'ɟː', 'cʰː', 'ˌa', 'ˈe', 'ˌɛː', 'tʰː', 'ˈɛ̃', 'iː', 'ˌɒ', 'ˈəʊ', 'ˈiə', 'ˌiː', 'ˌũ', 'ˈɛ', 'dː', 'ˈɔ̃', 'ʈː', 'eɪ', 'əl', 'iə', 'ˌɑː', 'ɑː', 'ʈʰː', 'ˈɜː', 'ˈeə', 'ˌəʊ', 'ɖː', 'ɖʰː']
# combine all symbols
normal_symbols = sorted(set(zh_symbols + ja_symbols + en_symbols + kr_symbols + es_symbols + fr_symbols + de_symbols + ru_symbols)) # add support for other languages (only hindi right now)
symbols = [pad] + normal_symbols + pu_symbols + hi_symbols + extra_symbols
sil_phonemes_ids = [symbols.index(i) for i in pu_symbols]

# combine all tones
num_tones = num_zh_tones + num_ja_tones + num_en_tones + num_kr_tones + num_es_tones + num_fr_tones + num_de_tones + num_ru_tones + num_hi_tones # add support for other languages (only hindi right now)

# language maps
language_id_map = {"ZH": 0, "JP": 1, "EN": 2, "ZH_MIX_EN": 3, 'KR': 4, 'ES': 5, 'SP': 5 ,'FR': 6, 'IN': 7}
num_languages = len(language_id_map.keys())

language_tone_start_map = {
    "ZH": 0,
    "ZH_MIX_EN": 0,
    "JP": num_zh_tones,
    "EN": num_zh_tones + num_ja_tones,
    'KR': num_zh_tones + num_ja_tones + num_en_tones,
    "ES": num_zh_tones + num_ja_tones + num_en_tones + num_kr_tones,
    "SP": num_zh_tones + num_ja_tones + num_en_tones + num_kr_tones,
    "FR": num_zh_tones + num_ja_tones + num_en_tones + num_kr_tones + num_es_tones,
    "IN": num_zh_tones + num_ja_tones + num_en_tones + num_kr_tones + num_es_tones + num_fr_tones + num_de_tones + num_ru_tones,
}

if __name__ == "__main__":
    a = set(zh_symbols)
    b = set(en_symbols)
    print(sorted(a & b))
