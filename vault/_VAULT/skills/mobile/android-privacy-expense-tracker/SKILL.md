---
name: android-privacy-expense-tracker
description: >
  Build privacy-first Android expense tracker apps that parse SMS for bank/UPI payments,
  auto-categorize them, and store everything locally. Covers manifest hardening, SMS
  parsing regex for Indian banks, payee-based auto-categorization, live capture via
  BroadcastReceiver, budget alerts, and rolling-time-window dashboards. Use when the
  task is building a local-only finance/expense tracking APK with SMS ingestion.
  Trigger phrases: "expense tracker", "PesaTrack", "SMS parser", "bank SMS", "UPI tracker",
  "local only finance app".
---

# Android Privacy-First Expense Tracker

Build an Android expense tracker that detects payments from bank SMS, categorizes them,
and keeps 100% of data on-device.

## Hard Requirements (Privacy)

1. **No internet permission** — omit `<uses-permission android:name="android.permission.INTERNET"/>`.
   Android blocks network calls at OS level if permission is missing.
2. **Disable backup** — `android:allowBackup="false"` in manifest. Without this, Google
   Drive can silently copy app data.
3. **Non-debuggable** — do not set `android:debuggable="true"`.
4. **Private storage only** — use `Context` internal storage (`/data/data/<pkg>/`).
   No external storage writes for sensitive data.
5. **No accounts, no analytics, no ads, no cloud sync** — confirm via APK analysis.

## SMS Ingestion

### Permissions
- `READ_SMS` — scan inbox history
- `RECEIVE_SMS` — live capture via `BroadcastReceiver`
- `POST_NOTIFICATIONS` (API 33+) — budget/capture alerts

### Live Capture Registration
Register `SmsReceiver` in manifest with `android:permission="android.permission.BROADCAST_SMS"`
and intent-filter for `android.provider.Telephony.SMS_RECEIVED`. In `onReceive()`,
parse the SMS and enqueue to DB. Guard against duplicates using message hash +
amount+timestamp window dedup.

### Parser Architecture
1. **Junk filter first** — reject OTPs, statements, KYC, offers, failed txn, loan spam.
2. **Debit word detection** — look for `debited|deducted|spent|paid|purchase|withdrawal|sent|charged|txn of|autopay`.
   If credit words present without debit words, skip.
3. **Amount picking** — prefer amount after debit verb (`sent Rs.X`, `Rs.X debited`).
   Fall back to first plausible amount in body. Handle `Rs.`, `INR`, `₹`, commas.
4. **Payee extraction** — ordered regex list:
   - Kotak `Sent Rs.X from Kotak Bank A/c X to PAYEE on DATE`
   - `sent to|paid to|transferred to|payment to PAYEE`
   - `to PAYEE on`, `to: PAYEE`, `at PAYEE`
   - `UPI/x@y/PAYEE/`
   - `paying PAYEE`, `merchant: PAYEE`, `towards PAYEE`
5. **Method guess** — `@okhdfc|@okaxis|@oksbi|@okicici` → GPay; `@ybl|@ibl|@axl` → PhonePe;
   `@paytm|@ptaxis` → Paytm; `upi` → UPI (other); `credit card` → Credit Card.

### Critical: Payee-Only Categorization
**Match categories against the extracted payee ONLY, never the full SMS body.**
Body text contains unrelated words (`recharge`, `movie`, etc.) that cause false positives.

```java
// WRONG: searches full body
if (bodyLower.contains("recharge")) return BILLS;
// RIGHT: searches only payee
if (payeeLower.contains("jio") || payeeLower.contains("airtel")) return BILLS;
```

## Auto-Categorization

### Keyword Map (payee.lowercase() matches)
- **Food & Dining:** swiggy, zomato, blinkit, big basket, domino, pizza hut, kfc, mcdonald, restaurant, canteen, food, chaipoint, chai, dhaba, mess, tiffin
- **Groceries:** grocery, supermarket, hypermarket, dmart, reliance fresh, big bazaar, spencer, more
- **Transport:** ola, uber, rapido, metro, petrol, fuel, parking, bus, train, irctc, redbus, rickshaw, auto, taxi
- **Bills:** jio, airtel, vi, vodafone, recharge, electricity, water, gas, bsnl
- **Shopping:** amazon, flipkart, meesho, myntra, ajio, snapdeal, zepto, retail
- **Entertainment:** netflix, spotify, youtube, hotstar, bookmyshow, pvr, cinema, movie, game, steam
- **Health:** pharmacy, medical, hospital, doctor, medicine, lab, diagnostic, health
- **Education:** university, college, school, coursera, udemy, byju, exam, book, education
- **Rent:** rent, landlord, tenant, property, society, maintenance
- **Travel:** flight, airline, hotel, makemytrip, goibibo, yatra, visa
- **Sent to People:** heuristic — 2-4 words, mostly letters, has mixed case (person name)

