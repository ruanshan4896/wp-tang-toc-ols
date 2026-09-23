import os
import zipfile
import hashlib
import time

def is_binary(data):
    return b'\x00' in data[:4096]

def create_zip(source_dir, zip_filename):
    print(f"==> Packaging {zip_filename} from {source_dir}...")
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        
    with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(source_dir):
            # Sort for deterministic archive ordering
            dirs.sort()
            files.sort()
            
            for d in dirs:
                dir_path = os.path.join(root, d)
                rel_path = os.path.relpath(dir_path, os.path.dirname(source_dir)).replace('\\', '/') + '/'
                zinfo = zipfile.ZipInfo(rel_path)
                zinfo.external_attr = 0o40755 << 16
                zinfo.date_time = time.localtime(time.time())[:6]
                z.writestr(zinfo, '')
                
            for f in files:
                file_path = os.path.join(root, f)
                rel_path = os.path.relpath(file_path, os.path.dirname(source_dir)).replace('\\', '/')
                
                with open(file_path, 'rb') as fp:
                    content = fp.read()
                    
                if not is_binary(content):
                    # Ensure LF line endings for all text/shell scripts
                    content = content.replace(b'\r\n', b'\n')
                    
                zinfo = zipfile.ZipInfo(rel_path)
                # 0o755 for scripts/executables
                zinfo.external_attr = 0o100755 << 16
                zinfo.date_time = time.localtime(time.time())[:6]
                z.writestr(zinfo, content)
                
    print(f"[OK] Done {zip_filename} ({os.path.getsize(zip_filename)} bytes)")

def calculate_hashes():
    files = [
        'wptangtoc-ols.zip',
        'wptangtoc-ols-user.zip',
        'wptangtoc-ols-almalinux',
        'wptangtoc-ols-almalinux-9',
        'wptangtoc-ols-almalinux-10',
        'wptangtoc-ols-ubuntu',
        'wptangtoc-ols'
    ]
    
    # Update checksum.txt (md5 of wptangtoc-ols.zip and wptangtoc-ols-user.zip)
    md5_1 = hashlib.md5(open('wptangtoc-ols.zip', 'rb').read()).hexdigest()
    md5_2 = hashlib.md5(open('wptangtoc-ols-user.zip', 'rb').read()).hexdigest()
    with open('checksum.txt', 'w', newline='\n') as f:
        f.write(f"{md5_1}\n{md5_2}\n")
    print(f"[OK] Updated checksum.txt")
    
    # Update SHA256SUMS.txt
    lines = []
    for f in files:
        if os.path.exists(f):
            h = hashlib.sha256(open(f, 'rb').read()).hexdigest()
            lines.append(f"{h}  {f}\n")
    with open('SHA256SUMS.txt', 'w', newline='\n') as f:
        f.writelines(lines)
    print(f"[OK] Updated SHA256SUMS.txt")

if __name__ == '__main__':
    create_zip('tool-wptangtoc-ols', 'wptangtoc-ols.zip')
    create_zip('tool-wptangtoc-ols-user', 'wptangtoc-ols-user.zip')
    calculate_hashes()
