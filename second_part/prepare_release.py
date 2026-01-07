import os
import glob
import sys

# Standard Linux Shebang for the university server
LINUX_SHEBANG = "#!/usr/bin/python3\n"

def normalize_files():
    files = glob.glob("*.cgi") + glob.glob("*.py")
    
    print(f"Scanning {len(files)} files for Linux compatibility...")
    
    for file_path in files:
        if file_path == os.path.basename(__file__):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.splitlines(keepends=True)
            modified = False
            
            # 1. Fix Shebang (only for executable scripts)
            if file_path.endswith('.cgi') or file_path == 'main.py': # logic: only entry points need shebang strictly, but harmless on others usually.
                if lines and (not lines[0].startswith("#!") or "python" in lines[0].lower()):
                    if lines[0] != LINUX_SHEBANG:
                        print(f"  [Shebang] Updating {file_path}")
                        if lines[0].startswith("#!"):
                            lines[0] = LINUX_SHEBANG
                        else:
                            lines.insert(0, LINUX_SHEBANG)
                        modified = True
            
            # 2. Fix Line Endings (CRLF -> LF)
            # Reconstruct content with \n only
            new_content = "".join(lines).replace("\r\n", "\n")
            if new_content != content:
               # Just saving it purely with \n might be enough if opened in 'w' mode with newline='\n'?
               # Actually, python 'w' mode translates \n to os.linesep (CRLF on Windows).
               # We must write in binary mode or force newline.
               pass 
               
            # Write back
            if modified or "\r\n" in content:
                print(f"  [LineEnd] Normalizing {file_path}")
                with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                    f.writelines(lines)
                    
        except Exception as e:
            print(f"  [Error] {file_path}: {e}")

if __name__ == "__main__":
    normalize_files()
    print("Done! Files are ready for SCP.")
