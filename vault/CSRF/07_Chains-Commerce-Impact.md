---
title: "CSRF → XSS → SSRF → RCE — chained impact and the commerce lane"
type: playbook
category: chains-commerce-impact
cwe: "CWE-352"
source_count: 43
full_bodies_available: 41 (+2 metadata-only: 149589, 133847)
corpus: "h1.security.nathan.sx roster (229 rows), bodies via hackerone.com/reports/<id>.json"
list_accessed: "2026-10-28"
note: "Anchor bodies: CSRF-125594 (Uber, server-side compromise narrative), CSRF-206319 (Teavana, high persistent-CSRF, $750 list), CSRF-152013 (Rockstar, $750 list). Claims trace to bodies read 2026-10-28."
---

# Chains & Commerce — CSRF as the first link

## 1. Overview

Forty-three corpus rows treat CSRF not as the finding but as the **delivery mechanism** — the
first link of XSS chains, SSRF chains, admin-compromise chains, and commerce interference. This
is also the module of *persistence*: CSRFs that fire every time the victim's browser visits, and
CSRFs whose state-change is permanent.

**Case-ID scheme: `CSRF-<report id>`.**

| Chain family | Cases |
|---|---|
| CSRF → stored XSS → server compromise | 125594, 152013, 65808, 64184, 59660 |
| CSRF → reflected XSS | 177508, 177639, 115248 |
| CSRF → SSRF | 110801 (module 06 cross-ref), 50537-adjacent |
| Persistent CSRF / permanent state | 206319 |
| Commerce mutations | 177472, 177635, 198470, 8843, 148417, 6378 |
| WordPress plugin cluster | 131108, 149589, 153580, 133847, 145583 |
| Generic forms (no token, era informative tail) | 83239, 85565, 13856, 17312, 25128, 144147, 202808, 191608, 191831, 42728, 137008, 172707, 109839, 216161, 65167, 226612, 257237, 13639, 166231, 7849, 7863, 6888, 7436 |

## 2. The anchor — CSRF-125594 (Uber eng.uber.com, server-side compromise)

WordPress plugin AJAX with no nonce, and the impact narrative is the class ceiling, verbatim:

> The site *eng.uber.com* uses a WordPress plugin called Fluid Responsive Slideshow. The plugin
> doesn't implement any CSRF check for AJAX requests. Some of these AJAX requests can be used to
> modify posts and pages on the system. An attacker could use this bug to inject arbitrary
> JavaScript in any page or post on eng.uber.com.
> The attack requires that an administrator of the site can be tricked to view an
> attacker-controlled website. If the attack succeeds, it would normally lead to server-side
> compromise via the administrative WordPress functions (plugin/theme editor).

The non-destructive probe is a **bogus-parameter no-op**:

```html
<form method=post action="https://eng.uber.com/wp-admin/admin-ajax.php?action=frs_show_modal">
<input type=text name="post_id" value="zzz">
```

> This shows that it's possible to access the AJAX functions of the plugin without any CSRF
> token or nonce. A non-logged-in user receives just a "0".

Agent lessons:

1. **Probe with a harmless action first** (`frs_show_modal`, bogus id) — proves nonce-absence
   without touching content; the destructive `frs_save` is stated, not fired.
2. **The chain is named, not just claimed**: CSRF → stored JS → admin victim → WP theme/plugin
   editor → server-side compromise. Each hop is a real WordPress primitive.
3. *"A non-logged-in user receives just a '0'"* — the response differential (0 vs JSON) is the
   auth oracle for the probe.

## 3. CSRF → stored XSS — CSRF-152013 (Rockstar, $750 list) and CSRF-65808 (concrete5)

