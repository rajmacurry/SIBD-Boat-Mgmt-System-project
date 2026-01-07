
import glob

def fix_files():
    files = glob.glob("*.cgi") + glob.glob("*.py")
    files = [f for f in files if "force_linux_format.py" not in f]
    
    print(f"Scanning {len(files)} files...")
    
    for filename in files:
        with open(filename, 'rb') as f:
            content = f.read()
        
        # Replace CRLF with LF
        new_content = content.replace(b'\r\n', b'\n')
        
        # Ensure shebang is correct for CGI
        if filename.endswith('.cgi') or filename == 'main.py':
            if new_content.startswith(b'#!') and b'python' in new_content.split(b'\n')[0].lower():
                 lines = new_content.split(b'\n')
                 lines[0] = b'#!/usr/bin/python3'
                 new_content = b'\n'.join(lines)
        
        if new_content != content:
            print(f"Fixing {filename}...")
            with open(filename, 'wb') as f:
                f.write(new_content)
        else:
            print(f"Clean {filename}")

if __name__ == '__main__':
    fix_files()
