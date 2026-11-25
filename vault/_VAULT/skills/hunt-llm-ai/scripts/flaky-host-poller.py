#!/usr/bin/env python3
"""
flaky-host-poller.py — resilient background poller for CTF boxes that flap.

These multi-app CTF hosts (e.g. 2.29.10.21 with HeliosBot/SENTINEL/LedgerLock/Vaultify
on different ports) frequently drop the GIVEN port (8081/SENTINEL, 8083/LedgerLock)
while the host still pings and sibling ports stay up. A one-shot probe just fails.
This wrapper loops a TCP-connect probe with a sleep, and the instant the target port
answers, it shells out to your real exploit harness (default: blackbox-agent-probe.py)
so the work happens during a stable window without manual babysitting.

Usage:
    python3 flaky-host-poller.py [BASE_URL] [EXPLOIT_SCRIPT]

Defaults:
    BASE_URL        http://2.29.10.21:8081
    EXPLOIT_SCRIPT  ./blackbox-agent-probe.py   (must sit beside this file, or pass a path)

Behavior:
    - Every `interval` seconds, TCP-connect to HOST:PORT (timeout 4s).
    - While down: print a heartbeat and sleep.
    - On first success: run EXPLOIT_SCRIPT (subprocess, inherits args), wait for it,
      then exit 0 (so a notify_on_complete cron/job fires once with the result).
    - Re-runs the exploit up to `max_runs` times if it crashes (host may die mid-run).
    - Honors SIGTERM cleanly.

Tuning:
    Set env POLL_INTERVAL (sec) and MAX_RUNS to override defaults.
"""
import os, sys, time, socket, subprocess, signal

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://2.29.10.21:8081"
EXPLOIT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "blackbox-agent-probe.py")

INTERVAL = int(os.environ.get("POLL_INTERVAL", "20"))
MAX_RUNS = int(os.environ.get("MAX_RUNS", "3"))
CONNECT_TIMEOUT = 4

def host_port(base):
    base = base.split("//", 1)[-1].strip("/")
    h, _, p = base.partition(":")
    return h, int(p or 80)

def up(host, port):
    try:
        with socket.create_connection((host, port), timeout=CONNECT_TIMEOUT):
            return True
    except OSError:
        return False

_running = True
def _term(sig, fr):
    global _running
    _running = False
signal.signal(signal.SIGTERM, _term)

def main():
    host, port = host_port(BASE)
    print(f"[poller] target {host}:{port}  exploit={EXPLOIT}  interval={INTERVAL}s  max_runs={MAX_RUNS}")
    runs = 0
    while _running and runs < MAX_RUNS:
        if up(host, port):
            print(f"[{time.strftime('%H:%M:%S')}] {host}:{port} UP — launching exploit")
            try:
                rc = subprocess.call([sys.executable, EXPLOIT, BASE])
                print(f"[poller] exploit exited rc={rc}")
            except Exception as e:
                print(f"[poller] exploit launch failed: {e}")
            runs += 1
            if runs >= MAX_RUNS:
                break
            # give the host a breather, then keep guarding
            print(f"[poller] run {runs}/{MAX_RUNS} done; resuming watch")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] {host}:{port} down. sleeping {INTERVAL}s")
            for _ in range(INTERVAL):
                if not _running:
                    break
                time.sleep(1)
    print("[poller] exit")

if __name__ == "__main__":
    main()
