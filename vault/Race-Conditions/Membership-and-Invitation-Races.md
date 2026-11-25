# Membership, Invitation & State-Corruption Races (Race-Conditions vault)

Pattern: an INSERT guarded only by a prior SELECT ("am I already a member?") with no UNIQUE constraint or transaction. Parallel replays create duplicate rows the owner's UI then cannot delete.

## 1. Double group join → undeletable member — RACE-604534 (Hacker101 CTF, bounty None)

Two accounts (leader + member). Member intercepts the join request:

```
POST /group/post_join HTTP/1.1
Host: ctf.hacker101.com
...
csrf=391aecf0c3125e90c437d04c18204ab6&invite=bb5c42ab578b12c63e5d868b3e03816c8c45597262aaf095ca2be19116b8fd0a
```

> Repeat the above requests in parallel. I did it for 5 parallel requests and I was able to add myself 2 times to that group:

> There exists a Race Condition in which the user can add themselves twice to a group which will make them unremovable from group. They themselves cannot remove themselves from the group as well as the group leader cannot remove that user from the group. Ofcourse this is a low severity as that malicious user first needs to have a valid invitation link, but nevertheless this leads to permanent membeship of group so this needs to be fixed in my opinion.

Impact as filed: `Irremovable/permanent member of the group. Even the group leader cannot remove that user.` The report closes with the remediation cost: the leader must delete the group (`This would lead to a state where the group leader will have to delete the group and create a new group if he wants the malicious user to get removed.`).

Honest severity — the reporter self-rates Low. Duplicate state, zero code execution; that honesty is exactly what makes the report triage-friendly.

## 2. Same bug, new build — RACE-1540969 (Hacker101 CTF group join, paid $500)

The successor report explicitly reopens the earlier one:

> Interestingly a race condition in this feature was reported in #604534, but it seems like the implementation has changed slightly, allowing the same issue to occur.

> A race condition in `https://ctf.hacker101.com/group/join` allows a user to join the same CTF group multiple times.

> The user will show up in the group member list multiple times, and affect the group statistics.

Weaponized with the Turbo Intruder gate script (full script in Synchronization-and-Tooling.md §4):

> 3. Start the attack, and observe multiple requests succeeding with status code 200.

Status-code observation note: a 200-per-replay response is the giveaway — membership state was written per response rather than per logical action.

## 3. Credential-claim race — RACE-488985 (H1 GraphQL `claimCredential`, bounty None)

Program test-credentials are claimable once per user/team; the claim is a check-then-insert. 22 Burp Intruder replays of the same `claimCredential` mutation:

> and I then sent this request to burp suite intruder and got 22 responses , 21 of them had the same response as this

> and the last one was holding a different set of credentials as this:

The 1-of-22 `was_successful:true` response carries a *fresh* credential set (distinct `private_id`), so the attacker walks away with multiple live test accounts. Impact as filed: `claiming multiple credentials for the same user`, plus the collateral that it `maybe block another user from getting a test account if the program provided a limited amount of test accounts.`

Lesson for operators: a mostly-failed burst is still a win — count distinct identities in the *success* set, not the failure count.

## 4. Invitation farm + cancel-refund loop — RACE-1460373 (FetLife, bounty None)

The invite endpoint debits 1 invite per POST and refunds on cancel — two unsynchronized ledgers:

> By sending many requests at the same time to endpoint `POST fetlife.com/users/invitation`. We are able to send many invites with the cost of 1 invite.

> Also, if we cancel sent-invite, we get back this invite. So basically, we can create unlimited invites by send many invites in race condition, then canceling them to get invites added back to our account.

Ten curls in one chain (`curl_command_1 & ... & curl_command_10`), 10 distinct plus-addressed emails, one debited invite. Impact: `Attacker is able to generate unlimited amount of invites.`

Note the composition: race mints N invites, the *refund* flow (a serial, non-raceable action) launders them back into the spendable balance. When a system has a cancel/refund path, always test the cancel after the race.

## Cross-references

- Financial/ledger siblings: Financial-Credit-and-Ledger-Races.md (same check-then-insert, different desk).
- ATO/tokens: Account-ATO-and-Token-Races.md (reset and OAuth endpoints duplicating state the same way).
- Business-Logic/ (same primitive, serial duplicate-submit instead of parallel).
