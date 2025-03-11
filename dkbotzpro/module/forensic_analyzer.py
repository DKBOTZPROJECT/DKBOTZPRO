import os
import math
import hashlib
import collections

def format_status(text):
    return " ".join(word.capitalize() for word in text.strip().split())

def calc_entropy(data):
    if not data:
        return 0
    freq = collections.Counter(data)
    probs = [v / len(data) for v in freq.values()]
    return -sum(p * math.log2(p) for p in probs)

def get_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            md5.update(chunk)
    return md5.hexdigest()

def read_tail(file_path, size_kb=500):
    size = os.path.getsize(file_path)
    with open(file_path, "rb") as f:
        if size > size_kb * 1024:
            f.seek(-size_kb * 1024, os.SEEK_END)
        return f.read()

def get_eof_offset(data, ext):
    ext = ext.lower()
    if ext in [".jpg", ".jpeg"]:
        return data.rfind(b'\xff\xd9') + 2
    elif ext == ".png":
        return data.rfind(b'IEND') + 4
    elif ext == ".gif":
        return data.rfind(b'\x3b') + 1
    elif ext == ".bmp":
        return len(data)
    elif ext == ".webp":
        return data.rfind(b'WEBP') + 4
    elif ext == ".tiff":
        return len(data)
    elif ext == ".ico":
        return len(data)
    elif ext == ".mp4":
        return data.rfind(b'mdat') + 4
    elif ext == ".mov":
        return data.rfind(b'moov') + 4
    elif ext == ".avi":
        return data.rfind(b'idx1') + 4
    elif ext == ".mkv":
        return data.rfind(b'\x1a\x45\xdf\xa3') + 4
    elif ext == ".flv":
        return data.rfind(b'FLV') + 3
    elif ext == ".webm":
        return data.rfind(b'\x1a\x45\xdf\xa3') + 4
    elif ext == ".wmv":
        return data.rfind(b'\x30\x26\xb2\x75') + 4
    elif ext == ".3gp":
        return data.rfind(b'mdat') + 4
    elif ext == ".zip":
        return data.rfind(b'PK\x05\x06') + 22
    elif ext == ".rar":
        return data.rfind(b'Rar!\x1a\x07\x00') + 7
    elif ext == ".7z":
        return data.rfind(b'7z\xbc\xaf\x27\x1c') + 6
    elif ext in [".tar", ".gz", ".bz2", ".xz", ".iso"]:
        return len(data)
    elif ext == ".pdf":
        return data.rfind(b'%%EOF') + 5
    elif ext in [".docx", ".xlsx", ".pptx"]:
        return data.rfind(b'PK\x05\x06') + 22
    elif ext in [".exe", ".dll"]:
        return len(data)
    elif ext in [".mp3", ".wav", ".ogg", ".flac"]:
        return len(data)
    return -1

def analyze_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    data_tail = read_tail(file_path)
    entropy_total = calc_entropy(data_tail)
    md5_hash = get_md5(file_path)

    print("\n🔍", format_status(f"Analyzing File: {file_path}"))
    print("📂", format_status(f"File Type Detected: {ext if ext else 'Unknown'}"))
    print("🧾", format_status(f"MD5 Hash: {md5_hash}"))
    print("📊", format_status(f"Entropy In Last 500KB: {entropy_total:.4f} (Max: 8.0)"))

    offset = get_eof_offset(data_tail, ext)

    if offset == -1 or offset >= len(data_tail):
        print("❌", format_status("Unsupported File Type Or EOF Marker Not Found"))
        print("ℹ️", format_status("Only Entropy Check Completed"))
        print("📌", format_status("Status: Neutral\n"))
        return

    after_eof = data_tail[offset:]
    entropy_after = calc_entropy(after_eof)

    if len(after_eof) < 32:
        print("✅", format_status("No Suspicious Data Found After EOF Marker"))
        print("📌", format_status("Status: Safe\n"))
        return

    print("📍", format_status(f"Data Found After EOF Marker: {len(after_eof)} Bytes"))
    print("📈", format_status(f"Entropy Of Extra Data: {entropy_after:.4f}"))

    if entropy_after > 7.4 and len(after_eof) > 64:
        print("🚨", format_status("High Entropy Data Detected After File End!"))
        print("⚠️", format_status("Status: Suspicious - Possible Hidden Content\n"))
    else:
        print("✅", format_status("No Significant Anomalies Found After File End"))
        print("📌", format_status("Status: Safe\n"))

    print("🧬", format_status("First 32 Bytes After EOF (Hex Preview):"))
    print(after_eof[:32].hex())

if __name__ == "__main__":
    path = input("📁 Enter File Path To Analyze: ")
    if not os.path.isfile(path):
        print("❌", format_status("File Not Found Or Not A Regular File"))
    else:
        analyze_file(path)
