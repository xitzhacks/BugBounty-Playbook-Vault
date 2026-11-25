# Drupal 9/10 Reflection Points — Where It Reflects and Why It's Inert

Measured 2026-10 on a 7-host Drupal 10 estate (Pantheon/Varnish behind Imperva), as part of a
"test every parameter" pass. Useful because Drupal throws **three** distinct reflection shapes and
a naive marker sweep reports all three as hits — none are XSS.

## The three reflection points

| # | Where | What you see | Why it's inert |
|---|---|---|---|
| 1 | `<script type="application/json" data-drupal-selector="drupal-settings-json">` → `"currentQuery":{"q":"<value>"}` | marker present on **every** page and **every** param | JSON encoder emits `\u003C` / `\u003E` (JSON_HEX_TAG). A `</script>` breakout is impossible at the encoder, independent of any WAF |
| 2 | webform `<form action="/?q=<value>" …>` | the whole query string is echoed into the action attribute | `rawurlencode`d — `a"b` → `a%22b`; entity input `&#34;` → `%26%2334%3B` (double-encoded, never decoded) |
| 3 | Yoast SEO `<title>You searched for <value>` + `og:title` + `og:url` | plain marker looks reflected | `esc_html` — `"`→`&quot;`, `<`→`&lt;`; tags stripped entirely (`<img …>` → empty value) |

## The encoder proof (do this, don't guess)

Send `<b>MARK</b>` and read the *raw bytes*:

```
?q=<b>H1XJS</b>  ->  "currentQuery":{"q":"\u003Cb\u003EH1XJS\u003C\/b\u003E"}
```

`\u003C` in the document means the browser never sees a `<`, so no `</script>` exists to break out
with. That is a stronger negative than "the WAF blocked my payload" — it holds even if the payload
reaches origin.

For the action attribute, the proof is that the quote never survives:

```
raw "        -> action='/?x=H1X%22q'
&#34;        -> action='/?x=H1X%26%2334%3Bq'
%2522        -> action='/?x=H1X%252522q'
```

## Bypass matrix result (13 variants, all negative)

`"`, `&#34;`, `&#x22;`, `%2522`, `\"`, fullwidth `＂`, `</title>`, `</TITLE>`, `</script>`,
`</script/>`, `</script >`, `]]>`, `<!-->` — none produced an unencoded dangerous character in
any of the three contexts.

Note Imperva answers `Request Rejected` (200 status, ~247-byte body, "support ID") for
`</script>` / `<script` / cdata, but **that is not the reason the class is clean** — point 1 is
already safe by encoding. Don't let a WAF response stand in for an encoder proof.

## One artifact worth understanding (still not a bug)

On the WordPress site in the same estate, `?s=` rendered `&#34;` back as `&#034;` in `<title>` —
i.e. `&` was not entity-encoded on that path. Tempting, but not exploitable: `<title>` is RCDATA
and text nodes are already tokenised, so a character reference can only ever produce *characters*,
never a tag. Verify the context before escalating an entity-survival observation.

## Where a real Drupal XSS would actually live

- A **views exposed filter** whose label/value is printed into a link or heading **without** the
  URL layer (BEF links are `Url::fromRoute` → encoded; a custom template echoing the raw value is not).
- A **webform confirmation message** with `[webform_submission:values:*]` rendered under a text
  format that allows HTML, viewed by an admin → stored XSS (needs a submission you own).
- A **field formatter / custom block** printing `$_GET` directly — grep the theme for
  `$_GET`, `\Drupal::request()->query`, `raw`/`Markup::create` near user input.

Everything else in core (`?q=`, `?destination=`, `?page=`, search, 404 path) is correctly encoded;
spend the time on the theme/module PHP instead.

## Sweep hygiene

A 96-host `q,s,url` marker sweep on this estate returned 10 "HTML-context" hits — **all 10** were
points 1–3 above. Classify by *emission form* before counting hits:
strip `<script>`/`<style>` blocks, then check whether the marker still appears in markup. If yes,
check the encoder; if no, it was framework state.
