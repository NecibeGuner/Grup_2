import os

def has_null_bytes(path):
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                return False
            if b'\x00' in chunk:
                return True

root = os.getcwd()
found = False

for dirpath, _, files in os.walk(root):
    for fn in files:
        if fn.endswith('.py'):
            full = os.path.join(dirpath, fn)
            if has_null_bytes(full):
                print(f"⚠️ Null baytı bulundu: {full}")
                found = True

if not found:
    print("✅ Hiçbir .py dosyasında null baytı bulunmadı.")