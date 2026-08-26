import sys
import struct
import zipfile
import io
import json

path = sys.argv[1]
with open(path, 'rb') as f:
    data = f.read()

magic, ver = struct.unpack('<4sI', data[:8])
if ver == 2:
    pk_len, sig_len = struct.unpack('<II', data[8:16])
    start = 16 + pk_len + sig_len
else:
    hdr_len, = struct.unpack('<I', data[8:12])
    start = 12 + hdr_len

z = zipfile.ZipFile(io.BytesIO(data[start:]))
manifest = json.loads(z.read('manifest.json').decode('utf-8-sig'))
print(manifest['version'])
