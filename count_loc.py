import os

EXCLUDE_DIRS = {
    'node_modules', '.git', 'venv', 'env', '.pytest_cache', 'dist', 'build',
    '__pycache__', 'uploads', '.system_generated', 'brain'
}

EXCLUDE_EXTS = {
    '.db', '.sqlite', '.sqlite3', '.png', '.jpg', '.jpeg', '.gif', '.ico',
    '.pdf', '.zip', '.tar', '.gz', '.log', '.bin', '.exe', '.dll', '.so',
    '.dylib', '.pyc', '.pyo'
}

def is_meaningful_line(line):
    s = line.strip()
    if not s:
        return False
    # Exclude pure comment lines
    if s.startswith('#') or s.startswith('//') or s.startswith('/*') or s.startswith('*'):
        return False
    return True

def count_file_loc(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            return sum(1 for line in lines if is_meaningful_line(line))
    except Exception:
        return 0

def run_loc_counter(root_dir):
    categories = {
        'Backend LOC': 0,
        'Frontend LOC': 0,
        'Tests LOC': 0,
        'Utilities LOC': 0,
        'Configuration LOC': 0,
        'Documentation LOC': 0
    }

    for current_root, dirs, files in os.walk(root_dir):
        # Prune excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue

            rel_path = os.path.relpath(os.path.join(current_root, file), root_dir).replace('\\', '/')
            
            # Skip package-lock or compiled bundle files
            if file in ['package-lock.json', 'yarn.lock']:
                continue

            loc = count_file_loc(os.path.join(current_root, file))

            if 'test' in rel_path.lower() or file.startswith('test_'):
                categories['Tests LOC'] += loc
            elif rel_path.startswith('docs/') or file.endswith('.md'):
                categories['Documentation LOC'] += loc
            elif rel_path.startswith('frontend/'):
                categories['Frontend LOC'] += loc
            elif rel_path.startswith('backend/app/utils') or 'services' in rel_path or 'utils' in rel_path:
                categories['Utilities LOC'] += loc
            elif rel_path.startswith('backend/'):
                categories['Backend LOC'] += loc
            elif file in ['config.py', 'package.json', 'vite.config.js', '.env', '.gitignore', 'pytest.ini']:
                categories['Configuration LOC'] += loc
            else:
                categories['Utilities LOC'] += loc

    total_loc = sum(categories.values())
    categories['TOTAL LOC'] = total_loc
    return categories

if __name__ == '__main__':
    project_root = os.path.abspath(os.path.dirname(__file__))
    res = run_loc_counter(project_root)

    print("=" * 40)
    print("      ACTUAL LINES OF CODE (LOC) REPORT")
    print("=" * 40)
    for cat, loc in res.items():
        print(f"{cat:<20}: {loc:>8,}")
    print("=" * 40)
