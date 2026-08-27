#!/usr/bin/env python3
"""Extrai a versão (manifest.json) de dentro de um arquivo .crx."""
import struct
import zipfile
import io
import json
import sys


def get_crx_version(path):
    with open(path, "rb") as f:
        data = f.read()

    magic, ver = struct.unpack("<4sI", data[:8])

    if ver == 2:
        pk_len, sig_len = struct.unpack("<II", data[8:16])
        start = 16 + pk_len + sig_len
    else:
        hdr_len, = struct.unpack("<I", data[8:12])
        start = 12 + hdr_len

    z = zipfile.ZipFile(io.BytesIO(data[start:]))
    manifest = json.loads(z.read("manifest.json").decode("utf-8-sig"))
    return manifest["version"]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: get_version.py <arquivo.crx>", file=sys.stderr)
        sys.exit(1)

    print(get_crx_version(sys.argv[1]))
