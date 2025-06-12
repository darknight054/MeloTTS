import os
import argparse
from pydub import AudioSegment
import whisperx

# WhisperX settings
DEVICE = 'cuda'
COMPUTE_TYPE = 'float16'  # or 'int8'


def load_alignment_models(langs=('en', 'hi')):
    """
    Preload WhisperX alignment models for given language codes.
    Returns a dict: lang -> (model, metadata).
    """
    models = {}
    for code in langs:
        print(f"Loading alignment model for '{code}'...")
        models[code] = whisperx.load_align_model(language_code=code, device=DEVICE)
    return models


def segment_manifest(manifest_path: str, output_dir: str, align_models):
    """
    Read manifest.list with format:
      path|speaker|default_lang_code|text|detected_lang
    and segment each English/Hindi audio into <=15s chunks using WhisperX alignment.
    Outputs clips to preprocessed-segment-data/ and writes manifest-segment.list.
    """
    # Prepare directories
    os.makedirs(output_dir, exist_ok=True)
    segment_dir = os.path.join(output_dir, 'preprocessed-segment-data')
    # Clear or create segment directory
    if os.path.isdir(segment_dir):
        # Remove old contents
        for f in os.listdir(segment_dir):
            os.remove(os.path.join(segment_dir, f))
    else:
        os.makedirs(segment_dir)

    seg_manifest_path = os.path.join(output_dir, 'manifest-segment.list')
    # Remove old manifest if exists
    if os.path.isfile(seg_manifest_path):
        os.remove(seg_manifest_path)

    with open(manifest_path, 'r', encoding='utf-8') as base_mf, \
         open(seg_manifest_path, 'w', encoding='utf-8') as seg_mf:
        for line in base_mf:
            parts = line.strip().split('|', 4)
            if len(parts) != 5:
                print(f"Skipping malformed line: {line.strip()}")
                continue
            path, speaker, default_code, text, lang = parts
            if lang not in align_models:
              continue

            # Load and duration
            audio = AudioSegment.from_wav(path)
            duration = len(audio) / 1000.0
            print(duration)
            # Align full segment
            segments = [{'text': text, 'start': 0.0, 'end': duration}]
            model_a, metadata = align_models[lang]
            print(f"Aligning audio '{path}' ({lang})...")
            result = whisperx.align(
                segments,
                model_a,
                metadata,
                whisperx.load_audio(path),
                DEVICE,
                return_char_alignments=False
            )
            aligned = result['segments']

            # Chunk <=15s
            chunks, current = [], []
            for seg in aligned:
                if not current or (seg['end'] - current[0]['start']) <= 15.0:
                    current.append(seg)
                else:
                    chunks.append(current)
                    current = [seg]
            if current:
                chunks.append(current)

            base_name = os.path.splitext(os.path.basename(path))[0]
            for idx, chunk in enumerate(chunks, start=1):
                start, end = chunk[0]['start'], chunk[-1]['end']
                clip = audio[int(start * 1000):int(end * 1000)]
                clip = clip.set_frame_rate(44100)
                fname = f"{base_name}_seg_{idx:03d}.wav"
                out_path = os.path.join(segment_dir, fname)
                clip.export(out_path, format='wav')

                chunk_text = ' '.join(c['text'].strip() for c in chunk)
                seg_mf.write(f"{out_path}|{speaker}|{default_code}|{chunk_text}|{lang}\n")

    print(f"Segmented audio and wrote manifest to: {seg_manifest_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Segment audio from manifest.list into <=15s clips with WhisperX alignment"
    )
    parser.add_argument(
        '--manifest', default='preprocessed-data/manifest.list',
        help="Path to the existing manifest.list"
    )
    parser.add_argument(
        '--output-dir', default='preprocessed-data-segment',
        help="Directory where segmented data and new manifest will be stored"
    )
    args = parser.parse_args()

    # Load models first
    align_models = load_alignment_models()
    # Start processing
    segment_manifest(args.manifest, args.output_dir, align_models)
