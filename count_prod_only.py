import os

PROD_DIRS = ['backend/app', 'frontend/src']
VALID_EXTS = {'.py', '.js', '.jsx'}

def is_meaningful(line):
    s = line.strip()
    if not s:
        return False
    if s.startswith('#') or s.startswith('//') or s.startswith('/*') or s.startswith('*'):
        return False
    return True

py_loc = 0
js_loc = 0

for pdir in PROD_DIRS:
    for root, dirs, files in os.walk(pdir):
        if 'tests' in root or '__pycache__' in root or 'node_modules' in root:
            continue
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTS and not file.startswith('test_'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        count = sum(1 for line in f if is_meaningful(line))
                        if ext == '.py':
                            py_loc += count
                        else:
                            js_loc += count
                except Exception:
                    pass

print("========================================")
print("   TRAINPLEX PROD APPLICATION LOC REPORT")
print("========================================")
print(f"Python Prod LOC    : {py_loc:>8,}")
print(f"JavaScript Prod LOC: {js_loc:>8,}")
print(f"TOTAL PROD LOC     : {py_loc + js_loc:>8,}")
print("========================================")
