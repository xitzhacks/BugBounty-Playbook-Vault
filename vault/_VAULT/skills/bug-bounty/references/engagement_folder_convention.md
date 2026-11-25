# [REDACTED_PII] — per-target bug bounty folder convention

When running a bug bounty / recon / vuln-hunt engagement for this user, create a
dedicated per-target folder and keep ALL artifacts isolated inside it. The user
explicitly requires per-target isolation ("make sure let him in different
folder by name").

Layout to use:
  ~/Bugbounty/<target>/
    target.txt          # pasted scope (domains, asset types, in-scope roots)
    subs_raw.txt        # subfinder/assetfinder output
    live_hosts.txt      # httpx live-host probe
    www_index.html      # SPA entry HTML
    js_files/           # downloaded SPA bundles (DECOMPRESS gzip first!)
    <target>_harness.py # token-gated cross-account / ATO harness
    <target>_REPORT.md  # consolidated findings across all bug classes

Do NOT use a shared/generic recon folder or mix two targets. Start by writing
target.txt from the user's pasted scope before any tooling runs.
