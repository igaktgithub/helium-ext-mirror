import os
import re

repo = os.environ.get('GITHUB_REPOSITORY', 'igaktgithub/helium-ext-mirror')
tag = os.environ.get('TAG', '')

versions = {}
with open('versions.env') as f:
    for line in f:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            versions[k] = v

existing = {}
if os.path.exists('update.xml'):
    with open('update.xml') as f:
        content = f.read()
    pattern = r"appid='([^']+)'>\s*<updatecheck codebase='([^']+)' version='([^']+)'"
    for m in re.finditer(pattern, content):
        existing[m.group(1)] = (m.group(2), m.group(3))

for ext_id, version in versions.items():
    codebase = f"https://github.com/{repo}/releases/download/{tag}/{ext_id}_{version}.crx"
    existing[ext_id] = (codebase, version)

lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<gupdate xmlns="http://www.google.com/update2/response" protocol="2.0">',
]
for ext_id, (codebase, version) in sorted(existing.items()):
    lines.append(f"  <app appid='{ext_id}'>")
    lines.append(f"    <updatecheck codebase='{codebase}' version='{version}' />")
    lines.append('  </app>')
lines.append('</gupdate>')

with open('update.xml', 'w') as f:
    f.write('\n'.join(lines))
