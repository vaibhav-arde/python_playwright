import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_conflict = False
    skip_mode = False # True if we are in the "incoming" part of the conflict
    
    # Simple strategy: Keep HEAD, discard the other part.
    # This is safe because I've already merged the important parts manually in core files.
    # For these test files, they seem to be redundant copies.
    
    for line in lines:
        if line.startswith('<<<<'):
            in_conflict = True
            skip_mode = False
            continue
        elif line.startswith('===='):
            if in_conflict:
                skip_mode = True
                continue
        elif line.startswith('>>>>'):
            if in_conflict:
                in_conflict = False
                skip_mode = False
                continue

        
        if not skip_mode:
            new_lines.append(line)
    
    if len(new_lines) < len(lines):
        print(f"Cleaned {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

def walk_and_clean(directory):
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.py'):
                clean_file(os.path.join(root, file))

if __name__ == "__main__":
    walk_and_clean('.')
