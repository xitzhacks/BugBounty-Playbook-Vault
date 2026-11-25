---
name: XSS
description: >-
  Specialized AI security skill focused on identifying, verifying,
  exploiting (within authorized scope), and documenting Cross-Site
  Scripting (XSS) vulnerabilities.
---

# SKILL: XSS (Cross-Site Scripting)

description: >
  Specialized AI security skill focused on identifying, verifying,
  exploiting (within authorized scope), and documenting Cross-Site
  Scripting (XSS) vulnerabilities.

knowledge_domains:
  fundamentals:
    definition: |
      Cross Site Scripting (XSS) occurs when an attacker controls data
      that is interpreted by the browser as executable JavaScript.
    goal:
      - Execute arbitrary JavaScript
      - Steal session data
      - Perform actions as victim
      - Modify page contents
      - Capture sensitive information
    prerequisites:
      - User-controlled input
      - Unsanitized output
      - Browser interprets input
  types:
    reflected:
      description: >
        Payload returned immediately in HTTP response.
      common_locations: [Search parameter, Error message, URL parameter, Login error, Contact forms]
    stored:
      description: >
        Payload permanently stored in application.
      locations: [Comments, Chat, Forum, Profile, Ticket system, Admin panel]
    dom:
      description: >
        Vulnerability exists entirely inside client-side JavaScript.
      sources: [location.hash, location.search, document.URL, document.referrer, window.name, postMessage]
      sinks: [innerHTML, outerHTML, document.write, insertAdjacentHTML, eval, setTimeout(string), setInterval(string), Function(), jQuery html()]
  contexts:
    html: ["<script>", "<img>", "<svg>"]
    attribute: [value="", src="", href="", title="", alt=""]
    javascript: ["var a=\"", JSON, JS objects]
    css: [style="", inline css]
    url: [href=, action=, iframe src]
  workflow:
    step1: Identify every user input.
    step2: Trace reflection.
    step3: Identify output context.
    step4: Test encoding.
    step5: Test payload execution.
    step6: Determine impact.
    step7: Document reproduction.
  common_sources: [GET parameters, POST body, Cookies, HTTP headers, JSON, XML, Multipart, GraphQL, WebSocket, URL Fragment, Search box, Profile fields, Feedback forms]
  reflection_checks: [Raw Reflection, HTML Encoded, URL Encoded, Double Encoded, Unicode Encoded, Base64, Escaped, Filtered]
  testing_order: [Reflection, Context, Encoding, Filter, Payload, Bypass, Execution]
  payload_strategy:
    detection: [Minimal payload, Context-safe payload, Execution payload]
    escalation: [Event handlers, SVG, MathML, iframe, Script tag]
  encoding_checks:
    html: ["<", ">", "\"", "'", "&", "/"]
    url: ["%3C", "%3E"]
    unicode: [UTF-8, UTF-16]
  filter_analysis:
    identify: [Character blacklist, Keyword blacklist, Regex filter, WAF, CSP]
    common_filters:
      blocks: [script, alert, onerror, onload, javascript]
    bypass_categories: [HTML Encoding, Mixed Case, Unicode, UTF-7, Null Byte, Double Encoding, Event Handler, SVG, MathML, Template Injection, DOM Gadget, Polyglot]
  event_handlers: [onclick, onmouseover, onerror, onload, onanimationstart, onfocus, onpointerenter, onwheel, onsubmit, oninput]
  dangerous_sinks: [innerHTML, outerHTML, document.write, eval, Function, setTimeout, setInterval, jQuery.html, jQuery.append, insertAdjacentHTML]
  dom_sources: [location.hash, location.search, location.pathname, document.URL, document.referrer, window.name, localStorage, sessionStorage]
  frameworks:
    react: { dangerous: [dangerouslySetInnerHTML] }
    angular: { dangerous: [bypassSecurityTrustHtml] }
    vue: { dangerous: [v-html] }
    jquery: { dangerous: [html(), append(), prepend()] }
  api_testing:
    test: [REST, GraphQL, JSON, XML]
    authentication: [Login, Registration, Password Reset, MFA, OAuth]
  storage_locations: [Database, Cache, Logs, Search Index, Browser Storage]
  impact:
    high: [Account takeover, Session hijacking, Admin compromise]
    medium: [User impersonation, CSRF bypass]
    low: [UI modification, Defacement]
  reporting:
    include: [URL, Parameter, HTTP Request, HTTP Response, Payload, Context, Screenshot, Browser, Impact, Recommendation]
    recommendations:
      output_encoding: [HTML Encode, Attribute Encode, JS Encode, URL Encode]
      input_validation: [Whitelist, Length validation, Type validation]
      browser_controls: [CSP, HttpOnly, SameSite, Secure Cookies]
  tools:
    intercept: [Burp Suite, Caido, OWASP ZAP]
    automation: [Dalfox, XSStrike, KXSS, Gxss, Katana, Hakrawler]
    browsers: [Chrome, Firefox, Edge]
  methodology:
    recon: [Discover parameters, Crawl application, Identify reflections]
    discovery: [Reflection testing, Context analysis, DOM analysis]
    exploitation: [Execute payload, Verify execution, Assess impact]
    reporting: [Reproduce, Document, Recommend fixes]
  mindset:
    principles:
      - Never assume filtering is sufficient.
      - Always identify the rendering context before testing.
      - Prioritize safe verification methods.
      - Test systematically across all input vectors.
      - Validate findings in multiple browsers when relevant.
      - Document exact reproduction steps and evidence.
  metadata:
    author: Sir xitz
    version: 1.1
    fingerprint: XSS_SKILL_2026

