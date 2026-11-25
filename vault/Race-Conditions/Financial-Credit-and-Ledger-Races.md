# Financial, Credit & Ledger Races (Race-Conditions vault)

Pattern: server credits a resource per accepted request; the "already paid / limit reached" check is not in the same transaction as the credit insert. Parallel (or tab-) racing mints N×.

## 1. Purchase-verify inflation — RACE-801743 (Reddit gold coins)

Endpoint: `POST https://oauth.reddit.com/api/v2/gold/android/verify_purchase` (Android purchase verification, body carries `transaction_id`, Google `token`, `package_name`, `product_id`).

> There exists a race condition on this endpoint which allows an attacker to get coins many times more than it was intended to.

> - We can simply repeat this request in parallel to get more coins.
> I did 10 parallel requests and got 9 of them through. An actual attacker will do more requests and get more coins. Like for example, they can do 40 requests and maybe if 35 of them get through they have 35x times the coins intended.

Note the verifier does not key on `transaction_id` (the receipt is re-checkable) nor `product_id` consumption — the *client-generated* `correlation_id` is in the body but apparently not a dedup key impact-wise. Reporter marked High: `This can lead to a huge business loss for Reddit`.

## 2. Payment confirm race → money duplication — RACE-429026 (HackerOne retest)

The retest-accept flow pays per confirmation; 5 curl-parallel confirmations produced a real $500 double credit visible two weeks later in bank statements:

> Observe that a $500 payment was sent from HackerOne 2 weeks ago, demonstrating that the race condition was successful:

Impact statement as sent:

> This allows an attacker to exploit the retesting feature to steal many times more money. Given that this went unnoticed by both the attacker and HackerOne for over 2 weeks, this has the potential to be exploited multiple times to steal money from HackerOne.

Lesson: payment/ledger endpoints are the worst place to skip idempotency keys — proof survived the disclosure window.

## 3. Promo accept race — RACE-1037430 (Badoo / Bumble "free premium days")

Flow: delete-account retention prompt offers 3 free premium days via `POST /webapi.phtml?SERVER_PROMO_ACCEPTED` (protobuf-ish body `{"$gpb":"badoo.bma.BadooMessage","body":[{"message_type":402,...}]}`).

> Here i found a race condition vulnerability through which i was able to get more than three days of premium.

> On the time of testing I  got  3 successful request  which got me 9 days of premium instead of  3 (where 1 week of premium costs about 5$) .

Tooling: stock Turbo Intruder race.py (see Synchronization module). Confirmation artifact: premium end date extended `it will stop on 27 November 2020` from start date `18 November`.

## 4. Redemption-limit race — RACE-1717650 (Stripe promotion codes)

Merchant creates code with `Redemption limit` N; the consumption check is raceable **across two checkout links in two tabs**:

> But there exists a race condition that allows use of promotion codes more than redemption limit.

> 2. As a user, Visit any two payment links of same merchant with the coupon.
> 3. In both payment links, Fill the form and apply coupon but don't hit Pay/ Subscribe.
> 4.Hit both link's pay/subscribe button as fast as you can.
> 5. Both payment will be successful using one coupon two times.

This is the widest toolless window in the corpus (click-speed racing works) — mark entry point: multi-session checkout where coupon apply happens before pay submit.

## 5. Faucet cap race — RACE-1438052 (cosmos/starport, paid $5,000)

Starport faucet honors `coins_max`, checked in an in-memory Go map; 50 concurrent requests gave alice 30 tokens against an 11 cap:

> Now when we check Alice balance it is 30 which should have not been more than 11

Root cause named (Go map not concurrency-safe) and class reference attached (`CWE-362` link in Supporting Material, per body `https://cwe.mitre.org/data/definitions/362.html`).

> A malicious user can send concurrent requests to fetch more tokes from faucets than the "max-credit limit" which allows.

## 6. Points/followers ledger races (low-ceremony, still paid)

- RACE-454949 (CTF flag submission, bounty None): same Trivial flag submitted ×70 for points — `I've used the Trivial Flag 70 times and earned 2 invitations.` — impact is invitation-gating integrity, not money.
- RACE-1566017 (judge.me, paid $250): like-endpoint race inflates follower counts, body `##summary:` line: `An attacker can increase the followers of  the users of judge.me` (sic, double space); Impact field adds: `The attacker can increase their followers in a bad way by creating fake followers`

Validation gate reminder: capture the *state* delta (balance panel, bank line, membership list, end-date), not the HTTP traffic alone.

## Cross-references

- `Business-Logic/` vault (upcoming): non-race variants of the same pattern (coupon stacking via serial reuse) live there once built.
- `privilege-escalation` / ledger integrity: none of these cases required admin; all authenticated-user shells.
