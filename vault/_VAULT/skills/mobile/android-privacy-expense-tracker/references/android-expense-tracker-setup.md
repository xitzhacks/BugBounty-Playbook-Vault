# Android Expense Tracker — Session References

## Indian Bank SMS Formats Observed (Oct 2026)

### Kotak Bank
- `Sent Rs.250.00 from Kotak Bank A/c X3656 to SWIGGY on 25-10-26.`
- `Sent Rs.XX.XX from XX3656 to PAYEE on DD-MM-YY.`
- `Rs.500.00 debited from A/c XX9876 on 25-10-26, Ref 412345678901- BHARAT PE QR-payment sent to SHARMA STORES-Sent-UPI/123@ybl/NA/NA`
- **Critical:** Kotak SMS contains anti-fraud URLs (`https://kotak.bank.in/...`, `https://kotk.in/...`). Do NOT filter SMS with `http` in junk filter.

### JioPay
- 64+ messages, many in Telugu script
- Sender variants: `JD-JioPay-S`, `JD-JIOPAY-S`, `JD-JIOINF-S`, `JL-JioSvc-S`

### Kotak Sender Variants
`JD-KOTAKD-S`, `AD-KOTAKB-S`, `JD-KOTAKB-S`, `JK-KOTAKD-S`, `JX-KOTAKB-S`, `AX-KOTAKB-S`, `JM-KOTAKD-S`, `VA-KOTAKB-S`, `JK-KOTAKB-S`

### Other Formats Tested
- `Rs.299 charged on your HDFC credit card XX1234 for NETFLIX`
- `ATM withdrawal of Rs.5,000 from your A/c XX1234`
- `Rs.499 autopay successful for SPOTIFY from HDFC Bank A/c`
- `Rs.60.00 debited from your a/c xx4433 towards UPI/7894561230@ybl/MERCHANT/NA`
- `e-txn: Rs.99 debited for UPI to CHAI POINT`
- `Rs.1,23,456.00 debited from A/c XX1234 on DD-MM-YY NEFT to RELIANCE INDUSTRIES`
- `INR 999.00 spent on Axis Bank Card xx1234 on DD-MM-YY at AMAZON PAY UPI`

## Parser Test Results (278 real SMS)

- Detected: 80/278 payment SMS after Kotak fixes
- Skipped junk: 198
- Auto-saved by category: 54 (Food 22, Bills 9, Sent to People 18, Shopping 5)
- Pending review: 26

## Build Script Pattern

```bash
SDK=~/Android/Sdk
javac -encoding UTF-8 --release 8 \
  -cp $SDK/platforms/android-36/android.jar \
  -d /tmp/classes \
  app/src/com/pesatrack/*.java
# then dx/d8 to dex, then apksigner + zipalign
```

## Device: ZD222GSLQT (Motorola Edge 40 Neo)

- Screen: 1080x2400
- Wake: `input keyevent KEYCODE_WAKEUP && wm dismiss-keyguard`
- Screencap: `exec-out screencap -p > /tmp/shot.png`
- UIAutomator: `uiautomator dump /sdcard/ui.xml && cat /sdcard/ui.xml`

## UI Anchor Points (1080x2400)

- Home: (160, 2310), History: (330, 2310), Insights: (640, 2310), Limits: (830, 2310), More: (972, 2310)
- Scan button (More tab): (540, 510)
- Live capture switch: bounds [887,475][1005,543], tap center (946, 509)
- FAB: (980, 2180)