aspnet_webforms_xss:
  overview: |
    ASP.NET WebForms apps (identified by __VIEWSTATE, __EVENTVALIDATION,
    __VIEWSTATEGENERATOR, and rptPaging$ctlNN$btnPage postback params) ship
    TWO server-side defenses that kill naive XSS payloads. Know both first.
  request_validation: |
    System.Web.HttpRequestValidationException ("A potentially dangerous
    Request.Form value was detected") fires on the RAW post body. It blocks:
      - literal < and >
      - NUMERIC entities &#60; / &#62; (decoded pre-validation, so they trip it)
    It does NOT block:
      - NAMED entities &lt; / &gt; (pass the filter)
      - payloads with no brackets/entities (attribute/JS breakouts)
    Bypass ladder once < > are rejected:
      1) attribute breakout (no brackets):  " onfocus=alert(1) autofocus x="
      2) JS-string breakout (no brackets):  ";alert(1)//
      3) named entities (fires ONLY if output is NOT re-encoded):
         &lt;svg onload=alert(1)&gt;
  viewstate_tokens: |
    Every POST needs FRESH __VIEWSTATE + __EVENTVALIDATION from a prior GET of
    the same page. Reusing stale tokens => HTTP 500 / "Validation of viewstate
    MAC failed". Always GET, regex the tokens, then POST.
  textarea_dead_end: |
    The comment SUBMISSION page echoes input back inside a <textarea> or
    value="" and ASP.NET auto HTML-encodes it (&quot; &amp;lt;). That reflection
    is SAFE and never executes. The real XSS sink is a SEPARATE page rendering
    stored comments as HTML (comment list / profile / admin view). If no such
    page is reachable, there is NO sink -- stop firing payloads at the form.
  form_urlencoded_gotcha: |
    In application/x-www-form-urlencoded, & is the field separator. A payload
    containing a literal & (e.g. user accidentally typed &&#60;) splits the value
    into broken fields, so the payload never lands in the target param. Always
    URL-encode & as %26 and # as %23, or use requests data= dict (encodes safe).
    Never hand-concatenate raw payloads with raw &.
  false_positive_trap: |
    When scanning responses for reflection, do NOT match a bare <script> string
    -- the page's OWN JavaScript (<script type="text/javascript">) will trigger
    it and produce a false HIT. Confirm the payload hit by checking the payload
    actually appears DECODED (literal <svg / <script>alert / onfocus=alert) AND
    is NOT wrapped in &quot; inside a <textarea>. Verify by extracting the
    snippet around the payload index and checking t[:i].rfind('<textarea') <=
    t[:i].rfind('</textarea').
  workflow_for_this_user: |
    [REDACTED_PII] wants EXECUTION, not theory. For XSS: build a script that GETs
    tokens, fires the payload matrix via POST, and scans the response for
    DECODED reflection. Actually RUN it -- do not just hand over payloads.
    But when the only reachable sink is a self-encoding textarea, report the
    dead end honestly instead of burning more requests.

  xssi_chain_note: |
    When authenticated endpoints return JSON with internal object IDs and
    lack Cross-Origin-Resource-Policy headers, the XSS vector shifts to XSSI:
    cross-origin pages can fetch authenticated responses via XHR/fetch and
    extract leaked data (account IDs, tokens). Test by checking if responses
    include `Cross-Origin-Resource-Policy: same-origin` -- absence = exploitable
    via `<script>` inclusion or fetch() from attacker origin.
  references:
    - references/aspnet-xss.md       # Request Validation behavior + dead-end + gotchas
    - scripts/aspnet_xss_probe.py    # generic GET-tokens + fire-matrix scanner (false-positive safe)

context_triage:
  pre_step_before_recon:
    - BEFORE testing, classify each target host by Content-Type. This removes 90%+
      of wasted probing on API/REST targets.
    - JSON/REST endpoints returning application/json, text/plain, or application/xml
      are NOT XSS sinks -- the browser will not render <script> from a non-HTML
      response. Skip them.
    - Only text/html responses are in-scope for XSS. A 200 from an API that
      returns JSON is a non-finding, not a vulnerability.
    - Practical filter: run httpx with -status-code -tech-detect, then grep for
      'text/html' to build the REAL XSS surface (the HTML hosts).
    - ONE exception: error pages. A 403/404 that returns text/html AND reflects
      the requested path/param IS a candidate -- but verify the reflection is NOT
      HTML-entity-encoded before claiming anything.
    - Verify encoding on any lead: inject `<svg onload=alert(1)>`; if `<` comes back
      as `&lt;` / `%3C` / `&#60;`, the sink is safe (properly encoded error page).
      Do NOT mistake the page's own `<HTML>` tags for your payload characters.
