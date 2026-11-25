# Account Takeover & Token Races (Race-Conditions vault)

Pattern: identity state minted per-request that should be minted once — email validation, OAuth grant exchange, password-reset tokens. The race creates a state the UI believes is already validated.

## 1. Email-confirmation race → partner/employee ATO — RACE-300305 (shopify, $15,250)

Corpus crown. Shopify converts a partner account into a collaborator when the email matches an employee's validated account. Business accounts must validate email — but validation and email-change were not one DB transaction:

> The bug works by hitting the email validation endpoint for an email you own, at the same time as changing your email to a victim's. It might take a few tries, but eventually your email will be changed and be validated due to not (properly) using a DB transaction.

Full chain from the body:

> 6. Go back to your partner account and change your email to that of the store employee from step 2, but intercept the request to not let it through yet.
> 7. Now the tricky part. The "change email" takes anywhere from 1,100 - 2,500 ms to load so you need to take that into account. But let the request go through, wait for some milliseconds, then in another tab visit that email confirmation link from step 5.
> 8. If done correctly you will now have confirmed an email you do not own.
> 9. Visit `https://partners.shopify.com/[ID]/managed_stores`, add the store, and you now have access.

Impact as filed: `Ability to take over stores, and possibly perform any other action that relies on a validated email as a security measure.`

Doctrine: the race alone is worth nothing — a `confirmed` flag on an attacker address. It pays $15,250 because a *different* system (collaborator auto-conversion) trusts that flag as employee identity. Always map confirmed/validated flags to every consumer.

## 2. OAuth2 code/refresh_token exchange race — RACE-55140 (ibb, bounty None)

RFC 6749: an authorization `code` may be redeemed once. Tested against 11 providers, 6 had the race:

> Race Condition allows a malicious application to obtain several `access_token` and `refresh_token` pairs while only one pair should be generated. Further, it leads to authorization bypass when access would be revoked.

> For different attempts result of its execution gives from 1 to 20 different `access_token` values (may be in pair with `refresh_token` values) for targets which has Race Condition bug (10 of 11 tested).

Exploit script in the body is the dumbest possible parallelization:

```bash
curl --data "grant_type=authorization_code&code=AUTHORIZATION_CODE_VALUE&client_id=APPLICATION_ID&client_secret=[REDACTED_SECRET]" "https://OAUTH_PROVIDER_DOMAIN/oauth/token" &
```

Refresh-token lane is worse — self-amplifying:

> Exploitation for `refresh_token` is more dangerous than for `access_token`, because there is no way for an attacker to fail. Each exploitation gives at least one new `refresh_token` which may be used further. Thus, number of token pairs grows exponentially.

And the revocation failure that makes it an ATO, not a curiosity:

> 7A) Go to **settings** or **applications** page in the victim's account and revoke access for the application. Then repeat step 5 and see if all `access_token`s become invalid or not. If all `access_token`s are invalid, It is good behavior despite successful Race Condition exploitation. Actually, in some cases only one `access_token` is revoked, while all the rest stay valid.

Probabilistic disclosure etiquette, quoted in the playbook and Synchronization module, originated here:

> Please note that Race Condition is probabilistic vulnerability. It may be needed to do few attempts with PoC to reproduce it.

## 3. Dual reset endpoints, independent token stores — RACE-772886 (nordsecurity, bounty None)

Not a strict parallel race — a *sequential* window created by logic duplication. Two endpoints (`/change-password/` authenticated, `/reset-password/` unauthenticated) issued independent tokens; using one never invalidated the other:

> It appears as though NordVPN uses two methods at two different endpoints (i.e., `/change-password/` and `/reset-password/`) to reset a user's password. By combining both methods, you are able to use multiple valid password reset tokens for one single account.

> The application issues two valid reset tokens for one user. After the 1st token is used, the 2nd token is able to be used as well (i.e., the application is *not* properly invalidating multiple tokens).

Impact as filed: `At attacker may be able to take over another user's account.` (sic) — plus a self-DoS (403 lockout) as secondary damage.

Operator rule: enumerate *every* endpoint that mints/consumes a token for the same account, then test cross-endpoint invalidation serially before testing parallel races.

## Cross-references

- `Authentication-Session/` — RACE-772886 belongs to its token-invalidation module; RACE-55140's revocation-bypass is the OAuth analogue.
- Membership module — RACE-488985's credential claim is the same primitive applied to test accounts.
- Check-Use module — RACE-300305's missing transaction is the web-app form of the DB-level root cause.
