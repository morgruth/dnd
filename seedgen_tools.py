#!/usr/bin/env python3
"""
Termux-friendly seedgen_tools.py
Saves output to: /storage/emulated/0/Documents/seeds/

Flags supported (you can combine):
    --generate       : Generate a single random seed (binary) and save it
    --binary         : (alias) same as --generate
    --png            : Create a PNG visual from the (most recent) binary
    --wav            : Create a WAV audio file from the (most recent) binary
    --image-bin      : Extract raw bytes from the PNG into image.bin
    --image-hex      : Export the binary file as hex (image.hex)
    --save-all       : Generate N seeds (default 10) -- use --count to override
    --count N        : Number to generate when using --save-all (default 10)
    --analyze        : Analyze a binary (bytes/hex/entropy/integers)
    --chars          : Analyze letters, digits, special printable, non-printable
    --visualize      : Save waveform + spectrogram for the WAV (or from binary if WAV absent)
    --stats          : Print quick stats for the selected binary
    --export         : Export analysis results as JSON (alongside files)
    --input PATH     : Use specified binary file instead of most-recent
    --menu           : Run an interactive menu (if you prefer)
    --quiet          : Avoid showing plots interactively (always saves images)
    --packet-network        : Creates a network packet
    --client        : Starts a client that connects to a server
"""

import argparse
import os
import sys
import time
import struct
import json
import math
from collections import Counter
from datetime import datetime

# Try to import third-party libs but fail gracefully with helpful message
try:
    from PIL import Image
except Exception as e:
    print("Missing dependency: Pillow. Install with: pip install Pillow")
    Image = None

try:
    import numpy as np
except Exception as e:
    print("Missing dependency: numpy. Install with: pip install numpy")
    np = None

try:
    import matplotlib
    # Use non-interactive backend by default (Termux usually headless)
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
except Exception as e:
    print("Missing dependency: matplotlib. Install with: pip install matplotlib")
    plt = None

try:
    from scipy.io import wavfile
    from scipy import signal
except Exception as e:
    print("Missing dependency: scipy. Install with: pip install scipy")
    wavfile = None
    signal = None

import wave
import random

# ------------------------
# Configuration
# ------------------------
OUT_DIR = "workspaces/gamebox/seed"
DEFAULT_COUNT = 10
DEFAULT_BYTES = 125000  # ~1 megabit (125000 bytes)
TIMESTAMP_FMT = "%Y%m%d_%H%M%S"

# Filenames created will be placed inside OUT_DIR

# ------------------------
# Helpers
# ------------------------
def ensure_outdir():
    os.makedirs(OUT_DIR, exist_ok=True)

def now_ts():
    return datetime.now().strftime(TIMESTAMP_FMT)

def make_seed_filename(ts_suffix=None):
    ts = ts_suffix or now_ts()
    return os.path.join(OUT_DIR, f"seed_{ts}.bin")

def make_image_filename(ts_suffix=None):
    ts = ts_suffix or now_ts()
    return os.path.join(OUT_DIR, f"seed_{ts}.png")

def make_wav_filename(ts_suffix=None):
    ts = ts_suffix or now_ts()
    return os.path.join(OUT_DIR, f"seed_{ts}.wav")

def make_hex_filename(bin_path):
    base = os.path.splitext(os.path.basename(bin_path))[0]
    return os.path.join(OUT_DIR, f"{base}.hex")

def make_image_bin_filename(image_path):
    base = os.path.splitext(os.path.basename(image_path))[0]
    return os.path.join(OUT_DIR, f"{base}_image.bin")

def find_most_recent_bin():
    files = [os.path.join(OUT_DIR, f) for f in os.listdir(OUT_DIR) if f.lower().endswith(".bin")]
    if not files:
        return None
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return files[0]

