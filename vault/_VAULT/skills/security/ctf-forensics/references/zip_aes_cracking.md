# WinZip-AES "exfil archive" cracking — command reference

## Identify
```
unzip -l target/exfil_data.zip          # method=99 / flag_bits=1 == WinZip AES
zipinfo -v target/exfil_data.zip | grep -i "compress\|flag"   # confirm
```
Encrypted inner file is NOT the flag; it CONTAINS `flag.txt`. Crack the outer password.

## Extract hash
```
gunzip -kf /usr/share/wordlists/rockyou.txt.gz      # if only .gz present
zip2john target/exfil_data.zip > exfil.hash
head -c 120 exfil.hash          # confirm $zip2$*0*3*0*... well-formed
```

## Crack (decision tree)
```
# 1) full rockyou (AES PBKDF2 ~10 min; BACKGROUND, poll .pot)
john --wordlist=rockyou.txt --pot=d7.pot exfil.hash
john --show --pot=d7.pot exfil.hash          # "0 password hashes cracked" => FAILED

# 2) IF plain rockyou FAILED => do NOT run --rules. Rules only mutate list words;
#    a 0-crack rockyou means the base word isn't there, so rules cannot help.
#    -> go straight to narrative-derived candidates (below) or ask for the brief.

# 3) narrative-derived brute (python, fast)
python3 - <<'PY'
import zipfile, itertools, re, os
zp="target/exfil_data.zip"
def ok(pw):
    try:
        with zipfile.ZipFile(zp) as z:
            z.read(z.infolist()[0].filename, pwd=[REDACTED_SECRET]; return True
    except Exception: return False
# vocab from all artifacts
toks=set()
for root,_,files in os.walk("."):
    for fn in files:
        if fn.endswith(".pcap"): continue
        try: t=open(os.path.join(root,fn),errors="replace").read()
        except: continue
        toks.update(re.findall(r"[A-Za-z0-9_.\-]{4,40}", t))
for pw in toks:
    if ok(pw): print("VOCAB:",pw); break
# MITRE 7-stage concatenations
stages=[["reconnaissance","recon"],["weaponization","weaponisation"],["delivery","deliver"],
        ["exploitation","exploit"],["installation","install","persistence"],
        ["commandandcontrol","c2","cc"],["exfiltration","exfil","actionsonobjectives"]]
for combo in itertools.product(*stages):
    for s in ["","_","-","."]:
        pw=s.join(combo)
        if ok(pw): print("KILLCHAIN:",pw); break
PY
```

## Extract once cracked
```
7z x target/exfil_data.zip          # prompt for password
# or
python3 -c "import zipfile; zipfile.ZipFile('target/exfil_data.zip').extractall(pwd=b'PASSWORD')"
```

## Pitfalls
- Rules after a 0-crack rockyou is the #1 time sink. Don't.
- Verify `$zip2$` hash well-formed before trusting a 0-result (corrupt hash => silent 0).
- The pcap is usually only beacon/SMB noise — it rarely holds the password. Confirm before mining it.
- CTF AES passwords are narrative-derived, not dictionary. If brute fails, get the challenge brief.
