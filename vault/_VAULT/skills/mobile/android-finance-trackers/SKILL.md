---
name: android-finance-trackers
description: >
  Patterns for building or modifying Android expense/finance tracking apps that use
  local SQLite storage, SMS parsing for bank debits, and category-based budgeting.
  Use when the task involves adding transaction detection, auto-categorization,
  pending-review queues, history list interactions, category management, or
  budget dashboards in an offline-first personal finance Android app.
  Triggers: "add auto-categorization", "review detected payments", "SMS to txn",
  "quick category change", "long-press history", "pending payments", "budget limits".
---

# Android Finance Trackers

## Architecture conventions

- Single-activity multi-tab layout: `dashboard`, `history`, `insights`, `limits`, `more`.
- Local-only: SQLite via `SQLiteOpenHelper`, no network, no accounts.
- SMS pipeline: `SmsReceiver` → `Sms.enqueue()` → `parse()` → `pending` or `txns`.
- Dedup: `smsrefs` by SHA-256 of body+date; also amount+time window dedup against existing txns and pending.

## Auto-categorization pattern

### Rule

Confidence-based: if categorization is certain, insert directly into `txns`; if uncertain, insert into `pending` for human review. Do NOT force large payments into review — let auto-categorization handle all amounts; the user can change any category later from History.

### Implementation

1. Add a `categorize(payee, body)` method in the SMS parsing class.
2. **Match payee keywords ONLY.** Do NOT pass the full SMS body into keyword matching; the body contains unrelated text (URLs, disclaimers, balance info) that causes false positives. Use a payee-only matcher.
3. Add a person-name heuristic (2–4 words, mixed case) for person-to-person transfers.
4. Return `OTHER` when no rule matches.
5. In `enqueue()`, call `categorize()` before deciding between `insertTxn()` and `addPending()`.
6. Always `addSmsRef(hash)` on either path to prevent re-processing.

### Keyword matcher

```java
private static boolean payeeMatch(String payeeLower, String... kws) {
    for (String k : kws) {
        if (payeeLower.contains(k)) return true;
    }
    return false;
}
```

Call with `payee.toLowerCase()` only. Never include the SMS body as a fallback search space.

### Person-name heuristic

```java
private static boolean looksLikePersonName(String raw) {
    if (raw == null || raw.isEmpty()) return false;
    String s = raw.trim();
    int words = s.split("[\\s-]+").length;
    if (words < 2 || words > 4) return false;
    int alpha = 0, upper = 0;
    for (int i = 0; i < s.length(); i++) {
        char c = s.charAt(i);
        if (Character.isLetter(c)) {
            alpha++;
            if (Character.isUpperCase(c)) upper++;
        }
    }
    if (alpha < 3 || alpha > 40) return false;
    return upper >= 1 && upper < alpha; // some uppercase, but not fully uppercase spam
}
```

Pitfall: do NOT lowercase the payee before checking uppercase count; check the raw extracted payee string. The previous pattern lowercased first, which made the uppercase check always return false.

### Category keyword list

- Food: swiggy, zomato, blinkit, big basket, domino, pizza hut, kfc, mcdonald, restaurant, canteen, food, chaipoint, chai, dhaba, mess, tiffin
- Groceries: grocery, supermarket, hypermarket, dmart, reliance fresh, big bazaar, spencer, more
- Transport: ola, uber, rapido, metro, petrol, fuel, parking, bus, train, irctc, redbus, rickshaw, auto, taxi
- Bills: jio, airtel, vi, vodafone, recharge, electricity, water, gas, bsnl
- Shopping: amazon, flipkart, meesho, myntra, ajio, snapdeal, zepto, retail
- Entertainment: netflix, spotify, youtube, hotstar, bookmyshow, pvr, cinema, movie, game, steam
- Health: pharmacy, medical, hospital, doctor, medicine, lab, diagnostic, health
- Education: university, college, school, coursera, udemy, byju, exam, book, education
- Rent: rent, landlord, tenant, property, society, maintenance
- Travel: flight, airline, hotel, makemytrip, goibibo, yatra, visa
- Send (P2P): person-name heuristic

## Review queue shrinkage

When auto-categorization covers most cases:

- Keep `ReviewActivity` but update copy to say it only shows unidentified payments.
- Remove the "Review detected payments" button from the More tab.
- Remove any pending-count badge from the More tab.
- Update scan feedback to mention that confident detections were auto-saved.

## History long-press quick actions

In the list adapter's `getView()`:

```java
card.setOnLongClickListener(v -> {
    CharSequence[] opts = new CharSequence[Cats.ID.length];
    for (int idx = 0; idx < Cats.ID.length; idx++) {
        opts[idx] = Cats.EM[idx] + " " + Cats.NM[idx];
    }
    new AlertDialog.Builder(context)
            .setTitle("Change category")
            .setItems(opts, (d, which) -> {
                db.updateTxn(t.id, t.amount, Cats.ID[which], t.method, t.note, t.ts);
                refreshAll();
            })
            .setNegativeButton("Cancel", null)
            .show();
    return true;
});
```

Pitfall: do not shadow the outer `i` loop variable inside `getView(int i, ...)` with another `int i`; rename to `idx`.

## Build / verification

- Project uses `aapt2` + `javac --release 8` + `d8` + `zipalign` + `apksigner`.
- Build script: `bash build.sh` at repo root.
- Keystore auto-generated on first build.
- APK output: `PesaTrack-v1.1.apk`.
- Java source: `app/src/com/pesatrack/*.java`.
- Resources: `app/res/`, manifest: `app/AndroidManifest.xml`.

## Category design

- Categories are constants in `Cats.java`: `ID[]`, `EM[]` (emoji), `NM[]` (display name), `CO[]` (colors).
- Methods are `METHODS[]` in the same class.
- New categories: add to all four arrays in the same index position.
- `OTHER` is the fallback and also the "unidentified" bucket.

## Safety rules

- Never expose raw SMS bodies or sender addresses outside the app.
- Do not add internet permissions or network calls.
- All exports go to `Downloads/PesaTrack/` via MediaStore on API 29+ or legacy external storage.
- Budget alerts post a notification; ensure `Notif.ensure()` is called before posting.
