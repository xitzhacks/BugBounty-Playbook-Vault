# GhostFrame APK — decoy-pointer pattern (CTF7, worked example)

## Challenge
Android APK "GhostFrame"; brief: investigate internal artifacts, recover the hidden
challenge secret. Hints: "use cyberchef", "thinking out of the box means what it says".
Flag format BI{...}.

## What the APK actually contained
- Tiny hand-built APK (~9 KB), 15 ZIP entries. assets/ghostframe.db (SQLite) with a
  fake "vault" schema (users / documents / events / challenge_secrets / ...).
- challenge_secrets single row: key_name=flag, value=Flag{IG_calls_me_Influencer_at_16.404_127}.
- DEX had a ForensicEngine with decoy helpers (base64("offline-ready"), SHA256 of a constant).
- No icon (android:icon=''), no res/drawable, no meta-data, no nested archive (binwalk clean).

## The trap
The Flag{...} value is a POINTER, not the flag: "IG calls me Influencer at 16.404_127"
names an Instagram handle @16.404_127. The narrative fluff is misdirection. The intended
secret is the handle re-wrapped in the required format: BI{16.404_127}.

## Chasing the pointer = pure misdirection (prove it, then stop)
Fetched @16.404_127 (GraphQL web_profile_info with IG UA) — exhaustively clean:
- bio "DM for unpaid r@geb@1t ... GOAT- @beluga1000" (email reversed = t1@beg@r, nothing).
- 1 post caption "hehe <> / logon to beluga.co.ne.ip.ss.hp.iu.pk / ..." — scrambled domain
  reverses to beluga.co, a real PEPPER e-commerce site (not challenge).
- post image + profile pic: cat memes (vision-checked, no flag; binwalk/steghide/QR/LSB clean).
- comments (GraphQL) age-gated/401; post page embedded JSON had no flag/comment text.
- linked @beluga1000 = real YouTuber "Beluga" (plushies) — unrelated.

## Decode battery on the narrative string (should yield nothing)
XOR (single + multi-byte: GhostFrame/cyberchef/Flag/BI/beluga...), ROT13, Reverse,
From-Base64, digit->bytes -> NO BI{...}. Conclusion: no extra cipher; the answer is the
handle re-wrapped.

## Reusable extraction (scripts/ig_profile_pull.py)
For any challenge that points at a social handle: pull bio + posts + caption + profile
pic via Instagram's public web_profile_info GraphQL endpoint with UA
"Instagram 269.0.0.18.75 Android" (the generic web UA gets "useragent mismatch"). Then
run binwalk/zbar/vision on each image and reverse any scrambled domain. Almost always
this confirms misdirection; the flag is the identifier, not the profile.

## Lesson
When a planted secret NAMES an external account/URL, the flag is the identifier
re-wrapped in the challenge format — not the long narrative, and not bytes hidden on the
external resource. Verify the external resource is misdirection, then submit the
handle-form flag. If that is also rejected, ask the platform error ("wrong format" vs
"not found") and whether a 2nd file was attached.
