"""Rebuild a WayForward engine .pak, optionally trimming .ivf videos / .mp3 audio.
usage: python -I shorten_pak.py <in.pak> <out.pak> [--verify]
--verify: rebuild unchanged and check byte-identical (format sanity check).
"""
import struct, sys

MAGIC = b'FILELINK_____END'
IVF_FRAMES = 30   # ~1 s at 30 fps
MP3_FRAMES = 40   # ~1 s

def trim_ivf(b):
    p, n = 32, 0
    while n < IVF_FRAMES and p < len(b):
        sz, _ = struct.unpack('<IQ', b[p:p + 12]); p += 12 + sz; n += 1
    out = bytearray(b[:p]); struct.pack_into('<I', out, 24, n); return bytes(out)

def trim_mp3(b):
    q = 10 + ((b[6] << 21) | (b[7] << 14) | (b[8] << 7) | b[9]) if b[:3] == b'ID3' else 0
    br = [0,32,40,48,56,64,80,96,112,128,160,192,224,256,320,0]; srt = [44100,48000,32000,0]
    for _ in range(MP3_FRAMES):
        h = b[q:q + 4]
        if len(h) < 4 or h[0] != 0xFF or (h[1] & 0xE0) != 0xE0: break
        q += 144 * br[h[2] >> 4] * 1000 // srt[(h[2] >> 2) & 3] + ((h[2] >> 1) & 1)
    return b[:q]

def main(src, dst, verify):
    d = open(src, 'rb').read()
    dirsize = struct.unpack_from('<I', d, 0)[0]
    marker = d[dirsize:dirsize + 64]; base = dirsize + 64
    ents = []; i = d.find(MAGIC, 0, dirsize)
    while i != -1:
        off, size = struct.unpack_from('<II', d, i + 16)
        name = d[i + 24:d.index(b'\0', i + 24)].decode()
        ents.append((i, off, size, name)); i = d.find(MAGIC, i + 1, dirsize)
    out = bytearray(d[:dirsize])
    for (pos, off, size, name) in sorted(ents, key=lambda e: e[1]):
        data = d[base + off:base + off + size]
        if not verify:
            if name.endswith('.ivf'): data = trim_ivf(data)
            elif name.endswith('.mp3'): data = trim_mp3(data)
        if len(out) > dirsize: out += marker
        else: out += marker
        struct.pack_into('<II', out, pos + 16, len(out) - base, len(data))
        print(f'{name}: {size} -> {len(data)}')
        out += data; out += b'?' * ((-len(out)) % 16)
    out += b'?' * 48  # trailer
    if verify:
        print('identical:', bytes(out) == d); return
    open(dst, 'wb').write(out); print('wrote', dst, len(out))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, '--verify' in sys.argv)
