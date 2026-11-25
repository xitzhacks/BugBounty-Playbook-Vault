---
title: "FirstBlood Hackevent XSS Report Index (BugBountyHunter.com)"
type: reference
reports_listed: 207
fetched: "2026-10-17"
source: "https://www.bugbountyhunter.com/hackevents/{firstblood,firstbloodv2,firstbloodv3}"
note: "All 207 XSS-typed reports disclosed on BugBountyHunter.com hackevents; every body retrieved"
---

# FirstBlood Hackevent XSS Report Index

Index of the **207 XSS-typed reports** (106 "Stored XSS", 101 "Reflective XSS") disclosed
on [BugBountyHunter.com](https://www.bugbountyhunter.com/disclosed) across the three
FirstBlood hackevents (v1: May 2021, per the event write-up; v2 and v3 dates are not
stated on the pages read — v3 report bodies carry 2022 timestamps). Every report page
was retrieved in full; payloads, steps, and impact statements quoted in playbooks come
from these pages. Severity labels are as assigned by the BugBountyHunter triage.

Severity distribution of XSS reports: **17 CRITICAL · 92 High · 95 Medium · 2 Low · 1 Informative**.

Events: `firstblood` = FirstBlood v1 (May 2021) · `firstbloodv2` (dates not stated in the pages read) · `firstbloodv3` (report bodies timestamped 2022).

| FB | Event | Type | Severity | FirstBlood ID | Endpoint | Parameter | Title |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FB-17 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php?aptid=56914507` | `fname` | [Stored XSS on](https://www.bugbountyhunter.com/hackevents/report?id=17) |
| FB-51 | firstblood | Stored XSS | High | 10 | `/api/ba.php` | `fname & lname` | [Stored XSS at http://firstbloodhackers.com:49229/api/ba.php (POST) and aptid enumeration at /api/qa.php can be used to steal cookie](https://www.bugbountyhunter.com/hackevents/report?id=51) |
| FB-56 | firstblood | Stored XSS | High | 10 | `/book-appointment.html` | `fname` | [Stored XSS on /drpanel/drapi/query.php?aptid=&lt;ID&gt;](https://www.bugbountyhunter.com/hackevents/report?id=56) |
| FB-78 | firstblood | Stored XSS | CRITICAL | 8 | `/api/ma.php` | `message` | [[COLLAB] 1 Click XSS can lead to Admin Account Takeover](https://www.bugbountyhunter.com/hackevents/report?id=78) |
| FB-82 | firstblood | Stored XSS | CRITICAL | 8 | `/drpanel/cancelled.php` | `message` | [Stored XSS via canceled appointment message](https://www.bugbountyhunter.com/hackevents/report?id=82) |
| FB-83 | firstblood | Stored XSS | High | 8 | `-` | `Payload:` | [Leaking PII data of users who have appointments using stored XSS and IDOR](https://www.bugbountyhunter.com/hackevents/report?id=83) |
| FB-93 | firstblood | Reflective XSS | Medium | 4 | `/register.php` | `ref` | [XSS using ref Parameter](https://www.bugbountyhunter.com/hackevents/report?id=93) |
| FB-116 | firstblood | Reflective XSS | Medium | 4 | `/register.php` | `?ref` | [Reflective XSS at http://firstbloodhackers.com:49369/register.php](https://www.bugbountyhunter.com/hackevents/report?id=116) |
| FB-119 | firstblood | Reflective XSS | Medium | 14 | `http://firstbloodhackers.com:49394/login` | `?goto=` | [POST Based Reflected XSS on Login](https://www.bugbountyhunter.com/hackevents/report?id=119) |
| FB-120 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php` | `***` | [Stored XSS on /drpanel/drapi/query.php?aptid](https://www.bugbountyhunter.com/hackevents/report?id=120) |
| FB-121 | firstblood | Reflective XSS | Medium | 3 | `http://firstbloodhackers.com:49394/login` | `?ref=` | [Reflected XSS via Javascript Scheme](https://www.bugbountyhunter.com/hackevents/report?id=121) |
| FB-122 | firstblood | Reflective XSS | Medium | 2 | `http://firstbloodhackers.com:49394/login` | `?goto=` | [Reflected XSS](https://www.bugbountyhunter.com/hackevents/report?id=122) |
| FB-131 | firstblood | Reflective XSS | Medium | 3 | `/login.php` | `ref` | [Reflective XSS at http://firstbloodhackers.com:49421/login.php can be used to steal cookie](https://www.bugbountyhunter.com/hackevents/report?id=131) |
| FB-133 | firstblood | Stored XSS | CRITICAL | 8 | `-` | `Payload:` | [Stored XSS through the appointments cancelation message leading to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=133) |
| FB-149 | firstblood | Reflective XSS | Medium | 4 | `-` | `Payload:` | [Reflective XSS through the vulnerable ref header on /register.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=149) |
| FB-150 | firstblood | Reflective XSS | Medium | 3 | `/login.php` | `ref` | [Reflected xss on login.php](https://www.bugbountyhunter.com/hackevents/report?id=150) |
| FB-153 | firstblood | Reflective XSS | Medium | 16 | `/register.php` | `ref` | [Reflected XSS on register.php](https://www.bugbountyhunter.com/hackevents/report?id=153) |
| FB-154 | firstblood | Reflective XSS | Medium | 3 | `-` | `Payload:` | [Reflective XSS on /login.php endpoint through the vulnerable `ref` parameter](https://www.bugbountyhunter.com/hackevents/report?id=154) |
| FB-155 | firstblood | Reflective XSS | Medium | 4 | `/register.php` | `ref` | [Reflected xss on register.php](https://www.bugbountyhunter.com/hackevents/report?id=155) |
| FB-171 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php` | `fname, lname` | [Stored XSS payload allowed in names when making an appointment can leak admin cookie](https://www.bugbountyhunter.com/hackevents/report?id=171) |
| FB-185 | firstblood | Reflective XSS | High | 2 | `-` | `-` | [Reflected XSS on using the hidden &quot;goto&quot; parameter leads to Admin Account Takeover](https://www.bugbountyhunter.com/hackevents/report?id=185) |
| FB-189 | firstblood | Stored XSS | CRITICAL | 8 | `/api/ma.php` | `message=` | [Stored Cross site scripting](https://www.bugbountyhunter.com/hackevents/report?id=189) |
| FB-195 | firstblood | Stored XSS | High | 10 | `http://firstbloodhackers.com:49521/api/b` | `fname` | [Stored XSS on admin Side - Collaboration with Jomar](https://www.bugbountyhunter.com/hackevents/report?id=195) |
| FB-200 | firstblood | Stored XSS | High | 10 | `/drpanel/index.php` | `firstname and lastname` | [script inclusion leads to phishing,ato,monitoring of clicks of the user [sxss] and intresting vulnerablity](https://www.bugbountyhunter.com/hackevents/report?id=200) |
| FB-201 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php?aptid={ID}` | `fname, lname` | [Stored XSS on /drpanel/drapi/query.php](https://www.bugbountyhunter.com/hackevents/report?id=201) |
| FB-202 | firstblood | Stored XSS | CRITICAL | 8 | `/api/ma.php` | `message` | [sxss`leads to manything entire site manipulation](https://www.bugbountyhunter.com/hackevents/report?id=202) |
| FB-207 | firstblood | Stored XSS | High | 10 | `-` | `Payload:` | [Stored XSS on /drpanel/drapi/query.php endpoint leading to Admin Account Takeover](https://www.bugbountyhunter.com/hackevents/report?id=207) |
| FB-208 | firstblood | Stored XSS | CRITICAL | 8 | `/api/ma.php` | `message=` | [[COLLAB] Stored XSS on message param through appointment annulation allow admin ATO](https://www.bugbountyhunter.com/hackevents/report?id=208) |
| FB-209 | firstblood | Reflective XSS | Medium | - | `/login.php?goto` | `goto` | [rxss leads to ato accountakeover](https://www.bugbountyhunter.com/hackevents/report?id=209) |
| FB-210 | firstblood | Reflective XSS | Medium | 4 | `/register.php` | `ref` | [Reflective XSS on Register page leading to leak of PII data](https://www.bugbountyhunter.com/hackevents/report?id=210) |
| FB-211 | firstblood | Reflective XSS | Medium | 2 | `/login.php` | `goto` | [Reflected xss on login.php leads to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=211) |
| FB-212 | firstblood | Reflective XSS | Medium | 3 | `/login.php` | `ref` | [Reflective XSS on Login page (requiring interaction), leading to leak of PII data](https://www.bugbountyhunter.com/hackevents/report?id=212) |
| FB-219 | firstblood | Reflective XSS | Medium | 16 | `/register.php` | `?ref=` | [DOM XSS](https://www.bugbountyhunter.com/hackevents/report?id=219) |
| FB-231 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php?aptid={APTID}` | `fname, lname` | [Stored XSS on Admn API endpoint for querying Appointment](https://www.bugbountyhunter.com/hackevents/report?id=231) |
| FB-238 | firstblood | Stored XSS | High | 9 | `manageappointment.php` | `message` | [Stored XSS on /manageappointment.php using the message parameter leading to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=238) |
| FB-241 | firstblood | Stored XSS | High | 9 | `/api/ma.php` | `message` | [Stored XSS via malicious appointment message leads to ATO](https://www.bugbountyhunter.com/hackevents/report?id=241) |
| FB-242 | firstblood | Stored XSS | High | 9 | `/yourappointments.php` | `message` | [Stored XSS on yourappointments.php can lead to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=242) |
| FB-243 | firstblood | Stored XSS | High | 9 | `/api/ma.php` | `message` | [Stored XSS on cancelled.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=243) |
| FB-258 | firstblood | Reflective XSS | Medium | 3 | `/login.php` | `ref` | [Reflected XSS on /login.php using ref parameter](https://www.bugbountyhunter.com/hackevents/report?id=258) |
| FB-264 | firstblood | Reflective XSS | Medium | 3 | `/login.php` | `ref` | [Reflected XSS on login Page via ref paramater](https://www.bugbountyhunter.com/hackevents/report?id=264) |
| FB-267 | firstblood | Reflective XSS | Medium | 3 | `/login.php` | `ref` | [Reflected XSS via ref parameter on login](https://www.bugbountyhunter.com/hackevents/report?id=267) |
| FB-268 | firstblood | Reflective XSS | Medium | 4 | `/register.php` | `ref` | [Reflected XSS on register page](https://www.bugbountyhunter.com/hackevents/report?id=268) |
| FB-273 | firstblood | Reflective XSS | Medium | 2 | `/login.php` | `goto` | [Reflected XSS on /login.php using the GET paramter 'goto'](https://www.bugbountyhunter.com/hackevents/report?id=273) |
| FB-274 | firstblood | Reflective XSS | Low | 2 | `/login.php` | `goto` | [Open Redirect on /login.php via goto body parameter](https://www.bugbountyhunter.com/hackevents/report?id=274) |
| FB-282 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php?aptid=56911904` | `fname, lname` | [Stored XSS + stealing cookies through XSS hunter](https://www.bugbountyhunter.com/hackevents/report?id=282) |
| FB-284 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php?aptid={appointm` | `fname and lname` | [Cross Site Scripting vulnerability in client firstname/lastname](https://www.bugbountyhunter.com/hackevents/report?id=284) |
| FB-286 | firstblood | Stored XSS | High | 10 | `/drpanel/drapi/query.php?aptid=56911630p` | `lname & fname` | [Stored XSS on query.php via lname &amp; fname parameter](https://www.bugbountyhunter.com/hackevents/report?id=286) |
| FB-308 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [Reflective XSS on login.php via goto parameter](https://www.bugbountyhunter.com/hackevents/report?id=308) |
| FB-312 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php?ref=j%0d%0aava%0d%0as%0d%0` | `ref` | [[COLLAB with isitbug] XSS Bypassed](https://www.bugbountyhunter.com/hackevents/report?id=312) |
| FB-314 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflective XSS via ref parameter on register.php](https://www.bugbountyhunter.com/hackevents/report?id=314) |
| FB-317 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php This report contains multiple` | `-` | [[COLLAB with isitbug] Reflected XSS bypassed](https://www.bugbountyhunter.com/hackevents/report?id=317) |
| FB-335 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [XSS bypass on cancel report](https://www.bugbountyhunter.com/hackevents/report?id=335) |
| FB-336 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php` | `message` | [[COLLAB with isitbug] Reflected XSS via message on cancelled appointment](https://www.bugbountyhunter.com/hackevents/report?id=336) |
| FB-341 | firstbloodv2 | Reflective XSS | Medium | 19 | `/login.php` | `Referer header` | [Referer header reflection leads to Reflective XSS](https://www.bugbountyhunter.com/hackevents/report?id=341) |
| FB-343 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [Reflective XSS on login.php via goto parameter after successful login](https://www.bugbountyhunter.com/hackevents/report?id=343) |
| FB-346 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [rXSS at /register.php](https://www.bugbountyhunter.com/hackevents/report?id=346) |
| FB-349 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [register.php is still vulenerable to Reflective XSS](https://www.bugbountyhunter.com/hackevents/report?id=349) |
| FB-364 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [rXSS on login.php leads to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=364) |
| FB-366 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php` | `message` | [Stored XSS via message parameter on manageappointment.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=366) |
| FB-368 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflected XSS on register.php through the ref parameter [Bypass]](https://www.bugbountyhunter.com/hackevents/report?id=368) |
| FB-395 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php?success&aptid={id` | `msg=` | [Stored XSS found on /manageappointment.php?success&amp;aptid={id}](https://www.bugbountyhunter.com/hackevents/report?id=395) |
| FB-401 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php` | `message` | [Stored XSS on /manageappointment.php using the message parameter [Bypass]](https://www.bugbountyhunter.com/hackevents/report?id=401) |
| FB-403 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `?ref` | [Reflected XSS at Register.php](https://www.bugbountyhunter.com/hackevents/report?id=403) |
| FB-420 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [Reflective XSS on login.php](https://www.bugbountyhunter.com/hackevents/report?id=420) |
| FB-423 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [Stored XSS on the /manageappointment.php endpoint when canceling an appointment](https://www.bugbountyhunter.com/hackevents/report?id=423) |
| FB-425 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [Stored XSS in cancelled appointments message functionality](https://www.bugbountyhunter.com/hackevents/report?id=425) |
| FB-427 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php?goto={payload}` | `goto=` | [Reflective XSS at /login.php](https://www.bugbountyhunter.com/hackevents/report?id=427) |
| FB-430 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflective xss on register.php with user interaction](https://www.bugbountyhunter.com/hackevents/report?id=430) |
| FB-432 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [Open Redirect on login page with &quot;goto&quot; parameter leading to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=432) |
| FB-441 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [Reflected XSS on the /login.php endpoint with the goto vulnerable parameter](https://www.bugbountyhunter.com/hackevents/report?id=441) |
| FB-443 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [goto parameter is still vulnerable to Reflective XSS](https://www.bugbountyhunter.com/hackevents/report?id=443) |
| FB-446 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflected XSS on the /register.php endpoint with the ref vulnerable parameter](https://www.bugbountyhunter.com/hackevents/report?id=446) |
| FB-453 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php?action=login&ref=ja%09vasc` | `ref=` | [[unpatched]Reflective XSS on /login.php?action=login&amp;ref={payload}](https://www.bugbountyhunter.com/hackevents/report?id=453) |
| FB-454 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `?goto` | [[COLLAB] Reflected XSS via login endpoint](https://www.bugbountyhunter.com/hackevents/report?id=454) |
| FB-455 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `?goto` | [Reflected XSS at Login.php](https://www.bugbountyhunter.com/hackevents/report?id=455) |
| FB-456 | firstbloodv2 | Stored XSS | High | 22 | `/drpanel/cancelled.php` | `message` | [[COLLAB with isitbug] Stored XSS via cancelled appointment's message that executes on doctors](https://www.bugbountyhunter.com/hackevents/report?id=456) |
| FB-461 | firstbloodv2 | Reflective XSS | Medium | 32 | `register.php` | `ref` | [Reflected XSS on register.php with ref parameter, leaking cookies (requires interaction)](https://www.bugbountyhunter.com/hackevents/report?id=461) |
| FB-463 | firstbloodv2 | Stored XSS | High | 22 | `/drpanel/cancelled.php` | `message` | [Cancelled Appintments is still vulnerable to Stored XSS](https://www.bugbountyhunter.com/hackevents/report?id=463) |
| FB-465 | firstbloodv2 | Reflective XSS | Medium | 26 | `login.php` | `goto` | [Reflected XSS on /login.php through the &quot;goto&quot; parameter leading to ATO](https://www.bugbountyhunter.com/hackevents/report?id=465) |
| FB-477 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [Reflected XSS on /login.php via goto parameter leads to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=477) |
| FB-478 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [Reflective xss vis 'goto=' parmater on login.php](https://www.bugbountyhunter.com/hackevents/report?id=478) |
| FB-479 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [Reflected XSS on /login.php using &quot;goto&quot; parameter and javascript scheme](https://www.bugbountyhunter.com/hackevents/report?id=479) |
| FB-490 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [parameter &quot;ref&quot; at endpoint /register.php is vulnerable to reflected XSS.](https://www.bugbountyhunter.com/hackevents/report?id=490) |
| FB-492 | firstbloodv2 | Stored XSS | High | 22 | `/drpanel/cancelled.php` | `message` | [Stored XSS through the appointments cancelation message leads to ATO](https://www.bugbountyhunter.com/hackevents/report?id=492) |
| FB-498 | firstbloodv2 | Stored XSS | High | 22 | `/drpanel/cancelled.php` | `message` | [Stored XSS on /drpanel/cancelled.php can lead to admin account takeover](https://www.bugbountyhunter.com/hackevents/report?id=498) |
| FB-523 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [POST-based rXSS on login.php](https://www.bugbountyhunter.com/hackevents/report?id=523) |
| FB-527 | firstbloodv2 | Stored XSS | High | 22 | `/api/ba.php` | `POST /api/ba.php HTTP/1.1` | [Stored XSS on /manageappointment.php](https://www.bugbountyhunter.com/hackevents/report?id=527) |
| FB-533 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [Stored XSS on /cancelled.php](https://www.bugbountyhunter.com/hackevents/report?id=533) |
| FB-538 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php` | `message` | [Modify Appointment Form is vulnerable to Stored XSS](https://www.bugbountyhunter.com/hackevents/report?id=538) |
| FB-544 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflected XSS on /register.php using ref parameter](https://www.bugbountyhunter.com/hackevents/report?id=544) |
| FB-550 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [goto paramerter at /login.php vulnerable to reflective xss.](https://www.bugbountyhunter.com/hackevents/report?id=550) |
| FB-559 | firstbloodv2 | Reflective XSS | Medium | 19 | `-` | `Payload:` | [XSS on internet explorer in the login page using the referer header](https://www.bugbountyhunter.com/hackevents/report?id=559) |
| FB-560 | firstbloodv2 | Stored XSS | High | 22 | `reflection: /drpanel/cancelled.php      ` | `message=` | [Stored xss leads to doctor / admin account takeover](https://www.bugbountyhunter.com/hackevents/report?id=560) |
| FB-563 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [DOM Based XSS via redirection to javascript uri](https://www.bugbountyhunter.com/hackevents/report?id=563) |
| FB-565 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflected XSS inside ref parameter on /register.php](https://www.bugbountyhunter.com/hackevents/report?id=565) |
| FB-579 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [Reflective XSS on /login.php?goto=](https://www.bugbountyhunter.com/hackevents/report?id=579) |
| FB-583 | firstbloodv2 | Reflective XSS | Medium | 19 | `/login.php` | `Referer:` | [Reflective XSS via Referer on login.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=583) |
| FB-596 | firstbloodv2 | Reflective XSS | Medium | 19 | `/login.php` | `href` | [IE-only Reflected XSS](https://www.bugbountyhunter.com/hackevents/report?id=596) |
| FB-607 | firstbloodv2 | Reflective XSS | Medium | 39 | `/drpanel/drapi/editpassword.php` | `goto` | [DOM-based XSS on /login.php via the goto parameter](https://www.bugbountyhunter.com/hackevents/report?id=607) |
| FB-609 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [Open redirect on /login.php via the goto parameter](https://www.bugbountyhunter.com/hackevents/report?id=609) |
| FB-610 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/pub/submit-vaccinat` | `user-agent` | [Stored XSS through the file upload and unsanitized User-Agent](https://www.bugbountyhunter.com/hackevents/report?id=610) |
| FB-613 | firstbloodv2 | Reflective XSS | High | 39 | `-` | `-` | [[COLLAB] Can register as a doctor and steal token upon login.](https://www.bugbountyhunter.com/hackevents/report?id=613) |
| FB-615 | firstbloodv2 | Reflective XSS | High | 39 | `-` | `-` | [A chain of two open redirects to leak some users token](https://www.bugbountyhunter.com/hackevents/report?id=615) |
| FB-617 | firstbloodv2 | Reflective XSS | Medium | 32 | `register.php` | `?ref=` | [[COLLAB] DOM XSS on register patch bypass](https://www.bugbountyhunter.com/hackevents/report?id=617) |
| FB-624 | firstbloodv2 | Reflective XSS | Medium | 32 | `register.php` | `ref=` | [Reflected XSS in register.php page](https://www.bugbountyhunter.com/hackevents/report?id=624) |
| FB-628 | firstbloodv2 | Reflective XSS | Medium | 39 | `login.php` | `goto` | [Reflected XSS on Login.php goto parameter](https://www.bugbountyhunter.com/hackevents/report?id=628) |
| FB-637 | firstbloodv2 | Reflective XSS | Medium | 19 | `-` | `Payload:` | [Referer Based XSS on /login.php endpoint leading to ATO](https://www.bugbountyhunter.com/hackevents/report?id=637) |
| FB-638 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [stored xss in message left at the time of cancelation of appointment.](https://www.bugbountyhunter.com/hackevents/report?id=638) |
| FB-646 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php` | `message=` | [[COLLAB] Stored XSS on Cancel appointment which leads to ATO](https://www.bugbountyhunter.com/hackevents/report?id=646) |
| FB-650 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [Stored XSS when cancelling an appointement triggered in doctor panel](https://www.bugbountyhunter.com/hackevents/report?id=650) |
| FB-666 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php?success&aptid=3a0` | `message=` | [Stored xss by meesage field on MANAGE APPOINTMENT](https://www.bugbountyhunter.com/hackevents/report?id=666) |
| FB-673 | firstbloodv2 | Stored XSS | High | 22 | `source=/api/ma.php,sink=/drpanel/cancell` | `message=` | [[Unpatched] Stored XSS still working on admin's cancelled report panel](https://www.bugbountyhunter.com/hackevents/report?id=673) |
| FB-674 | firstbloodv2 | Stored XSS | High | 22 | `/drpanel/cancelled.php` | `message=` | [0 click admin account takeover via stored xss on admin dashboard through cancel appointment.](https://www.bugbountyhunter.com/hackevents/report?id=674) |
| FB-678 | firstbloodv2 | Stored XSS | High | 29 | `vaccination-manager/portal.php` | `User-Agent` | [Stored XSS on vaccination-manager/portal.php](https://www.bugbountyhunter.com/hackevents/report?id=678) |
| FB-680 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `?ref=` | [Reflected xss bypass on register.php with ref paramter](https://www.bugbountyhunter.com/hackevents/report?id=680) |
| FB-682 | firstbloodv2 | Stored XSS | Low | 41 | `/drpanel/index.php#` | `DOB` | [Stored XSS through DOB](https://www.bugbountyhunter.com/hackevents/report?id=682) |
| FB-691 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/portal.php` | `N/A` | [XSS on /vaccination-manager/portal.php through User-agent pollution](https://www.bugbountyhunter.com/hackevents/report?id=691) |
| FB-694 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/portal.php` | `User-Agent header` | [[COLLAB]Vaccination Management portal is vulnerable to Stored XSS](https://www.bugbountyhunter.com/hackevents/report?id=694) |
| FB-700 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/pub/submit-vaccinat` | `User-Agent header` | [Stored XSS on /vaccination-manager/portal.php](https://www.bugbountyhunter.com/hackevents/report?id=700) |
| FB-703 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflective XSS on register page](https://www.bugbountyhunter.com/hackevents/report?id=703) |
| FB-722 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/pub/submit-vaccinat` | `User-Agent` | [Stored can be gained by giving payload in User-Agent Request header . It's fired on /vaccination-manager/portal.php.](https://www.bugbountyhunter.com/hackevents/report?id=722) |
| FB-726 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/portal.php` | `User-Agent header` | [[COLLAB with isitbug] Blind XSS through User-Agent header on Vaccination Management portal affecting admins](https://www.bugbountyhunter.com/hackevents/report?id=726) |
| FB-737 | firstbloodv2 | Reflective XSS | High | 26 | `/login.php This report contains multiple` | `-` | [XSS through hidden `goto` parameter on `/login.php`](https://www.bugbountyhunter.com/hackevents/report?id=737) |
| FB-738 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflected XSS on /register.php via the ref parameter](https://www.bugbountyhunter.com/hackevents/report?id=738) |
| FB-751 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [XSS on login page](https://www.bugbountyhunter.com/hackevents/report?id=751) |
| FB-759 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `?ref=` | [Reflected XSS on register.php leads to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=759) |
| FB-762 | firstbloodv2 | Stored XSS | High | 29 | `useragent` | `useragent` | [XSS in vaccine portal](https://www.bugbountyhunter.com/hackevents/report?id=762) |
| FB-781 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `?goto=` | [The parameter &quot;goto&quot; is vulnerable to XSS on login.php.](https://www.bugbountyhunter.com/hackevents/report?id=781) |
| FB-784 | firstbloodv2 | Stored XSS | High | 22 | `/api/ba.php` | `msg` | [Stored XSS at /book-appointment.php](https://www.bugbountyhunter.com/hackevents/report?id=784) |
| FB-786 | firstbloodv2 | Stored XSS | High | 22 | `/manage-appointment.php` | `msg` | [Stored XSS Leads to Admin Account Takeover](https://www.bugbountyhunter.com/hackevents/report?id=786) |
| FB-787 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/portal.php` | `User-Agent header` | [Stored XSS on Vaccination Manager Portal through User Agent](https://www.bugbountyhunter.com/hackevents/report?id=787) |
| FB-789 | firstbloodv2 | Reflective XSS | Medium | 32 | `/register.php` | `ref` | [Reflective XSS at /register.php](https://www.bugbountyhunter.com/hackevents/report?id=789) |
| FB-791 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `goto` | [Reflective XSS on Login page using the hidden &quot;goto&quot; parameter](https://www.bugbountyhunter.com/hackevents/report?id=791) |
| FB-792 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login` | `goto` | [Reflective XSS at /login.php due to goto](https://www.bugbountyhunter.com/hackevents/report?id=792) |
| FB-794 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/portal.php` | `User-Agent` | [Stored XSS via User-Agent header value in /vaccination-manager/portal.php](https://www.bugbountyhunter.com/hackevents/report?id=794) |
| FB-807 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [Stored XSS on /drpanel/index.php by cancelling an appointment](https://www.bugbountyhunter.com/hackevents/report?id=807) |
| FB-811 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php` | `message` | [Stored XSS on /manageappointment.php can lead to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=811) |
| FB-812 | firstbloodv2 | Stored XSS | High | 22 | `/drpanel/cancelled.php` | `message` | [Stored XSS on cancelled appointment can leak admin cookies](https://www.bugbountyhunter.com/hackevents/report?id=812) |
| FB-823 | firstbloodv2 | Reflective XSS | Medium | 19 | `/login.php` | `Referer` | [Reflected XSS using Referer header on /login.php](https://www.bugbountyhunter.com/hackevents/report?id=823) |
| FB-834 | firstbloodv2 | Stored XSS | High | 22 | `/manageappointment.php?success&aptid=360` | `message` | [Cancel Stored XSS at the reservation function](https://www.bugbountyhunter.com/hackevents/report?id=834) |
| FB-842 | firstbloodv2 | Reflective XSS | Informative | - | `/login/php` | `goto` | [Open Redirect on login.php with goto parameter](https://www.bugbountyhunter.com/hackevents/report?id=842) |
| FB-843 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [Stored XSS via cancel appointment functionality](https://www.bugbountyhunter.com/hackevents/report?id=843) |
| FB-848 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message=` | [Stored XSS in cancelled appointment message](https://www.bugbountyhunter.com/hackevents/report?id=848) |
| FB-849 | firstbloodv2 | Stored XSS | High | 22 | `manageappointment.php` | `message` | [stored XSS in manageappointment.php](https://www.bugbountyhunter.com/hackevents/report?id=849) |
| FB-854 | firstbloodv2 | Stored XSS | High | 22 | `drpanel/cancelled.php` | `message left from patient` | [stored XSS in cancelled appointment](https://www.bugbountyhunter.com/hackevents/report?id=854) |
| FB-862 | firstbloodv2 | Stored XSS | High | 22 | `/api/ma.php` | `message` | [Stored XSS on cancelled appointmnent message](https://www.bugbountyhunter.com/hackevents/report?id=862) |
| FB-864 | firstbloodv2 | Stored XSS | High | 29 | `-` | `Payload:` | [[COLLAB] Stored/Blind XSS / DOS via vaccination portal](https://www.bugbountyhunter.com/hackevents/report?id=864) |
| FB-865 | firstbloodv2 | Stored XSS | High | 22 | `/drpanel/cancelled.php` | `message` | [Stored XSS on Cancel Appointment Message.](https://www.bugbountyhunter.com/hackevents/report?id=865) |
| FB-869 | firstbloodv2 | Reflective XSS | Medium | 19 | `/login.php` | `Referer header` | [Reflected XSS on login.php using Referer header](https://www.bugbountyhunter.com/hackevents/report?id=869) |
| FB-892 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `?goto=` | [Reflected XSS on the login form in the goto parameter](https://www.bugbountyhunter.com/hackevents/report?id=892) |
| FB-900 | firstbloodv2 | Reflective XSS | Medium | 39 | `/login.php` | `goto` | [Open redirect via goto parameter on /login.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=900) |
| FB-912 | firstbloodv2 | Stored XSS | High | 22 | `/book-appointment.php` | `message` | [DOM xss found on management portal](https://www.bugbountyhunter.com/hackevents/report?id=912) |
| FB-917 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/pub/submit-vaccinat` | `User Agent` | [The User Agent parameter is vulnerable to XSS in the vaccination-manager portal.](https://www.bugbountyhunter.com/hackevents/report?id=917) |
| FB-926 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `?goto` | [Reflective xss on login.php by goto paramter](https://www.bugbountyhunter.com/hackevents/report?id=926) |
| FB-927 | firstbloodv2 | Reflective XSS | Medium | 26 | `/login.php` | `?goto` | [Reflected XSS at /login.php using goto patameter leads to Account Takeover](https://www.bugbountyhunter.com/hackevents/report?id=927) |
| FB-947 | firstbloodv2 | Stored XSS | High | 29 | `/vaccination-manager/portal.php` | `User-Agent header` | [[COLLAB]Vaccination Management portal is vulnerable to Stored XSS](https://www.bugbountyhunter.com/hackevents/report?id=947) |
| FB-1020 | firstbloodv3 | Stored XSS | CRITICAL | 59 | `/api/hackerback.php` | `phone` | [Stored XSS on drpanel](https://www.bugbountyhunter.com/hackevents/report?id=1020) |
| FB-1049 | firstbloodv3 | Reflective XSS | Medium | 46 | `/book-appointment.html` | `return_url` | [Reflective XSS in appointment feature](https://www.bugbountyhunter.com/hackevents/report?id=1049) |
| FB-1102 | firstbloodv3 | Reflective XSS | Medium | 45 | `/about.html` | `redirect_url` | [DOM-based XSS on /about.html can lead to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=1102) |
| FB-1116 | firstbloodv3 | Reflective XSS | Medium | 63 | `/drpanel/edit-doctor.php` | `id` | [Reflected XSS on /edit-doctor.php](https://www.bugbountyhunter.com/hackevents/report?id=1116) |
| FB-1126 | firstbloodv3 | Reflective XSS | Medium | 46 | `/book-appointment.html` | `redirect_url` | [DOM-based XSS on /book-appointment.html can lead to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=1126) |
| FB-1127 | firstbloodv3 | Reflective XSS | Medium | 47 | `/doctors.php` | `doctor` | [Reflected XSS](https://www.bugbountyhunter.com/hackevents/report?id=1127) |
| FB-1135 | firstbloodv3 | Reflective XSS | Medium | 45 | `/about.html` | `return_url` | [Reflected XSS at about.html](https://www.bugbountyhunter.com/hackevents/report?id=1135) |
| FB-1138 | firstbloodv3 | Reflective XSS | Medium | 47 | `/doctors.php` | `doctor` | [Reflected XSS on /doctors.php](https://www.bugbountyhunter.com/hackevents/report?id=1138) |
| FB-1145 | firstbloodv3 | Reflective XSS | Medium | 47 | `doctors.php` | `doctor` | [Refelcted XSS at doctors.php](https://www.bugbountyhunter.com/hackevents/report?id=1145) |
| FB-1146 | firstbloodv3 | Reflective XSS | Medium | 47 | `/doctors.php` | `doctor` | [Reflected XSS on https://a939f6568e92-mrxhunt.a.firstbloodhackers.com/doctors.php](https://www.bugbountyhunter.com/hackevents/report?id=1146) |
| FB-1186 | firstbloodv3 | Stored XSS | High | 53 | `/api/ambulances.php` | `fname` | [Stored XSS on ambulance API](https://www.bugbountyhunter.com/hackevents/report?id=1186) |
| FB-1191 | firstbloodv3 | Stored XSS | CRITICAL | 59 | `/drpanel/index.php` | `phone` | [Stored XSS in Mobile no. of Hackerback Joinee](https://www.bugbountyhunter.com/hackevents/report?id=1191) |
| FB-1201 | firstbloodv3 | Reflective XSS | Medium | 47 | `/doctors.php` | `doctor` | [Reflected xss on doctors.php](https://www.bugbountyhunter.com/hackevents/report?id=1201) |
| FB-1236 | firstbloodv3 | Stored XSS | High | 53 | `/api/ambulances.php` | `name` | [Unauthenticated Stored XSS on ambulances.php can lead to account takeover (of doctors)](https://www.bugbountyhunter.com/hackevents/report?id=1236) |
| FB-1254 | firstbloodv3 | Stored XSS | High | 64 | `/meet_drs.php` | `photoUrl` | [Stored XSS through Doctors photo URL pn endpoint meet_drs.php](https://www.bugbountyhunter.com/hackevents/report?id=1254) |
| FB-1265 | firstbloodv3 | Reflective XSS | Medium | 63 | `/drpanel/edit-doctor.php` | `id` | [Reflected XSS at id parameter](https://www.bugbountyhunter.com/hackevents/report?id=1265) |
| FB-1268 | firstbloodv3 | Stored XSS | High | 54 | `/meet_drs.php` | `name` | [Stored XSS at meet_drs.pho](https://www.bugbountyhunter.com/hackevents/report?id=1268) |
| FB-1283 | firstbloodv3 | Reflective XSS | Medium | 46 | `/book-appointment.html` | `redirect_url` | [Reflected XSS on /book-appointment.html endpoint in the `redirect_url` parameter](https://www.bugbountyhunter.com/hackevents/report?id=1283) |
| FB-1289 | firstbloodv3 | Reflective XSS | Medium | 63 | `/drpanel/edit-doctor.php` | `id` | [Reflected XSS on /drpanel/edit-doctor.php endpoint in the `id` parameter](https://www.bugbountyhunter.com/hackevents/report?id=1289) |
| FB-1298 | firstbloodv3 | Stored XSS | High | 53 | `/api/ba.php & /api/ambulances.php` | `hello">document.location=` | [Enable Ambulance Service for the Appointment leading to Stored XSS](https://www.bugbountyhunter.com/hackevents/report?id=1298) |
| FB-1310 | firstbloodv3 | Stored XSS | CRITICAL | 72 | `/login.php` | `username/password` | [Blind XSS on login page disclosing admin panel access](https://www.bugbountyhunter.com/hackevents/report?id=1310) |
| FB-1320 | firstbloodv3 | Stored XSS | CRITICAL | 72 | `/login.php` | `username` | [Blind XSS in username field](https://www.bugbountyhunter.com/hackevents/report?id=1320) |
| FB-1335 | firstbloodv3 | Stored XSS | CRITICAL | 59 | `/api/hackerback.php` | `phone` | [Stored XSS to account takeover of doctors](https://www.bugbountyhunter.com/hackevents/report?id=1335) |
| FB-1377 | firstbloodv3 | Stored XSS | CRITICAL | 59 | `/api/hackerback.php` | `phone` | [Stored XSS on drpanel after joining hackerback can lead to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=1377) |
| FB-1379 | firstbloodv3 | Stored XSS | High | 54 | `https://019046743f9e-pichik.a.firstblood` | `name` | [ATO with stored XSS in doctor name](https://www.bugbountyhunter.com/hackevents/report?id=1379) |
| FB-1386 | firstbloodv3 | Stored XSS | High | 57 | `/manageappointment.php` | `name` | [Stored XSS on manageappointment.php after selecting a doctor](https://www.bugbountyhunter.com/hackevents/report?id=1386) |
| FB-1389 | firstbloodv3 | Stored XSS | High | 54 | `/meet_drs.php` | `name` | [Stored XSS on /meet_drs.php due to unfiltered doctor's name](https://www.bugbountyhunter.com/hackevents/report?id=1389) |
| FB-1396 | firstbloodv3 | Stored XSS | High | 55 | `/doctors.php` | `name` | [Stored XSS on doctors.php](https://www.bugbountyhunter.com/hackevents/report?id=1396) |
| FB-1402 | firstbloodv3 | Reflective XSS | Medium | 63 | `/drpanel/edit-doctor.php` | `id` | [2nd Reflected XSS on edit-doctor.php (different injection point + payload)](https://www.bugbountyhunter.com/hackevents/report?id=1402) |
| FB-1446 | firstbloodv3 | Stored XSS | High | 64 | `/drpanel/drapi/edit-dr.php` | `photoUrl` | [[COLLAB] Able to update profile picture of doctor](https://www.bugbountyhunter.com/hackevents/report?id=1446) |
| FB-1453 | firstbloodv3 | Stored XSS | High | 64 | `/drpanel/drapi/edit-dr.php` | `photoUrl` | [Change Docto's image](https://www.bugbountyhunter.com/hackevents/report?id=1453) |
| FB-1456 | firstbloodv3 | Stored XSS | High | 64 | `/drpanel/drapi/edit-dr.php` | `photoUrl` | [Stored XSS on /meet_drs.php can lead to full account takeover](https://www.bugbountyhunter.com/hackevents/report?id=1456) |
| FB-1462 | firstbloodv3 | Stored XSS | High | 65 | `/drpanel/drapi/edit-dr.php` | `photoUrl` | [Storred XSS with photo in /about endpoint](https://www.bugbountyhunter.com/hackevents/report?id=1462) |
| FB-1498 | firstbloodv3 | Reflective XSS | Medium | 45 | `/about.html` | `redirect_url` | [redirect_url vulnerable to XSS and Open redirect](https://www.bugbountyhunter.com/hackevents/report?id=1498) |
| FB-1517 | firstbloodv3 | Reflective XSS | Medium | 63 | `/drpanel/edit-doctor.php` | `id` | [Reflected xss on edit-doctor.php](https://www.bugbountyhunter.com/hackevents/report?id=1517) |
| FB-1544 | firstbloodv3 | Stored XSS | High | 70 | `/meet_drs.php` | `xx"><svg onload=alert(docume` | [[Collab] Tagline XSS on /meet_drs.php](https://www.bugbountyhunter.com/hackevents/report?id=1544) |
| FB-1548 | firstbloodv3 | Stored XSS | High | 73 | `/api/manageambulances.php` | `Method` | [Anyone can edit ambulances](https://www.bugbountyhunter.com/hackevents/report?id=1548) |
| FB-1552 | firstbloodv3 | Stored XSS | High | 76 | `/api/manageambulances.php` | `driver` | [Stored XSS in ambulance driver](https://www.bugbountyhunter.com/hackevents/report?id=1552) |
| FB-1555 | firstbloodv3 | Stored XSS | High | 70 | `/drpanel/drapi/edit-dr.php` | `tagline` | [Stored XSS through doctor tagline on meet_drs.php](https://www.bugbountyhunter.com/hackevents/report?id=1555) |
| FB-1559 | firstbloodv3 | Stored XSS | CRITICAL | 72 | `/login_attempts.php?id=118125` | `username` | [Blind Stored XSS on admin panel can lead to SSRF](https://www.bugbountyhunter.com/hackevents/report?id=1559) |
| FB-1571 | firstbloodv3 | Stored XSS | CRITICAL | 72 | `/login_attempts.php` | `username` | [Blind XSS on Internal Adminstrator dashboard](https://www.bugbountyhunter.com/hackevents/report?id=1571) |
| FB-1576 | firstbloodv3 | Stored XSS | High | 56 | `/about.php` | `name` | [Stored XSS on about.php's doctor of the month field](https://www.bugbountyhunter.com/hackevents/report?id=1576) |
| FB-1577 | firstbloodv3 | Stored XSS | High | 65 | `/drpanel/drapi/edit-dr.php` | `drid=3&photoUrl` | [Stored XSS on about.php through doctor of the profile photo](https://www.bugbountyhunter.com/hackevents/report?id=1577) |
| FB-1589 | firstbloodv3 | Stored XSS | High | 53 | `/api/ambulances.php?select={ID}` | `fname and lname` | [Stored xss on api/ambulances.php](https://www.bugbountyhunter.com/hackevents/report?id=1589) |
| FB-1608 | firstbloodv3 | Stored XSS | CRITICAL | 78 | `/manage_appointment.php` | `fname` | [Blind XSS on Internal Dashboard of Adminstrator (Manage Appointments)](https://www.bugbountyhunter.com/hackevents/report?id=1608) |
| FB-1613 | firstbloodv3 | Stored XSS | CRITICAL | 59 | `/api/hackerback.php` | `phone` | [Stored XSS leading to account takeover in admin user's dashboard via signing up for hackerback](https://www.bugbountyhunter.com/hackevents/report?id=1613) |
| FB-1640 | firstbloodv3 | Stored XSS | High | 76 | `/api/manageambulances.php` | `driver` | [Unauthenticated Access to Api Call leads to Stored XSS in the Drivers Name](https://www.bugbountyhunter.com/hackevents/report?id=1640) |
| FB-1651 | firstbloodv3 | Stored XSS | High | 70 | `/meet_drs.php` | `tagline` | [Stored xss in doctors tagline](https://www.bugbountyhunter.com/hackevents/report?id=1651) |
| FB-1716 | firstbloodv3 | Reflective XSS | Medium | 47 | `/doctors.php` | `doctor` | [DOM XSS on doctors.php via doctor parameter](https://www.bugbountyhunter.com/hackevents/report?id=1716) |
| FB-1729 | firstbloodv3 | Stored XSS | CRITICAL | 78 | `/api/ba.php` | `lname,fname` | [Blind XSS in appointments](https://www.bugbountyhunter.com/hackevents/report?id=1729) |
| FB-1772 | firstbloodv3 | Stored XSS | High | 53 | `/api/ambulances.php` | `select` | [Stored XSS on ambulances.php](https://www.bugbountyhunter.com/hackevents/report?id=1772) |

Total: **207** reports. Bodies with full submitted text: **207** (all pages fetched).

## Payload family distribution (declared payload field)

Automatically grouped from the `Payload:` declarations (tiered — a payload matching
`javascript:` groups there before `<script>`, etc.): event-handler-only `114`,
`<script>` tags `23`, `javascript:` URIs `18`, autofocus/event-handler-composite `17`,
`<svg>` `7`, `<img>` `2`, `<iframe>` `2`, other `2`, not declared `22`.

## Related files

- [`../Filter-Bypass-and-Encoding.md`](../Filter-Bypass-and-Encoding.md) — FB-082, FB-189, FB-131, FB-150 case studies; BBH-001 methodology (filter-decision flow, WAF tips)
- [`../Stored-XSS.md`](../Stored-XSS.md) — FB-078, FB-610/678, FB-1310, FB-1559 case studies
- [`../DOM-Based-XSS.md`](../DOM-Based-XSS.md) — FB-219; BBH-002 JS-file sink keywords
- [`../Reflected-XSS.md`](../Reflected-XSS.md) — FB-150 chain; BBH-001 reflection-discovery flow
- [`../XSS-Testing-Agent-Playbook.md`](../XSS-Testing-Agent-Playbook.md) — logged-metadata contexts (C13/C14) sourced from this corpus

## Non-XSS disclosed reports in the same hackevents (355)

Metadata preserved from the event listing pages (no bodies fetched for these; they
are future inputs for other bug-class playbooks, e.g. the IDOR vault). Type labels
are as shown on the listing pages. "Multiple types" rows mix classes.

| FB | Event | Type | Severity | Title |
| --- | --- | --- | --- | --- |
| FB-5 | firstblood | Server misconfiguration | Informative | [FirstBlood runs on http](https://www.bugbountyhunter.com/hackevents/report?id=5) |
| FB-7 | firstblood | Authorisation Issue | CRITICAL | [PII leak via /drpanel/drapi/qp.php?name=sanjay](https://www.bugbountyhunter.com/hackevents/report?id=7) |
| FB-10 | firstblood | Insecure direct object reference | High | [Viewing/Cancelling anyone's appointment](https://www.bugbountyhunter.com/hackevents/report?id=10) |
| FB-12 | firstblood | Insecure direct object reference | High | [IDOR on /api/qa.php](https://www.bugbountyhunter.com/hackevents/report?id=12) |
| FB-14 | firstblood | Application/Business Logic | High | [The patient email can be changed even though the application UI mentioned that this is not allowed.](https://www.bugbountyhunter.com/hackevents/report?id=14) |
| FB-15 | firstblood | Open Redirect | Low | [Open Url redirection](https://www.bugbountyhunter.com/hackevents/report?id=15) |
| FB-16 | firstblood | Insecure direct object reference | High | [Editing other users appointments with IDOR](https://www.bugbountyhunter.com/hackevents/report?id=16) |
| FB-18 | firstblood | Info leak | CRITICAL | [Users information disclosure via /attendees/event.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=18) |
| FB-20 | firstblood | Application/Business Logic | CRITICAL | [Enumerating PII.](https://www.bugbountyhunter.com/hackevents/report?id=20) |
| FB-21 | firstblood | Application/Business Logic | CRITICAL | [Newly created Doctor account was able to search for patient info via the query api](https://www.bugbountyhunter.com/hackevents/report?id=21) |
| FB-22 | firstblood | Open Redirect | Low | [OpenRedirect on Secure Logout](https://www.bugbountyhunter.com/hackevents/report?id=22) |
| FB-25 | firstblood | Authorisation Issue | High | [Invite Code leaking on Reddit](https://www.bugbountyhunter.com/hackevents/report?id=25) |
| FB-28 | firstblood | Info leak | CRITICAL | [/attendees/event.php authoriation bypass using X-SITE-REQ: permitted](https://www.bugbountyhunter.com/hackevents/report?id=28) |
| FB-32 | firstblood | Authorisation Issue | High | [Multiple Register on same Username](https://www.bugbountyhunter.com/hackevents/report?id=32) |
| FB-41 | firstblood | Open Redirect | Low | [Open URL Redirect on /drpanel/logout.php](https://www.bugbountyhunter.com/hackevents/report?id=41) |
| FB-43 | firstblood | Authorisation Issue | High | [Doctor Registration code misconfiguration](https://www.bugbountyhunter.com/hackevents/report?id=43) |
| FB-44 | firstblood | Insecure direct object reference | High | [Leakage of P2 information of users who have taken appointment](https://www.bugbountyhunter.com/hackevents/report?id=44) |
| FB-47 | firstblood | Open Redirect | Low | [Open redirect on the logout.php endpoint [COLLAB]](https://www.bugbountyhunter.com/hackevents/report?id=47) |
| FB-48 | firstblood | Application/Business Logic | High | [[IDOR] Modifying anyone's Appointment information](https://www.bugbountyhunter.com/hackevents/report?id=48) |
| FB-49 | firstblood | Authorisation Issue | CRITICAL | [New Account Patient Information restriction bypass](https://www.bugbountyhunter.com/hackevents/report?id=49) |
| FB-50 | firstblood | Authorisation Issue | High | [account takeover via re-register with the same username](https://www.bugbountyhunter.com/hackevents/report?id=50) |
| FB-53 | firstblood | Authorisation Issue | CRITICAL | [Un-Authorized users can access &quot;/drpanel/drapi/qp.php&quot; endpoint and access users PII [COLLAB]](https://www.bugbountyhunter.com/hackevents/report?id=53) |
| FB-58 | firstblood | Insecure direct object reference | High | [aptid enumeration via http://firstbloodhackers.com:49276/api/qa.php can be used to leak Appointment data](https://www.bugbountyhunter.com/hackevents/report?id=58) |
| FB-63 | firstblood | Open Redirect | Low | [Open redirect on logout](https://www.bugbountyhunter.com/hackevents/report?id=63) |
| FB-64 | firstblood | Application/Business Logic | High | [Modification of the appointement's data  - Collaboration with Jomar](https://www.bugbountyhunter.com/hackevents/report?id=64) |
| FB-65 | firstblood | Application/Business Logic | High | [doctorAuthed cookie given at /register.php can be used to modify patient email at Appointment Form /manageappointment.php](https://www.bugbountyhunter.com/hackevents/report?id=65) |
| FB-67 | firstblood | Insecure direct object reference | High | [Leak arbitrary users appointment details   Manage/delete them](https://www.bugbountyhunter.com/hackevents/report?id=67) |
| FB-70 | firstblood | Info leak | CRITICAL | [Info leak at http://firstbloodhackers.com:49280/attendees/event.php?q=560720](https://www.bugbountyhunter.com/hackevents/report?id=70) |
| FB-71 | firstblood | Authorisation Issue | High | [Invite Code Leaked on Reddit leading to broken Authorisation](https://www.bugbountyhunter.com/hackevents/report?id=71) |
| FB-72 | firstblood | Insecure direct object reference | High | [I can see &amp; cancel other patients appointments](https://www.bugbountyhunter.com/hackevents/report?id=72) |
| FB-75 | firstblood | Insecure direct object reference | High | [IDOR in aptid which grants access to every appointment](https://www.bugbountyhunter.com/hackevents/report?id=75) |
| FB-76 | firstblood | Insecure direct object reference | High | [Cancel arbitrary reports through 'aptid' parameter](https://www.bugbountyhunter.com/hackevents/report?id=76) |
| FB-77 | firstblood | Authorisation Issue | CRITICAL | [PII disclosure using GET request](https://www.bugbountyhunter.com/hackevents/report?id=77) |
| FB-81 | firstblood | Application/Business Logic | High | [A User can modify the Email of their appointment despite being disabled for safeguarding reasons](https://www.bugbountyhunter.com/hackevents/report?id=81) |
| FB-92 | firstblood | Open Redirect | Low | [Open redirect at http://firstbloodhackers.com:49330/drpanel/logout.php](https://www.bugbountyhunter.com/hackevents/report?id=92) |
| FB-97 | firstblood | Authorisation Issue | High | [Registring to the application as a doctor due to the leaked invitation code [COLLAB]](https://www.bugbountyhunter.com/hackevents/report?id=97) |
| FB-101 | firstblood | Authorisation Issue | High | [Invite codes do not expire after use](https://www.bugbountyhunter.com/hackevents/report?id=101) |
| FB-104 | firstblood | Application/Business Logic | CRITICAL | [New doctors can query appointments and users informations using vulnerable /drpanel/drapi/query.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=104) |
| FB-105 | firstblood | Authorisation Issue | High | [Info leak on reddit leads to create acc with admin privileges](https://www.bugbountyhunter.com/hackevents/report?id=105) |
| FB-106 | firstblood | Authorisation Issue | High | [An new user account can bypass security and view all patient data](https://www.bugbountyhunter.com/hackevents/report?id=106) |
| FB-109 | firstblood | Application/Business Logic | CRITICAL | [An new user account can bypass security and view all appointment data](https://www.bugbountyhunter.com/hackevents/report?id=109) |
| FB-110 | firstblood | Authorisation Issue | High | [Information Leak leads to full backend access](https://www.bugbountyhunter.com/hackevents/report?id=110) |
| FB-113 | firstblood | Authorisation Issue | High | [Account takeover of a doctor account is possible due to flawed logic in the registration process](https://www.bugbountyhunter.com/hackevents/report?id=113) |
| FB-114 | firstblood | Authorisation Issue | CRITICAL | [IDOR at http://firstbloodhackers.com:49369/drpanel/drapi/qp.php can be used to query patient data without doctor account](https://www.bugbountyhunter.com/hackevents/report?id=114) |
| FB-117 | firstblood | Info leak | CRITICAL | [Un-Authorized access to critical users PII through the vulnerable /attendees/event.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=117) |
| FB-118 | firstblood | Info leak | CRITICAL | [Info leak for events and attendees including PII data](https://www.bugbountyhunter.com/hackevents/report?id=118) |
| FB-124 | firstblood | Application/Business Logic | CRITICAL | [IDOR - Restricted doctor can view all the details of the patient such as contact details etc.](https://www.bugbountyhunter.com/hackevents/report?id=124) |
| FB-126 | firstblood | Open Redirect | Low | [Open Redirect /drpanel/logout.php](https://www.bugbountyhunter.com/hackevents/report?id=126) |
| FB-127 | firstblood | Insecure direct object reference | High | [IDOR on ma.php](https://www.bugbountyhunter.com/hackevents/report?id=127) |
| FB-128 | firstblood | Authorisation Issue | CRITICAL | [IDOR - Restricted user can view the details of hospital user.](https://www.bugbountyhunter.com/hackevents/report?id=128) |
| FB-129 | firstblood | Insecure direct object reference | High | [IDOR 2 on ma.php - confirms numerical id for bug chain to report 127 without the need for drpanel](https://www.bugbountyhunter.com/hackevents/report?id=129) |
| FB-130 | firstblood | Application/Business Logic | CRITICAL | [It is possible to view patient's data as a new doctor](https://www.bugbountyhunter.com/hackevents/report?id=130) |
| FB-134 | firstblood | Open Redirect | Low | [Open redirect on /drpanel/logout.php](https://www.bugbountyhunter.com/hackevents/report?id=134) |
| FB-136 | firstblood | Authorisation Issue | High | [Leaked invite ID allows anyone to register for an account.](https://www.bugbountyhunter.com/hackevents/report?id=136) |
| FB-137 | firstblood | Authorisation Issue | High | [Potentially takeover other doctors account?](https://www.bugbountyhunter.com/hackevents/report?id=137) |
| FB-138 | firstblood | Authorisation Issue | High | [Creating a new user with same username overrides old password which can lead to account takeover](https://www.bugbountyhunter.com/hackevents/report?id=138) |
| FB-140 | firstblood | Authorisation Issue | High | [Invitation code leaked on reddit](https://www.bugbountyhunter.com/hackevents/report?id=140) |
| FB-141 | firstblood | Authorisation Issue | High | [Doctor Invitation Code doesn't expire after first uage](https://www.bugbountyhunter.com/hackevents/report?id=141) |
| FB-142 | firstblood | Application/Business Logic | CRITICAL | [IDOR on newly registered doctor](https://www.bugbountyhunter.com/hackevents/report?id=142) |
| FB-143 | firstblood | Application/Business Logic | CRITICAL | [IDOR on /drpanel/drapi/qp.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=143) |
| FB-145 | firstblood | Application/Business Logic | High | [Patient's can modify their information without authorization on &quot;/manageappointment.php&quot; endpoint](https://www.bugbountyhunter.com/hackevents/report?id=145) |
| FB-146 | firstblood | Info leak | CRITICAL | [Leak PII through the events API](https://www.bugbountyhunter.com/hackevents/report?id=146) |
| FB-148 | firstblood | Application/Business Logic | CRITICAL | [New Doctors can use the api to get patients data](https://www.bugbountyhunter.com/hackevents/report?id=148) |
| FB-151 | firstblood | Info leak | CRITICAL | [Event attendees leaked](https://www.bugbountyhunter.com/hackevents/report?id=151) |
| FB-159 | firstblood | Authorisation Issue | CRITICAL | [Unauthenticated access to PII data on /drpanel/drapi/qp.php](https://www.bugbountyhunter.com/hackevents/report?id=159) |
| FB-160 | firstblood | Info leak | CRITICAL | [Hackerback event attendees information disclosed through /attendees/event.php](https://www.bugbountyhunter.com/hackevents/report?id=160) |
| FB-164 | firstblood | Info leak | CRITICAL | [Can know who are attending an HackerBack event](https://www.bugbountyhunter.com/hackevents/report?id=164) |
| FB-165 | firstblood | Info leak | CRITICAL | [P2 information disclosure of the users attending the events](https://www.bugbountyhunter.com/hackevents/report?id=165) |
| FB-166 | firstblood | Info leak | CRITICAL | [PII Creditcard information leaking via Event](https://www.bugbountyhunter.com/hackevents/report?id=166) |
| FB-167 | firstblood | Auth issues | High | [Creating Admin account using a leaked token on r/BugBountyHunter and using restricted API calls .](https://www.bugbountyhunter.com/hackevents/report?id=167) |
| FB-169 | firstblood | Authorisation Issue | High | [Found a way to register as non-admin user](https://www.bugbountyhunter.com/hackevents/report?id=169) |
| FB-172 | firstblood | Application/Business Logic | High | [Adding cookie to the request allows us to modify way more data then allowed](https://www.bugbountyhunter.com/hackevents/report?id=172) |
| FB-173 | firstblood | Info leak | CRITICAL | [PII disclosure - I can see email,contact No of patients who is/has attending/attended the hackerback event](https://www.bugbountyhunter.com/hackevents/report?id=173) |
| FB-174 | firstblood | Info leak | CRITICAL | [[Two Tales of Info leak] Site setting can be accessed and leaked a &quot;x-site-req&quot; header. This header can be used to get HackerBack event attendees info.](https://www.bugbountyhunter.com/hackevents/report?id=174) |
| FB-176 | firstblood | Insecure direct object reference | High | [Emails and comments of other users can be changed using IDOR on aptID](https://www.bugbountyhunter.com/hackevents/report?id=176) |
| FB-177 | firstblood | Application/Business Logic | CRITICAL | [New doctors can query appointments and users information using /drpanel/drapi/qp.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=177) |
| FB-182 | firstblood | Application/Business Logic | CRITICAL | [New doctors are able to view patient's private data through /drpanel/drapi/qp.php](https://www.bugbountyhunter.com/hackevents/report?id=182) |
| FB-183 | firstblood | Insecure direct object reference | High | [GUUID is replaceable by an 8 digit number which makes it vulnerable to IDOR](https://www.bugbountyhunter.com/hackevents/report?id=183) |
| FB-184 | firstblood | Application/Business Logic | High | [Authorisation vulnerabilities with cookies](https://www.bugbountyhunter.com/hackevents/report?id=184) |
| FB-187 | firstblood | Authorisation Issue | High | [Information Disclosure allowing an attacker to register as a doctor](https://www.bugbountyhunter.com/hackevents/report?id=187) |
| FB-192 | firstblood | Application/Business Logic | CRITICAL | [Privilege Escalation on /drpanel/drapi/query.php and /drpanel/drapi/query.php](https://www.bugbountyhunter.com/hackevents/report?id=192) |
| FB-193 | firstblood | Application/Business Logic | CRITICAL | [Application Logic allowing access to unauthorised information belonging to patients](https://www.bugbountyhunter.com/hackevents/report?id=193) |
| FB-194 | firstblood | Insecure direct object reference | High | [IDOR found on /api/ma.php](https://www.bugbountyhunter.com/hackevents/report?id=194) |
| FB-197 | firstblood | Application/Business Logic | CRITICAL | [Application Logic Issue allowing a doctor who is not authorised to view patients information on the dashboard](https://www.bugbountyhunter.com/hackevents/report?id=197) |
| FB-204 | firstblood | Authorisation Issue | High | [Info leak that leads to non admin login](https://www.bugbountyhunter.com/hackevents/report?id=204) |
| FB-214 | firstblood | Application/Business Logic | High | [Can change email when modifying an appointment](https://www.bugbountyhunter.com/hackevents/report?id=214) |
| FB-215 | firstblood | Authorisation Issue | High | [Account Creation with same Username overrides the one made before.](https://www.bugbountyhunter.com/hackevents/report?id=215) |
| FB-216 | firstblood | Application/Business Logic | CRITICAL | [IDOR to view Patient Information from a Lower Privileged User](https://www.bugbountyhunter.com/hackevents/report?id=216) |
| FB-217 | firstblood | Application/Business Logic | CRITICAL | [IDOR in Search Patient Functionality Leads to PII Leakage](https://www.bugbountyhunter.com/hackevents/report?id=217) |
| FB-221 | firstblood | Application/Business Logic | CRITICAL | [Patient's information can be obtained from a non admin account](https://www.bugbountyhunter.com/hackevents/report?id=221) |
| FB-226 | firstblood | Application/Business Logic | CRITICAL | [Recently registered doctor account can still query /drpanel/drapi/qp.php &amp; /drpanel/drapi/query.php](https://www.bugbountyhunter.com/hackevents/report?id=226) |
| FB-228 | firstblood | Insecure direct object reference | High | [Docauth cookie used to amend email - Additionally chained with Rpt 127 and 129 - This is the full report.](https://www.bugbountyhunter.com/hackevents/report?id=228) |
| FB-234 | firstblood | Info leak | CRITICAL | [Event is leaking attendees Personal information.](https://www.bugbountyhunter.com/hackevents/report?id=234) |
| FB-235 | firstblood | Insecure direct object reference | High | [a Doctor can cancel patient's appointments](https://www.bugbountyhunter.com/hackevents/report?id=235) |
| FB-237 | firstblood | Open Redirect | Low | [Open Redirect via logout ref parameter](https://www.bugbountyhunter.com/hackevents/report?id=237) |
| FB-239 | firstblood | Authorisation Issue | High | [Attacker can register a user name that has already been registered](https://www.bugbountyhunter.com/hackevents/report?id=239) |
| FB-246 | firstblood | Insecure direct object reference | High | [idor](https://www.bugbountyhunter.com/hackevents/report?id=246) |
| FB-259 | firstblood | Open Redirect | Low | [CWE-601 Open Redirect on GET /drpanel/logout.php via ref param](https://www.bugbountyhunter.com/hackevents/report?id=259) |
| FB-260 | firstblood | Insecure direct object reference | High | [[COLLAB] Query appointment with simple ID / Bypass front end restriction](https://www.bugbountyhunter.com/hackevents/report?id=260) |
| FB-262 | firstblood | Open Redirect | Low | [Open Redirect Vulnerability Observed in the Firstbloodhacker.com](https://www.bugbountyhunter.com/hackevents/report?id=262) |
| FB-263 | firstblood | Authorisation Issue | High | [New Doctor Registration Invitation Code Leaked to the Public](https://www.bugbountyhunter.com/hackevents/report?id=263) |
| FB-265 | firstblood | Application/Business Logic | CRITICAL | [Critical PII of Patients Leaked to the Public](https://www.bugbountyhunter.com/hackevents/report?id=265) |
| FB-270 | firstblood | Application/Business Logic | High | [Email id can be modified for a patient](https://www.bugbountyhunter.com/hackevents/report?id=270) |
| FB-272 | firstblood | Insecure direct object reference | High | [PII Data of the Fistbloodhacker.com All patient's were Publicly Accessible](https://www.bugbountyhunter.com/hackevents/report?id=272) |
| FB-275 | firstblood | Authorisation Issue | High | [register as non admin doctor](https://www.bugbountyhunter.com/hackevents/report?id=275) |
| FB-278 | firstblood | Open Redirect | Low | [Open redirect in logout function](https://www.bugbountyhunter.com/hackevents/report?id=278) |
| FB-279 | firstblood | Application/Business Logic | High | [a non admin doctor can still view patient information using the api](https://www.bugbountyhunter.com/hackevents/report?id=279) |
| FB-281 | firstblood | Info leak | CRITICAL | [Hackerback Event Details Along with Attendee's Personal Information Exposed to Public](https://www.bugbountyhunter.com/hackevents/report?id=281) |
| FB-309 | firstbloodv2 | Authorisation Issue | Informative | [Admin Panel Exposure by old credentials](https://www.bugbountyhunter.com/hackevents/report?id=309) |
| FB-322 | firstbloodv2 | Info leak | Low | [File Enumeration inside /api/checkproof.php?proof=file:///etc/passwd](https://www.bugbountyhunter.com/hackevents/report?id=322) |
| FB-324 | firstbloodv2 | Authorisation Issue | Informative | [[COLLAB with isitbug] Old admin credentials still work](https://www.bugbountyhunter.com/hackevents/report?id=324) |
| FB-325 | firstbloodv2 | Application/Business Logic | Medium | [Test user can query all patients](https://www.bugbountyhunter.com/hackevents/report?id=325) |
| FB-328 | firstbloodv2 | Authorisation Issue | Medium | [Valid doctor credentials could be obtained without an invitation code](https://www.bugbountyhunter.com/hackevents/report?id=328) |
| FB-354 | firstbloodv2 | Open Redirect | Low | [Open Redirect on /logout.php](https://www.bugbountyhunter.com/hackevents/report?id=354) |
| FB-357 | firstbloodv2 | Open Redirect | Low | [Open redirect via ref parameter on /drpanel/logout.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=357) |
| FB-358 | firstbloodv2 | Authorisation Issue | Informative | [Admin access is still possible](https://www.bugbountyhunter.com/hackevents/report?id=358) |
| FB-375 | firstbloodv2 | SQL Injection | CRITICAL | [Error-based SQL injection](https://www.bugbountyhunter.com/hackevents/report?id=375) |
| FB-377 | firstbloodv2 | Authorisation Issue | Medium | [Unique invite code bypass](https://www.bugbountyhunter.com/hackevents/report?id=377) |
| FB-380 | firstbloodv2 | Authorisation Issue | Medium | [Easily guessed invited code on doctor register](https://www.bugbountyhunter.com/hackevents/report?id=380) |
| FB-382 | firstbloodv2 | Open Redirect | Low | [logout.php is still vulnearble to Open Redirect](https://www.bugbountyhunter.com/hackevents/report?id=382) |
| FB-383 | firstbloodv2 | Auth issues | CRITICAL | [Edit password functionality can be used to reset password of any user](https://www.bugbountyhunter.com/hackevents/report?id=383) |
| FB-386 | firstbloodv2 | Authorisation Issue | CRITICAL | [Any user can update another's user password via /drpanel/drapi/editpassword.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=386) |
| FB-392 | firstbloodv2 | Application/Business Logic | Medium | [[COLLAB with isitbug] Still able to modify email on appointment](https://www.bugbountyhunter.com/hackevents/report?id=392) |
| FB-394 | firstbloodv2 | Application/Business Logic | Medium | [Modifying more information than intended on /manageappointment.php](https://www.bugbountyhunter.com/hackevents/report?id=394) |
| FB-404 | firstbloodv2 | Auth issues | CRITICAL | [Able to change any username's password without login (including drAdmin)](https://www.bugbountyhunter.com/hackevents/report?id=404) |
| FB-413 | firstbloodv2 | Open Redirect | Low | [Open redirect at https://62f9cb44c755-0xconft.a.firstbloodhackers.com/drpanel/logout.php?ref=//http:evil.org](https://www.bugbountyhunter.com/hackevents/report?id=413) |
| FB-414 | firstbloodv2 | Application/Business Logic | Medium | [email value in Modify Appointment Form is still changable](https://www.bugbountyhunter.com/hackevents/report?id=414) |
| FB-417 | firstbloodv2 | Application/Business Logic | Medium | [Un-Authorized users can access &quot;/drpanel/drapi/qp.php&quot; endpoint and access users personal information](https://www.bugbountyhunter.com/hackevents/report?id=417) |
| FB-418 | firstbloodv2 | Application/Business Logic | Medium | [Email of an appointment could be modified if cookie doctorAuthed is present](https://www.bugbountyhunter.com/hackevents/report?id=418) |
| FB-436 | firstbloodv2 | Authorisation Issue | Medium | [A doctors invite code is easily guessable and grants anyone access to the doctor portal and patient PII data](https://www.bugbountyhunter.com/hackevents/report?id=436) |
| FB-440 | firstbloodv2 | Authorisation Issue | Medium | [Anyone can register as a doctor due to weak Invite key](https://www.bugbountyhunter.com/hackevents/report?id=440) |
| FB-445 | firstbloodv2 | Authorisation Issue | Medium | [[COLLAB with isitbug] Invite code is literally &quot;test&quot;](https://www.bugbountyhunter.com/hackevents/report?id=445) |
| FB-448 | firstbloodv2 | Authorisation Issue | CRITICAL | [normal doctor can update other users' password](https://www.bugbountyhunter.com/hackevents/report?id=448) |
| FB-449 | firstbloodv2 | Application/Business Logic | Medium | [A User can modify the Email of their appointment despite being disabled for safeguarding reasons](https://www.bugbountyhunter.com/hackevents/report?id=449) |
| FB-450 | firstbloodv2 | Info leak | Low | [[COLLAB with isitbug] Blind LFI on /api/checkproof.php](https://www.bugbountyhunter.com/hackevents/report?id=450) |
| FB-451 | firstbloodv2 | Deserialization | CRITICAL | [RCE at https://62f9cb44c755-0xconft.a.firstbloodhackers.com/api/checkproof.php](https://www.bugbountyhunter.com/hackevents/report?id=451) |
| FB-452 | firstbloodv2 | Application/Business Logic | Medium | [[COLLAB with itisbug] Non admin doctor can search patients through api](https://www.bugbountyhunter.com/hackevents/report?id=452) |
| FB-468 | firstbloodv2 | Open Redirect | Low | [[COLLAB with isitbug] Open redirect bypass on logout](https://www.bugbountyhunter.com/hackevents/report?id=468) |
| FB-474 | firstbloodv2 | Auth issues | CRITICAL | [[COLLAB with isitbug] Able to change doctor passwords via admin API that is accessible by any doctor](https://www.bugbountyhunter.com/hackevents/report?id=474) |
| FB-475 | firstbloodv2 | Information leak/disclosure | CRITICAL | [[COLLAB] RCE via insecure deserialization in /api/checkproof.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=475) |
| FB-481 | firstbloodv2 | Authorisation Issue | Medium | [Able to register account using invite code &quot;test&quot;](https://www.bugbountyhunter.com/hackevents/report?id=481) |
| FB-482 | firstbloodv2 | Auth issues | CRITICAL | [Able to change password of any account (admin account access)](https://www.bugbountyhunter.com/hackevents/report?id=482) |
| FB-485 | firstbloodv2 | Authorisation Issue | CRITICAL | [login as Admin](https://www.bugbountyhunter.com/hackevents/report?id=485) |
| FB-488 | firstbloodv2 | Application/Business Logic | Medium | [Able to change the email id in any appointment](https://www.bugbountyhunter.com/hackevents/report?id=488) |
| FB-502 | firstbloodv2 | Info leak | Low | [Enumerating files/directories and tools/binaries installed on FirstBlood server](https://www.bugbountyhunter.com/hackevents/report?id=502) |
| FB-504 | firstbloodv2 | Auth issues | CRITICAL | [Endpoint allows unauthorized users to update other user's passwords](https://www.bugbountyhunter.com/hackevents/report?id=504) |
| FB-506 | firstbloodv2 | Info leak | CRITICAL | [Several Information leakage through vaccination proof list](https://www.bugbountyhunter.com/hackevents/report?id=506) |
| FB-509 | firstbloodv2 | Authorisation Issue | Medium | [weak unique invite code for registering doctor account](https://www.bugbountyhunter.com/hackevents/report?id=509) |
| FB-510 | firstbloodv2 | Application/Business Logic | Medium | [New registered doctor account can query patient directly via POST https://a9381b5eb20c-0xconft.a.firstbloodhackers.com/drpanel/drapi/qp.php](https://www.bugbountyhunter.com/hackevents/report?id=510) |
| FB-511 | firstbloodv2 | Auth issues | CRITICAL | [Can update any users password if know the username, and therefore takeover any account and get Admin access](https://www.bugbountyhunter.com/hackevents/report?id=511) |
| FB-515 | firstbloodv2 | Application/Business Logic | Medium | [non-admin doctor account can use qp.php API](https://www.bugbountyhunter.com/hackevents/report?id=515) |
| FB-519 | firstbloodv2 | Auth issues | CRITICAL | [Account takeover via /drpanel/drapi/editpassword.php](https://www.bugbountyhunter.com/hackevents/report?id=519) |
| FB-535 | firstbloodv2 | Open Redirect | Low | [Open Redirect on /drpanel/logout.php?ref=](https://www.bugbountyhunter.com/hackevents/report?id=535) |
| FB-536 | firstbloodv2 | Authorisation Issue | Medium | [Anyone can register as doctor by giving invite code &quot;test&quot;](https://www.bugbountyhunter.com/hackevents/report?id=536) |
| FB-537 | firstbloodv2 | Open Redirect | Informative | [The ref parameter is redirectable in the register.php path](https://www.bugbountyhunter.com/hackevents/report?id=537) |
| FB-540 | firstbloodv2 | Authorisation Issue | Medium | [Test Credentials are still working](https://www.bugbountyhunter.com/hackevents/report?id=540) |
| FB-542 | firstbloodv2 | Info leak | High | [Environment Files Exposed Publicly](https://www.bugbountyhunter.com/hackevents/report?id=542) |
| FB-548 | firstbloodv2 | Application/Business Logic | Medium | [[Unpatched] Patient's information can be changed that is not allowed to change by the webapp](https://www.bugbountyhunter.com/hackevents/report?id=548) |
| FB-551 | firstbloodv2 | Application/Business Logic | Low | [enumerate usernames](https://www.bugbountyhunter.com/hackevents/report?id=551) |
| FB-554 | firstbloodv2 | Application/Business Logic | Medium | [Modifying information on Appointment Form which are not allowed to be modified.](https://www.bugbountyhunter.com/hackevents/report?id=554) |
| FB-558 | firstbloodv2 | Auth issues | CRITICAL | [Admin password can be changed and retained by anyone](https://www.bugbountyhunter.com/hackevents/report?id=558) |
| FB-561 | firstbloodv2 | Insecure direct object reference | Medium | [a normal user can change the message in an appointment of another user](https://www.bugbountyhunter.com/hackevents/report?id=561) |
| FB-562 | firstbloodv2 | Deserialization | CRITICAL | [RCE via PHAR deserialization on /api/checkproof.php](https://www.bugbountyhunter.com/hackevents/report?id=562) |
| FB-564 | firstbloodv2 | Open Redirect | Low | [open redirect inside drpanel/logout.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=564) |
| FB-566 | firstbloodv2 | Auth issues | CRITICAL | [Any user can update admin's password](https://www.bugbountyhunter.com/hackevents/report?id=566) |
| FB-568 | firstbloodv2 | Application/Business Logic | Medium | [patient can change his email when he's not supposed to](https://www.bugbountyhunter.com/hackevents/report?id=568) |
| FB-569 | firstbloodv2 | Authorisation Issue | Medium | [Default credentials allow any unauthorized user to get access to a doctor account](https://www.bugbountyhunter.com/hackevents/report?id=569) |
| FB-570 | firstbloodv2 | Application/Business Logic | Medium | [Applogic at Modifying Appointment Details](https://www.bugbountyhunter.com/hackevents/report?id=570) |
| FB-578 | firstbloodv2 | Authorisation Issue | Medium | [Application Logic flaw leads to anyone registering a doctor account without invite code](https://www.bugbountyhunter.com/hackevents/report?id=578) |
| FB-580 | firstbloodv2 | Auth issues | CRITICAL | [Unauthorized access to edit password API leading to Account Takeover](https://www.bugbountyhunter.com/hackevents/report?id=580) |
| FB-585 | firstbloodv2 | Authorisation Issue | CRITICAL | [Admin account takeover](https://www.bugbountyhunter.com/hackevents/report?id=585) |
| FB-586 | firstbloodv2 | Open Redirect | Low | [Open Redirect on logout.php endpoint [Bypass]](https://www.bugbountyhunter.com/hackevents/report?id=586) |
| FB-588 | firstbloodv2 | Info leak | High | [Important files leaking on firstblood](https://www.bugbountyhunter.com/hackevents/report?id=588) |
| FB-590 | firstbloodv2 | Auth issues | CRITICAL | [drAdmin account recoverable using editpassword.php](https://www.bugbountyhunter.com/hackevents/report?id=590) |
| FB-592 | firstbloodv2 | Authorisation Issue | Medium | [register a doctor](https://www.bugbountyhunter.com/hackevents/report?id=592) |
| FB-603 | firstbloodv2 | SQL Injection | CRITICAL | [SQL Injection on /vaccination-manager/login.php through password parameter](https://www.bugbountyhunter.com/hackevents/report?id=603) |
| FB-618 | firstbloodv2 | Authorisation Issue | Medium | [Can register as a doctor by using 'test' as invite code](https://www.bugbountyhunter.com/hackevents/report?id=618) |
| FB-621 | firstbloodv2 | Application/Business Logic | Medium | [PII Information leaked to newly registered Doctor](https://www.bugbountyhunter.com/hackevents/report?id=621) |
| FB-622 | firstbloodv2 | Deserialization | CRITICAL | [Insecure Deserialization leading to RCE [COLLAB]- mrrootsec](https://www.bugbountyhunter.com/hackevents/report?id=622) |
| FB-629 | firstbloodv2 | Authorisation Issue | CRITICAL | [Admin account takeover by password reset](https://www.bugbountyhunter.com/hackevents/report?id=629) |
| FB-633 | firstbloodv2 | Deserialization | CRITICAL | [[COLLAB] RCE using insecure deserialization](https://www.bugbountyhunter.com/hackevents/report?id=633) |
| FB-635 | firstbloodv2 | Auth issues | CRITICAL | [drAdmin ATO by  using   doctor account.](https://www.bugbountyhunter.com/hackevents/report?id=635) |
| FB-643 | firstbloodv2 | Info leak | CRITICAL | [[COLLAB with isitbug] Information disclosure on multiple API endpoints](https://www.bugbountyhunter.com/hackevents/report?id=643) |
| FB-653 | firstbloodv2 | Authorisation Issue | Medium | [Account takeover by overwriting user's password](https://www.bugbountyhunter.com/hackevents/report?id=653) |
| FB-662 | firstbloodv2 | Auth issues | CRITICAL | [It is possible to reset drAdmin's password](https://www.bugbountyhunter.com/hackevents/report?id=662) |
| FB-671 | firstbloodv2 | Info leak | CRITICAL | [Vaccination proof leak](https://www.bugbountyhunter.com/hackevents/report?id=671) |
| FB-672 | firstbloodv2 | Info leak | CRITICAL | [Leaked proofs of vaccination on /vaccination-manager/api/vax-proof-list.php](https://www.bugbountyhunter.com/hackevents/report?id=672) |
| FB-675 | firstbloodv2 | Deserialization | CRITICAL | [PrivEsc to root user on firstblood through deserialisation aided by unintended disclosure of composer installation](https://www.bugbountyhunter.com/hackevents/report?id=675) |
| FB-679 | firstbloodv2 | Application/Business Logic | Low | [Cancelled appointments are still accessible through /manageappointment.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=679) |
| FB-681 | firstbloodv2 | RCE | CRITICAL | [Root access on the web server](https://www.bugbountyhunter.com/hackevents/report?id=681) |
| FB-686 | firstbloodv2 | SQL Injection | CRITICAL | [sql injection on /vaccination-manager/login.php](https://www.bugbountyhunter.com/hackevents/report?id=686) |
| FB-687 | firstbloodv2 | Deserialization | CRITICAL | [[COLLAB with isitbug] RCE through file upload deserialization](https://www.bugbountyhunter.com/hackevents/report?id=687) |
| FB-689 | firstbloodv2 | Authorisation Issue | Medium | [Bypass the invitation code and register your self as a doctor](https://www.bugbountyhunter.com/hackevents/report?id=689) |
| FB-690 | firstbloodv2 | Deserialization | CRITICAL | [Insecure Deserialization leading to complete server takeover + Privesc](https://www.bugbountyhunter.com/hackevents/report?id=690) |
| FB-692 | firstbloodv2 | RCE | CRITICAL | [Becoming a root on the server](https://www.bugbountyhunter.com/hackevents/report?id=692) |
| FB-695 | firstbloodv2 | Info leak | CRITICAL | [User's vaacination data leak and with other info without needing to log into vaccine-manger portal](https://www.bugbountyhunter.com/hackevents/report?id=695) |
| FB-699 | firstbloodv2 | Info leak | CRITICAL | [All vaccination proof records leaked](https://www.bugbountyhunter.com/hackevents/report?id=699) |
| FB-706 | firstbloodv2 | Authorisation Issue | CRITICAL | [Full Account takeover (even for admins)](https://www.bugbountyhunter.com/hackevents/report?id=706) |
| FB-707 | firstbloodv2 | Application/Business Logic | Medium | [newly created dr accounts can access patient PII via search api](https://www.bugbountyhunter.com/hackevents/report?id=707) |
| FB-712 | firstbloodv2 | SQL Injection | CRITICAL | [vaccination-management login panel can be bypassed using sql injection in password paramerter for username=admin.](https://www.bugbountyhunter.com/hackevents/report?id=712) |
| FB-717 | firstbloodv2 | Application/Business Logic | Medium | [New doctors unauthorized access to patients management details](https://www.bugbountyhunter.com/hackevents/report?id=717) |
| FB-718 | firstbloodv2 | Open Redirect | Low | [Open redirect by logout.php](https://www.bugbountyhunter.com/hackevents/report?id=718) |
| FB-723 | firstbloodv2 | SQL Injection | CRITICAL | [[COLLAB isitbug] SQL Injection on Vaccination Management login page leading to unauthorized access to the panel](https://www.bugbountyhunter.com/hackevents/report?id=723) |
| FB-725 | firstbloodv2 | SQL Injection | CRITICAL | [Vaccine Login is vulnerable to SQLi](https://www.bugbountyhunter.com/hackevents/report?id=725) |
| FB-728 | firstbloodv2 | Deserialization | CRITICAL | [Remote Command Execution via deserialization by uploading phar file](https://www.bugbountyhunter.com/hackevents/report?id=728) |
| FB-729 | firstbloodv2 | Auth issues | CRITICAL | [Dangerous /drpanel/drapi/editpassword.php endpoint leading to 0 click account takeover](https://www.bugbountyhunter.com/hackevents/report?id=729) |
| FB-730 | firstbloodv2 | Open Redirect | Low | [Open Url Redirect found at /drpanel/logout.php?ref=](https://www.bugbountyhunter.com/hackevents/report?id=730) |
| FB-731 | firstbloodv2 | Application/Business Logic | Medium | [Posibility to modify email of any appointment via /api/ma.php endpoint if attacker know the appointment id](https://www.bugbountyhunter.com/hackevents/report?id=731) |
| FB-732 | firstbloodv2 | Application/Business Logic | Informative | [User can upload infinite times vaccination certificate with same email leads to app/business Logic failure.](https://www.bugbountyhunter.com/hackevents/report?id=732) |
| FB-735 | firstbloodv2 | Application/Business Logic | Medium | [User can modify appointment email address which is supposed to be not editable](https://www.bugbountyhunter.com/hackevents/report?id=735) |
| FB-736 | firstbloodv2 | Deserialization | CRITICAL | [[COLLAB] Phar deserialization to RCE via upload vaccination proof](https://www.bugbountyhunter.com/hackevents/report?id=736) |
| FB-739 | firstbloodv2 | Application/Business Logic | Low | [Session Doesn't not expire at /drpanel/index.php and /vaccination-manager/portal.php.](https://www.bugbountyhunter.com/hackevents/report?id=739) |
| FB-741 | firstbloodv2 | Authorisation Issue | CRITICAL | [[COLLAB] Password change endpoint leads to ATO of drAdmin account.](https://www.bugbountyhunter.com/hackevents/report?id=741) |
| FB-742 | firstbloodv2 | SQL Injection | CRITICAL | [[COLLAB] Enumerate users via vaccination manager login](https://www.bugbountyhunter.com/hackevents/report?id=742) |
| FB-743 | firstbloodv2 | Info leak | CRITICAL | [[COLLAB] Exposed api allows viewing of all vaccination proof leaking user emails](https://www.bugbountyhunter.com/hackevents/report?id=743) |
| FB-757 | firstbloodv2 | Application/Business Logic | Low | [[COLLAB ] Session Invalidation at Vaccine Management Portal](https://www.bugbountyhunter.com/hackevents/report?id=757) |
| FB-760 | firstbloodv2 | Info leak | High | [multiple server config files are accessable publicly.](https://www.bugbountyhunter.com/hackevents/report?id=760) |
| FB-763 | firstbloodv2 | Deserialization | CRITICAL | [Rce can be obtained by uploading malicious .phar file at image field on /vaccination-manager/pub/upload-vaccination-proof.php because of vulnerable version of monolog.](https://www.bugbountyhunter.com/hackevents/report?id=763) |
| FB-766 | firstbloodv2 | Application/Business Logic | Medium | [New doctor can query patients information by API endpoint.](https://www.bugbountyhunter.com/hackevents/report?id=766) |
| FB-771 | firstbloodv2 | RCE | CRITICAL | [finding and logging into the vaccination portal](https://www.bugbountyhunter.com/hackevents/report?id=771) |
| FB-773 | firstbloodv2 | SQL Injection | CRITICAL | [SQL Injection Vulnerability in Vaccine Management Portal Allow Authentication Bypass](https://www.bugbountyhunter.com/hackevents/report?id=773) |
| FB-774 | firstbloodv2 | Application/Business Logic | Low | [No session invalidation after logout on vaccine-portal](https://www.bugbountyhunter.com/hackevents/report?id=774) |
| FB-776 | firstbloodv2 | Deserialization | CRITICAL | [Insecure Deserialization leading to RCE and rooting the server](https://www.bugbountyhunter.com/hackevents/report?id=776) |
| FB-779 | firstbloodv2 | Info leak | CRITICAL | [Info disclosure on /vaccination-manager/api/vax-proof-list.php](https://www.bugbountyhunter.com/hackevents/report?id=779) |
| FB-780 | firstbloodv2 | SQL Injection | CRITICAL | [SQLi on /vaccination-manager/login.php](https://www.bugbountyhunter.com/hackevents/report?id=780) |
| FB-785 | firstbloodv2 | SQL Injection | CRITICAL | [SQL Injection on vaccination-manager login page to access portal](https://www.bugbountyhunter.com/hackevents/report?id=785) |
| FB-788 | firstbloodv2 | Authorisation Issue | Medium | [Unexpected registered users](https://www.bugbountyhunter.com/hackevents/report?id=788) |
| FB-790 | firstbloodv2 | SQL Injection | CRITICAL | [SQLi allows to bypass login page for the vaccination-manager portal](https://www.bugbountyhunter.com/hackevents/report?id=790) |
| FB-793 | firstbloodv2 | Authorisation Issue | Medium | [Invalidate previously registered users by using duplicate invitations](https://www.bugbountyhunter.com/hackevents/report?id=793) |
| FB-800 | firstbloodv2 | Info leak | CRITICAL | [Information about vaccination proof can be accessed by any user via /vaccination-manager/api/vax-proof-list.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=800) |
| FB-804 | firstbloodv2 | Application/Business Logic | Medium | [Patient data can be accessed by Non Admin doctors](https://www.bugbountyhunter.com/hackevents/report?id=804) |
| FB-806 | firstbloodv2 | RCE | CRITICAL | [Privilege escalation when having root](https://www.bugbountyhunter.com/hackevents/report?id=806) |
| FB-808 | firstbloodv2 | SQL Injection | CRITICAL | [SQL Injection in vaccination manager login](https://www.bugbountyhunter.com/hackevents/report?id=808) |
| FB-809 | firstbloodv2 | Authorisation Issue | Medium | [An account with the same username can be created which leads to the original account being deleted and replaced with the attackers](https://www.bugbountyhunter.com/hackevents/report?id=809) |
| FB-813 | firstbloodv2 | Application/Business Logic | Medium | [Appointment data can still be modified when upon adding a cookie](https://www.bugbountyhunter.com/hackevents/report?id=813) |
| FB-814 | firstbloodv2 | Application/Business Logic | Medium | [Auth issue allowing a new doctor to view all appointment details that should require admin access](https://www.bugbountyhunter.com/hackevents/report?id=814) |
| FB-816 | firstbloodv2 | Open Redirect | Low | [Open Redirect on logout.php using ref parameter](https://www.bugbountyhunter.com/hackevents/report?id=816) |
| FB-824 | firstbloodv2 | Application/Business Logic | Medium | [Administrator endpoints can be accessed by non privileged doctor accounts which reveals sensitive patient information.](https://www.bugbountyhunter.com/hackevents/report?id=824) |
| FB-825 | firstbloodv2 | Application/Business Logic | Low | [vaccination manager doesnt destroy the cookie on logout](https://www.bugbountyhunter.com/hackevents/report?id=825) |
| FB-826 | firstbloodv2 | Authorisation Issue | Medium | [Original account  registered with invite code get deleted after registering another account with invite code](https://www.bugbountyhunter.com/hackevents/report?id=826) |
| FB-828 | firstbloodv2 | Application/Business Logic | Medium | [a non admin doctor can search for patients](https://www.bugbountyhunter.com/hackevents/report?id=828) |
| FB-829 | firstbloodv2 | Application/Business Logic | Medium | [Deleted doctor account can be used to  access private user information of paient](https://www.bugbountyhunter.com/hackevents/report?id=829) |
| FB-830 | firstbloodv2 | Application/Business Logic | Medium | [Patients can still change their application email](https://www.bugbountyhunter.com/hackevents/report?id=830) |
| FB-831 | firstbloodv2 | Open Redirect | Low | [Open Redirect at Doctor Panel](https://www.bugbountyhunter.com/hackevents/report?id=831) |
| FB-833 | firstbloodv2 | Open Redirect | Low | [[BYPASS] Open URL Redirect on /drpanel/logout.php](https://www.bugbountyhunter.com/hackevents/report?id=833) |
| FB-836 | firstbloodv2 | Info leak | CRITICAL | [patient information who have uploaded vaccination certificate  is publicly exposed on endpoint /vaccination-manager/api/vax-proof-list.php](https://www.bugbountyhunter.com/hackevents/report?id=836) |
| FB-837 | firstbloodv2 | Authorisation Issue | CRITICAL | [Change user passwords at will to enable account takeover](https://www.bugbountyhunter.com/hackevents/report?id=837) |
| FB-838 | firstbloodv2 | Application/Business Logic | Medium | [Regular accounts can override access to patient information](https://www.bugbountyhunter.com/hackevents/report?id=838) |
| FB-840 | firstbloodv2 | Application/Business Logic | Medium | [All user information is leaked due to unexpired cookies](https://www.bugbountyhunter.com/hackevents/report?id=840) |
| FB-850 | firstbloodv2 | Application/Business Logic | High | [Application logic error on /drpanel/ leads to ATO of doctors who have never signed in](https://www.bugbountyhunter.com/hackevents/report?id=850) |
| FB-851 | firstbloodv2 | Application/Business Logic | High | [[COLLAB with isitbug] Account takeover of TestDoctor with drps=%20 cookie](https://www.bugbountyhunter.com/hackevents/report?id=851) |
| FB-853 | firstbloodv2 | Application/Business Logic | Medium | [Unauthorized modification of mailbox](https://www.bugbountyhunter.com/hackevents/report?id=853) |
| FB-856 | firstbloodv2 | Authorisation Issue | Medium | [Registering as Doctor by using  `Test` as invite code](https://www.bugbountyhunter.com/hackevents/report?id=856) |
| FB-857 | firstbloodv2 | Auth issues | CRITICAL | [Changing Anyone's Password Including drAdmin (As a Non-authenticated user)](https://www.bugbountyhunter.com/hackevents/report?id=857) |
| FB-866 | firstbloodv2 | Application/Business Logic | Medium | [The endpoint MA.php (to modify an appointment) only allows for certain values to be modified, however due to some application logic error, if the user has tried to signup as a doctor and has the cookie &quot;doctorAuthed&quot; set, then it allows them to modify the email address for any appointment.](https://www.bugbountyhunter.com/hackevents/report?id=866) |
| FB-867 | firstbloodv2 | Deserialization | CRITICAL | [Insecure Deserialization leading to Remote Code Execution](https://www.bugbountyhunter.com/hackevents/report?id=867) |
| FB-870 | firstbloodv2 | Information leak/disclosure | CRITICAL | [Swagger UI reveals unauthenticated endpoint leaking sensitive data](https://www.bugbountyhunter.com/hackevents/report?id=870) |
| FB-873 | firstbloodv2 | SQL Injection | CRITICAL | [Username enumeration and SQL Injection on Vaccine Management login page](https://www.bugbountyhunter.com/hackevents/report?id=873) |
| FB-874 | firstbloodv2 | Application/Business Logic | Medium | [New doctors can easily get access to patients private data](https://www.bugbountyhunter.com/hackevents/report?id=874) |
| FB-875 | firstbloodv2 | SQL Injection | CRITICAL | [SQL Injection in vaccine management login can be used to view appointment details table](https://www.bugbountyhunter.com/hackevents/report?id=875) |
| FB-876 | firstbloodv2 | Application/Business Logic | Medium | [New doctor account (limited access) can view patient information through an API call](https://www.bugbountyhunter.com/hackevents/report?id=876) |
| FB-877 | firstbloodv2 | Application/Business Logic | Medium | [It is possible to modify the email address of an appointment.](https://www.bugbountyhunter.com/hackevents/report?id=877) |
| FB-885 | firstbloodv2 | Application/Business Logic | Medium | [Broken Access Control Leads to Information Leak](https://www.bugbountyhunter.com/hackevents/report?id=885) |
| FB-886 | firstbloodv2 | Application/Business Logic | Low | [Drpanel admin username enumeration](https://www.bugbountyhunter.com/hackevents/report?id=886) |
| FB-887 | firstbloodv2 | Authorisation Issue | Medium | [Doctor Role can be obtained using leaked invite code](https://www.bugbountyhunter.com/hackevents/report?id=887) |
| FB-888 | firstbloodv2 | SQL Injection | CRITICAL | [SQL Injection on /vaccination-manager/login.php](https://www.bugbountyhunter.com/hackevents/report?id=888) |
| FB-893 | firstbloodv2 | Info leak | High | [Information about used dependencies is leaked via /vendor/composer/installed.json](https://www.bugbountyhunter.com/hackevents/report?id=893) |
| FB-897 | firstbloodv2 | Open Redirect | Low | [Open redirect vulnerability in the logout function](https://www.bugbountyhunter.com/hackevents/report?id=897) |
| FB-899 | firstbloodv2 | Authorisation Issue | High | [editpassword Function lead to ATO fore any users](https://www.bugbountyhunter.com/hackevents/report?id=899) |
| FB-907 | firstbloodv2 | Application/Business Logic | Medium | [Newly Registered Doctor's can query for patient inforamtion](https://www.bugbountyhunter.com/hackevents/report?id=907) |
| FB-913 | firstbloodv2 | Application/Business Logic | Medium | [[BYPASS] Newly registered Doctor can access to PII data](https://www.bugbountyhunter.com/hackevents/report?id=913) |
| FB-914 | firstbloodv2 | SQL Injection | CRITICAL | [The login form for Vaccination Manager is vulnerable to SQL injection](https://www.bugbountyhunter.com/hackevents/report?id=914) |
| FB-915 | firstbloodv2 | Info leak | CRITICAL | [List of vaccination disclosure](https://www.bugbountyhunter.com/hackevents/report?id=915) |
| FB-916 | firstbloodv2 | RCE | CRITICAL | [FirstBlood server Rooted!](https://www.bugbountyhunter.com/hackevents/report?id=916) |
| FB-918 | firstbloodv2 | Application/Business Logic | Medium | [A normal doctor still can access /drpanel/drapi/qp.php and search patients via a POST request](https://www.bugbountyhunter.com/hackevents/report?id=918) |
| FB-922 | firstbloodv2 | Application/Business Logic | Low | [Various authentication issues](https://www.bugbountyhunter.com/hackevents/report?id=922) |
| FB-923 | firstbloodv2 | Deserialization | CRITICAL | [phar out - PHP deseriliazation RCE + priv. escalation](https://www.bugbountyhunter.com/hackevents/report?id=923) |
| FB-924 | firstbloodv2 | Authorisation Issue | Medium | [AppLogic when registering as a doctor using invite code](https://www.bugbountyhunter.com/hackevents/report?id=924) |
| FB-928 | firstbloodv2 | Application/Business Logic | High | [It is possible to login as TestDoctor with &lt;BLANK&gt; cookie.](https://www.bugbountyhunter.com/hackevents/report?id=928) |
| FB-929 | firstbloodv2 | Deserialization | CRITICAL | [Server misconfigurations post-RCE](https://www.bugbountyhunter.com/hackevents/report?id=929) |
| FB-939 | firstbloodv2 | Deserialization | CRITICAL | [Remote Code Execution via insecure deserialization on /api/checkproof.php](https://www.bugbountyhunter.com/hackevents/report?id=939) |
| FB-940 | firstbloodv2 | Open Redirect | Low | [Open redirect on logout.php](https://www.bugbountyhunter.com/hackevents/report?id=940) |
| FB-943 | firstbloodv2 | Info leak | CRITICAL | [Endpoint discloses information about all vaccination proof records](https://www.bugbountyhunter.com/hackevents/report?id=943) |
| FB-950 | firstbloodv2 | Deserialization | CRITICAL | [[COLLAB] RCE using insecure deserialization](https://www.bugbountyhunter.com/hackevents/report?id=950) |
| FB-954 | firstbloodv2 | SQL Injection | CRITICAL | [[COLLAB]vaccination-manager Login page is vulnerable to SQL injection](https://www.bugbountyhunter.com/hackevents/report?id=954) |
| FB-957 | firstbloodv2 | Info leak | CRITICAL | [[COLLAB]PII leakage via vax-proof-list API](https://www.bugbountyhunter.com/hackevents/report?id=957) |
| FB-958 | firstbloodv2 | Deserialization | CRITICAL | [[COLLAB]Upload Proof of Vaccination is vulnerable to RCE](https://www.bugbountyhunter.com/hackevents/report?id=958) |
| FB-985 | firstbloodv2 | Application/Business Logic | Medium | [[COLLAB] Able to modify email post booking an appointment](https://www.bugbountyhunter.com/hackevents/report?id=985) |
| FB-1000 | firstbloodv3 | Auth issues | CRITICAL | [Change Password of admin user](https://www.bugbountyhunter.com/hackevents/report?id=1000) |
| FB-1001 | firstbloodv3 | Multiple types | CRITICAL | [Admin Account takeover](https://www.bugbountyhunter.com/hackevents/report?id=1001) |
| FB-1002 | firstbloodv3 | Multiple types | High | [XSS on /api/ambulances.php?select=](https://www.bugbountyhunter.com/hackevents/report?id=1002) |
| FB-1005 | firstbloodv3 | Multiple types | Medium | [xss on about.html](https://www.bugbountyhunter.com/hackevents/report?id=1005) |
| FB-1007 | firstbloodv3 | Auth issues | CRITICAL | [Default Credentials](https://www.bugbountyhunter.com/hackevents/report?id=1007) |
| FB-1008 | firstbloodv3 | Multiple types | Low | [CSRF in Modify Doctor](https://www.bugbountyhunter.com/hackevents/report?id=1008) |
| FB-1010 | firstbloodv3 | Multiple types | CRITICAL | [Store xss on doctor admin dashboard](https://www.bugbountyhunter.com/hackevents/report?id=1010) |
| FB-1011 | firstbloodv3 | Multiple types | Low | [Open Redirect on logout.php](https://www.bugbountyhunter.com/hackevents/report?id=1011) |
| FB-1013 | firstbloodv3 | Auth issues | CRITICAL | [Default credentials on login page](https://www.bugbountyhunter.com/hackevents/report?id=1013) |
| FB-1014 | firstbloodv3 | Multiple types | Low | [CSRF to edit doctors information](https://www.bugbountyhunter.com/hackevents/report?id=1014) |
| FB-1027 | firstbloodv3 | Multiple types | Low | [Can make book appointment to unavailable doctor](https://www.bugbountyhunter.com/hackevents/report?id=1027) |
| FB-1028 | firstbloodv3 | Application/Business Logic | Low | [Business logic allows to book appointments with unavailable doctors](https://www.bugbountyhunter.com/hackevents/report?id=1028) |
| FB-1053 | firstbloodv3 | Auth issues | CRITICAL | [editpassword.php allows anyone to edit any user's passwords](https://www.bugbountyhunter.com/hackevents/report?id=1053) |
| FB-1059 | firstbloodv3 | Information leak/disclosure | High | [Leak doctors private emails and internal data](https://www.bugbountyhunter.com/hackevents/report?id=1059) |
| FB-1061 | firstbloodv3 | Information leak/disclosure | High | [PII data leak](https://www.bugbountyhunter.com/hackevents/report?id=1061) |
| FB-1073 | firstbloodv3 | Auth issues | CRITICAL | [Change doctor passwords via admin API that is accessible by any doctor](https://www.bugbountyhunter.com/hackevents/report?id=1073) |
| FB-1079 | firstbloodv3 | Open Redirect | Low | [Open redirect still works on logout.php](https://www.bugbountyhunter.com/hackevents/report?id=1079) |
| FB-1090 | firstbloodv3 | Broken access control | High | [Leak doctors private emails and internal data](https://www.bugbountyhunter.com/hackevents/report?id=1090) |
| FB-1124 | firstbloodv3 | Auth issues | CRITICAL | [Stored XSS in the Doctor Name on /doctors.php as well as /about.php](https://www.bugbountyhunter.com/hackevents/report?id=1124) |
| FB-1142 | firstbloodv3 | Cross Site Request Forgery | Low | [CSRF leading to Modify the doctors data](https://www.bugbountyhunter.com/hackevents/report?id=1142) |
| FB-1148 | firstbloodv3 | Multiple types | CRITICAL | [Stored xss in HackerBack sign up phone number to Account takeover](https://www.bugbountyhunter.com/hackevents/report?id=1148) |
| FB-1154 | firstbloodv3 | Auth issues | CRITICAL | [Default credentials admin:admin work on login.php](https://www.bugbountyhunter.com/hackevents/report?id=1154) |
| FB-1166 | firstbloodv3 | Open Redirect | Low | [Open redirect on logout remained unpatched](https://www.bugbountyhunter.com/hackevents/report?id=1166) |
| FB-1174 | firstbloodv3 | Open Redirect | Low | [Open Redirect on /logout.php endpoint](https://www.bugbountyhunter.com/hackevents/report?id=1174) |
| FB-1176 | firstbloodv3 |  | Informative | [Username enumeration through editpassword.php](https://www.bugbountyhunter.com/hackevents/report?id=1176) |
| FB-1184 | firstbloodv3 | Cross Site Request Forgery | Low | [CSRF bypass on edit-dr.php](https://www.bugbountyhunter.com/hackevents/report?id=1184) |
| FB-1192 | firstbloodv3 | Information leak/disclosure | High | [[Collab] Unauthorized Access to Patients' PII at /api/ambulances.php](https://www.bugbountyhunter.com/hackevents/report?id=1192) |
| FB-1198 | firstbloodv3 | Application/Business Logic | Low | [Modifying appointment](https://www.bugbountyhunter.com/hackevents/report?id=1198) |
| FB-1200 | firstbloodv3 | Application/Business Logic | Low | [Change doctors images via the admin panel](https://www.bugbountyhunter.com/hackevents/report?id=1200) |
| FB-1209 | firstbloodv3 | Information leak/disclosure | High | [Leakage of all users assigned to ambulances](https://www.bugbountyhunter.com/hackevents/report?id=1209) |
| FB-1232 | firstbloodv3 |  | Informative | [No CSRF protection on editpassword.php](https://www.bugbountyhunter.com/hackevents/report?id=1232) |
| FB-1319 | firstbloodv3 | Multiple types | CRITICAL | [Blind xss on FirstBloodHackers INTERNAL ADMIN PANEL](https://www.bugbountyhunter.com/hackevents/report?id=1319) |
| FB-1331 | firstbloodv3 | Auth issues | CRITICAL | [Admin account takeover with editpassword](https://www.bugbountyhunter.com/hackevents/report?id=1331) |
| FB-1368 | firstbloodv3 | Application/Business Logic | Low | [Can change the data of the cancelled Appointments](https://www.bugbountyhunter.com/hackevents/report?id=1368) |
| FB-1383 | firstbloodv3 | Cross Site Request Forgery | Low | [Edit doctor details with CSRF](https://www.bugbountyhunter.com/hackevents/report?id=1383) |
| FB-1390 | firstbloodv3 | Multiple types | High | [Stored xss in doctors name](https://www.bugbountyhunter.com/hackevents/report?id=1390) |
| FB-1395 | firstbloodv3 | Application/Business Logic | Medium | [Appointment leakage](https://www.bugbountyhunter.com/hackevents/report?id=1395) |
| FB-1399 | firstbloodv3 | Application/Business Logic | Low | [It is possible to book an appointment with an unavailable doctor](https://www.bugbountyhunter.com/hackevents/report?id=1399) |
| FB-1406 | firstbloodv3 |  | Informative | [Open redirect](https://www.bugbountyhunter.com/hackevents/report?id=1406) |
| FB-1422 | firstbloodv3 | Multiple types | Low | [CSRF on edit-dr.php leads to admin DoS](https://www.bugbountyhunter.com/hackevents/report?id=1422) |
| FB-1432 | firstbloodv3 | Application/Business Logic | Low | [Book non-bookable doctors in appointment](https://www.bugbountyhunter.com/hackevents/report?id=1432) |
| FB-1443 | firstbloodv3 | Auth issues | CRITICAL | [Zero click account takeover](https://www.bugbountyhunter.com/hackevents/report?id=1443) |
| FB-1445 | firstbloodv3 | Information leak/disclosure | High | [Get Request to `/api/doctors.php` leaks the PII of the Doctors](https://www.bugbountyhunter.com/hackevents/report?id=1445) |
| FB-1455 | firstbloodv3 | Application/Business Logic | Low | [Doctors can change doctor's profile photo](https://www.bugbountyhunter.com/hackevents/report?id=1455) |
| FB-1459 | firstbloodv3 | Application/Business Logic | Low | [It is possible to bypass relative URL by using triple forward slashes on photoURL and load external images](https://www.bugbountyhunter.com/hackevents/report?id=1459) |
| FB-1475 | firstbloodv3 | Multiple types | High | [Info Leak on api/ambulances.php leads to IDOR on manageappointment](https://www.bugbountyhunter.com/hackevents/report?id=1475) |
| FB-1481 | firstbloodv3 | Information leak/disclosure | High | [PII of doctors leaked through /api/doctors.php](https://www.bugbountyhunter.com/hackevents/report?id=1481) |
| FB-1541 | firstbloodv3 | Information leak/disclosure | High | [Leakage of doctors PII](https://www.bugbountyhunter.com/hackevents/report?id=1541) |
| FB-1543 | firstbloodv3 | Broken access control | High | [Anyone can edit doctors](https://www.bugbountyhunter.com/hackevents/report?id=1543) |
| FB-1547 | firstbloodv3 | Broken access control | High | [Private office locations disclosed on /api/locations.php](https://www.bugbountyhunter.com/hackevents/report?id=1547) |
| FB-1607 | firstbloodv3 | Broken access control | High | [Infomation Disclosure about private locations](https://www.bugbountyhunter.com/hackevents/report?id=1607) |
| FB-1632 | firstbloodv3 | Broken access control | High | [Information disclosure](https://www.bugbountyhunter.com/hackevents/report?id=1632) |
| FB-1637 | firstbloodv3 | Broken access control | High | [Unauthenticated Modification of the Doctors Data via New Api Call](https://www.bugbountyhunter.com/hackevents/report?id=1637) |
| FB-1668 | firstbloodv3 | Multiple types | High | [Stored xss in ambulance driver name](https://www.bugbountyhunter.com/hackevents/report?id=1668) |
| FB-1670 | firstbloodv3 | Multiple types | High | [Unauthenticated user is able to change a doctors profile](https://www.bugbountyhunter.com/hackevents/report?id=1670) |
| FB-1672 | firstbloodv3 | Multiple types | High | [Able to delete an ambulance from an appointment](https://www.bugbountyhunter.com/hackevents/report?id=1672) |
| FB-1678 | firstbloodv3 | Multiple types | High | [3 stored XSS in meet_drs.php](https://www.bugbountyhunter.com/hackevents/report?id=1678) |
| FB-1683 | firstbloodv3 | Broken access control | High | [Delete Ambulance Provided to any Appointment](https://www.bugbountyhunter.com/hackevents/report?id=1683) |
| FB-1701 | firstbloodv3 | Multiple types | Informative | [DoS on about.php, doctors.php and meet_drs.php pages due on edit-dr.php](https://www.bugbountyhunter.com/hackevents/report?id=1701) |
| FB-1710 | firstbloodv3 | Multiple types | High | [Stored xss in doctors photo on meet_drs.php](https://www.bugbountyhunter.com/hackevents/report?id=1710) |
| FB-1724 | firstbloodv3 | Broken access control | High | [Doctor params vulnerable to stored XSS](https://www.bugbountyhunter.com/hackevents/report?id=1724) |
| FB-1757 | firstbloodv3 | Multiple types | High | [Stored xss in doctors bio via about.php](https://www.bugbountyhunter.com/hackevents/report?id=1757) |
| FB-1762 | firstbloodv3 | Information leak/disclosure | High | [Leak all the Appointment Id with ambulance enabled](https://www.bugbountyhunter.com/hackevents/report?id=1762) |
| FB-1774 | firstbloodv3 | Cross Site Request Forgery | Low | [Edit doctor page CSRF](https://www.bugbountyhunter.com/hackevents/report?id=1774) |
| FB-1785 | firstbloodv3 | Broken access control | High | [Stored XSS with tagline](https://www.bugbountyhunter.com/hackevents/report?id=1785) |
| FB-1801 | firstbloodv3 | Application/Business Logic | Low | [It is still possible to edit some data of a confirmed &amp; cancelled appointment](https://www.bugbountyhunter.com/hackevents/report?id=1801) |
| FB-1804 | firstbloodv3 | Information leak/disclosure | High | [Appointment UUIDs leaked through new ambulances API endpoint](https://www.bugbountyhunter.com/hackevents/report?id=1804) |

Total non-XSS rows: **355** (XSS rows above: 207; grand total 562).
