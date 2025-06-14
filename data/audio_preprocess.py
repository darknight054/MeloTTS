import os
import csv
import re
import argparse
import difflib
import requests
from urllib.parse import urlparse
from pydub import AudioSegment
import whisperx
import unicodedata

# Configuration defaults
DEFAULT_SPEAKER_MAP = {
    'en': ('EN-Default', 'EN'),
    'hi': ('IN-Default', 'IN'),
}
DEFAULT_SPEAKER = 'IN-Default'
DEFAULT_LANG = 'IN'
SIMILARITY_THRESHOLD = 0.90  # for fuzzy deduplication

# WhisperX settings
DEVICE = 'cuda'
MODEL_BATCH_SIZE = 16  # reduce if low on GPU memory
COMPUTE_TYPE = 'float16'  # or 'int8'
MODEL = whisperx.load_model('large-v3-turbo', DEVICE, compute_type=COMPUTE_TYPE)

# Utilities

def clean_text(text: str) -> str:
    text = unicodedata.normalize('NFKC', text)
    text = text.replace(u'\u2018', "'").replace(u'\u2019', "'").replace('–', '')
    text = text.replace('\n', ' ').strip().strip('"\'"')
    emoji_pattern = re.compile('[\U0001F600-\U0001F64F'  # emoticons
                               '\U0001F300-\U0001F5FF'  # symbols & pictographs
                               '\U0001F680-\U0001F6FF'  # transport & map symbols
                               '\U0001F1E0-\U0001F1FF'  # flags
                               ']+', flags=re.UNICODE)
    text = emoji_pattern.sub('', text)
    ascii_emo = re.compile(r'(?:(?:[:;=8])[-^o*]?[)\]\(\[DPp\\/])')
    return ascii_emo.sub('', text)


def is_valid_url(u: str) -> bool:
    p = urlparse(u)
    return p.scheme in ('http', 'https') and bool(p.netloc)


def download_audio(url: str, out_path: str) -> None:
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(out_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def convert_to_wav(src: str, dst: str, target_rate: int = 44100) -> None:
    audio = AudioSegment.from_file(src)
    audio = audio.set_frame_rate(target_rate).set_channels(1)
    audio.export(dst, format='wav')


def count_punct(text: str) -> int:
    return len(re.findall(r'[^\w\s]', text))


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    temp_dir = os.path.join(args.output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    seen_texts, entries, removed = [], [], []

    # Read and dedupe CSV
    with open(args.csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for idx, row in enumerate(reader, start=1):
            if len(row) != 2:
                print(f"Skipping malformed row {idx}: {row}")
                continue
            raw_text, url = row
            text = clean_text(raw_text)
            if len(text.split()) < 4:
                text = ''

            if idx == 1 and not is_valid_url(url):
                removed.append((url, text)); continue
            if not text or not is_valid_url(url):
                removed.append((url, text)); continue

            dup = next((i for i, e in enumerate(seen_texts)
                        if difflib.SequenceMatcher(None, text, e).ratio() >= SIMILARITY_THRESHOLD), None)
            if dup is not None:
                old = seen_texts[dup]
                p_new, p_old = count_punct(text), count_punct(old)
                if p_new > p_old:
                    removed.append((url, text)); continue
                removed.append((entries[dup][1], old))
                seen_texts.pop(dup); entries.pop(dup)

            seen_texts.append(text)
            entries.append((text, url))

    manifest_lines = []

    # Process each entry: download/convert, detect lang, save
    for i, (text, url) in enumerate(entries, start=1):
        lang_code, speaker = DEFAULT_LANG, DEFAULT_SPEAKER
        # Prepare paths
        src = os.path.join(temp_dir, f'src_{i}')
        wav_name = f'audio_{i:03d}.wav'

        if args.download_audio:
            try:
                download_audio(url, src)
                convert_to_wav(src, os.path.join(args.output_dir, wav_name))
            except Exception as e:
                print(f"Error processing {url}: {e}")
                removed.append((url, text)); continue

            wav_path = os.path.join(args.output_dir, wav_name)
            audio = whisperx.load_audio(wav_path)
            detected = MODEL.detect_language(audio)
            code = detected.get('language', args.language)
            # Map to fields and folder
            speaker, lang_code = DEFAULT_SPEAKER_MAP.get(code, (args.speaker, args.language))
            out_dir = os.path.join(args.output_dir, code)
            os.makedirs(out_dir, exist_ok=True)
            final_path = os.path.join(out_dir, wav_name)
            os.replace(wav_path, final_path)
            wav_path = final_path

        manifest_lines.append(f"{wav_path}|{speaker}|{lang_code}|{text}|{code}")

    # Write outputs
    with open(os.path.join(args.output_dir, args.manifest), 'w', encoding='utf-8') as mf:
        mf.write("\n".join(manifest_lines))
    with open(os.path.join(args.output_dir, args.removed), 'w', encoding='utf-8') as rf:
        rf.write("\n".join(f"{u}|{args.speaker}|{args.language}|{t}" for u, t in removed))

    # Cleanup
    for f in os.listdir(temp_dir): os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)
    print(f"Processed {len(manifest_lines)} items. Manifest at {args.manifest}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_path', required=True)
    parser.add_argument('--output-dir', default='preprocessed-data')
    parser.add_argument('--speaker', default=DEFAULT_SPEAKER)
    parser.add_argument('--language', default=DEFAULT_LANG)
    parser.add_argument('--manifest', default='manifest.list')
    parser.add_argument('--removed', default='removed.txt')
    parser.add_argument('--download_audio', action='store_true')
    args = parser.parse_args()
    main(args)
