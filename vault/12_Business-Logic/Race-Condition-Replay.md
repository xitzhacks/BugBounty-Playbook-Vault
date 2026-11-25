---
title: "Race-condition replay — the parallel-replay slice of business logic (gift cards, credits, locations)"
type: playbook
category: race_condition_replay
cwe: "CWE-366"
source_count: 6
full_bodies_available: 6
corpus: "h1-brain disclosed_reports.db, bucket business-logic (module race_condition_replay, 6 rows, bodies-win)"
list_accessed: "2026-11-07"
note: "Claims trace to bodies read 2026-11-07 and archived in references/archive/BL-bodies-full-dump.txt; quotes byte-true."
---


# Race-condition replay


Pattern: a consume-once action is checked in one request and applied in another. Parallel replay of the same request mints the surplus. This module is the business-logic overlap with the Race vault — kept here because the bucket classified them, cross-cited in both.


## 1. Overview


Case stock (6 rows / 2 paid / $750; bucket module `race_condition_replay`):


| Case | Target | Mechanism | Bounty |
|---|---|---|---|
| [BL-381356](https://hackerone.com/reports/381356) | security | Client-Side Race Condition using Marketo, allows sending user to da... | - |
| [BL-413759](https://hackerone.com/reports/413759) | shopify | Race condition at create new Location | $500 |
| [BL-759247](https://hackerone.com/reports/759247) | reverb | Race Condition allows to redeem multiple times gift cards which lea... | - |
| [BL-974892](https://hackerone.com/reports/974892) | helium | Race Condition of Transfer data Credits to Organization Leads to Ad... | $250 |
| [BL-1285538](https://hackerone.com/reports/1285538) | omise | Race condition on action: Invite members to a team | - |
| [BL-2616045](https://hackerone.com/reports/2616045) | automattic | Race condition on add 1 free domain | - |


## 2. Gift-card double redemption — BL-759247 (reverb, unpaid)


A $25 gift card redeemed 7 times via Turbo Intruder:


> def queueRequests(target, wordlists):
>     engine = RequestEngine(endpoint=target.endpoint,
>                            concurrentConnections=30,
>                            requestsPerConnection=30,
>                            pipeline=False
>                            )




> In my case I bought one gift card which was worth of 25$ and as we can see from the picture I was able to redeem it 7 times which makes 25*7 = 175$.


## 3. Credit-transfer mint — BL-974892 (helium, $250)


Transfer-data-credits raced between two organizations leaves both balances whole:


> * Send it to Turbo Intruder and Select Race.py Script
> * Go Boom execute and refresh the balance




> Abusing the Race Condition inorder to add extra free data Credits to the organization without buying and lead to business impact


## 4. Plan-limit bypass via location race — BL-413759 (shopify, $500)


Store-location creation checked against the plan limit serially, raced in parallel:


> Intercept request and send it multiple at once. See screensots




> I created 12 store location when 4 possible


## 5. Invite / grant duplication — BL-1285538 (omise, unpaid) and BL-2616045 (automattic, unpaid)


Omise's `/team/memberships` invite endpoint races to multi-invite one email —


> As you can see there is multiple `200 OK` which means a race condition vulnerability happened.


WordPress/Gravatar's free-domain claim races to buy more than the one free domain allowed:


> 7. after complete changing meta, send all request with Group (parallel)


## 6. Client-side race — BL-381356 (security, unpaid; the module's outlier)


A postMessage race on `www.hackerone.com`'s Marketo form: no origin check on the listener between #3 and #6, so an attacker message wins the race and `followUpUrl` redirects the victim — on Safari, even to a `data:` credential-harvesting page:


> Since no origin check is made on the listener initated in #3, we can from our end try to race the message between #3 and #6. If our message comes through we can direct the user to whatever location we like if we find a form that doesn't utilize `onSuccess`.


## 7. What pays / what doesn't


**Pays:** limit-bypass with a countable surplus (413759: 12 locations against a 4 cap, $500; 974892: free credits, $250). **Doesn't price here:** the gift-card race (759247, $0 — shown money math but no payout figure in the DB) and the client-side race (381356, $0, reporter themselves `pretty divided on the impact`).


## 8. Cross-references


- `Race-Conditions/` vault: the same primitives, full treatment; this module is the bucket's slice.
- Commerce module §4: BL-1849626 proves the serial replay must be tested before the race — many of these modules' rows would also pass …once.
