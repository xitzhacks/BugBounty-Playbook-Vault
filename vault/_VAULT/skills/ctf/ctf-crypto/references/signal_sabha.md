# Reference: Signal Sabha (TRIVARNA CTF, "MISC" challenge)

## Challenge premise
"The Independence Day signal desk collected relay logs from several volunteer booths ... real tricolor
fragments, wrong-date rehearsals, fake flags, and timestamps from different time zones. The final message
was split, encoded in mixed bases, and logged out of order."

## File layout (as shipped)
- `attachments_VLWOpSP.tgz` -> extracts a `booth.log`
- `booth.log` is ITSELF a ZIP (PK magic) containing `booth_alpha.log`, `booth_beta.log`, `booth_gamma.log`
- Each log: comment line `# Signal Sabha booth export`, then one JSON object per line.

## Booth color map
alpha=saffron, beta=white, gamma=green (Indian flag order top->bottom).

## Genuine fragments (valid==true, tag==CEREMONY, color matches booth, date==15-08-1947)
Decoded byte-for-byte:
  alpha 55494346  hex  -> UICF
  alpha 21334e36  hex  -> !3N6
  alpha 344d367d  hex  -> 4M6}
  beta  VHthZQ==  b64  -> T{ae
  beta  U1JAcg==  b64  -> SR@r
  gamma MJQV65I   b32  -> ba_u
  gamma KBQWQ5A   b32  -> Paht

## Decoys (drop these)
  alpha/white VU5JNkNURntWaXNpYmxlX1NhYmhhX0RlY295fQ== b64 -> UNI6CTF{Visible_Sabha_Decoy}  (wrong color)
  beta/saffron 554e4936... hex -> UNI6CTF{Wrong_Date_Signal}                                  (wrong color + date 16-08)
  gamma/green KVHESNSD... b32 -> UNI6CTF{Invalid_Relay_Flag}                                  (valid:false)
  alpha 736f72742d... hex -> "sort-by-string-is-wrong"                                          (valid:false HINT: do NOT sort alphabetically)

## Decoy lesson
All decoys decode to clean `UNI6CTF{...}` strings -> the REAL flag uses the same wrapper family but
different inner words (theme: "Invisible_Sabha" etc). Wrapper is event-dynamic.

## Chronological-UTC assembly (intended order per "different time zones" + "out of order")
  18:30 alpha UICF
  18:38 beta  SR@r
  18:46 gamma ba_u
  18:51 alpha !3N6
  18:59 beta  T{ae
  19:07 gamma Paht
  19:12 alpha 4M6}
  => UICFSR@rba_u!3N6T{aePaht4M6}
  Brance-delimited substring (T{ae .. 4M6}): T{aePaht4M6

## UNRESOLVED BRANCH (important for next session)
All 5040 permutations of the 7 decoded fragments are gibberish; no single-layer ordering reads as English.
The byte-for-byte single decode is forced (each fragment decodes cleanly in exactly ONE base). This means
the intended flag likely needs either:
  (a) a chained codec per fragment (b64-of-hex, ROT, etc.) that produces the missing inner words, OR
  (b) a non-obvious ordering key (by timezone-offset magnitude, or booth-internal time order joined in
      tricolor sequence alpha->beta->gamma), OR
  (c) the literal reconstructed string IS the flag in leetspeak and the human discards the noise.
Candidate submissions, in priority:
  1. T{aePaht4M6
  2. TRIVARNA{aePaht4M6
  3. UICFSR@rba_u!3N6T{aePaht4M6
Document the resolution here if found.
