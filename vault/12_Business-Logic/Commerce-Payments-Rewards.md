---
title: "Commerce, payments & rewards — price, quantity, coupon, status-field and protocol tampering"
type: playbook
category: commerce_payments_rewards
cwe: "CWE-840"
source_count: 28
full_bodies_available: 28
corpus: "h1-brain disclosed_reports.db, bucket business-logic (module commerce_payments_rewards, 28 rows, bodies-win)"
list_accessed: "2026-11-07"
note: "Claims trace to bodies read 2026-11-07 and archived in references/archive/BL-bodies-full-dump.txt; quotes byte-true."
---


# Commerce, payments & rewards


Pattern: the server trusts client-supplied money math. Quantity, totals, plan IDs, approval flags and signature strings are validated in the browser, if at all; the server applies them as stated. This module holds the vault's crown row ($7,500 wallet-mint) and its two other five-figure rows.


## 1. Overview


Case stock (28 rows / 8 paid / $19,150; bucket module `commerce_payments_rewards`):


| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [BL-336131](https://hackerone.com/reports/336131) | shopify | Potential to abuse pricing errors in saved carts | - |
| [BL-357929](https://hackerone.com/reports/357929) | reverb | Items bought for free due to lacks of quantity controls | - |
| [BL-361960](https://hackerone.com/reports/361960) | upserve | Insufficient validation of sides/modifiers quantity | $500 |
| [BL-364843](https://hackerone.com/reports/364843) | upserve | OLO Total price manipulation using negative quantities | - |
| [BL-403783](https://hackerone.com/reports/403783) | zomato | [www.zomato.com] Tampering with Order Quantity and paying less amou... | - |
| [BL-422331](https://hackerone.com/reports/422331) | aaf | attacker can book unlimited tickets in free at https://aaf.com/chec... | - |
| [BL-486629](https://hackerone.com/reports/486629) | zomato | Improper validation allows user to unlock Zomato Gold multiple time... | - |
| [BL-511044](https://hackerone.com/reports/511044) | zomato | [www.zomato.com] Availing Zomato Gold membership for free by tamper... | - |
| [BL-592803](https://hackerone.com/reports/592803) | automattic | Gaining unlimited bonus points on websites with WooCommerce Points ... | - |
| [BL-665798](https://hackerone.com/reports/665798) | makerdao_bbp | Earn free DAI interest (inflation) through instant CDP+DSR in one tx | - |
| [BL-672487](https://hackerone.com/reports/672487) | curve | Business Logic Flaw - A non premium user can change/update retailer... | - |
| [BL-672664](https://hackerone.com/reports/672664) | makerdao_bbp | Steal collateral during `end` process, by earning DSR interest afte... | - |
| [BL-771694](https://hackerone.com/reports/771694) | semrush | An attacker can buy marketplace articles for lower prices as it all... | - |
| [BL-789260](https://hackerone.com/reports/789260) | nordsecurity | Past payments using the Direct Debit method keep subscriptions acti... | - |
| [BL-882848](https://hackerone.com/reports/882848) | gitlab | Possibilty to purchase Ultimate - 1 Year (EDU or OSS) | - |
| [BL-963774](https://hackerone.com/reports/963774) | basecamp | Premium Email Address Check Bypass - Hey | - |
| [BL-1029027](https://hackerone.com/reports/1029027) | imgur | Bypass subscription | - |
| [BL-1070510](https://hackerone.com/reports/1070510) | logitech | Manipulating response leads to free access to Streamlabs Prime | - |
| [BL-1089978](https://hackerone.com/reports/1089978) | shopify | [h1-2102] [Yaworski's Broskis] Suspected overcharge and chargebacks... | - |
| [BL-1213765](https://hackerone.com/reports/1213765) | reddit | IDOR to pay less for coin purchases on oauth.reddit.com via /api/v2... | $500 |
| [BL-1295844](https://hackerone.com/reports/1295844) | valve | Modify in-flight data to payment provider Smart2Pay | $7,500 |
| [BL-1322334](https://hackerone.com/reports/1322334) | automattic | Ability to subscribe to inactive Post+ creators | - |
| [BL-1538669](https://hackerone.com/reports/1538669) | omise | IDOR Payments Status | $100 |
| [BL-1543159](https://hackerone.com/reports/1543159) | reddit | Able to approve admin approval and change effective status without ... | $5,000 |
| [BL-1849626](https://hackerone.com/reports/1849626) | stripe | Fee discounts can be redeemed many times, resulting in unlimited fe... | $5,000 |
| [BL-2125049](https://hackerone.com/reports/2125049) | indrive | Unlimited fake rate to the passenger in city to city, Affected endp... | - |
| [BL-2257374](https://hackerone.com/reports/2257374) | x | Bypassing x profile verification to receive instant blue checkmark ... | $250 |
| [BL-3136790](https://hackerone.com/reports/3136790) | toolsforhumanity | Unlock underage blocked app without support interaction using airpl... | $300 |


Corpus mix: three five-figure anchors (valve $7,500; reddit $5,000; stripe $5,000) plus a $500/$300/$250/$100 tier; 20 of 28 rows carry no figure. The unpaid 20 are not noise — they carry every quantity-tampering primitive in the class (negative, zero, fractional).


## 2. Wallet mint via in-flight signature injection — BL-1295844 (valve, $7,500)


Steam wallet top-ups route through Smart2Pay, whose request `Hash` is a concatenation hash over field names+values. The reporter registers an email embedding extra fields (`brixamount100abc@…`), then rewrites the intercepted POST so the provider parses an injected `amount` while the signature still verifies:


> We cant change parameters as there is Hash field with signature, however signature is generated like that hash(ALL_FIELDS_NAMES_VALUES_CONTACTED)




> For example, we can change original `Amount=2000` to `Amount2=000` and after contacting it still will be `Amount2000`




> Then we can change email from `CustomerEmail=brixamount100abc%40████` to `CustomerEmail=brix&amount=100&ab=c%40█████████` by this we are adding new field amount with our value.




> Then just pay 1 $ and you should get your money on steam wallet in few hours/days those are some transactions made with this metod:


Impact as filed:


> I think impact is pretty obvious, attacker can generate money and break steam market, sell game keys for cheap etc.


Doctrine: never hash-concatenate attacker-controlled values into a signature without length-prefixing or domain separation — any value that can smuggle `&field=value` becomes a new signed field.


## 3. Admin-approval overwrite → free ad delivery — BL-1543159 (reddit, $5,000)


Reddit Ads keeps campaigns `PENDING` until payment + admin review. The server accepts a client PATCH that simply rewrites both gates:


> But changing the value of admin_approval to APPROVED and effective_status to ACTIVE , the ads is approved and thus we receive the confirmation email from reddit ads that our ads is approved .




> {"data":
> {"configured_status":"ACTIVE",
> "effective_status":"ACTIVE",
> "admin_approval":"APPROVED"
> }}




> Can bypass the review process and change the ads status to approve and active without payment process .


Server-side lesson: approval/review state fields must be server-computed, never client-settable via the same API that edits ads.


## 4. Fee-discount replay, serial not race — BL-1849626 (stripe, $5,000)


A $20,000 fee-discount offer is accepted by `/ajax/accept_fee_discount_offer`. The reporter reaches for a race, but the endpoint never marks the offer consumed:


> It seems a race was not even needed though, as I called it 30 times and 30 fee discounts were immediately applied to my account! As a result, I now have $600,000 of fee-free processing applied to my account.




> Unlimited fee-free discounts. This will cost Stripe about 3% of each discount, so $600 each time a $20k discount is abused.


One-time-accept endpoints need the same consume-once discipline as tokens: serial replay is the cheaper attack; test it before wasting time on parallel races.


## 5. Quantity / total manipulation family (mostly unpaid, fully evidenced)


BL-364843 (upserve, unpaid): a negative-quantity line item drags the order total down —


> Manipulating an order request JSON object, containing an additional item with a negative quantity directly manipulates the total amount of the order.




> In the following JSON request, an order is submitted for 2 ChickenBurgers ($12 each), as well as -1 BreadPuddings ($9 each).


BL-771694 (semrush, unpaid) prices the same class with receipts:


> {"items":{"article_500":4,"article_1000":-2}}




> 4 * $40- 2 * $70= $160 - $140 = $20


BL-403783 (zomato, unpaid) pushes the quantity fractional — 0.1 of a ₹99 biryani delivers a full meal —


> But when we set a quantity to a decimal number, for example: let's say I am trying to order 1 Biryani that costs 99₹, I can set the quantity to 0.1 and now the order price will total to 9.9₹.


BL-357929 (reverb, unpaid) is the zero edge: `quantity: 0` accepted as 1, `Items are sold gratis`. BL-361960 (upserve, $500) is the modifier-count variant — client caps `sides` at 1 via JavaScript; the server never re-checks:


> the application restricts the number of sides/modifies that can be selected on the client side through javascript, but does not validate the request on the server side for the number of sides/modifiers.


BL-422331 (aaf, unpaid) swaps `3-seats-3` → `10-seats-10` for a $0 order.



## 6. Plan-ID and order-ID substitution


BL-511044 (zomato, unpaid) enumerates `plan_id`s with Intruder, finds the zero-price plan, and mints a month of Zomato Gold —


> Using the intruder, I figured out that the plan_Id 147 has a membership cost of 0.




> {"response":{"status":"success","message":"Transaction Approved Without Sending to Gateway"


BL-1213765 (reddit, $500) is the order-ID sibling: create the small coin order, swap the big order's `order_id` for the small one's in the response, pay $1.99, receive the large pack:


> Pay, and boom ! You paid 1.99$, but when you complete the order you will be given the amount of coins you "purchased" for the "fake price".


BL-1089978 (shopify, unpaid) inverts the direction — `amount_rounding: -1.0` makes the PoS overcharge the customer and divert the shop's money. BL-882848 (gitlab, unpaid) buys the education-only Ultimate plan by direct `plan_id` URL. BL-1322334 (automattic, unpaid) swaps `blogMembershipsId` to resurrect an inactive Post+ blog.


## 7. Entitlement, promo and rewards abuse


BL-486629 (zomato, unpaid) re-claims Zomato Gold at the same restaurant the same day; BL-592803 (automattic, unpaid) farms WooCommerce points via cash-on-delivery `processing` status:


> However, this assumption is wrong for payment gateway Cash On Delivery, which immediately changes order status to Processing on all new orders. Plugin then increases bonus points for the order total which are immediately available to spend.


BL-672487 (curve, unpaid) edits the profile-response body client-side to reset its 3-retailer cap to `merchants: []` — a client-enforced entitlement. BL-1029027 (imgur, unpaid) prepends a space to `avatar_id`, relying on server-side TRIM after the paid-check. BL-963774 (basecamp, unpaid) registers `jp  @hey.com` to defeat the premium short-address check. BL-2257374 (x, $250) upgrade/downgrade-cycles Premium+ to skip profile-pic review. BL-3136790 (toolsforhumanity, $300) airplane-modes past an underage lock requiring support.


## 8. Contract-economics rows (makerdao_bbp, unpaid, protocol-level)


BL-665798 and BL-672664 are smart-contract accounting flaws: DSR interest paid on balances that exist for a single transaction inflates DAI supply; `pot` stays live after `end.cage`, letting saved-rate minting steal settlement collateral. Both are pure business-logic (no code executed, no reentrancy) with 10%+-of-collateral impact claims. Kept here because the corpus class is the flaw, not the stack.


## 9. What pays / what doesn't


**Pays:** (1) real-money deltas with a screenshot — wallet balance (1295844, $7,500), fee-discount ledger (1849626, $5,000), delivered ad (1543159, $5,000); (2) externalized cost framing (`This will cost Stripe about 3% of each discount`) (3) order-ID substitution at $500 (1213765). **Doesn't price (in this corpus):** theoretical PoS overcharge without a live gateway (1089978, reporter admits `need verification from the side of Shopify`), airplane-mode bypass with an unfinished PoC (3136790 got $300 precisely because the bypass completed even uncompleted-verification).


## 10. Cross-references


- Race vault (`../Race-Conditions/`): BL-1849626's expected-race-that-wasn't and BL-413759/759247's actual races are its serial/parallel boundary cases.
- Account module: BL-1538669 (omise, $100) payment-status IDOR and BL-2125049 (indrive, unpaid) unbounded `rating` are access-control-shaped commerce rows, kept here by body.
- Rate-limit module: BL-592803's points farm is the rewards analogue of its state-abuse rows.
