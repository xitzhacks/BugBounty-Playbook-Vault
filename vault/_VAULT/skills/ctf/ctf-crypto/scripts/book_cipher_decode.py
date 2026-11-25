#!/usr/bin/env python3
"""
Book-cipher / "numbered note" decoder for CTF stego.

Scheme (seen in a prisoner dead-drop challenge):
  - A public/shared text is the "book" (here: a handbill manifesto).
  - A strip of number PAIRS, format A//B (optional trailing '-'),
    indexes into the book: B-th CHARACTER of the A-th WORD (1-indexed).
  - The lone '-' (e.g. 11//4-) means "take the character BEFORE" the
    indexed one (previous char of that word).

Usage:
  python3 book_cipher_decode.py --book handbill.txt --pairs "26//1 1//2 ..."
  cat pairs.txt | python3 book_cipher_decode.py --book handbill.txt -

Tokenizes words as [A-Za-z']+.
"""
import re, sys, argparse

def decode(book_text, cipher_tokens, dash_mode="prev"):
    words = re.findall(r"[A-Za-z']+", book_text)
    out = []
    for tok in cipher_tokens:
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r"(\d+)//(\d+)(-?)", tok)
        if not m:
            out.append(f"[{tok}]")
            continue
        a, b, dash = int(m.group(1)), int(m.group(2)), m.group(3)
        if not (1 <= a <= len(words)):
            out.append(f"#{a}#")
            continue
        w = words[a - 1]
        ci = (b - 2) if (dash == "-" and dash_mode == "prev") else (b - 1)
        if 0 <= ci < len(w):
            out.append(w[ci])
        else:
            out.append(f"?{a}:{b}{dash}?")
    return "".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--book", required=True, help="path to the 'book' text file")
    ap.add_argument("pairs", nargs="?", help="quoted pair string, or '-' for stdin")
    ap.add_argument("--dash", default="prev", choices=["prev", "same"])
    args = ap.parse_args()

    with open(args.book, encoding="utf-8", errors="replace") as f:
        book = f.read()

    if args.pairs and args.pairs != "-":
        toks = args.pairs.split()
    else:
        toks = sys.stdin.read().split()

    raw = decode(book, toks, args.dash)
    print("RAW :", raw)
    print("GRP :", " ".join(raw[i:i + 5] for i in range(0, len(raw), 5)))

if __name__ == "__main__":
    main()
