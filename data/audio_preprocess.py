import os
import csv
import re
import argparse
import difflib
import requests
from urllib.parse import urlparse
from pydub import AudioSegment
# Import your Indic language identifier model
from ai4bharat.IndicLID import IndicLID
import unicodedata

# Configuration defaults
DEFAULT_SPEAKER = "IN-default"
DEFAULT_LANG = "IN"
SIMILARITY_THRESHOLD = 0.90  # for fuzzy deduplication
IndicLID_model = IndicLID(input_threshold = 0.5, roman_lid_threshold = 0.6)

def clean_text(text: str) -> str:
    """
    Normalize text by:
    - Unicode normalization (NFKC) to standardize curly quotes and other symbols
    - Replacing newlines with spaces
    - Stripping leading/trailing whitespace
    - Stripping all leading/trailing single or double quotes
    - Removing Unicode emoji
    - Removing ASCII emoticons
    """
    # Unicode normalize to NFKC (decompose and compatibility fold)
    text = unicodedata.normalize('NFKC', text)
    text = text.replace(u'\u2018', "'").replace(u'\u2019', "'").replace('–', '')
    # Replace newlines with spaces
    text = text.replace('\n', ' ')
    # Strip whitespace
    text = text.strip()
    # Strip all leading/trailing quotes (both single and double)
    text = text.strip('"\'')

    # Remove Unicode emoji (common emoji ranges)
    emoji_pattern = re.compile(
        '['
        '\U0001F600-\U0001F64F'  # emoticons
        '\U0001F300-\U0001F5FF'  # symbols & pictographs
        '\U0001F680-\U0001F6FF'  # transport & map symbols
        '\U0001F1E0-\U0001F1FF'  # flags
        ']+',
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)

    # Remove ASCII emoticons like :-) :D ;P etc.
    ascii_emo_pattern = re.compile(r'(?:(?:[:;=8])[-^o*]?[)\]\(\[DPp/\\])')
    text = ascii_emo_pattern.sub('', text)

    return text


def is_valid_url(u: str) -> bool:
    """
    Simple URL validation: must have http(s) scheme and network location.
    """
    p = urlparse(u)
    return p.scheme in ('http', 'https') and bool(p.netloc)


def download_audio(url: str, out_path: str) -> None:
    """
    Download audio from URL to out_path.
    """
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(out_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)


def convert_to_wav(src_path: str, dst_path: str, target_rate: int = 44100) -> None:
    """
    Convert any audio file at src_path to WAV at target_rate Hz.
    """
    audio = AudioSegment.from_file(src_path)
    audio = audio.set_frame_rate(target_rate).set_channels(1)
    audio.export(dst_path, format='wav')


def count_punct(text: str) -> int:
    """
    Count punctuation characters in text.
    """
    return len(re.findall(r'[^\w\s]', text))


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)
    temp_dir = os.path.join(args.output_dir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    seen_texts = []         # list of cleaned texts kept
    entries = []            # list of (text, url) kept
    removed_entries = []    # list of (url, text) removed

    # Read CSV
    with open(args.csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row_num, row in enumerate(reader, start=1):
            if len(row) != 2:
                print(f"Skipping malformed row {row_num}: {row}")
                continue
            raw_text, url = row
            text = clean_text(raw_text)
            if len(text.split()) < 4:
              text = ""

            # Header row
            if row_num == 1 and not is_valid_url(url):
                print(f"Skipping header at row {row_num}")
                removed_entries.append((url, text))
                continue

            # Invalid URL or empty text
            if not text or not is_valid_url(url):
                print(f"Skipping invalid URL or empty text at row {row_num}: {url}")
                removed_entries.append((url, text))
                continue

            # Duplicate detection: prefer text with fewer punctuation marks
            dup_index = None
            for i, existing in enumerate(seen_texts):
                if difflib.SequenceMatcher(None, text, existing).ratio() >= SIMILARITY_THRESHOLD:
                    dup_index = i
                    break

            if dup_index is not None:
                existing_text = seen_texts[dup_index]
                existing_url = entries[dup_index][1]
                p_new = count_punct(text)
                p_old = count_punct(existing_text)
                if p_new > p_old:
                    print(f"Skipping duplicate (more punctuation) at row {row_num}")
                    removed_entries.append((url, text))
                    continue
                else:
                    print(f"Removing prior duplicate (more punctuation) at row {dup_index+1}")
                    removed_entries.append((existing_url, existing_text))
                    seen_texts.pop(dup_index)
                    entries.pop(dup_index)

            seen_texts.append(text)
            entries.append((text, url))

    # Language identification
    test_samples = [text for text, _ in entries]
    predictions = IndicLID_model.batch_predict(test_samples, batch_size=args.batch_size)

    manifest_lines = []
    # Iterate each entry alongside its prediction
    for idx, ((text, url), pred) in enumerate(zip(entries, predictions), start=1):
        # pred may contain more fields; we assume language code is second element
        try:
            lang_script = pred[1]
        except Exception:
            # Fallback to default
            lang_script = args.language
        # Determine folder: english if Latin script, else use detected code
        folder = 'english' 
        if 'Latn' in lang_script:
          folder = "english"
        elif 'Deva' in lang_script:
          folder = "hindi"
        else:
          folder = lang_script
        lang_dir = os.path.join(args.output_dir, folder)
        os.makedirs(lang_dir, exist_ok=True)
        wav_name = f"audio_{idx:03d}.wav"
        wav_path = os.path.join(lang_dir, wav_name)
        temp_src = os.path.join(temp_dir, f"src_{idx}")

        if args.download_audio:
            try:
                download_audio(url, temp_src)
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                removed_entries.append((url, text))
                continue

            try:
                convert_to_wav(temp_src, wav_path, target_rate=44100)
            except Exception as e:
                print(f"Failed to convert {temp_src}: {e}")
                removed_entries.append((url, text))
                continue

        manifest_lines.append(f"{wav_path}|{args.speaker}|{lang_script}|{text}")

    # Write manifest
    manifest_path = os.path.join(args.output_dir, args.manifest)
    with open(manifest_path, 'w', encoding='utf-8') as mf:
        for line in manifest_lines:
            mf.write(line + '\n')

    # Write removed entries
    removed_path = os.path.join(args.output_dir, args.removed)
    with open(removed_path, 'w', encoding='utf-8') as rf:
        for url, text in removed_entries:
            rf.write(f"{url}|{args.speaker}|{args.language}|{text}\n")

    # Cleanup temp
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))
    os.rmdir(temp_dir)

    print(f"Processed {len(manifest_lines)} files. Manifest saved to {manifest_path}")
    print(f"Recorded {len(removed_entries)} removed entries in {removed_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Preprocess audio CSV and generate WAV manifest with language routing.")
    parser.add_argument('--csv_path', required=True, help="Path to input CSV file (pipe-separated)")
    parser.add_argument('--output-dir', default='preprocessed-data', help="Directory to save WAVs and manifests")
    parser.add_argument('--speaker', default=DEFAULT_SPEAKER, help="Speaker name field")
    parser.add_argument('--language', default=DEFAULT_LANG, help="Default language code for removed entries")
    parser.add_argument('--manifest', default='manifest.list', help="Name of the output manifest file")
    parser.add_argument('--removed', default='removed.txt', help="Name of the removed-items file")
    parser.add_argument('--download_audio', action='store_true', help="Flag to download and convert audio files")
    parser.add_argument('--batch_size', type=int, default=32, help="Batch size for language identification model")
    args = parser.parse_args()
    main(args)
