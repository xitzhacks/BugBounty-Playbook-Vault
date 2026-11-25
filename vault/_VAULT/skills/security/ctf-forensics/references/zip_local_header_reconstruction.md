# Reconstructing a ZIP with a Stripped Local File Header

## When this applies
A challenge gives a file that *contains* a ZIP but the ZIP won't parse in
`zip2john`/`bkcrack` with errors like:
- `! Did not find local file header for X at 0`
- `Did not find a Central Directory File Header at expected file offset N`

The author "broke the vessel": they deleted the local file header but left the
central directory + EOCD + the raw encrypted bytes intact. Rebuild a parseable
zip so the standard tools work.

## Layout of a normal zip entry
```
[local file header 30B] [filename fnLen] [extra extraLen]
[encrypted data: 12-byte ZipCrypto header + ciphertext]   <- csize bytes
...
[central directory file header 46B] [filename] [extra] [comment]
[EOCD 22B]
```
The central-dir header records `lho` = offset (in the zip) where the LOCAL
header *should* be. If the local header is gone, set `lho=0` and build the
local header yourself at offset 0.

## Step-by-step (Python)
```python
import struct, zipfile, io

raw = open('container.bin','rb').read()      # whole file
base = 21364                                 # offset where the zip starts
zipb = raw[base:]
cd = zipb.find(b'PK\x01\x02')
cdf = zipb[cd:cd+46]
(ver,vernd,flag,method,mt,md,crc,csize,usize,
 fnl,efl,cl,dsk,ia,ea,lho) = struct.unpack('<HHHHHHIIIHHHHHII', cdf[4:46])
fname = b'AuthorLovesCat.jpg'                # from the central-dir filename field

# 1) local header (30 + fnl + efl)
local = struct.pack('<IHHHHHIIIHH', 0x04034b50, 20, flag, method, 0,0,
                     crc, csize, usize, fnl, efl) + fname + b'\x00'*efl
assert len(local) == 30 + fnl + efl          # e.g. 72 for fnl18/efl24

# 2) encrypted bytes (already include the 12-byte ZipCrypto header)
enc = zipb[72 : 72 + csize]
assert len(enc) == csize

# 3) central dir + EOCD from the original carve
central_and_eo = zipb[cd:]

# 4) pad so the central dir lands at the EOCD's recorded cd offset
cd_off = int.from_bytes(eocd[16:20],'little')   # from last 22 bytes of zipb
gap = cd_off - (len(local) + csize)
rebuilt = local + enc + b'\x00'*gap + central_and_eo
open('rebuilt.zip','wb').write(rebuilt)

# verify
z = zipfile.ZipFile(io.BytesIO(rebuilt))
print(z.namelist())            # ['AuthorLovesCat.jpg']
z.testzip()                    # raises "password required" == good (it's encrypted)
```

## After reconstruction
- `zip2john rebuilt.zip > hash.txt` -> produces a `$pkzip$` (PKZIP/ZipCrypto) hash.
- For wordlist/dictionary cracks use `john --wordlist=rockyou.txt hash.txt`.
- For known-plaintext, run `bkcrack -C rebuilt.zip -c 'AuthorLovesCat.jpg' -p plain.bin -o 0`.
  The `-c` name must match the central-dir filename EXACTLY.

## Gotchas
- `struct.unpack` field order for the central dir (after the 4-byte sig):
  verMade H, verNeed H, flag H, method H, modT H, modD H, crc I, csize I,
  usize I, fnLen H, extraLen H, commLen H, diskStart H, intAttr H, extAttr I, lho I.
  That is `<HHHHHHIIIHHHHHII` (42 bytes of fields after the sig).
- The encrypted bytes start right after the (missing) local header. The first 12
  bytes of `enc` are the random ZipCrypto header; the rest is ciphertext.
- If `zip2john` says "Did not find a Central Directory File Header at expected
  offset", the `gap` padding is wrong -- recompute `cd_off` from the EOCD
  (last 22 bytes: offset = `int.from_bytes(eocd[16:20],'little')`).
- bkcrack Z-search timings (observed): ~709k Z-values ~ 46 min; ~1.16M ~ 75+ min.
  Run multiple plaintext candidates as parallel background processes.