- **152013** — the payload chain is one request: `set.php` age parameter stored, reflected on
  `get.php`; the PoC form submits to a hidden iframe then navigates:
  > Sending a POST request to set.php with age='PAYLOAD' will cause a stored XSS on the GET.php
  > file (most likely caused by the cookie, since that's what the `age` is based on).
- **65808 (concrete5)** — dashboard points-action creation without CSRF + stored XSS in the
  same write, PoC verbatim including the payload style:
  > `<input type="hidden" name="upaHandle" value="<sVg/OnLOaD=prompt(1)>" />`
  with the admin as the *victim* — the CSRF lands the XSS in a privileged context.
- **64184/59660 (concrete5)** — add-group/add-community-points variants of the same
  un-tokened dashboard POSTs.

## 4. Persistent CSRF — CSRF-206319 (Teavana, $750 list, high)

The corpus's most original commerce finding — the CSRF's state-change **locks the account out
of purchasing permanently**:

> Hello, I have found an extremely interesting issue that can be used to permanently lock a
> user's possibility of ever buying anything from teavana.com by removing the credit card
> payment method.

The mechanism: `GiftCert-AddToBasket` puts a $100 gift certificate into the victim's basket
persistently; the gift-card line item removes the credit-card payment option, so checkout can
never complete. Agent lessons:

1. **Test idempotence and persistence**: does the forged state-change survive logout/login? Can
   the victim undo it? "Persistent CSRF" is a different severity than a one-shot.
2. **Payment-option gating is business logic** — the CSRF rides a commerce-rule side effect
   nobody defended. Commerce rails (demandware.store here) have many such rules; the hunt-
   business-logic skill's negative-quantity/price-tamper lanes pair directly.
3. The body found the endpoint by *"searching for demandware.store hidden links"* —
   hidden-endpoint discovery as the entry step.

## 5. Commerce mutations — the Starbucks pair (CSRF-177472, CSRF-177635)

- **177472 ($250 list, medium)** — add-to-cart forgery:
  > 3. If victim click the form/link, An item would automatically add to victim's cart.
  > 4. If victim do not find this item, he/she would pay for this item which can greatly
  > influence your repuation. (sic)
- **177635 ($150 list)** — save payment card. **198470** — duplicate report of 177472's
  blog-comment variant. **8843 (stopthehacker)** — disable orders. **148417** — coupon redeem
  (title-only). **6378 (Khan Academy store)** — add/remove cart items.

## 6. WordPress plugin cluster

- **CSRF-131108 (Akismet, $75 list)** — *"Basically all actions on Akismet are vulnerable to
  CSRF"* — account cancel, subscription cancel, site add; the user-id in the path is *ignored*,
  making every endpoint id-collision-free for the attacker.
- **CSRF-149589 ($1,337 list, metadata-only)** — "CSRF to add admin"; the register's
  highest-listed plugin row with no retrievable body — recorded, never quoted, never cited.
- **CSRF-145583** — WP lost-password form CSRF (generic form lane); **153580 (BGMP)** and
  **133847 (ProBlog)** — settings CSRF rows, one not-applicable, one metadata-only.

## 7. The era informative tail

Twenty-three rows are generic "form without token" reports — 83239/85565 (ownCloud),
13856 (Crashlytics), 17312, 25128, 144147, 202808, 191608, 191831 (DoD), 42728, 137008,
172707, 109839, 216161, 65167 ($20), 226612, 257237 ("CSRF Token", empty body), 13639
("X/Csrf token problem"), 166231 (LegalRobot), 7849, 7863, 6888, 7436 ("ALL DETAILS IN
VIDEO" — video-only PoC, no technique content). They stay in the register as the corpus's
**noise floor**: what triagers paid nothing or token amounts for, and the standard against
which the module cases above are the exceptions.

## 8. Execution template

```
STEP 1 — find the un-tokened write primitive (module 05 strip matrix first).

STEP 2 — classify the written value:
  HTML/JS-bearing fields (posts, comments, titles, template bodies) → XSS chain
  URLs/IPs/hosts the server will fetch → SSRF chain
  cart/payment/option rows → commerce lane
  identity fields → module 03 chain

STEP 3 — build the chain with the no-op probe (125594 standard):
  harmless action, bogus id, capture response differential.

STEP 4 — demonstrate ONE destructive-free end-state:
  stored payload rendered in victim context (screenshot),
  or SSRF callback received,
  or payment option gated (206319) — with a recovery path documented.

STEP 5 — write the chain explicitly:
  CSRF (delivery) → X (stored/reflected action) → Y (privilege/impact).
  Era payouts tracked chain length × honesty: settings-only ≈ $100,
  stored-XSS ≈ $750, server-compromise narrative ≈ highest.
```

## 9. Validation gates (all must pass)

1. **Chain written as explicit hops**, each hop evidenced (125594's narrative is the standard).
2. **No-op probe before destructive PoC** — bogus ids, harmless actions, sacrificial accounts.
3. **Recovery path documented** for any persistent state change (206319 lane).
4. **XSS lane only with the stored/reflected proof** — CSRF-to-XSS claims need the payload
   rendered in a logged-in victim context, cross-referenced to Vault/XSS modules.
5. **Video-only PoCs are kill-gated** (7436 pattern) — no technique content, no citation.

## 10. Adjacency

- **Vault/XSS** — the second link lives there (stored-XSS module).
- **Vault/SSRF** — 110801's Press-This scan lane (`0.0.0.0` filter gap) pairs with
  Media-Processing-SSRF; hunt-ssrf skill for the internal-ports matrix.
- **Vault/Business-Logic (row 12 pending)** — the payment-option-gating and cart lanes.
- **hunt-csrf skill** — Scenario D (XSS chains); hunt-dom for delivery gadgets.

## 11. Cross-references

- Module 05 (validation gaps) — the entry primitive for every chain here.
- [`references/blogs-index.md`](references/blogs-index.md) §1 — zseano's CSRF→XSS chain lesson
  (byte-quoted); §3 — modern chained citations.
- [`../XSS/Stored-XSS.md`](../XSS/Stored-XSS.md) — payload-landing discipline.