### Confidence Flow
- Category matched → auto-save to `txns` table, no review needed
- No category match → enqueue to `pending` table → show in ReviewActivity
- User can long-press any transaction in History to change category anytime

## Time Windows

### Rolling vs Calendar
- **Today:** midnight → now (calendar day)
- **This week:** rolling 7-day window ending today (`dayStart(now) - 6 days`).
  Calendar-week boundaries hide recent spend on Mon/Tue.
- **This month:** calendar month start → now

```java
public static long dayStart(long ts) {
    Calendar c = Calendar.getInstance();
    c.setTimeInMillis(ts);
    c.set(HOUR_OF_DAY, 0); c.set(MINUTE, 0); c.set(SECOND, 0); c.set(MILLISECOND, 0);
    return c.getTimeInMillis();
}

// Rolling 7-day window
public static long weekStart(long ts) {
    return dayStart(ts) - 6 * 86400000L;
}
```

## Budget Alerts

- On limit save AND on app resume, check if total/category spend >= limit.
- Fire notification at **exact limit** with "Do less expense" message.
- Fire 80% warning with different color (orange).
- Use separate notification channels: `captures` (bank SMS) and `budget` (alerts).

## UI Workflow

- **Dashboard:** total month, today, week, payment count, recent 5
- **History:** month-grouped list with daily totals, category filter dropdown,
  long-press → change category dialog
- **Insights:** category breakdown with progress bars, method breakdown, top payees.
  Tapping a category row jumps to History filtered by that category.
- **Limits:** overall + per-category limits with edit fields, spent/limit bars
- **More:** Scan inbox, Live capture toggle, Export CSV, Delete all
- **Review:** only for pending/unidentified payments. If empty, show
  "No unidentified payments. Most detected payments are categorized and saved automatically."

## Build & Deploy

- Build: `./build.sh` → `PesaTrack-v1.1.apk`
- Install: `adb install -r PesaTrack-v1.1.apk`
- Grant SMS: `adb shell pm grant com.pesatrack android.permission.READ_SMS`
- Verify: `adb shell dumpsys package com.pesatrack | grep permission`
- Test scan: launch → tap scan button → verify toast + entries appear

## Known Pitfalls

1. **Patch tool unescapes Java regex** — `\\s` becomes `\s` and breaks compilation.
   Use `write_file` for full-file rewrites when regex escaping is involved.
2. **ADB tap coordinates are device-specific** — use UIAutomator dump to get exact
   bounds: `adb shell uiautomator dump && adb shell cat /sdcard/ui.xml`
3. **Multi-line SMS bodies break row parsing** — use `(?m)^Row:\d+\s*` split with
   `re.S` flag instead of line-by-line.
4. **Screen off/locked blocks ADB screencap** — wake with `input keyevent KEYCODE_WAKEUP`
   and `wm dismiss-keyguard` before capturing.
5. **Person-name heuristic dead if passed lowercase** — check uppercase on original
   raw string, not on `.toLowerCase()` copy.
6. **Calendar week start hides recent spend** — use rolling 7-day window instead.
7. **Body-matching causes category false positives** — always categorize from payee only.
8. **Big payments still need review** — if user wants manual confirmation for high-value,
   add threshold check in `enqueue()` before auto-save. Otherwise remove it.
9. **Terminal SIGINT storms during long ADB chains** — `input tap` followed by `sleep` then `screencap`
   can trigger repeated interrupts. Use single `&&`-chained commands with explicit `sleep`
   instead of separate calls, or break work into smaller terminal invocations.

## Reference

- `references/android-expense-tracker-setup.md` — Indian bank SMS formats, parser
  test results, build script pattern, device-specific ADB coordinates, and UI
  anchor points from real PesaTrack sessions.