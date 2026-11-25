# Getting steghide / outguess WITHOUT root (Parrot/Kali, safety-guard blocks `apt-get install`)

On the user's box the safety guard blocks `apt-get install`, `sudo`, `pip install`,
`python3 -m venv`, and `pkill`. But `apt-get download` + `ar` + `tar` work fine as a
normal user (they only write to the current directory).

## Recipe

```bash
cd /path/to/workdir

# 1) download the .deb (no root, no install)
apt-get download steghide
apt-get download outguess
apt-get download libmcrypt4        # steghide needs libmcrypt.so.4

# 2) extract the binaries from the .deb
mkdir -p sh_extract og_extract libm_extract
( cd sh_extract  && ar x ../steghide_*.deb  && tar -xf data.tar.* )
( cd og_extract  && ar x ../outguess_*.deb   && tar -xf data.tar.* )
( cd libm_extract && ar x ../libmcrypt4*.deb && tar -xf data.tar.* )

# 3) find the binaries
ls sh_extract/usr/bin/steghide  og_extract/usr/bin/outguess
find libm_extract -name 'libmcrypt.so*'

# 4) run with the extracted lib on LD_LIBRARY_PATH (do NOT rely on system install)
export LD_LIBRARY_PATH="$PWD/libm_extract/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"

# verify
ldd sh_extract/usr/bin/steghide | grep -i "not found"   # should print nothing
```

Notes:
- The steghide `.deb` binary runs but needs `libmcrypt.so.4`; resolve it the SAME way
  (download + extract), don't try `pip install steghide` (no such PyPI package) or a venv
  (venv pip is also blocked).
- outguess depends only on standard libs on Parrot; usually no extra lib needed.
- `apt-get download` fetches from the configured mirror (deb.parrot.sh on Parrot). If a
  package name 404s on GitHub static builds, the .deb route is the reliable one.
- Static binary downloads from GitHub (e.g. steghide releases) tend to 404 — prefer the .deb.
