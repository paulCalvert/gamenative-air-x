"""Make Jedi Knight: Dark Forces II level-start autosaves show up in the Load Game list.

JK writes an autosave at the start of every level as `_JKAUTO_<level>.jks` in
`player/<profile>/`, but the Load Game screen hides them. Per OpenJKDF2's
jkGUISaveLoad.c, the list:
  1. skips any file whose name starts with `_JKAUTO_`
  2. only lists saves whose header saveName contains `~`, and shows the text after it

This tool copies an autosave to a normal slot name (e.g. save0101.jks) and rewrites
its saveName so it lists as e.g. "START 01 - Katarn's Home".

.jks header (little-endian):
  0     int32      version (6)
  4     char[128]  episode
  132   char[128]  jkl (level file)
  260   float32    health
  264   float32    maxHealth
  268   float32[200] binAmts
  1068  char16[256] saveName (UTF-16LE, 512 bytes, NUL-padded)

Usage:
  python -I jk_autosave_visible.py info <file.jks> [...]
  python -I jk_autosave_visible.py make <_JKAUTO_xx.jks> <out.jks> "<label>" [--title "<title>"]

Work on copies, keep backups of the profile folder, and restart the game to see new saves.
"""
import struct, sys

NAME_OFF, NAME_LEN = 1068, 512


def cstr(b):
    return b.split(b'\0', 1)[0].decode('latin-1')


def info(path):
    d = open(path, 'rb').read()
    ver = struct.unpack_from('<i', d, 0)[0]
    hp, maxhp = struct.unpack_from('<ff', d, 260)
    name = d[NAME_OFF:NAME_OFF + NAME_LEN].decode('utf-16-le').split('\0', 1)[0]
    print(f'{path}: version={ver} episode={cstr(d[4:132])!r} jkl={cstr(d[132:260])!r} '
          f'health={hp:.0f}/{maxhp:.0f} saveName={name!r}')


def make(src, dst, label, title=None):
    d = bytearray(open(src, 'rb').read())
    if struct.unpack_from('<i', d, 0)[0] != 6:
        sys.exit('unexpected save version (expected 6)')
    title = title or label
    raw = f'{title}~{label}'.encode('utf-16-le')
    if len(raw) > NAME_LEN - 2:
        sys.exit('name too long')
    d[NAME_OFF:NAME_OFF + NAME_LEN] = raw + b'\0' * (NAME_LEN - len(raw))
    open(dst, 'wb').write(d)
    info(dst)


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == 'info':
        for p in a[1:]:
            info(p)
    elif len(a) >= 4 and a[0] == 'make':
        t = a[a.index('--title') + 1] if '--title' in a else None
        make(a[1], a[2], a[3], t)
    else:
        print(__doc__)
