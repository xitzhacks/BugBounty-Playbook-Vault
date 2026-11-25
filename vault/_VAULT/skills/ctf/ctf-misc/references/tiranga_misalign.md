# Worked example: "U - Tiranga of freedom" (misc CTF)

## Artifact
- Zip: `Challenge_misc.zip` → `Challenge misc.txt` (6189 bytes) + decoy dir `Intercepted Independence Activation SMS/` (huge fake GSM/SMS audit + routing logs — IGNORE).
- Capture format: `N|content` rows; `# redraw jitter NN: ignore this terminal status line` and `# --- END CAPTURE ---` are skip markers.

## Capture anatomy
- 60 content rows, each ≤ 98 chars wide (most exactly 98). ~59 rows of 98 = a 98-wide terminal capture.
- Characters: `-` solid horizontal borders, `/ \` diagonals (the flag cloth), `v >` arrows, `+` plus fill, `? = , . : ;` = the chakra (wheel) in the green/white band, alphanumerics = the hidden flag letters.

## Bands (visualized via tiny render)
- Rows 0–17: top saffron band (`/ \` diagonals + `-` border).
- Rows 18–27: white band + chakra region — letters here.
- Rows 28–47: green band with a dense `?=,.:;` chakra cluster — more letters here.
- Rows 48–59: bottom band (`/ \` diagonals, `<<\` tokens) + short trailing rows.

## Embedded letters (row, col, char) found by code scan
White band:
- (18,48) U  → `---/U/\-n`  (18,52) n
- (19,79) N  → `---/N/\/d`  (19,83) d
- (21,13) I  → `---/I/\-i`  (21,17) i
- (22,44) 6  → `---/6/\-4`  (22,48) 4
Green band:
- (30,96) I  (31,1) i  (32,28) I  (32,34) I  (33,59) I  (33,65) l  (34,92) I  (34,94) i

Plus two `v` arrow-runs at (9,7-16) and (10,38-47) (decoration, not flag letters).

## Realignment attempts (key learning)
- Naive reading-order concat → `vvvvvvvvvvvvvvvvvvvvUnNdIi64IiIIIlIi` = garbage. Confirms shear/wrap.
- **Deshear:** shift row r left by `round(slope*r) mod W`; tested slopes −3..4.5. Did NOT cleanly yield a readable word — the flag letters are sparse and a single global shear isn't the whole story for this instance.
- **Unwrap (join pairs):** joining rows 2-at-a-time → width ~194, height 30. Tiny render showed a sunburst emblem at top with empty below — wrong unwrap factor for this file.
- Lesson: for THIS challenge the intended realignment was left unsolved in-session; the robust approach is to (a) try several slopes, (b) try several unwrap widths (2,3,4 physical rows per logical line), (c) re-render each small and eyeball, (d) re-extract letters in the corrected column order. Capture the technique; the exact key depends on the challenge.

## Verified-good sub-routines (reuse)
```python
import re
rows=[]
for ln in open(path, encoding="latin-1").read().split("\n"):
    m=re.match(r'^\s*(\d+)\|(.*)$', ln)
    if m: rows.append(m.group(2))
    elif ln.startswith("#"): rows.append(None)
    else: rows.append(ln)
real=[r for r in rows if r is not None and r.strip()!=""]
W=max(len(r) for r in real); real=[r.ljust(W) for r in real]
# letters
letters=[(y,x,ch) for y,r in enumerate(real) for x,ch in enumerate(r) if ch.isalnum()]
# deshear
def deshear(grid, slope):
    H=len(grid); Wd=len(grid[0])
    out=[]
    for r in range(H):
        s=int(round(slope*r))%Wd
        out.append(grid[r][s:]+grid[r][:s])
    return out
# unwrap join k
def join(grid,k):
    return ["".join(grid[i:i+k]) for i in range(0,len(grid)-k+1,k)]
```