def safe_open_read(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    return open(path, "rb")

# ------------------------
# Core functionality
# ------------------------

def generate_one(file_size=DEFAULT_BYTES, path=None):
    """Generate a single random binary file and save it. Returns path."""
    ensure_outdir()
    path = path or make_seed_filename()
    data = os.urandom(file_size)
    with open(path, "wb") as f:
        f.write(data)
    print(f"[OK] Generated binary: {path} ({file_size} bytes)")
    return path

def binary_to_png(bin_path=None, width=None, height=None):
    """Convert binary to grayscale PNG. If width/height omitted, choose square."""
    if Image is None:
        raise RuntimeError("Pillow not installed.")
    ensure_outdir()
    bin_path = bin_path or find_most_recent_bin()
    if not bin_path:
        print("[ERROR] No binary file found. Generate one first (--generate).")
        return None
    with open(bin_path, "rb") as f:
        data = f.read()

    if width and height:
        w, h = width, height
        needed = w * h
        if len(data) < needed:
            data = data + b'\x00' * (needed - len(data))
        else:
            data = data[:needed]
    else:
        side = int(len(data) ** 0.5)
        if side < 1:
            print("[ERROR] Binary too small to create image.")
            return None
        w = h = side
        data = data[:w*h]

    img = Image.frombytes('L', (w, h), data)
    out_path = make_image_filename(ts_suffix=os.path.splitext(os.path.basename(bin_path))[0] + "_" + now_ts())
    img.save(out_path)
    print(f"[OK] Saved PNG: {out_path} (size {w}x{h})")
    return out_path

def binary_to_wav(bin_path=None, sample_width=2, frame_rate=44100):
    """Convert binary to WAV. sample_width must be 1 or 2."""
    ensure_outdir()
    bin_path = bin_path or find_most_recent_bin()
    if not bin_path:
        print("[ERROR] No binary file found. Generate one first (--generate).")
        return None
    with open(bin_path, "rb") as f:
        data = f.read()
    if sample_width not in (1, 2):
        raise ValueError("sample_width must be 1 or 2")

    # Make length multiple of sample width
    n_frames = len(data) // sample_width
    data = data[:n_frames * sample_width]

    if sample_width == 2:
        fmt = '<' + 'h' * (len(data) // 2)
        try:
            samples = struct.unpack(fmt, data)
        except struct.error:
            # fallback: interpret raw bytes as unsigned then shift
            samples = [int.from_bytes(data[i:i+2], 'little', signed=False) - 32768
                       for i in range(0, len(data), 2)]
    else:
        fmt = '<' + 'B' * len(data)
        samples = struct.unpack(fmt, data)

    wav_path = make_wav_filename(ts_suffix=os.path.splitext(os.path.basename(bin_path))[0] + "_" + now_ts())
    with wave.open(wav_path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(frame_rate)
        # repack to bytes
        wf.writeframes(struct.pack(fmt, *samples))
    print(f"[OK] Saved WAV: {wav_path} (rate={frame_rate}, width={sample_width})")
    return wav_path

def image_to_binary(image_path=None):
    """Given a PNG path (or most recent), extract raw pixel bytes into a .bin."""
    if Image is None:
        raise RuntimeError("Pillow not installed.")
    image_path = image_path or find_most_recent_png()
    if not image_path:
        print("[ERROR] No PNG found. Create one first (--png).")
        return None
    with Image.open(image_path) as im:
        px = im.load()
        w, h = im.size
        out_path = make_image_bin_filename(image_path)
        with open(out_path, "wb") as out:
            for y in range(h):
                for x in range(w):
                    p = px[x, y]
                    if isinstance(p, tuple):
                        out.write(struct.pack('B' * len(p), *p))
                    else:
                        out.write(struct.pack('B', p))
    print(f"[OK] Extracted image bytes to: {out_path}")
    return out_path

def find_most_recent_png():
    files = [os.path.join(OUT_DIR, f) for f in os.listdir(OUT_DIR) if f.lower().endswith(".png")]
    if not files:
        return None
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return files[0]

def binary_to_hex(bin_path=None):
    bin_path = bin_path or find_most_recent_bin()
    if not bin_path:
        print("[ERROR] No binary file found.")
        return None
    with open(bin_path, "rb") as f:
        data = f.read()
    hex_text = data.hex()
    out = make_hex_filename(bin_path)
    with open(out, "w") as w:
        w.write(hex_text)
    print(f"[OK] Saved hex: {out}")
    return out

# ------------------------
# Analysis functions
# ------------------------
def analyze_binary(bin_path=None):
    """Detailed analysis: hex/text preview, byte distribution, entropy, integer decode."""
    bin_path = bin_path or find_most_recent_bin()
    if not bin_path:
        print("[ERROR] No binary file found to analyze.")
        return None
    with open(bin_path, "rb") as f:
        data = f.read()
    total = len(data)
    print(f"Analyzing: {bin_path}")
    print(f"Total bytes: {total}")
    print(f"First 1024 hex chars: {data.hex()[:1024]}")
    print(f"First 1024 text (with replacement): {data.decode(errors='replace')[:1024]}")

    counts = Counter(data)
    print(f"Unique byte values: {len(counts)}")
    print("Top 16 bytes (hex:count):")
    for b, c in counts.most_common(16):
        print(f"  {b:02x} : {c}")

    # Shannon entropy
    entropy = -sum((c/total) * math.log2(c/total) for c in counts.values())
    print(f"Shannon entropy: {entropy:.4f} bits/byte (max 8.0)")

    # 32-bit signed integer decode (if possible)
    nints = total // 4
    ints = []
    if nints > 0:
        try:
            ints = list(struct.unpack(f"{nints}i", data[:nints*4]))
            print(f"Decoded {len(ints)} 32-bit integers. First 8: {ints[:8]}")
        except struct.error as e:
            print(f"[WARN] integer decode failed: {e}")

    return {
        "path": bin_path,
        "total_bytes": total,
        "unique_bytes": len(counts),
        "top_bytes": counts.most_common(32),
        "entropy": entropy,
        "first_integers": ints[:16],
    }

def analyze_chars(bin_path=None):
    """Classify bytes into Uppercase/Lowercase/Digit/Special/Non-printable and show counts + top specials."""
    bin_path = bin_path or find_most_recent_bin()
    if not bin_path:
        print("[ERROR] No binary file found to analyze.")
        return None
    with open(bin_path, "rb") as f:
        data = f.read()
    total = len(data)

    def classify(b):
        if 65 <= b <= 90:
            return "Uppercase"
        elif 97 <= b <= 122:
            return "Lowercase"
        elif 48 <= b <= 57:
            return "Digit"
        elif 32 <= b <= 126:
            return "Special"
        else:
            return "Non-printable"

    counts = Counter(classify(b) for b in data)
    print(f"Char classification for: {bin_path}")
    for cat in ("Uppercase", "Lowercase", "Digit", "Special", "Non-printable"):
        c = counts.get(cat, 0)
        pct = (c / total) * 100 if total else 0.0
        print(f"{cat:14s}: {c:8d} ({pct:5.2f}%)")

    # list top printable special characters
    specials = Counter()
    for b in data:
        if 32 <= b <= 126 and not (48 <= b <= 57 or 65 <= b <= 90 or 97 <= b <= 122):
            specials[chr(b)] += 1
    if specials:
        print("\nTop printable special characters:")
        for s, cnt in specials.most_common(20):
            print(f"  '{s}' : {cnt}")
    return {
        "path": bin_path,
        "counts": counts,
        "top_specials": specials.most_common(20),
    }

# ------------------------
# Visualization + export
# ------------------------
def save_waveform_and_spectrogram(wav_path=None):
    """Save waveform and spectrogram images (requires scipy & matplotlib)."""
    if wavfile is None or signal is None or plt is None:
        print("[ERROR] scipy and matplotlib are required for audio visualization.")
        return None
    wav_path = wav_path or find_most_recent_wav_or_generate()
    if not wav_path:
        print("[ERROR] No WAV available for visualization.")
        return None
    sr, samples = wavfile.read(wav_path)
    if samples.ndim > 1:
        samples = samples[:, 0]

    times = np.linspace(0, len(samples) / sr, num=len(samples))
    frequencies, times_spec, Sxx = signal.spectrogram(samples, sr)
    Sxx_db = 10 * np.log10(Sxx + 1e-10)

    out_path = os.path.join(OUT_DIR, f"audio_vis_{os.path.splitext(os.path.basename(wav_path))[0]}_{now_ts()}.png")
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(times, samples)
    plt.title("Waveform")
    plt.xlabel("Time [s]")

    plt.subplot(1, 2, 2)
    plt.pcolormesh(times_spec, frequencies, Sxx_db, shading='gouraud')
    plt.title("Spectrogram")
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")

    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[OK] Saved audio visualization: {out_path}")
    return out_path

def find_most_recent_wav_or_generate():
    files = [os.path.join(OUT_DIR, f) for f in os.listdir(OUT_DIR) if f.lower().endswith(".wav")]
    if files:
        files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return files[0]
    # try to generate from most recent bin
    recent_bin = find_most_recent_bin()
    if recent_bin:
        return binary_to_wav(recent_bin)
    return None

def export_analysis_json(result: dict, prefix: str = "analysis"):
    ensure_outdir()
    if not result:
        print("[WARN] Nothing to export.")
        return None
    base = os.path.splitext(os.path.basename(result.get("path", "analysis")))[0]
    out_path = os.path.join(OUT_DIR, f"{base}_{prefix}_{now_ts()}.json")
    # Make JSON serializable for Counter items
    serial = {}
    for k, v in result.items():
        if isinstance(v, Counter):
            serial[k] = v.most_common()
        else:
            try:
                json.dumps({k: v})
                serial[k] = v
            except Exception:
                serial[k] = str(v)
    # If result is a dict, just dump it
    with open(out_path, "w") as f:
        json.dump(result, f, default=lambda o: str(o), indent=2)
    print(f"[OK] Exported analysis JSON: {out_path}")
    return out_path

# ------------------------
# Menu (simple)
# ------------------------
def interactive_menu():
    ensure_outdir()
    while True:
        print("\nSeedGen Interactive Menu")
        print("1) Generate one seed")
        print("2) Generate PNG from latest binary")
        print("3) Generate WAV from latest binary")
        print("4) Analyze latest binary (detailed)")
        print("5) Analyze chars (letters/digits/special)")
        print("6) Save waveform & spectrogram")
        print("0) Exit")
        c = input("Choice: ").strip()
        if c == "1":
            generate_one()
        elif c == "2":
            binary_to_png()
        elif c == "3":
            binary_to_wav()
        elif c == "4":
            analyze_binary()
        elif c == "5":
            analyze_chars()
        elif c == "6":
            save_waveform_and_spectrogram()
        elif c == "0":
            break
        else:
            print("Unknown choice.")

# ------------------------
# CLI parsing
# ------------------------
def main():
    parser = argparse.ArgumentParser(description="SeedGen Tools (Termux-friendly)")
    parser.add_argument("--generate", action="store_true", help="Generate a single random binary")
    parser.add_argument("--binary", action="store_true", help="Alias for --generate")
    parser.add_argument("--png", action="store_true", help="Create PNG from binary")
    parser.add_argument("--wav", action="store_true", help="Create WAV from binary")
    parser.add_argument("--image-bin", dest="image_bin", action="store_true", help="Extract image -> image.bin")
    parser.add_argument("--image-hex", action="store_true", help="Export binary as hex to .hex file")
    parser.add_argument("--save-all", action="store_true", help="Generate multiple seeds")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT, help="Count for --save-all (default 10)")
    parser.add_argument("--analyze", action="store_true", help="Detailed binary analysis")
    parser.add_argument("--chars", action="store_true", help="Analyze letters/digits/specials")
    parser.add_argument("--visualize", action="store_true", help="Save waveform + spectrogram")
    parser.add_argument("--stats", action="store_true", help="Quick stats for binary")
    parser.add_argument("--export", action="store_true", help="Export analysis to JSON")
    parser.add_argument("--input", type=str, default=None, help="Input binary file to operate on")
    parser.add_argument("--menu", action="store_true", help="Run interactive menu")
    parser.add_argument("--quiet", action="store_true", help="Suppress interactive plotting (use only save files)")
    args = parser.parse_args()

    ensure_outdir()

    # If menu requested, go interactive and exit
    if args.menu:
        interactive_menu()
        return

    # If save-all requested: generate N seeds
    generated_files = []
    if args.save_all:
        for i in range(args.count):
            generated_files.append(generate_one(file_size=DEFAULT_BYTES))
    elif args.generate or args.binary:
        generated_files.append(generate_one(file_size=DEFAULT_BYTES))

    # Determine target binary for downstream ops
    target_bin = args.input if args.input else find_most_recent_bin()

    # If png requested
    if args.png:
        png_path = binary_to_png(bin_path=target_bin)
        # optional image->bin if requested
        if args.image_bin and png_path:
            image_to_binary(png_path)

    # If wav requested
    if args.wav:
        binary_to_wav(bin_path=target_bin)

    # image-hex
    if args.image_hex:
        binary_to_hex(bin_path=target_bin)

    # analyze
    results = None
    if args.analyze:
        results = analyze_binary(bin_path=target_bin)
    if args.chars:
        char_results = analyze_chars(bin_path=target_bin)
        if results:
            results['char_analysis'] = char_results

    # stats: quick print of totals & top 5 bytes
    if args.stats:
        if not target_bin:
            print("[ERROR] No binary available for stats.")
        else:
            with open(target_bin, "rb") as f:
                d = f.read()
            c = Counter(d)
            total = len(d)
            print(f"Quick stats for: {target_bin}")
            print(f"Total bytes: {total}")
            print("Top 5 bytes (hex:count):")
            for b, cnt in c.most_common(5):
                print(f"  {b:02x} : {cnt}")

    # visualize
    if args.visualize:
        save_waveform_and_spectrogram()

    # export results if asked
    if args.export and results:
        export_analysis_json(results)

    # If nothing passed, show help
    if len(sys.argv) == 1:
        parser.print_help()

if __name__ == "__main__":
    # adapt old flag name: argparse does not allow hyphen variable names directly in namespace
    # To support earlier code that referenced args.save_all, set alias:
    # (We'll parse normally and handle in main)
    # Run main
    # Small compatibility shim: map env var or similar not necessary
    # Launch
    # Create OUT_DIR if missing
    ensure_outdir()
    # Run main
    main()