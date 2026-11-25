---
title: "Vault class RCE — Code Execution"
type: dataset-view
class: "Code Execution"
vault_category: "RCE/"
rows: 843
paid_rows: 193
bounty_sum: 624,658
full_bodies_available: 557
source: "public HackerOne vault (hackerone disclosed), harvested 2026-11-17"
---

# RCE — Code Execution

843 rows · 193 with a bounty figure · **$624,658** total · 557 with full write-up stored.
Playbook: `Vault/RCE/` · Dataset: `Vault/_VAULT/reports.sqlite` (`SELECT * FROM reports WHERE ...`).

| Report | Program | Severity | Bounty | Votes | Disclosed | Weakness | Title |
|---|---|---|---|---|---|---|---|
| [1679624](https://hackerone.com/reports/1679624) | GitLab | critical | $33,510 | 392 | 2022-10-06 | Command Injection - Generic | Remote Command Execution via Github import |
| [1609965](https://hackerone.com/reports/1609965) | GitLab | critical | $33,510 | 387 | 2022-09-13 | Command Injection - Generic | RCE via the DecompressedArchiveSizeValidator and Project BulkImports (behind feature flag) |
| [925585](https://hackerone.com/reports/925585) | PayPal | critical | $30,000 | 946 | 2021-02-09 | Code Injection | RCE via npm misconfig -- installing internal libraries from the public registry |
| [455645](https://hackerone.com/reports/455645) | Snapchat | critical | $25,000 | 1191 | 2021-07-29 | OS Command Injection | Exposed Kubernetes API - RCE/Exposed Creds |
| [591295](https://hackerone.com/reports/591295) | X / xAI | critical | $20,160 | 1246 | 2019-08-10 | OS Command Injection | Potential pre-auth RCE on Twitter VPN |
| [141956](https://hackerone.com/reports/141956) | Pornhub |  | $20,000 | 607 |  | Code Injection | [phpobject in cookie] Remote shell/command execution |
| [1154542](https://hackerone.com/reports/1154542) | GitLab | critical | $20,000 | 508 | 2021-05-14 | Code Injection | RCE when removing metadata with ExifTool |
| [1125425](https://hackerone.com/reports/1125425) | GitLab | critical | $20,000 | 427 | 2021-04-20 | Code Injection | RCE via unsafe inline Kramdown options when rendering certain Wiki pages |
| [181879](https://hackerone.com/reports/181879) | shopify-scripts | critical | $18,000 | 14 | 2016-12-17 | Code Injection | Struct type confusion RCE |
| [873614](https://hackerone.com/reports/873614) | PlayStation | critical | $15,000 | 780 | 2020-12-04 | Code Injection | Websites Can Run Arbitrary Code on Machines Running the 'PlayStation Now' Application |
| [658013](https://hackerone.com/reports/658013) | GitLab | critical | $12,000 | 777 | 2019-12-19 | Command Injection - Generic | Git flag injection - local file overwrite to remote code execution |
| [587854](https://hackerone.com/reports/587854) | GitLab | critical | $12,000 | 542 | 2019-07-17 | Command Injection - Generic | Local files could be overwritten in GitLab, leading to remote command execution |
| [3782701](https://hackerone.com/reports/3782701) | Mozilla | critical | $12,000 | 361 | 2026-08-05 | Code Injection | Unauthenticated RCE in Taskcluster web-server via GraphQL filter argument (sift $where) |
| [733072](https://hackerone.com/reports/733072) | GitLab | high | $12,000 | 142 | 2022-06-07 | Command Injection - Generic | Path traversal, to RCE |
| [1043385](https://hackerone.com/reports/1043385) | LY Corporation | critical | $11,500 | 288 | 2021-07-05 | Code Injection | Arbitrary Code Execution via npm misconfiguration – installing internal libraries from the public registry |
| [518637](https://hackerone.com/reports/518637) | Mail.ru |  | $10,000 | 359 |  | Code Injection | RCE on shared.mail.ru due to "widget" plugin |
| [1312641](https://hackerone.com/reports/1312641) | Pornhub |  | $10,000 | 271 |  | Deserialization of Untrusted Data | Deserialization of untrusted data at https://www.redtube.com/media/hls?s=data |
| [72243](https://hackerone.com/reports/72243) | Pornhub |  | $10,000 | 211 |  | Code Injection | Publicly exposed SVN repository, ht.pornhub.com |
| [125980](https://hackerone.com/reports/125980) | Uber |  | $10,000 | 137 | 2016-04-06 | Code Injection | uber.com may RCE by Flask Jinja2 Template Injection |
| [1007014](https://hackerone.com/reports/1007014) | Uber | critical | $9,000 | 325 | 2021-02-24 | Code Injection | RCE via npm misconfig -- installing internal libraries from the public registry |
| [2255750](https://hackerone.com/reports/2255750) | Mozilla | critical | $8,000 | 58 | 2024-01-20 | Code Injection | Remote code execution and exfiltration of secret tokens by poisoning the mozilla/fxa CI build cache |
| [3694007](https://hackerone.com/reports/3694007) | HackerOne | high | $7,000 | 174 | 2026-06-17 | Code Injection | Authenticated Elasticsearch Painless script execution via Query.search.sort_query on hackerone.com/graphql |
| [682442](https://hackerone.com/reports/682442) | GitLab | high | $7,000 | 130 | 2019-12-15 | Command Injection - Generic | Git flag injection - Search API with scope 'blobs' |
| [138869](https://hackerone.com/reports/138869) | Uber |  | $7,000 | 83 | 2016-07-15 | Code Injection | OneLogin authentication bypass on WordPress sites via XMLRPC |
| [1418891](https://hackerone.com/reports/1418891) | Aiven Ltd | critical | $6,000 | 134 | 2022-11-08 | Command Injection - Generic | Apache Flink RCE via GET jar/plan API Endpoint |
| [365271](https://hackerone.com/reports/365271) | Basecamp | critical | $5,000 | 417 | 2020-11-26 | Command Injection - Generic | Remote code execution on Basecamp.com |
| [713006](https://hackerone.com/reports/713006) | Keybase |  | $5,000 | 196 |  | Remote File Inclusion | Keybase client (Windows 10): Write files anywhere in userland using relative path in "download attachement" feature |
| [1104874](https://hackerone.com/reports/1104874) | Basecamp | high | $5,000 | 102 | 2021-08-10 | Command Injection - Generic | Insecure Bundler configuration fetching internal Gems (okra) from Rubygems.org |
| [189192](https://hackerone.com/reports/189192) | Pornhub |  | $5,000 | 73 |  | Code Injection | Unsecured DB instance |
| [2231019](https://hackerone.com/reports/2231019) | Kubernetes | high | $5,000 | 67 | 2023-12-21 | Code Injection | CVE-2023-5528: Insufficient input sanitization in in-tree storage plugin leads to privilege escalation on Windows nodes |
| [1547877](https://hackerone.com/reports/1547877) | Aiven Ltd | critical | $5,000 | 56 | 2022-11-08 | Unrestricted Upload of File with Dangerous Type | [Kafka Connect] [JdbcSinkConnector][HttpSinkConnector] RCE by leveraging file upload via SQLite JDBC driver and SSRF to internal Jolokia |
| [1529790](https://hackerone.com/reports/1529790) | Aiven Ltd | critical | $5,000 | 45 | 2022-11-08 | Deserialization of Untrusted Data | Kafka Connect RCE via connector SASL  JAAS JndiLoginModule configuration |
| [72735](https://hackerone.com/reports/72735) | Pornhub |  | $5,000 | 7 |  | Command Injection - Generic | Unauthenticated access to Content Management System - www1.pornhubpremium.com |
| [2585376](https://hackerone.com/reports/2585376) | Internet Bug Bounty | high | $4,920 | 31 | 2024-07-13 | Inclusion of Functionality from Untrusted Control Sphere | important: Apache HTTP Server may use exploitable/malicious backend application output to run local handlers via internal redirect (CVE-2024-38476) |
| [2438265](https://hackerone.com/reports/2438265) | Internet Bug Bounty | high | $4,860 | 88 | 2024-03-29 | Code Injection | CVE-2024-27281: RCE vulnerability with .rdoc_options in RDoc |
| [1196124](https://hackerone.com/reports/1196124) | GitHub Security Lab |  | $4,500 | 72 |  | Code Injection | [Python] CWE-400: Regular Expression Injection |
| [1212273](https://hackerone.com/reports/1212273) | GitHub Security Lab |  | $4,500 | 33 |  | Code Injection | [Python] CWE-090: LDAP Injection |
| [1287573](https://hackerone.com/reports/1287573) | GitHub Security Lab |  | $4,500 | 26 |  |  | Java: Unsafe deserialization with Jackson |
| [1118508](https://hackerone.com/reports/1118508) | GitHub Security Lab |  | $4,500 | 20 |  | Code Injection | Java: Query for detecting JEXL injections |
| [1135877](https://hackerone.com/reports/1135877) | GitHub Security Lab |  | $4,500 | 15 |  |  | Java: Query for detecting unsafe deserialization with Spring exporters |
| [1602237](https://hackerone.com/reports/1602237) | GitHub Security Lab |  | $4,500 | 8 |  | Code Injection | PYTHON: CWE-079 - Add query for email injection |
| [1738940](https://hackerone.com/reports/1738940) | GitHub Security Lab |  | $4,500 | 5 |  | Code Injection | C/C++: Command injection via wordexp |
| [1319270](https://hackerone.com/reports/1319270) | GitHub Security Lab |  | $4,500 | 1 |  |  | [C#]: Deserialization sinks |
| [3031518](https://hackerone.com/reports/3031518) | Internet Bug Bounty | high | $4,323 | 56 | 2025-04-27 | Deserialization of Untrusted Data | CVE-2025-24813: Remote Code Execution and/or Information disclosure and/or malicious content added to uploaded files via write enabled Default Servlet |
| [294911](https://hackerone.com/reports/294911) | Mapbox | critical | $4,000 | 133 | 2017-12-21 | Command Injection - Generic | Admin Panel Accessed (OAuth Bypassed ) |
| [1776476](https://hackerone.com/reports/1776476) | Internet Bug Bounty | high | $4,000 | 60 | 2023-01-05 | Code Injection | CVE-2022-40127: RCE in Apache Airflow <2.4.0 bash example |
| [653125](https://hackerone.com/reports/653125) | GitLab | critical | $3,500 | 169 | 2019-12-19 | Command Injection - Generic | Git flag injection leading to file overwrite and potential remote code execution |
| [854032](https://hackerone.com/reports/854032) | Mail.ru |  | $3,000 | 404 |  | Code Injection | Unrestricted file upload on [ambassador.mail.ru] |
| [1274695](https://hackerone.com/reports/1274695) | PortSwigger Web Security | high | $3,000 | 172 | 2023-10-10 | Command Injection - Generic | RCE of Burp  Scanner / Crawler via Clickjacking |
| [798135](https://hackerone.com/reports/798135) | Mail.ru |  | $3,000 | 137 |  | Code Injection | PHP code injection at tz.mail.ru |
| [787113](https://hackerone.com/reports/787113) | GitHub Security Lab |  | $3,000 | 51 |  | Code Injection | CodeQL query for finding LDAP Injection (CWE-90) vulnerabilities in Java |
| [1401444](https://hackerone.com/reports/1401444) | GitLab |  | $3,000 | 50 | 2022-04-12 | OS Command Injection | RCE via WikiCloth markdown rendering if the `rubyluabridge` gem is installed |
| [3861550](https://hackerone.com/reports/3861550) | 8x8 | critical | $3,000 | 49 | 2026-09-01 | Deserialization of Untrusted Data | connect.8x8.com: Deserialization Vulnerability  in Automation Builder via Jint→Newtonsoft serializer coercion (TypeNameHandling) |
| [1728174](https://hackerone.com/reports/1728174) | Kubernetes | high | $2,500 | 57 | 2023-11-24 | Code Injection | Ingress nginx annotation injection causes arbitrary command execution |
| [1620702](https://hackerone.com/reports/1620702) | Kubernetes | high | $2,500 | 47 | 2023-10-26 | Code Injection | RCE  on ingress-nginx-controller via Ingress spec.rules.http.paths.path field |
| [2039464](https://hackerone.com/reports/2039464) | Kubernetes | high | $2,500 | 40 | 2023-10-25 | Code Injection | Code inject via nginx.ingress.kubernetes.io/permanent-redirect annotation |
| [956295](https://hackerone.com/reports/956295) | GitHub Security Lab |  | $2,500 | 29 |  | Code Injection | LDAP injection vulnerability in Java |
| [666062](https://hackerone.com/reports/666062) | MyEtherWallet |  | $2,500 | 9 |  | Code Injection | Malicious Node JavaScript Injection Leading to Theft of Private Keys and User Funds |
| [1891795](https://hackerone.com/reports/1891795) | Internet Bug Bounty | medium | $2,400 | 30 | 2023-03-18 | Code Injection | RCE vulnerability in apache-airflow-providers-apache-sqoop 3.1.0 |
| [892465](https://hackerone.com/reports/892465) | GitHub Security Lab |  | $2,300 | 28 |  | Code Injection | CodeQL query to detect JNDI injections |
| [896298](https://hackerone.com/reports/896298) | GitHub Security Lab |  | $2,300 | 13 |  | Code Injection | CodeQL query for SpEL injections |
| [1928279](https://hackerone.com/reports/1928279) | GitHub Security Lab |  | $2,300 | 13 |  | Code Injection | [Ruby]: Server Side Template Injection |
| [894870](https://hackerone.com/reports/894870) | GitHub Security Lab |  | $2,300 | 4 |  | Code Injection | CodeQL query for MVEL injections |
| [917455](https://hackerone.com/reports/917455) | GitHub Security Lab |  | $2,300 | 2 |  | Code Injection | CodeQL query to detect OGNL injections |
| [821962](https://hackerone.com/reports/821962) | Razer |  | $2,000 | 676 |  | OS Command Injection | 🐞 OS Command Injection at https://sea-web.gold.razer.com/lab/ws-lookup via IP parameter |
| [1044716](https://hackerone.com/reports/1044716) | Eternal | critical | $2,000 | 229 | 2021-02-22 | Code Injection | SQL Injection in www.hyperpure.com |
| [703910](https://hackerone.com/reports/703910) | Mail.ru |  | $2,000 | 163 |  | Command Injection - Generic | JMX RMI command injection on 195.211.131.82(Mail.ru Gaming) |
| [536130](https://hackerone.com/reports/536130) | Mail.ru |  | $2,000 | 152 |  | Code Injection | Path traversal, SSTI and RCE on a MailRu acquisition |
| [540242](https://hackerone.com/reports/540242) | Uber | critical | $2,000 | 80 | 2021-02-24 | Command Injection - Generic | Pre-auth Remote Code Execution on multiple Uber SSL VPN servers |
| [298873](https://hackerone.com/reports/298873) | GitLab | critical | $2,000 | 50 | 2018-04-27 | Command Injection - Generic | Command injection by overwriting authorized_keys file through GitLab import |
| [402362](https://hackerone.com/reports/402362) | pixiv | critical | $2,000 | 44 | 2021-03-16 | Code Injection | RCE due to ImageTragick v2 |
| [1705717](https://hackerone.com/reports/1705717) | Linux Foundation Decentralized Trust | critical | $2,000 | 39 | 2022-10-20 | Command Injection - Generic | POOL_UPGRADE request handler may allow an unauthenticated attacker to remotely execute code on every node in the network. |
| [1652042](https://hackerone.com/reports/1652042) | Internet Bug Bounty | high | $2,000 | 14 | 2022-09-10 | Code Injection | CVE-2022-21831: Possible code injection vulnerability in Rails / Active Storage |
| [125218](https://hackerone.com/reports/125218) | Uber |  | $2,000 | 8 | 2016-05-26 | Command Injection - Generic | Bypassing Uber Partner's 3 Cancel Limit |
| [1368720](https://hackerone.com/reports/1368720) | GitHub Security Lab |  | $1,800 | 7 |  |  | [Java] CWE-502: Unsafe deserialization with three JSON frameworks |
| [1204660](https://hackerone.com/reports/1204660) | GitHub Security Lab |  | $1,800 | 6 |  | Code Injection | [Java] CWE-094: Rhino code injection |
| [852316](https://hackerone.com/reports/852316) | GitHub Security Lab |  | $1,800 | 4 |  | Code Injection | Go/CWE-643: XPath Injection Query in Go |
| [1175842](https://hackerone.com/reports/1175842) | GitHub Security Lab |  | $1,800 | 4 |  | Code Injection | [Java] Query for detecting Jakarta Expression Language injections |
| [1204659](https://hackerone.com/reports/1204659) | GitHub Security Lab |  | $1,800 | 4 |  | Code Injection | [Java] CWE-094: Jython code injection |
| [1241579](https://hackerone.com/reports/1241579) | GitHub Security Lab |  | $1,800 | 4 |  |  | Java: CodeQL query for unsafe RMI deserialization |
| [1483918](https://hackerone.com/reports/1483918) | GitHub Security Lab |  | $1,800 | 4 |  | Code Injection | [Java]: CWE-073 - File path injection with the JFinal framework |
| [1219492](https://hackerone.com/reports/1219492) | GitHub Security Lab |  | $1,800 | 3 |  | Code Injection | [Java]: CWE-730 Regex injection |
| [974368](https://hackerone.com/reports/974368) | GitHub Security Lab |  | $1,800 | 1 |  | Code Injection | CodeQL query to detect XSLT injections |
| [833080](https://hackerone.com/reports/833080) | Slack | high | $1,500 | 101 | 2020-06-30 | Unrestricted Upload of File with Dangerous Type | Tricking the "Create snippet" feature into displaying the wrong filetype can lead to RCE on Slack users |
| [458842](https://hackerone.com/reports/458842) | Valve | high | $1,500 | 99 | 2020-02-24 | Malware | Malformed save files (.sav) allow to write files with arbitrary extensions and content in GoldSrc-based games. |
| [274990](https://hackerone.com/reports/274990) | RubyGems | critical | $1,500 | 51 | 2017-11-09 | Deserialization of Untrusted Data | Remote code execution on rubygems.org |
| [202949](https://hackerone.com/reports/202949) | Pornhub |  | $1,500 | 48 |  | Command Injection - Generic | Wordpress Content injection |
| [473888](https://hackerone.com/reports/473888) | Ruby on Rails | high | $1,500 | 41 | 2019-03-13 | Command Injection - Generic | RCE which may occur due to `ActiveSupport::MessageVerifier` or `ActiveSupport::MessageEncryptor` (especially Active storage) |
| [142352](https://hackerone.com/reports/142352) | Pornhub |  | $1,500 | 16 |  | Code Injection | (Pornhub & Youporn & Brazzers ANDROID APP) : Upload Malicious APK / Overrite Existing APK  / Android BackOffice Access |
| [113928](https://hackerone.com/reports/113928) | Ruby on Rails |  | $1,500 | 7 | 2016-03-01 | Code Injection | Remote code execution using render :inline |
| [98259](https://hackerone.com/reports/98259) | Shopify |  | $1,500 | 6 | 2015-11-10 | Code Injection | 'Limited' RCE in certain places where Liquid is accepted |
| [163292](https://hackerone.com/reports/163292) | Dropbox |  | $1,458 | 13 |  | Command Injection - Generic | Subtile Code Injection Vulnerability in Dropbox for Windows |
| [1391549](https://hackerone.com/reports/1391549) | Internet Bug Bounty | medium | $1,200 | 22 | 2021-11-04 | Code Injection | Request line injection via HTTP/2 in Apache mod_proxy |
| [1624137](https://hackerone.com/reports/1624137) | U.S. Dept Of Defense | critical | $1,000 | 94 | 2022-11-18 | Command Injection - Generic | LOGJ4 VUlnerability [HtUS] |
| [152398](https://hackerone.com/reports/152398) | Internet Bug Bounty |  | $1,000 | 81 | 2019-11-12 | Code Injection | In correct casting from size_t to int lead to heap overflow in mcrypt_generic |
| [1425474](https://hackerone.com/reports/1425474) | Acronis | critical | $1,000 | 76 | 2022-07-13 | Deserialization of Untrusted Data | [CVE-2021-44228] nps.acronis.com is vulnerable to the recent log4shell 0-day |
| [1167773](https://hackerone.com/reports/1167773) | Kubernetes | medium | $1,000 | 45 | 2021-08-07 | Deserialization of Untrusted Data | Loading YAML in Java client can lead to command execution |
| [317043](https://hackerone.com/reports/317043) | Mail.ru |  | $1,000 | 36 |  | OS Command Injection | Shell upload in http://widget.support.my.com/ |
| [1360208](https://hackerone.com/reports/1360208) | Mail.ru |  | $1,000 | 34 |  | OS Command Injection | OS command injection on seedr.ru |
| [380594](https://hackerone.com/reports/380594) | Augur |  | $1,000 | 32 |  | Code Injection | Full UI hijack via dormant browser service workers |
| [1624172](https://hackerone.com/reports/1624172) | U.S. Dept Of Defense | critical | $1,000 | 28 | 2023-01-06 | Code Injection | [███████] Remote Code Execution at ██████ [CVE-2021-44529] [HtUS] |
| [152399](https://hackerone.com/reports/152399) | Internet Bug Bounty |  | $1,000 | 14 | 2019-11-12 | Code Injection | php curl ext size_t overflow lead to heap corruption |
| [116286](https://hackerone.com/reports/116286) | Internet Bug Bounty |  | $1,000 | 13 | 2016-09-20 | Code Injection | Type confusion in partial.setstate, partial_repr, partial_call leads to memory corruption, reliable control flow hijack |
| [152400](https://hackerone.com/reports/152400) | Internet Bug Bounty |  | $1,000 | 12 | 2019-11-12 | Code Injection | php mcrypt ext - In correct casting from size_t to int lead to heap overflow in mdecrypt_generic |
| [99424](https://hackerone.com/reports/99424) | Uber |  | $1,000 | 10 | 2016-05-09 | Code Injection | Mass Assignment Vulnerability in partners.uber.com |
| [1807214](https://hackerone.com/reports/1807214) | Kubernetes | medium | $1,000 | 10 | 2023-04-25 | Code Injection | The `io.kubernetes.client.util.generic.dynamic.Dynamics` contains a code execution vulnerability due to SnakeYAML |
| [1443028](https://hackerone.com/reports/1443028) | GitHub Security Lab |  | $1,000 | 9 |  | Code Injection | Java: Regex injection |
| [801230](https://hackerone.com/reports/801230) | GitHub Security Lab |  | $1,000 | 5 |  | Code Injection | CodeQL query for finding ReDoS and Regex Injection vulnerabilities in Java |
| [127212](https://hackerone.com/reports/127212) | Internet Bug Bounty |  | $1,000 | 3 | 2016-05-01 | Code Injection | php_snmp_error() Format String Vulnerability |
| [114078](https://hackerone.com/reports/114078) | Internet Bug Bounty |  | $1,000 | 1 | 2019-11-12 | Code Injection | Use-after-free vulnerability in SPL(ArrayObject, unserialize) |
| [114079](https://hackerone.com/reports/114079) | Internet Bug Bounty |  | $1,000 | 1 | 2019-11-12 | Code Injection | Use-after-free vulnerability in SPL(SplObjectStorage, unserialize) |
| [167688](https://hackerone.com/reports/167688) | Internet Bug Bounty |  | $1,000 | 1 | 2016-09-20 | Code Injection | msilib.OpenDatabase Type Confusion |
| [106548](https://hackerone.com/reports/106548) | Internet Bug Bounty |  | $1,000 | 0 | 2016-01-10 | Code Injection | Format string vulnerability in zend_throw_or_error() |
| [1692603](https://hackerone.com/reports/1692603) | 8x8 | high | $777 | 51 | 2023-02-10 | OS Command Injection | Jitsi Desktop Client RCE By Interacting with Malicious URL Schemes on Windows |
| [1109620](https://hackerone.com/reports/1109620) | New Relic |  | $768 | 39 |  | Deserialization of Untrusted Data | Untrusted deserialization issue when loading newrelic.yml file in Java agent leads to code execution on host |
| [1644062](https://hackerone.com/reports/1644062) | Linktree | medium | $750 | 33 | 2022-09-15 | Unrestricted Upload of File with Dangerous Type | No validation to Image upload user can upload ( php APK zip files and can be used as storage purpose) |
| [411329](https://hackerone.com/reports/411329) | Valve | medium | $750 | 28 | 2019-01-07 | Code Injection | code injection, steam chat client |
| [702252](https://hackerone.com/reports/702252) | Razer |  | $750 | 26 |  | Code Injection | DLL Hijacking in Synapse 2  CrashSender1402.exe via version.dll |
| [1974296](https://hackerone.com/reports/1974296) | Valve | high | $750 | 18 | 2023-08-01 | Code Injection | Steam Deck Single Click Root Remote Code Execution |
| [784714](https://hackerone.com/reports/784714) | Slack | medium | $750 | 10 | 2020-04-01 | Command Injection - Generic | Relative Path Vulnerability Results in Arbitrary Command Execution/Privilege Escalation |
| [769684](https://hackerone.com/reports/769684) | Razer |  | $750 | 3 |  | Code Injection | User Access Control Bypass Via Razer elevated service ( RzKLService.exe ) which loads  exe in misconfigured way. |
| [410237](https://hackerone.com/reports/410237) | Vanilla |  | $600 | 39 |  | Deserialization of Untrusted Data | Vanilla Forums ImportController index file_exists Unserialize Remote Code Execution Vulnerability |
| [410882](https://hackerone.com/reports/410882) | Vanilla |  | $600 | 32 |  | Deserialization of Untrusted Data | Vanilla Forums domGetImages getimagesize Unserialize Remote Code Execution Vulnerability (critical) |
| [407552](https://hackerone.com/reports/407552) | Vanilla |  | $600 | 25 |  | Deserialization of Untrusted Data | Vanilla Forums Gdn_Format unserialize() Remote Code Execution Vulnerability |
| [2293731](https://hackerone.com/reports/2293731) | Internet Bug Bounty | low | $540 | 39 | 2024-02-28 | Code Injection | Command Injection using malicious hostname in expanded proxycommand |
| [214022](https://hackerone.com/reports/214022) | Discourse | high | $512 | 45 | 2017-05-13 | Command Injection - Generic | Admin Command Injection via username in user_archive ExportCsvFile |
| [134321](https://hackerone.com/reports/134321) | Algolia |  | $500 | 74 | 2016-10-01 | Code Injection | RCE on facebooksearch.algolia.com |
| [154096](https://hackerone.com/reports/154096) | Uber |  | $500 | 56 | 2016-08-08 | Command Injection - Generic | Blind OOB XXE At "http://ubermovement.com/" |
| [2221404](https://hackerone.com/reports/2221404) | Mozilla | low | $500 | 56 | 2024-12-08 | Code Injection | RCE on worker host due to unsanitized "env" variable name in task definition on community-tc.services.mozilla.com |
| [1748961](https://hackerone.com/reports/1748961) | MetaMask | medium | $500 | 40 | 2023-01-04 | Command Injection - Generic | CSV Injection at https://assets-paris-demo.codefi.network/ |
| [146593](https://hackerone.com/reports/146593) | Pornhub |  | $500 | 38 |  | Command Injection - Generic | RCE Possible Via Video Manager Export using @ character in Video Title |
| [369557](https://hackerone.com/reports/369557) | Mail.ru |  | $500 | 25 |  | Code Injection | Shell upload in partner service |
| [683318](https://hackerone.com/reports/683318) | Internet Bug Bounty | low | $500 | 13 | 2019-09-24 | Code Injection | Windows builds with insecure path defaults (CVE-2019-1552) |
| [304545](https://hackerone.com/reports/304545) | Mail.ru |  | $500 | 12 |  | Code Injection | Возможность залить шелл на https://widget.operator.mail.ru |
| [46019](https://hackerone.com/reports/46019) | Ruby on Rails | high | $500 | 9 | 2016-02-12 | Code Injection | Explicit, dynamic render path: Dir. Trav + RCE |
| [226335](https://hackerone.com/reports/226335) | RubyGems | low | $500 | 6 | 2017-08-30 | Command Injection - Generic | Escape sequence injection in "summary" field |
| [159958](https://hackerone.com/reports/159958) | Internet Bug Bounty |  | $500 | 5 | 2019-11-12 | Code Injection | Integer overflow lead to heap corruption in sql_regcase |
| [159961](https://hackerone.com/reports/159961) | Internet Bug Bounty |  | $500 | 5 | 2019-11-12 | Code Injection | integer overflow in php_uuencode caused heap corruption |
| [159959](https://hackerone.com/reports/159959) | Internet Bug Bounty |  | $500 | 4 | 2019-11-12 | Code Injection | integer overflow in quoted_printable_encode caused heap corruption |
| [159960](https://hackerone.com/reports/159960) | Internet Bug Bounty |  | $500 | 4 | 2019-11-12 | Code Injection | integer overflow in urlencode caused heap corruption |
| [182169](https://hackerone.com/reports/182169) | Internet Bug Bounty | low | $500 | 4 | 2016-12-03 | Code Injection | Type confusion in FutureIter_throw() which may potentially lead to an arbitrary code execution |
| [180814](https://hackerone.com/reports/180814) | Internet Bug Bounty | low | $500 | 3 | 2019-11-12 | Code Injection | crash in locale_compose() function |
| [39428](https://hackerone.com/reports/39428) | Phabricator |  | $500 | 2 | 2015-01-14 | Code Injection | Phabricator Phame Blog Skins Local File Inclusion |
| [73257](https://hackerone.com/reports/73257) | Internet Bug Bounty |  | $500 | 1 | 2015-05-18 |  | PHP yaml_parse/yaml_parse_file/yaml_parse_url Unsafe Deserialization |
| [126652](https://hackerone.com/reports/126652) | Internet Bug Bounty |  | $500 | 1 | 2019-10-13 | Code Injection | potential remote code execution with phar archive |
| [175260](https://hackerone.com/reports/175260) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Code Injection | missing NULL check in dom_document_save_html |
| [175262](https://hackerone.com/reports/175262) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Code Injection | NULL pointer dereference in SimpleXMLElement::asXML() |
| [175263](https://hackerone.com/reports/175263) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Code Injection | crash in openssl_random_pseudo_bytes function |
| [175264](https://hackerone.com/reports/175264) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Code Injection | heap overflow in php_ereg_replace function |
| [180115](https://hackerone.com/reports/180115) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Code Injection | crash in locale_get_keywords() when keyword value in locale string too long |
| [180116](https://hackerone.com/reports/180116) | Internet Bug Bounty | low | $500 | 1 | 2019-11-12 | Code Injection | another crash in locale_get_keywords function |
| [42236](https://hackerone.com/reports/42236) | X / xAI |  | $420 | 4 | 2015-01-01 | Code Injection | URGENT - Subdomain Takeover on users.tweetdeck.com , the same issue  of report #32825 |
| [60573](https://hackerone.com/reports/60573) | Mail.ru |  | $400 | 1 |  | Code Injection | http://fitter1.i.mail.ru/browser/ торчит Graphite в мир |
| [895696](https://hackerone.com/reports/895696) | GSA Bounty | medium | $300 | 61 | 2020-07-10 | Use of Inherently Dangerous Function | Blind SSRF on https://labs.data.gov/dashboard/Campaign/json_status/ Endpoint |
| [895972](https://hackerone.com/reports/895972) | GSA Bounty | medium | $300 | 48 | 2020-07-09 | Remote File Inclusion | Limited LFI |
| [410212](https://hackerone.com/reports/410212) | Vanilla |  | $300 | 24 |  | Deserialization of Untrusted Data | Vanilla Forums Xenforo password splitHash Unserialize Remote Code Execution Vulnerability |
| [174474](https://hackerone.com/reports/174474) | Harvest |  | $300 | 15 |  | Command Injection - Generic | Cookie Injection at 'harvestapp.com' |
| [186352](https://hackerone.com/reports/186352) | Phabricator |  | $300 | 8 | 2016-12-29 | Code Injection | Fetching binaries (for software installation) over HTTP without verification (RCE as ROOT by MITM) |
| [49408](https://hackerone.com/reports/49408) | Mail.ru |  | $300 | 3 |  | Command Injection - Generic | RCE через JDWP |
| [808862](https://hackerone.com/reports/808862) | Visma Public |  | $250 | 268 |  | Unrestricted Upload of File with Dangerous Type | Unrestricted file upload leads to Stored XSS |
| [788397](https://hackerone.com/reports/788397) | Visma Public |  | $250 | 57 |  | Unrestricted Upload of File with Dangerous Type | Unrestricted file upload when creating quotes allows for Stored XSS |
| [2307625](https://hackerone.com/reports/2307625) | Nextcloud |  | $250 | 37 | 2024-06-14 | Code Injection | Code injection in Nextcloud Desktop Client for macOS |
| [1019389](https://hackerone.com/reports/1019389) | Basecamp | medium | $250 | 29 | 2021-04-22 | Code Injection | Lack of quarantine macOS attribute(com.apple.quarantine) leads multiple issues including RCE |
| [1461194](https://hackerone.com/reports/1461194) | Slack | low | $250 | 28 | 2022-05-19 | Code Injection | Email html Injection |
| [950180](https://hackerone.com/reports/950180) | New Relic |  | $250 | 25 |  | Code Injection | HTML injection at Alert email |
| [1051192](https://hackerone.com/reports/1051192) | Kubernetes | low | $250 | 17 | 2021-05-01 | Code Injection | Code Injection via Insecure Yaml.load |
| [232499](https://hackerone.com/reports/232499) | Rockstar Games | low | $250 | 7 | 2017-06-23 | Code Injection | Control characters incorrectly handled on Crew Status Update |
| [801370](https://hackerone.com/reports/801370) | Linux Foundation Decentralized Trust | medium | $200 | 12 | 2022-08-06 | Deserialization of Untrusted Data | RCE vulnerability in Hyperledger Fabric SDK for Java |
| [67317](https://hackerone.com/reports/67317) | VK.com |  | $200 | 8 | 2017-02-13 | Code Injection | Уязвимость получения всех номеров телефонов вк (по совместительству логинов профилей) |
| [122932](https://hackerone.com/reports/122932) | Mail.ru |  | $200 | 6 |  | Code Injection | bgplay.mail.ru |
| [66235](https://hackerone.com/reports/66235) | VK.com |  | $200 | 3 | 2015-09-07 | Code Injection | Уязвимость в Указание мест на фото + фича + хакинг |
| [62531](https://hackerone.com/reports/62531) | Mail.ru |  | $200 | 2 |  | Code Injection | tt-mac.i.mail.ru: Quagga 0.99.23.1 (Router) : Default password and default enable password |
| [67161](https://hackerone.com/reports/67161) | Mail.ru |  | $200 | 1 |  | Code Injection | Possible xWork classLoader RCE: shared.mail.ru |
| [97657](https://hackerone.com/reports/97657) | Slack |  | $200 | 1 | 2015-11-11 | Command Injection - Generic | File upload XSS (Java applet) on http://slackatwork.com/ |
| [743345](https://hackerone.com/reports/743345) | Eternal | low | $150 | 26 | 2021-09-07 | Code Injection | HTML injection leads to reflected XSS |
| [1072857](https://hackerone.com/reports/1072857) | Mail.ru |  | $150 | 7 |  | OS Command Injection | [titans.3clans.ru] phpBB 3.0.8 - Захват аккаунта администратора + удалённое выполнение кода. |
| [1215263](https://hackerone.com/reports/1215263) | Nextcloud | medium | $125 | 10 | 2021-08-11 | Code Injection | Download of file with arbitrary extension via injection into attachment header |
| [622170](https://hackerone.com/reports/622170) | Nextcloud | medium | $100 | 59 | 2020-08-05 | Code Injection | Arbitrary code execution in desktop client via OpenSSL config |
| [1456063](https://hackerone.com/reports/1456063) | Basecamp | low | $100 | 30 | 2022-04-26 | Deserialization of Untrusted Data | RCE via exposed JMX server on jabber.37signals.com/jabber.basecamp.com |
| [720306](https://hackerone.com/reports/720306) | Nextcloud | critical | $100 | 16 | 2020-03-14 | Code Injection | Docker image with FPM is vulnerable to CVE-2019-11043 |
| [1763704](https://hackerone.com/reports/1763704) | Kubernetes | low | $100 | 14 | 2023-05-25 | Code Injection | Git Arg Injection in  kubernetes-sigs/release-sdk |
| [138824](https://hackerone.com/reports/138824) | LocalTapiola |  | $100 | 11 |  | Code Injection | Remote Code Execution in NovaStor NovaBACKUP DataCenter backup software (Hiback) |
| [232347](https://hackerone.com/reports/232347) | Nextcloud | low | $100 | 10 | 2018-07-29 | Code Injection | [FG-VD-17-063] NextCloud Insufficient Attack Protection Vulnerability Notification |
| [137850](https://hackerone.com/reports/137850) | Pornhub |  | $100 | 8 |  | Command Injection - Generic | CSV Macro injection in Video Manager (CEMI) |
| [105977](https://hackerone.com/reports/105977) | GlassWire |  | $100 | 6 | 2016-02-04 | Code Injection | DLL Hijacking Vulnerability in GlassWireSetup.exe |
| [160520](https://hackerone.com/reports/160520) | Ian Dunn | low | $100 | 4 | 2016-10-12 | Command Injection - Generic | Bypass fix in https://hackerone.com/reports/151516 report. |
| [65330](https://hackerone.com/reports/65330) | VK.com |  | $100 | 1 | 2015-10-30 | Command Injection - Generic | Не достаточная проверка логина скайп |
| [1427589](https://hackerone.com/reports/1427589) | Judge.me | none | $50 | 40 | 2021-12-21 | Code Injection | Log4j RCE on https://judge.me/reviews |
| [158016](https://hackerone.com/reports/158016) | Instacart |  | $50 | 21 | 2016-10-12 | Code Injection | Server side request forgery on image upload for lists |
| [277525](https://hackerone.com/reports/277525) | Ian Dunn | medium | $50 | 13 | 2017-10-23 | Command Injection - Generic | Formula injection via CSV exports in WordCamp Talks plugin |
| [151475](https://hackerone.com/reports/151475) | ownCloud |  | $50 | 5 | 2016-08-31 | Code Injection | ownCloud 2.2.2.6192 DLL Hijacking Vulnerability |
| [57914](https://hackerone.com/reports/57914) | Enter |  | $50 | 1 | 2015-11-26 | Command Injection - Generic | HTML injection in email sent by romit.io |
| [257335](https://hackerone.com/reports/257335) | Unikrn | low | $25 | 56 | 2019-03-04 | Remote File Inclusion | ssh: unprivileged users may hijack due to backdated ssh version open port found(███.unikrn.com) |
| [422944](https://hackerone.com/reports/422944) | Shopify | medium | - | 830 | 2020-02-06 | Command Injection - Generic | H1514 Remote Code Execution on kitcrm using bulk customer update of Priority Products |
| [403417](https://hackerone.com/reports/403417) | Semrush | critical | - | 824 | 2019-06-24 | Command Injection - Generic | Remote Code Execution on www.semrush.com/my_reports on Logo upload |
| [506646](https://hackerone.com/reports/506646) | Starbucks | critical | - | 688 | 2019-11-13 | OS Command Injection | Webshell via File Upload on ecjobs.starbucks.com.cn |
| [502758](https://hackerone.com/reports/502758) | Starbucks | critical | - | 572 | 2019-04-10 | Code Injection | RCE and Complete Server Takeover of http://www.█████.starbucks.com.sg/ |
| [544928](https://hackerone.com/reports/544928) | Ubiquiti Inc. | critical | - | 553 | 2019-11-08 | Command Injection - Generic | Privilege Escalation From user to SYSTEM via unauthenticated command execution |
| [180074](https://hackerone.com/reports/180074) | Paragon Initiative Enterprises | none | - | 549 | 2016-11-04 | Command Injection - Generic | BAD Code ! |
| [783877](https://hackerone.com/reports/783877) | Slack | critical | - | 509 | 2020-08-28 | Code Injection | Remote Code Execution in Slack desktop apps + bonus |
| [816254](https://hackerone.com/reports/816254) | QIWI |  | - | 475 |  | Code Injection | SQL injection on contactws.contact-sys.com in TScenObject action ScenObjects leads to remote code execution |
| [631956](https://hackerone.com/reports/631956) | Valve | critical | - | 420 | 2019-10-08 | Code Injection | Panorama UI XSS leads to Remote Code Execution via Kick/Disconnect Message |
| [423541](https://hackerone.com/reports/423541) | Shopify |  | - | 409 | 2019-04-04 | Code Injection | H1514 Server Side Template Injection in Return Magic email templates? |
| [1858574](https://hackerone.com/reports/1858574) | HackerOne | critical | - | 371 | 2023-03-16 | Remote File Inclusion | [CVE-2022-44268] Arbitrary Remote Leak via ImageMagick |
| [946409](https://hackerone.com/reports/946409) | Yelp | critical | - | 366 | 2021-02-09 | Download of Code Without Integrity Check | RCE on build server via misconfigured pip install |
| [748123](https://hackerone.com/reports/748123) | Mail.ru |  | - | 343 |  | Remote File Inclusion | SSRF & LFR via on city-mobil.ru |
| [487008](https://hackerone.com/reports/487008) | Flickr | critical | - | 340 | 2020-01-25 | Code Injection | Arbitrary file read via ffmpeg HLS parser at https://www.flickr.com/photos/upload |
| [851807](https://hackerone.com/reports/851807) | Nextcloud | high | - | 317 | 2020-06-02 | Code Injection | Code injection possible with malformed Nextcloud Talk chat commands |
| [1024575](https://hackerone.com/reports/1024575) | TikTok | critical | - | 312 | 2021-04-15 | Code Injection | RCE on TikTok Ads Portal |
| [1672388](https://hackerone.com/reports/1672388) | GitLab | critical | - | 271 | 2022-11-16 | OS Command Injection | RCE via github import |
| [396954](https://hackerone.com/reports/396954) | Rootstock Labs | critical | - | 258 | 2019-09-18 | Deserialization of Untrusted Data | Attacker can add arbitrary data to the blockchain without paying gas |
| [212696](https://hackerone.com/reports/212696) | Imgur | critical | - | 229 | 2017-04-26 | Command Injection - Generic | RCE by command line argument injection to `gm convert` in `/edit/process?a=crop` |
| [713900](https://hackerone.com/reports/713900) | QIWI |  | - | 221 |  | Code Injection | Unauthenticated SSRF in jira.tochka.com leading to RCE in confluence.bank24.int |
| [303061](https://hackerone.com/reports/303061) | LocalTapiola |  | - | 209 |  | OS Command Injection | RCE using bash command injection on /system/images (toimitilat.lahitapiola.fi) |
| [329689](https://hackerone.com/reports/329689) | Mapbox | critical | - | 209 | 2020-07-28 | Command Injection - Generic | Test-scripts for postgis in mason-repository using unsafe unzip of content from unclaimed bucket creates potential RCE-issues |
| [816086](https://hackerone.com/reports/816086) | QIWI |  | - | 194 |  | Code Injection | Remote Code Execution on contactws.contact-sys.com via SQL injection in TCertObject operation "Delete" |
| [412021](https://hackerone.com/reports/412021) | ██████ |  | - | 184 |  | Code Injection | Remote Command execution due to image tragick |
| [971386](https://hackerone.com/reports/971386) | Google |  | - | 171 |  | Code Injection | CVE-2020-8913 - Persistent arbitrary code execution in Android's Google Play Core Library: details, explanation and the PoC |
| [783360](https://hackerone.com/reports/783360) | Stripo Inc | critical | - | 158 | 2020-01-31 | Exposed Dangerous Method or Function | Open memory dump method leaking customer information ,secret keys , password , source code & admin accounts |
| [514664](https://hackerone.com/reports/514664) | 50m-ctf |  | - | 152 |  | Command Injection - Generic | $50 million CTF Writeup |
| [983548](https://hackerone.com/reports/983548) | QIWI |  | - | 148 |  | Deserialization of Untrusted Data | MobileIron Unauthenticated RCE on mdm.qiwi.com with WAF bypass |
| [2483422](https://hackerone.com/reports/2483422) | HackerOne | medium | - | 138 | 2024-07-23 | Remote File Inclusion | Payload delivery via Social Media urls on H1 profile |
| [2516732](https://hackerone.com/reports/2516732) | Basecamp | medium | - | 136 | 2024-05-30 | Deserialization of Untrusted Data | Account takeover via insecure intent handling |
| [824689](https://hackerone.com/reports/824689) | GitLab | medium | - | 135 | 2020-07-27 | Command Injection - Generic | Send arbitrary PUT requests when user clicks on a link |
| [546753](https://hackerone.com/reports/546753) | Nextcloud | high | - | 124 | 2019-05-30 | OS Command Injection | Remote Code Execution via Extract App Plugin |
| [164224](https://hackerone.com/reports/164224) | Unikrn |  | - | 122 | 2017-08-17 | Code Injection | Urgent: Server side template injection via Smarty template allows for RCE |
| [1001255](https://hackerone.com/reports/1001255) | Nord Security |  | - | 120 |  | OS Command Injection | Possible RCE through Windows Custom Protocol on Windows client |
| [206227](https://hackerone.com/reports/206227) | Imgur | critical | - | 119 | 2017-04-16 | Code Injection | Remote Code Execution on Git.imgur-dev.com |
| [210741](https://hackerone.com/reports/210741) | Rockstar Games | critical | - | 119 | 2017-12-13 | Code Injection | Unserialize leading to arbitrary PHP function invoke |
| [1842674](https://hackerone.com/reports/1842674) | Krisp | critical | - | 119 | 2023-02-22 | Deserialization of Untrusted Data | SQL Injection + Insecure Deserialization leads to Remote Code Execution on https://krisp.ai |
| [768266](https://hackerone.com/reports/768266) | U.S. Dept Of Defense | critical | - | 118 | 2020-01-31 | Code Injection | Public instance of Jenkins on https://██████████/ with /script enabled |
| [816560](https://hackerone.com/reports/816560) | QIWI |  | - | 118 |  | Code Injection | SQL injection on contactws.contact-sys.com in TRateObject.AddForOffice in USER_ID parameter leads to remote code execution |
| [1890284](https://hackerone.com/reports/1890284) | TikTok | medium | - | 118 | 2023-04-12 | Unrestricted Upload of File with Dangerous Type | Unrestricted File Upload on https://partner.tiktokshop.com/wsos_v2/oec_partner/upload |
| [768322](https://hackerone.com/reports/768322) | Concrete CMS | medium | - | 114 | 2020-07-21 | Code Injection | Remote Code Execution (Reverse Shell) - File Manager |
| [2083771](https://hackerone.com/reports/2083771) | U.S. Dept Of Defense | critical | - | 114 | 2024-12-18 | Command Injection - Generic | Remote Code Execution and AWS IAM Credentials Exfiltration in https://████████/ |
| [3637898](https://hackerone.com/reports/3637898) | AWS VDP | high | - | 111 | 2026-07-06 | OS Command Injection | OS Command Injection in `aws-cdk-lib` NodejsFunction via Unsanitized `OsCommand` Helper (Supply Chain RCE) |
| [816156](https://hackerone.com/reports/816156) | Slack | high | - | 107 | 2021-05-09 | Code Injection | Team members can trigger arbitrary code execution in Slack Desktop Apps via HTML Notifications |
| [1072832](https://hackerone.com/reports/1072832) | U.S. Dept Of Defense | critical | - | 104 | 2023-05-15 | Code Injection | [hta3] Remote Code Execution on ████ |
| [191884](https://hackerone.com/reports/191884) | X / xAI | low | - | 100 | 2017-02-26 | Code Injection | Remote Unrestricted file Creation/Deletion and Possible RCE. |
| [495382](https://hackerone.com/reports/495382) | Notepad++ | medium | - | 99 | 2019-06-06 | Command Injection - Generic | No SearchEngine sanatizing can lead to command injection |
| [666716](https://hackerone.com/reports/666716) | ok.ru | critical | - | 98 | 2019-09-20 | Command Injection - Generic | [insideok.ru] Remote Command Execution via file upload. |
| [470637](https://hackerone.com/reports/470637) | Slack | high | - | 97 | 2019-09-14 | Code Injection | User-assisted RCE in Slack for macOS (from official site) due to improper quarantine meta-attribute handling for downloaded files |
| [710864](https://hackerone.com/reports/710864) | U.S. Dept Of Defense | critical | - | 94 | 2020-05-11 | OS Command Injection | Remote Code Execution in ██████ |
| [453791](https://hackerone.com/reports/453791) | PayPal | medium | - | 93 | 2021-04-30 | Deserialization of Untrusted Data | Unsafe deserialization leads to token leakage in PayPal & PayPal for Business [Android] |
| [2701701](https://hackerone.com/reports/2701701) | Kubernetes | high | - | 91 | 2026-03-07 | Code Injection | Injection in path parameter of Ingress-nginx |
| [2325023](https://hackerone.com/reports/2325023) | GitHub | high | - | 88 | 2024-09-17 | Command Injection - Generic | Management Console Editor Privilege Escalation to Root SSH Access in GitHub Enterprise Server via RCE in ghe-update-check |
| [2182202](https://hackerone.com/reports/2182202) | MTN Group | critical | - | 87 | 2024-10-09 | Code Injection | Remote code execution [CVE-2023-36845] |
| [3014158](https://hackerone.com/reports/3014158) | PortSwigger Web Security | high | - | 85 | 2025-02-26 | Code Injection | Burp Suite extensions can execute arbitrary code |
| [248116](https://hackerone.com/reports/248116) | U.S. Dept Of Defense | critical | - | 84 | 2019-10-04 | Code Injection | Remote Code Execution (RCE) in a DoD website |
| [403083](https://hackerone.com/reports/403083) | Automattic | high | - | 84 | 2019-12-19 | Deserialization of Untrusted Data | Authenticated Code Execution through Phar deserialization in CSV Importer as Shop manager in WooCommerce |
| [1104120](https://hackerone.com/reports/1104120) | QIWI |  | - | 84 |  | Code Injection | Remote Code Execution on contactws.contact-sys.com via SQL injection in TAktifBankObject.GetOrder in parameter DOC_ID |
| [1104693](https://hackerone.com/reports/1104693) | Mail.ru |  | - | 84 |  | Command Injection - Generic | [app-01.youdrive.club] RCE in CI/CD via dependency confusion |
| [2248328](https://hackerone.com/reports/2248328) | Nextcloud | critical | - | 83 | 2023-12-28 | Deserialization of Untrusted Data | RCE on Wordpress website |
| [401136](https://hackerone.com/reports/401136) | ██████ |  | - | 80 |  | Code Injection | Remote Code Execution on Proxy Service (as root) |
| [2332623](https://hackerone.com/reports/2332623) | GitHub | high | - | 80 | 2024-09-13 | Command Injection - Generic | Management Console Editor Privilege Escalation to Root SSH Access in GitHub Enterprise Server via nomad template injection and audit-forward |
| [3088290](https://hackerone.com/reports/3088290) | IBM | critical | - | 80 | 2025-05-02 | Command Injection - Generic | Middleware Authentication Bypass on IBM Portal |
| [1806939](https://hackerone.com/reports/1806939) | LinkedIn | medium | - | 79 | 2023-05-22 | Code Injection | Entire database of emails exposed through URN injection |
| [2357778](https://hackerone.com/reports/2357778) | Mars | critical | - | 78 | 2024-02-19 | Unrestricted Upload of File with Dangerous Type | Unrestricted File Upload at ██████████ |
| [955016](https://hackerone.com/reports/955016) | GitLab | high | - | 77 | 2020-11-04 | OS Command Injection | GitLab-Runner on Windows `DOCKER_AUTH_CONFIG` container host Command Injection |
| [3079738](https://hackerone.com/reports/3079738) | Basecamp | high | - | 77 | 2025-11-11 | Deserialization of Untrusted Data | Two click Account Takeover |
| [1356845](https://hackerone.com/reports/1356845) | Elastic | critical | - | 75 | 2021-10-06 | Code Injection | CVE-2021-40870 on [52.204.160.31] |
| [2978923](https://hackerone.com/reports/2978923) | Autodesk | medium | - | 75 | 2025-04-07 | Code Injection | HTML Injection in Business Name Parameter in Payapps |
| [403402](https://hackerone.com/reports/403402) | Ubiquiti Inc. | critical | - | 74 | 2018-09-10 | Code Injection | Public Jenkins instance with /script enabled |
| [1430622](https://hackerone.com/reports/1430622) | Acronis | critical | - | 74 | 2024-08-28 | OS Command Injection | [forum.acronis.com] JNDI Code Injection due an outdated log4j component |
| [1419213](https://hackerone.com/reports/1419213) | MariaDB | medium | - | 73 | 2022-01-06 | Remote File Inclusion | Grafana LFI on https://grafana.mariadb.org |
| [79348](https://hackerone.com/reports/79348) | Slack |  | - | 72 | 2016-06-24 | Command Injection - Generic | OSX slack:// protocol handler javascript injection |
| [198734](https://hackerone.com/reports/198734) | Internet Bug Bounty | high | - | 68 | 2019-10-13 | Code Injection | GMP Deserialization Type Confusion Vulnerability [MyBB <= 1.8.3 RCE Vulnerability] |
| [576887](https://hackerone.com/reports/576887) | U.S. Dept Of Defense | critical | - | 68 | 2019-07-01 | Code Injection | RCE on █████ via CVE-2017-10271 |
| [60578](https://hackerone.com/reports/60578) | Yahoo! |  | - | 67 |  | Code Injection | YQL: From CR/LF injection to root compromise |
| [1115864](https://hackerone.com/reports/1115864) | Mattermost | high | - | 67 | 2021-06-03 | Code Injection | Persistant Arbitrary code execution in mattermost android |
| [3458235](https://hackerone.com/reports/3458235) | IBM | critical | - | 67 | 2025-12-18 | Code Injection | [RCE] Remote Code Execution via  React Server Components Vulnerability CVE-2025-55182 |
| [2289836](https://hackerone.com/reports/2289836) | MercadoLibre | high | - | 66 | 2024-06-28 | Code Injection | Account Takeover / Arbitrary File read and deletion / Partial code execution (intent redirection) |
| [3122019](https://hackerone.com/reports/3122019) | Fastify | none | - | 66 | 2025-05-28 | Code Injection | Remote Code Execution via unsafe usage of `reply.view({ raw })` in @fastify/view (EJS template engine) |
| [3619288](https://hackerone.com/reports/3619288) | DuckDuckGo | critical | - | 66 | 2026-06-11 | Code Injection | RCE + PAT Exfiltration via pull_request_target in privacy-configuration/auto-respond-pr.yml — Direct Supply Chain to All DDG Browsers |
| [1039821](https://hackerone.com/reports/1039821) | HackerOne | low | - | 64 | 2021-06-18 | Code Injection | Second-order SOQL injection through email and campaign name parameter in Salesforce lead submission |
| [182104](https://hackerone.com/reports/182104) | Udemy | high | - | 63 | 2017-06-17 | Code Injection | Completed Compromise & Source Code Disclosure via Exposed Jenkins Dashboard at https://jenkins101.udemy.com |
| [2383092](https://hackerone.com/reports/2383092) | GitHub | low | - | 63 | 2024-08-19 | Code Injection | Source Code and data exfiltration via Github Copilot |
| [651518](https://hackerone.com/reports/651518) | Ruby |  | - | 62 | 2019-08-29 | OS Command Injection | OS Command Injection via egrep in Rake::FileList |
| [2742457](https://hackerone.com/reports/2742457) | U.S. Dept Of Defense | critical | - | 62 | 2024-10-25 | OS Command Injection | CVE-2020-7961 RCE Liferay Portal Unauthenticated via https://████████/ |
| [269066](https://hackerone.com/reports/269066) | Ubiquiti Inc. | critical | - | 61 | 2017-11-29 | Command Injection - Generic | Remote Code Execution at http://tw.corp.ubnt.com |
| [2329466](https://hackerone.com/reports/2329466) | GitHub | high | - | 61 | 2024-09-13 | Command Injection - Generic | Management Console Editor Privilege Escalation to Root SSH Access in GitHub Enterprise Server via RCE in syslog-ng |
| [2332551](https://hackerone.com/reports/2332551) | GitHub | high | - | 61 | 2024-09-13 | Command Injection - Generic | Management Console Editor Privilege Escalation to Root SSH Access in GitHub Enterprise Server via nomad template injection |
| [2817658](https://hackerone.com/reports/2817658) | Trellix | critical | - | 60 | 2025-01-12 | OS Command Injection | Unauthenticated Path Traversal and Command Injection in Trellix Enterprise Security Manager 11.6.10 |
| [3463045](https://hackerone.com/reports/3463045) | IBM | critical | - | 60 | 2025-12-31 | Code Injection | Remote Code Execution identified on IBM endpoint. |
| [949361](https://hackerone.com/reports/949361) | Valve | critical | - | 59 | 2024-07-30 | OS Command Injection | Shell command injection in https://partner.steamgames.com/admin/game/publish/ via screenshot URL |
| [1677047](https://hackerone.com/reports/1677047) | MTN Group | critical | - | 59 | 2023-12-31 | Code Injection | Remote code execution via crafted pentaho report uploaded using default credentials for pentaho business server |
| [3090123](https://hackerone.com/reports/3090123) | Mars | critical | - | 59 | 2025-05-12 | Deserialization of Untrusted Data | insecure deserilize object leads to RCE On Sitecore (CVE-██████████-27218) |
| [538771](https://hackerone.com/reports/538771) | U.S. Dept Of Defense | high | - | 58 | 2019-10-04 | Remote File Inclusion | LFI with potential to RCE on ██████ using CVE-2019-3396 |
| [536134](https://hackerone.com/reports/536134) | Starbucks | critical | - | 57 | 2019-12-12 | OS Command Injection | Store Development Resource Center was vulnerable to a Remote Code Execution - Unauthenticated Remote Command Injection (CVE-2019-0604) |
| [876708](https://hackerone.com/reports/876708) | U.S. Dept Of Defense | high | - | 56 | 2020-05-27 | OS Command Injection | Remote Code Execution through DNN Cookie Deserialization |
| [2467232](https://hackerone.com/reports/2467232) | Liberapay | low | - | 55 | 2024-05-04 | Deserialization of Untrusted Data | Unsafe yaml load can lead to remote code execution |
| [2705661](https://hackerone.com/reports/2705661) | Internet Bug Bounty | low | - | 54 | 2024-12-07 | Code Injection | CVE-2024-45498: Apache Airflow Command injection in read_dataset_event_from_classic DAG |
| [188086](https://hackerone.com/reports/188086) | Brave Software | critical | - | 53 | 2018-09-18 | Command Injection - Generic | Sending arbitrary IPC messages via overriding Function.prototype.apply |
| [840243](https://hackerone.com/reports/840243) | Valve | critical | - | 53 | 2024-07-30 | Command Injection - Generic | Shell command injection in https://partner.steamgames.com/apps/communityitems/ via file extension of item_image_small and item_image_large |
| [1104111](https://hackerone.com/reports/1104111) | QIWI |  | - | 52 |  | Code Injection | Remote Code Execution on contactws.contact-sys.com via SQL injection in TPrabhuObject.BeginOrder in parameter DOC_ID |
| [1167530](https://hackerone.com/reports/1167530) | PortSwigger Web Security | none | - | 51 | 2021-04-22 | Code Injection | RCE in 'Copy as Node Request' BApp via code injection |
| [134738](https://hackerone.com/reports/134738) | Automattic |  | - | 50 | 2016-07-10 | Code Injection | WordPress SOME bug in plupload.flash.swf leading to RCE |
| [147196](https://hackerone.com/reports/147196) | Informatica | high | - | 50 | 2016-12-31 | Command Injection - Generic | [careers.informatica.com] Reflected Cross Site Scripting to XSS Shell Possible |
| [494979](https://hackerone.com/reports/494979) | Notepad++ | medium | - | 50 | 2019-06-06 | Command Injection - Generic | Insufficient sanitizing can lead to arbitrary commands execution |
| [497312](https://hackerone.com/reports/497312) | Notepad++ | medium | - | 50 | 2019-05-07 | Command Injection - Generic | Command injection by setting a custom search engine |
| [914392](https://hackerone.com/reports/914392) | Engel & Völkers Technology GmbH |  | - | 49 |  | Code Injection | Remote Code Execution (RCE) at "juid" parameter in /get_zip.php (printshop.engelvoelkers.com) |
| [1379130](https://hackerone.com/reports/1379130) | IBM | critical | - | 49 | 2021-11-04 | Command Injection - Generic | Remote Code Execution at https://169.38.86.185/ (edst.ibm.com) |
| [221294](https://hackerone.com/reports/221294) | Starbucks | critical | - | 48 | 2017-05-22 | Code Injection | Java Deserialization RCE via JBoss on card.starbucks.in |
| [1016966](https://hackerone.com/reports/1016966) | Basecamp | high | - | 48 | 2020-11-19 | Code Injection | Remote Code Execution in Basecamp Windows Electron App |
| [1429014](https://hackerone.com/reports/1429014) | U.S. Dept Of Defense | critical | - | 48 | 2022-01-03 | Code Injection | Log4Shell: RCE 0-day exploit on █████████ |
| [2778350](https://hackerone.com/reports/2778350) | MTN Group | critical | - | 48 | 2025-02-19 | Command Injection - Generic | Cisco IOS XE instance at ████ vulnerable to CVE-██████ |
| [3478646](https://hackerone.com/reports/3478646) | AWS VDP | low | - | 48 | 2026-08-03 | Inclusion of Functionality from Untrusted Control Sphere | GitHub Retired UsernameTakeover From  [aws/████████] |
| [3558713](https://hackerone.com/reports/3558713) | AWS VDP | high | - | 48 | 2026-06-11 | OS Command Injection | Command Injection via Unsanitized Bundling Options in `aws-cdk-lib/aws-lambda-nodejs` |
| [652649](https://hackerone.com/reports/652649) | Valve | critical | - | 47 | 2024-07-30 | Command Injection - Generic | WG call injection in /economy/contextcommand |
| [926169](https://hackerone.com/reports/926169) | Valve | critical | - | 47 | 2024-07-30 | OS Command Injection | Shell command injection in https://partner.steamgames.com/bundles/savestore/ via overwriting asset_path_identifier |
| [1636382](https://hackerone.com/reports/1636382) | Elastic | high | - | 47 | 2023-04-08 | Code Injection | Synthetics Recorder: Code injection when recording website with malicious content |
| [2309291](https://hackerone.com/reports/2309291) | MTN Group | high | - | 47 | 2025-02-22 | Command Injection - Generic | CVE-2023-41763 Business Elevation of Privilege vulnerability on [.mtn.com] |
| [2323292](https://hackerone.com/reports/2323292) | GitHub | high | - | 47 | 2024-09-17 | Command Injection - Generic | Management Console Editor Privilege Escalation to Root SSH Access in GitHub Enterprise Server via RCE in actions-console |
| [2329547](https://hackerone.com/reports/2329547) | GitHub | high | - | 47 | 2024-09-17 | Command Injection - Generic | Management Console Editor Privilege Escalation to Root SSH Access in GitHub Enterprise Server via RCE in collectd |
| [395737](https://hackerone.com/reports/395737) | Brave Software | high | - | 46 | 2018-09-25 | Code Injection | `chrome://brave` available for navigation in Release build [-> RCE] + navigation to `chrome://*` using tab_helper ["Open in new tab"] |
| [415501](https://hackerone.com/reports/415501) | h1-5411-CTF | critical | - | 46 | 2018-10-22 | Code Injection | RCE via Local File Read -> php unserialization-> XXE -> unpickling |
| [1492896](https://hackerone.com/reports/1492896) | Internet Bug Bounty | high | - | 46 | 2022-04-01 | Command Injection - Generic | CVE-2022-24288: Apache Airflow: TWO RCEs in example DAGs |
| [1519841](https://hackerone.com/reports/1519841) | 8x8 | critical | - | 46 | 2022-03-25 | Code Injection | F5 BIG-IP TMUI RCE - CVE-2020-5902 (██.packet8.net) |
| [2762119](https://hackerone.com/reports/2762119) | MTN Group | critical | - | 46 | 2024-11-16 | Code Injection | CVE-2017-9822 DotNetNuke Cookie Deserialization Remote Code Execution (RCE) on lonidoor.mtn.ci |
| [3781492](https://hackerone.com/reports/3781492) | Revive Adserver | high | - | 46 | 2026-06-25 | Code Injection | PHP code injection in delivery-limitation `logical` validation bypass - XML-RPC setChannelTargeting |
| [838196](https://hackerone.com/reports/838196) | U.S. Dept Of Defense | critical | - | 45 | 2020-05-07 | Deserialization of Untrusted Data | Remote Code Execution via Insecure Deserialization in Telerik UI |
| [3531216](https://hackerone.com/reports/3531216) | curl | low | - | 45 | 2026-02-05 | Code Injection | MQTT Protocol Packet Injection via Unchecked CONNACK Remaining Length |
| [139398](https://hackerone.com/reports/139398) | Ubiquiti Inc. |  | - | 44 | 2016-08-05 | Command Injection - Generic | Read-Only user can execute arbitraty shell commands on AirOS |
| [357858](https://hackerone.com/reports/357858) | Monero | high | - | 43 | 2018-07-27 | Code Injection | forum.getmonero.org Shell upload |
| [1095633](https://hackerone.com/reports/1095633) | VK.com |  | - | 43 | 2021-05-27 | Code Injection | [VK Android] Access to app protected components leads to arbitrary code execution |
| [3523953](https://hackerone.com/reports/3523953) | curl | medium | - | 43 | 2026-01-26 | Command Injection - Generic | wcurl Argument Injection via Unquoted Variable |
| [3557138](https://hackerone.com/reports/3557138) | AWS VDP | none | - | 43 | 2026-03-09 | Code Injection | Arbitrary Code Execution via Scanner Bypass in **aws-diagram-mcp-server** `exec()` Namespace |
| [153026](https://hackerone.com/reports/153026) | Starbucks |  | - | 42 | 2017-02-03 | Code Injection | Java Deserialization RCE via JBoss JMXInvokerServlet/EJBInvokerServlet on card.starbucks.in |
| [410334](https://hackerone.com/reports/410334) | IBM | high | - | 42 | 2022-02-04 | OS Command Injection | Reflected XSS and Blind out of band command injection at subdomain dstuid-ww.dst.ibm.com |
| [807961](https://hackerone.com/reports/807961) | 8x8 | high | - | 42 | 2020-06-22 | Command Injection - Generic | Blind Command Injection #1 |
| [825764](https://hackerone.com/reports/825764) | Ubiquiti Inc. | high | - | 42 | 2021-05-23 | Command Injection - Generic | View Only to Root Privilege Escalation on UniFi Protect |
| [288704](https://hackerone.com/reports/288704) | Phabricator | critical | - | 41 | 2017-11-11 | Command Injection - Generic | Command injection on Phabricator instance with an evil hg branch name |
| [1187477](https://hackerone.com/reports/1187477) | Ruby |  | - | 41 | 2024-07-03 | Code Injection | RCE by parsing `.rdoc_options` in RDoc |
| [3619287](https://hackerone.com/reports/3619287) | DuckDuckGo | critical | - | 41 | 2026-06-11 | Code Injection | RCE + Supply Chain Attack via pull_request_target in content-scope-scripts/semver-label.yml — Affects All DuckDuckGo Browsers |
| [329572](https://hackerone.com/reports/329572) | Sony | critical | - | 40 | 2019-01-23 | Deserialization of Untrusted Data | Remote Code Execution (RCE) in a Sony WebSystem |
| [943725](https://hackerone.com/reports/943725) | Rocket.Chat | critical | - | 40 | 2020-11-07 | Code Injection | Remote Code Execution in Rocket.Chat-Desktop |
| [1374017](https://hackerone.com/reports/1374017) | HackerOne | low | - | 40 | 2023-05-12 | Code Injection | HTML injection in email at https://www.hackerone.com/ |
| [260005](https://hackerone.com/reports/260005) | Internet Bug Bounty | high | - | 39 | 2017-09-21 | OS Command Injection | RCE via ssh:// URIs in multiple VCS |
| [1327769](https://hackerone.com/reports/1327769) | U.S. Dept Of Defense | critical | - | 39 | 2023-12-21 | OS Command Injection | RCE in ███ [CVE-2021-26084] |
| [986380](https://hackerone.com/reports/986380) | Sony | high | - | 37 | 2022-12-16 | Command Injection - Generic | LFI at http://www.████ |
| [3923967](https://hackerone.com/reports/3923967) | WordPress | high | - | 37 | 2026-10-21 | Code Injection | WordPress 7.1 Media Processing Race Enables Persistent PHP File Write and Author-to-RCE |
| [449482](https://hackerone.com/reports/449482) | Ruby |  | - | 36 | 2019-04-01 | Command Injection - Generic | Command injection in Pathname |
| [1066607](https://hackerone.com/reports/1066607) | TikTok | low | - | 36 | 2021-03-19 | Code Injection | HTML Injection through Account Name field on TikTok ads portal being rendered on emails |
| [1391576](https://hackerone.com/reports/1391576) | 8x8 | critical | - | 36 | 2022-02-03 | Code Injection | Remote Code Execution on ██.8x8.com via .NET VSTATE Deserialization |
| [3656781](https://hackerone.com/reports/3656781) | Revive Adserver | high | - | 36 | 2026-06-03 | Code Injection | PHP code injection via delivery limitation logical |
| [55431](https://hackerone.com/reports/55431) | drchrono |  | - | 35 | 2016-06-13 | Code Injection | XML Parser Bug: XXE over which leads to RCE |
| [58914](https://hackerone.com/reports/58914) | Zendesk |  | - | 35 |  | Code Injection | Remote code execution as root on [REDACTED] |
| [185051](https://hackerone.com/reports/185051) | shopify-scripts | critical | - | 35 | 2017-01-15 | Code Injection | Type confusion in wrap_decimal leading to memory corruption |
| [399166](https://hackerone.com/reports/399166) | Rocket.Chat | medium | - | 35 | 2018-08-28 | Code Injection | Remote code execution by hijacking an unclaimed S3 bucket in Rocket.Chat's installation script. |
| [3679660](https://hackerone.com/reports/3679660) | Shopify | none | - | 35 | 2026-04-24 | Code Injection | mruby-engine: UAF in MRubyEngine#initialize enables local RCE |
| [3780854](https://hackerone.com/reports/3780854) | Revive Adserver | high | - | 35 | 2026-06-25 | Code Injection | PHP code injection in delivery-limitation `logical` validation bypass |
| [688270](https://hackerone.com/reports/688270) | Central Security Project | critical | - | 34 | 2019-10-29 | Command Injection - Generic | OS Command Injection in Nexus Repository Manager 2.x(bypass CVE-2019-5475) |
| [1378175](https://hackerone.com/reports/1378175) | Kubernetes | high | - | 34 | 2022-08-13 | Code Injection | Ingress-nginx annotation injection allows retrieval of ingress-nginx serviceaccount token and secrets across all namespaces |
| [1442644](https://hackerone.com/reports/1442644) | Adobe |  | - | 34 |  | Code Injection | Log4j Java RCE in [beta.dev.adobeconnect.com] |
| [2255968](https://hackerone.com/reports/2255968) | Linux Foundation Decentralized Trust | high | - | 34 | 2024-01-08 | Deserialization of Untrusted Data | CVE-2023-46132 |
| [3874004](https://hackerone.com/reports/3874004) | Weblate | high | - | 34 | 2026-09-15 | OS Command Injection | Incomplete fix for CVE-2022-23915: Mercurial argument injection in HgRepository.get_file() leads to command execution |
| [1459714](https://hackerone.com/reports/1459714) | Acronis | critical | - | 33 | 2024-08-28 | Code Injection | [CVE-2021-44228] Arbitrary Code Execution on ng01-cloud.acronis.com |
| [2054184](https://hackerone.com/reports/2054184) | U.S. Dept Of Defense | critical | - | 33 | 2023-12-21 | Command Injection - Generic | RCE via File Upload  with a Null Byte Truncated File Extension at https://██████/ |
| [135072](https://hackerone.com/reports/135072) | HackerOne |  | - | 32 | 2016-06-08 | Code Injection | RCE in profile picture upload |
| [378148](https://hackerone.com/reports/378148) | GitLab | critical | - | 32 | 2018-08-22 | Command Injection - Generic | Vulnerability in project import leads to arbitrary command execution |
| [1250293](https://hackerone.com/reports/1250293) | U.S. Dept Of Defense | medium | - | 32 | 2021-07-29 | Code Injection | SQL injection my method -1 OR 3*2*1=6 AND 000159=000159 |
| [4170](https://hackerone.com/reports/4170) | Yahoo! |  | - | 31 |  | Code Injection | Code execution in "ymon" WebService, reached after bypassing the anti-loopback blacklist through YQL and HTTP redirects |
| [184596](https://hackerone.com/reports/184596) | U.S. Dept Of Defense | critical | - | 31 | 2016-12-22 | Command Injection - Generic | Unrestricted File Upload |
| [188284](https://hackerone.com/reports/188284) | U.S. Dept Of Defense | critical | - | 31 | 2017-01-12 | Code Injection | Remote code execution on an Army website |
| [236552](https://hackerone.com/reports/236552) | Automattic | critical | - | 31 | 2017-09-15 | Code Injection | Unauthenticated RCE in Vaultpress |
| [633262](https://hackerone.com/reports/633262) | Mail.ru |  | - | 31 |  | Code Injection | Code Injection in macOS Desktop Client |
| [671749](https://hackerone.com/reports/671749) | U.S. Dept Of Defense | critical | - | 31 | 2019-12-02 | OS Command Injection | Pulse Secure File disclosure, clear text and potential RCE |
| [899964](https://hackerone.com/reports/899964) | Rocket.Chat | critical | - | 31 | 2021-01-01 | OS Command Injection | XSS leads to RCE on the RocketChat desktop client. |
| [2552879](https://hackerone.com/reports/2552879) | Basecamp | medium | - | 31 | 2024-07-09 | Deserialization of Untrusted Data | Navgraph confusion allows any 3p app to send and read requests from the server at app.hey.com |
| [3712343](https://hackerone.com/reports/3712343) | curl | critical | - | 31 | 2026-05-05 | ASI05: Unexpected Code Execution (RCE) | MQTT CONNACK Packet Type Bypass leads to RCE via Malicious Broker |
| [791293](https://hackerone.com/reports/791293) | Endless Group | high | - | 30 | 2020-02-12 | Code Injection | Modify Host Header which is sent to email |
| [889886](https://hackerone.com/reports/889886) | h1-ctf | critical | - | 30 | 2020-06-18 | Code Injection | [H1-2006 2020]  Connecting the dots to send hackers their Bug Bounty |
| [1248052](https://hackerone.com/reports/1248052) | U.S. Dept Of Defense | high | - | 30 | 2023-12-21 | Code Injection | Pre-auth RCE in ForgeRock OpenAM (CVE-2021-35464) |
| [1425565](https://hackerone.com/reports/1425565) | MTN Group | critical | - | 30 | 2024-08-24 | OS Command Injection | Remote code injection in Log4j on  https://mymtn.mtncongo.net - CVE-2021-44228 |
| [3679471](https://hackerone.com/reports/3679471) | Monero | medium | - | 30 | 2026-08-20 | Code Injection | HTML Injection in Transaction Confirmation Dialog via Address Book Description Enables UI Spoofing Before Fund Transfer |
| [181321](https://hackerone.com/reports/181321) | shopify-scripts | critical | - | 29 | 2016-12-16 | Code Injection | Use after free vulnerability in mruby Array#to_h causing DOS possible RCE |
| [184279](https://hackerone.com/reports/184279) | U.S. Dept Of Defense | critical | - | 29 | 2017-01-11 | Code Injection | RCE on a Department of Defense website |
| [211381](https://hackerone.com/reports/211381) | U.S. Dept Of Defense | critical | - | 29 | 2017-04-13 | Code Injection | Remote Code Execution (RCE) in a DoD website |
| [633266](https://hackerone.com/reports/633266) | Nextcloud | low | - | 29 | 2020-04-10 | Code Injection | Code injection in macOS Desktop Client |
| [810755](https://hackerone.com/reports/810755) | MTN Group | critical | - | 29 | 2021-04-25 | OS Command Injection | Remote OS Command Execution on Oracle Weblogic server via [CVE-2017-10271] |
| [944359](https://hackerone.com/reports/944359) | GitHub Security Lab |  | - | 29 |  | Code Injection | Python : Add query to detect Server Side Template Injection |
| [1070532](https://hackerone.com/reports/1070532) | MTN Group | high | - | 29 | 2021-09-09 | Code Injection | RCE Apache Struts2 remote command execution (S2-045) on [wifi-partner.mtn.com.gh] |
| [2545994](https://hackerone.com/reports/2545994) | Enjin | low | - | 29 | 2024-06-19 | Code Injection | Cloudflare /cdn-cgi/ path allows resizing images from unauthorised sources on enjinusercontent.com |
| [3648199](https://hackerone.com/reports/3648199) | curl | critical | - | 29 | 2026-04-03 | Code Injection | Internal application wrapper or script using curl |
| [73567](https://hackerone.com/reports/73567) | Shopify |  | - | 28 | 2015-07-16 | Command Injection - Generic | Attention! Remote Code Execution at http://wpt.ec2.shopify.com/ |
| [294462](https://hackerone.com/reports/294462) | Ruby | low | - | 28 | 2017-12-19 | Command Injection - Generic | NET::Ftp allows command injection in filenames |
| [358049](https://hackerone.com/reports/358049) | Automattic | high | - | 28 | 2018-07-26 | Code Injection | RCE via Print function [Simplenote 1.1.3 - Desktop app] |
| [654888](https://hackerone.com/reports/654888) | Central Security Project | critical | - | 28 | 2019-08-20 | OS Command Injection | OS Command Injection in Nexus Repository Manager 2.x |
| [728614](https://hackerone.com/reports/728614) | U.S. Dept Of Defense | critical | - | 28 | 2024-06-18 | Deserialization of Untrusted Data | [HTAF4-213] [Pre-submission] Unsafe AMF deserialization (CVE-2017-5641) in Apache Flex BlazeDS at the https://www.███████/daip/messagebroker/amf |
| [921288](https://hackerone.com/reports/921288) | Concrete CMS | high | - | 28 | 2021-10-20 | Deserialization of Untrusted Data | Arbitrary File delete via PHAR deserialization |
| [1104349](https://hackerone.com/reports/1104349) | Glovo | high | - | 28 | 2022-07-11 | Code Injection | Server Side Template Injection on Name parameter during Sign Up process |
| [1119120](https://hackerone.com/reports/1119120) | RubyGems |  | - | 28 | 2024-03-12 | Deserialization of Untrusted Data | Bundler's RCE with response using Marshal |
| [1122791](https://hackerone.com/reports/1122791) | U.S. Dept Of Defense | critical | - | 28 | 2022-09-15 | Code Injection | [hta3] Remote Code Execution on  https://███ via improper access control to SCORM Zip upload/import |
| [1413541](https://hackerone.com/reports/1413541) | GitHub Security Lab |  | - | 28 |  | Code Injection | [porcupiney.hairs]: [Python] Add Flask Path injection sinks |
| [197958](https://hackerone.com/reports/197958) | Ubiquiti Inc. | medium | - | 27 | 2017-07-21 | Command Injection - Generic | [EdgeSwitch] Web GUI command injection as root with Privilege-1 and Privilege-15 users |
| [796414](https://hackerone.com/reports/796414) | Ubiquiti Inc. | high | - | 27 | 2021-05-23 | Command Injection - Generic | Readonly to Root Privilege Escalation on EdgeSwitch |
| [833470](https://hackerone.com/reports/833470) | Rocket.Chat | medium | - | 27 | 2020-06-24 | Code Injection | [Security Vulnerability Rocket.chat] HTML Injection into Email via Signup |
| [1154034](https://hackerone.com/reports/1154034) | Ruby on Rails | high | - | 27 | 2023-07-28 | Code Injection | Argument/Code Injection via ActiveStorage's image transformation functionality |
| [1174185](https://hackerone.com/reports/1174185) | U.S. Dept Of Defense | critical | - | 27 | 2021-06-03 | Deserialization of Untrusted Data | Remote Code Execution via Insecure Deserialization in Telerik UI (CVE-2019-18935) |
| [3357960](https://hackerone.com/reports/3357960) | curl |  | - | 27 | 2025-09-26 | Command Injection - Generic | SMTP Command Injection Vulnerabilities in curl |
| [680480](https://hackerone.com/reports/680480) | U.S. Dept Of Defense | critical | - | 26 | 2020-05-07 | Command Injection - Generic | Command Injection (via CVE-2019-11510 and CVE-2019-11539) |
| [1092574](https://hackerone.com/reports/1092574) | Invision Power Services, Inc. | high | - | 26 | 2021-05-28 | Code Injection | PHP Code Injection through "previewBlock()" method |
| [1339430](https://hackerone.com/reports/1339430) | Sony | critical | - | 26 | 2022-07-06 | OS Command Injection | Blind User-Agent SQL Injection to Blind Remote OS Command Execution at █████████ |
| [2471956](https://hackerone.com/reports/2471956) | Linux Foundation Decentralized Trust | medium | - | 26 | 2024-04-28 | Code Injection | Code exec on Github runner via Pull request name |
| [3590576](https://hackerone.com/reports/3590576) | Nextcloud | medium | - | 26 | 2026-04-20 | Remote File Inclusion | SMIL values and by attributes bypass remote image blocking via unvalidated resource-loading animations, enabling email tracking without consent |
| [608577](https://hackerone.com/reports/608577) | curl | high | - | 25 | 2019-06-29 | Code Injection | CVE-2019-5443: Windows Privilege Escalation: Malicious OpenSSL Engine |
| [810778](https://hackerone.com/reports/810778) | MTN Group | critical | - | 25 | 2021-04-25 | OS Command Injection | Remote OS Command Execution on Oracle Weblogic server via [CVE-2017-3506] |
| [3584149](https://hackerone.com/reports/3584149) | curl | none | - | 25 | 2026-03-04 | Command Injection - Generic | SSTI leads to Command injection |
| [3897236](https://hackerone.com/reports/3897236) | AWS VDP | high | - | 25 | 2026-10-13 | Code Injection | RCE in AWS Amplify CLI via Prototype Chain Traversal in amplify-velocity-template |
| [244677](https://hackerone.com/reports/244677) | WakaTime |  | - | 24 | 2017-07-20 | Code Injection | Add arbitrary content to Password Reset Email |
| [722919](https://hackerone.com/reports/722919) | lemlist | medium | - | 24 | 2020-04-01 | Unrestricted Upload of File with Dangerous Type | Unrestricted File Upload on https://app.lemlist.com |
| [822002](https://hackerone.com/reports/822002) | U.S. Dept Of Defense | critical | - | 24 | 2021-01-12 | Code Injection | Apache solr RCE via velocity template |
| [2905013](https://hackerone.com/reports/2905013) | Internet Bug Bounty | high | - | 24 | 2025-05-27 | Code Injection | [SECURITY] CVE-2024-50379 Apache Tomcat - RCE via write-enabled default servlet |
| [3217840](https://hackerone.com/reports/3217840) | AWS VDP | none | - | 24 | 2025-08-14 | Code Injection | Remote Code Execution in Amazon MWAA due to outdated Apache Airflow version |
| [181893](https://hackerone.com/reports/181893) | shopify-scripts | critical | - | 23 | 2016-12-16 | Code Injection | TOCTTOU bug in mrb_str_setbyte leading the memory corruption |
| [3633123](https://hackerone.com/reports/3633123) | AWS VDP | high | - | 23 | 2026-09-16 | OS Command Injection | Incomplete Input Sanitization in CodeInterpreter install_packages Allows Command Injection via pip Flags |
| [3669305](https://hackerone.com/reports/3669305) | curl | critical | - | 23 | 2026-04-13 | Command Injection - Generic | Argument Injection via curl Short-Flag Grouping |
| [109699](https://hackerone.com/reports/109699) | Ubiquiti Inc. |  | - | 22 | 2016-02-14 | Code Injection | Subdomain Takeover in http://assets.goubiquiti.com/ |
| [128750](https://hackerone.com/reports/128750) | Ubiquiti Inc. |  | - | 22 | 2016-08-05 | Command Injection - Generic | Read-Only user can execute arbitraty shell commands on AirOS |
| [143966](https://hackerone.com/reports/143966) | Internet Bug Bounty |  | - | 22 | 2016-05-03 | Code Injection | Insufficient shell characters filtering leads to (potentially remote) code execution (CVE-2016-3714) |
| [330028](https://hackerone.com/reports/330028) | Sony | critical | - | 22 | 2019-01-23 | Deserialization of Untrusted Data | Remote Code Execution (RCE) in a Sony Pictures WebSystem |
| [470547](https://hackerone.com/reports/470547) | Kaspersky | medium | - | 22 | 2019-11-24 | Command Injection - Generic | Unauthorized command execution in Web protection component of Anti-Virus products family [IE] |
| [579760](https://hackerone.com/reports/579760) | Django | critical | - | 22 | 2019-05-16 | OS Command Injection | Jenkins Unauthenticated RCE on https://djangoci.com/ |
| [723707](https://hackerone.com/reports/723707) | Semrush | medium | - | 22 | 2019-11-01 | Code Injection | Code injection in https://www.semrush.com |
| [841397](https://hackerone.com/reports/841397) | ExpressionEngine | high | - | 22 | 2024-05-28 | Code Injection | Low privileges (auth) Remote Command Execution - PHP file upload bypass. |
| [1671140](https://hackerone.com/reports/1671140) | Internet Bug Bounty | high | - | 22 | 2022-09-23 | Command Injection - Generic | CVE-2022-38362: Apache Airflow Docker Provider <3.0 RCE vulnerability in example dag |
| [1888351](https://hackerone.com/reports/1888351) | Expedia Group Bug Bounty | low | - | 22 | 2023-05-20 | Code Injection | https://www.wotif.com/vc/blog/info.php script is prone to reflected HTML/CSS injection and COOKIE leak |
| [255991](https://hackerone.com/reports/255991) | Brave Software | high | - | 21 | 2017-08-31 | Use of Inherently Dangerous Function | URL Spoof / Brave Shield Bypass |
| [335761](https://hackerone.com/reports/335761) | ExpressionEngine | high | - | 21 | 2018-04-20 | Command Injection - Generic | RCE By import channel field |
| [406702](https://hackerone.com/reports/406702) | Mail.ru |  | - | 21 |  | Code Injection | ICQ 10.0.12371 icq: Uri Handler '-testability' URL File Insecure Library Loading Code Execution Vulnerability |
| [415275](https://hackerone.com/reports/415275) | h1-5411-CTF | critical | - | 21 | 2018-11-21 | Deserialization of Untrusted Data | CTF Writeup flag{cha1n1ng_bugs_f0r_fun_4nd_pr0f1t?_or_rep0rt_an_LF1} |
| [415967](https://hackerone.com/reports/415967) | Brave Software | critical | - | 21 | 2018-10-23 | Code Injection | chrome://brave navigation from web |
| [470519](https://hackerone.com/reports/470519) | Kaspersky | medium | - | 21 | 2019-11-25 | Command Injection - Generic | Kaspersky Protection extension for Google Chrome is vulnerable to abuse its features |
| [513525](https://hackerone.com/reports/513525) | 50m-ctf |  | - | 21 |  | OS Command Injection | Several vulnerabilities lead to Remote Code Execution and Arbitraty File Read on multiple servers |
| [678496](https://hackerone.com/reports/678496) | U.S. Dept Of Defense | critical | - | 21 | 2019-12-02 | OS Command Injection | Arbitrary File Reading leads to RCE in the Pulse Secure SSL VPN on the https://███ |
| [1431624](https://hackerone.com/reports/1431624) | Krisp | none | - | 21 | 2021-12-29 | Code Injection | Log4j CVE-2021–44228 |
| [1631258](https://hackerone.com/reports/1631258) | Rocket.Chat | critical | - | 21 | 2023-03-04 | Command Injection - Generic | Rocket.Chat Server RCE |
| [121940](https://hackerone.com/reports/121940) | Ubiquiti Inc. |  | - | 20 | 2016-10-15 | Command Injection - Generic | Shell Injection via Web Management Console (dl-fw.cgi) |
| [216243](https://hackerone.com/reports/216243) | GitLab | medium | - | 20 | 2017-07-21 | Command Injection - Generic | CSV injection in gitlab.com via issues export feature. |
| [244292](https://hackerone.com/reports/244292) | Grab | medium | - | 20 | 2017-10-27 | Command Injection - Generic | CSV Injection https://hub.grab.com |
| [415222](https://hackerone.com/reports/415222) | h1-5411-CTF | critical | - | 20 | 2018-10-22 | Code Injection | Solution for h15411's CTF challenge |
| [1081656](https://hackerone.com/reports/1081656) | Informatica | medium | - | 20 | 2021-02-12 | Code Injection | Html injection on ██████.informatica.com via search.html?q=1 |
| [2461831](https://hackerone.com/reports/2461831) | Node.js | high | - | 20 | 2024-07-09 | Command Injection - Generic | Bypass incomplete fix of CVE-2024-27980 |
| [3250117](https://hackerone.com/reports/3250117) | curl | high | - | 20 | 2025-07-13 | Code Injection | Uncontrolled File Write/Arbitrary File Creation |
| [214370](https://hackerone.com/reports/214370) | Rockstar Games | medium | - | 19 | 2017-09-11 | Code Injection | Comments Denial of Service in socialclub.rockstargames.com |
| [291539](https://hackerone.com/reports/291539) | Automattic | high | - | 19 | 2017-12-01 | Code Injection | [Simplenote for Windows] Client RCE via External JavaScript Inclusion leveraging Electron |
| [518348](https://hackerone.com/reports/518348) | Valve | critical | - | 19 | 2024-07-30 | Command Injection - Generic | RCE on partner.steampowered.com |
| [826288](https://hackerone.com/reports/826288) | Qulture.Rocks |  | - | 19 |  | Deserialization of Untrusted Data | Unrestricted File Upload in Chat Window |
| [881548](https://hackerone.com/reports/881548) | Starbucks | medium | - | 19 | 2020-06-16 | OS Command Injection | Default credentials for the temporary POC site alipoc.stg.starbucks.com.cn permitted WAF bypass and RCE |
| [962013](https://hackerone.com/reports/962013) | U.S. Dept Of Defense | critical | - | 19 | 2020-09-03 | Code Injection | Remote Code Execution on █████████ |
| [1031613](https://hackerone.com/reports/1031613) | Rocket.Chat | medium | - | 19 | 2024-08-10 | Code Injection | CSS Injection in Message Avatar |
| [1063256](https://hackerone.com/reports/1063256) | U.S. Dept Of Defense | high | - | 19 | 2021-03-24 | Command Injection - Generic | [CVE-2018-7600] Remote Code Execution due to outdated Drupal server on www.█████████ |
| [1093444](https://hackerone.com/reports/1093444) | ExpressionEngine | medium | - | 19 | 2024-05-28 | Code Injection | PHP Code Injection through "Translate::save()" method |
| [3427370](https://hackerone.com/reports/3427370) | AWS VDP | none | - | 19 | 2026-01-16 | Command Injection - Generic | Command Injection on Amazon Q Developer CLI via malicious .amazonq/mcp.json leads to arbitrary code execution |
| [119317](https://hackerone.com/reports/119317) | Ubiquiti Inc. |  | - | 18 | 2016-08-05 | Command Injection - Generic | Read-Only user can execute arbitraty shell commands on AirOS |
| [262004](https://hackerone.com/reports/262004) | Unikrn | high | - | 18 | 2017-08-23 | Command Injection - Generic | HTML injection in email in unikrn.com |
| [361341](https://hackerone.com/reports/361341) | Liberapay |  | - | 18 | 2018-06-04 | Deserialization of Untrusted Data | Unsafe deserialization in Libera Pay allows to escalate a SQL injection to Remote Command Execution |
| [1327701](https://hackerone.com/reports/1327701) | U.S. Dept Of Defense | critical | - | 18 | 2023-12-21 | OS Command Injection | RCE on ███████ [CVE-2021-26084] |
| [149442](https://hackerone.com/reports/149442) | Paragon Initiative Enterprises |  | - | 17 | 2016-07-05 | Command Injection - Generic | Site support SNI But Browser can't |
| [212985](https://hackerone.com/reports/212985) | U.S. Dept Of Defense | critical | - | 17 | 2017-07-03 | Code Injection | Remote code execution vulnerability on a DoD website |
| [235605](https://hackerone.com/reports/235605) | U.S. Dept Of Defense | critical | - | 17 | 2018-04-17 | Code Injection | Remote Code Execution (RCE) in DoD Websites |
| [365755](https://hackerone.com/reports/365755) | Uber | low | - | 17 | 2018-11-13 | Code Injection | Privacy policy contains hardcoded link using unencrypted HTTP |
| [415682](https://hackerone.com/reports/415682) | h1-5411-CTF | critical | - | 17 | 2018-10-22 | OS Command Injection | Remote Command Execution in a internal server to get the flag file |
| [843171](https://hackerone.com/reports/843171) | Rocket.Chat | high | - | 17 | 2020-11-05 | Code Injection | Desktop app RCE (#276031 bypass) |
| [902739](https://hackerone.com/reports/902739) | Node.js third-party modules | high | - | 17 | 2020-06-27 | Code Injection | bunyan - RCE via insecure command formatting |
| [913695](https://hackerone.com/reports/913695) | U.S. Dept Of Defense | critical | - | 17 | 2020-08-13 | Deserialization of Untrusted Data | Remote Code Execution via CVE-2019-18935 |
| [1133672](https://hackerone.com/reports/1133672) | Mail.ru |  | - | 17 |  | Code Injection | Development configurations file  with a sensitive data exposure could be leads to take down the social media accounts and the DB |
| [1425563](https://hackerone.com/reports/1425563) | MTN Group | critical | - | 17 | 2024-08-24 | OS Command Injection | Remote code injection in Log4j on http://mtn1app.mtncameroon.net  - CVE-2021-44228 |
| [2095061](https://hackerone.com/reports/2095061) | 8x8 | medium | - | 17 | 2024-08-26 | Command Injection - Generic | Jitsi: Bridge Message Spoofing due to Improper JSON Handling leads to Prototype Pollution |
| [523](https://hackerone.com/reports/523) | Internet Bug Bounty |  | - | 16 | 2013-12-13 | Code Injection | PHP openssl_x509_parse() Memory Corruption Vulnerability |
| [155657](https://hackerone.com/reports/155657) | ownCloud |  | - | 16 | 2016-11-23 | Command Injection - Generic | Arbitrary Code Injection in ownCloud’s Windows Client |
| [415258](https://hackerone.com/reports/415258) | Brave Software | high | - | 16 | 2018-10-22 | Code Injection | RCE: DnDing shortcut files to chrome://brave allows loading HTML files in Muon's context |
| [562335](https://hackerone.com/reports/562335) | ownCloud | critical | - | 16 | 2019-07-01 | Deserialization of Untrusted Data | Remote Code Execution through Deserialization Attack in OwnBackup app. |
| [841947](https://hackerone.com/reports/841947) | Concrete CMS | high | - | 16 | 2020-07-03 | Code Injection | Remote Code Execution through Extension Bypass on Log Functionality |
| [1069105](https://hackerone.com/reports/1069105) | MTN Group | critical | - | 16 | 2021-08-19 | Remote File Inclusion | 2x Remote file inclusion within your VMware Instances |
| [2334460](https://hackerone.com/reports/2334460) | Internet Bug Bounty | low | - | 16 | 2024-01-29 | Deserialization of Untrusted Data | Pickle deserialization vulnerability in XComs |
| [2554003](https://hackerone.com/reports/2554003) | U.S. Dept Of Defense | low | - | 16 | 2024-07-19 | Command Injection - Generic | HTML Injection into https://www.██████.mil |
| [118582](https://hackerone.com/reports/118582) | HackerOne | low | - | 15 | 2019-04-08 | Command Injection - Generic | CSV Injection at the CSV export feature |
| [151516](https://hackerone.com/reports/151516) | Ian Dunn |  | - | 15 | 2016-08-18 | Command Injection - Generic | CSV Injection at Camptix Event Ticketing |
| [177225](https://hackerone.com/reports/177225) | LocalTapiola |  | - | 15 |  | Code Injection | Email Server Compromised at secure.lahitapiola.fi |
| [271960](https://hackerone.com/reports/271960) | Rockstar Games | medium | - | 15 | 2018-05-01 | Code Injection | Client-side Template Injection in Search, user email/token leak and maybe sandbox escape |
| [330957](https://hackerone.com/reports/330957) | Node.js third-party modules | high | - | 15 | 2018-04-19 | Command Injection - Generic | [pdfinfojs] Command Injection on filename parameter |
| [508256](https://hackerone.com/reports/508256) | Ubiquiti Inc. | medium | - | 15 | 2019-03-31 | Command Injection - Generic | EdgeSwitch Command Injection |
| [701183](https://hackerone.com/reports/701183) | Node.js third-party modules | high | - | 15 | 2019-12-04 | Code Injection | [tree-kill] RCE via insecure command concatenation (only Windows) |
| [781664](https://hackerone.com/reports/781664) | Node.js third-party modules | critical | - | 15 | 2020-02-24 | Code Injection | Several simple remote code execution in pdf-image |
| [825729](https://hackerone.com/reports/825729) | Node.js third-party modules | high | - | 15 | 2020-05-09 | Code Injection | [logkitty] RCE via insecure command formatting |
| [870615](https://hackerone.com/reports/870615) | Kaspersky | high | - | 15 | 2021-03-31 | Code Injection | [Fixed] A vulnerability in KAVKIS 2020 products family allows full disabling of protection |
| [900179](https://hackerone.com/reports/900179) | U.S. Dept Of Defense | high | - | 15 | 2020-07-08 | Unrestricted Upload of File with Dangerous Type | Unrestricted File Upload Leads to XSS & Potential RCE |
| [970869](https://hackerone.com/reports/970869) | GitLab | medium | - | 15 | 2022-02-10 | Command Injection - Generic | Sending Arbitrary Requests through Jupyter Notebooks on gitlab.com and Self-Hosted GitLab Instances |
| [975514](https://hackerone.com/reports/975514) | Brave Software | medium | - | 15 | 2022-06-30 | Code Injection | Arbitrary file download due to bad handling of Redirects in WebTorrent |
| [1125329](https://hackerone.com/reports/1125329) | U.S. Dept Of Defense | critical | - | 15 | 2021-03-24 | OS Command Injection | Unauth RCE on Jenkins Instance at https://█████████/ |
| [54631](https://hackerone.com/reports/54631) | Snapchat |  | - | 14 | 2015-10-22 | Command Injection - Generic | Vulnerable to JavaScript injection. (WXS)  (Javascript injection)! |
| [106797](https://hackerone.com/reports/106797) | Informatica | high | - | 14 | 2016-12-09 | Command Injection - Generic | [marketplace.informatica.com] - XXE |
| [162955](https://hackerone.com/reports/162955) | Slack |  | - | 14 | 2017-07-14 | Command Injection - Generic | Code Injection in Slack's Windows Desktop Client leads to Privilege Escalation |
| [386116](https://hackerone.com/reports/386116) | Chaturbate | low | - | 14 | 2018-09-20 | OS Command Injection | CSV Injection with the CSV export feature |
| [390631](https://hackerone.com/reports/390631) | Node.js third-party modules | high | - | 14 | 2018-09-08 | Command Injection - Generic | [ascii-art] Command injection |
| [469730](https://hackerone.com/reports/469730) | U.S. Dept Of Defense | high | - | 14 | 2022-05-26 | Code Injection | [Urgent] Critical Vulnerability [RCE] on ███ vulnerable to Remote Code Execution by exploiting MS15-034, CVE-2015-1635 |
| [690010](https://hackerone.com/reports/690010) | Node.js third-party modules | medium | - | 14 | 2020-05-28 | OS Command Injection | OS Command Injection on Jison [all-parser-ports] |
| [903872](https://hackerone.com/reports/903872) | ownCloud | medium | - | 14 | 2021-06-21 | Code Injection | Remote Code Execution through "Files_antivirus" plugin |
| [1267488](https://hackerone.com/reports/1267488) | ExpressionEngine | medium | - | 14 | 2024-05-28 | Code Injection | Authenticated RCE via page title |
| [1593913](https://hackerone.com/reports/1593913) | GitHub | medium | - | 14 | 2022-11-16 | Deserialization of Untrusted Data | [Git Gud] GitHub.com Svnbridge memcached deserialization vulnerability chain leading to Remote Code Execution |
| [2468496](https://hackerone.com/reports/2468496) | U.S. Dept Of Defense | critical | - | 14 | 2026-01-12 | OS Command Injection | GlobalProtect - OS Command Injection #█████████ |
| [44513](https://hackerone.com/reports/44513) | Ruby on Rails |  | - | 13 | 2015-06-16 | Code Injection | RCE due to Web Console IP Whitelist bypass in Rails 4.0 and 4.1 |
| [72785](https://hackerone.com/reports/72785) | HackerOne |  | - | 13 | 2015-09-21 | Command Injection - Generic | CSV Injection with the CVS export feature |
| [122475](https://hackerone.com/reports/122475) | Imgur |  | - | 13 | 2016-04-16 | Code Injection | Local file read in image editor |
| [130661](https://hackerone.com/reports/130661) | Moneybird |  | - | 13 | 2017-03-17 | Command Injection - Generic | XXE issue |
| [171473](https://hackerone.com/reports/171473) | OWOX, Inc. |  | - | 13 | 2016-12-20 | Command Injection - Generic | HTTP Response Splitting(CRLF injection) in bi.owox.com |
| [276031](https://hackerone.com/reports/276031) | Rocket.Chat | high | - | 13 | 2018-09-18 | Code Injection | Remote Code Execution in Rocket.Chat Desktop |
| [329397](https://hackerone.com/reports/329397) | U.S. Dept Of Defense | critical | - | 13 | 2018-04-17 | Deserialization of Untrusted Data | Remote Code Execution (RCE) in a DoD website |
| [390881](https://hackerone.com/reports/390881) | Node.js third-party modules | medium | - | 13 | 2018-10-28 | Code Injection | Code Injection Vulnerability in morgan Package |
| [470544](https://hackerone.com/reports/470544) | Kaspersky | medium | - | 13 | 2019-11-24 | Command Injection - Generic | Unauthorized command execution in Web protection component of Anti-Virus products family |
| [534630](https://hackerone.com/reports/534630) | U.S. Dept Of Defense | high | - | 13 | 2020-05-11 | OS Command Injection | Remote Code Execution - Unauthenticated Remote Command Injection (via Microsoft SharePoint CVE-2019-0604) |
| [706841](https://hackerone.com/reports/706841) | Mail.ru |  | - | 13 |  | Command Injection - Generic | RCE Jira(CVE-2019–11581) [my-com.atlassian.net] |
| [778629](https://hackerone.com/reports/778629) | 8x8 | high | - | 13 | 2020-02-12 | Code Injection | (Critical) Remote Code Execution Through Old TinyMCE upload bypass |
| [924151](https://hackerone.com/reports/924151) | Rocket.Chat | critical | - | 13 | 2022-08-01 | OS Command Injection | Insecure use of shell.openExternal() in Rocket.Chat Desktop App leading to RCE |
| [1720043](https://hackerone.com/reports/1720043) | Nextcloud | medium | - | 13 | 2023-02-10 | Code Injection | Desktop client can be tricked into opening/executing local files when clicking a nc://open/ link |
| [3293801](https://hackerone.com/reports/3293801) | curl | critical | - | 13 | 2025-08-10 | Code Injection | Title: Remote Code Execution (RCE) via Arbitrary Library Loading in `--engine` option |
| [3817602](https://hackerone.com/reports/3817602) | Node.js | high | - | 13 | 2026-06-23 | OS Command Injection | Node --run POSIX positional argument escaping allows shell command injection |
| [4077800](https://hackerone.com/reports/4077800) | AWS VDP | medium | - | 13 | 2026-11-06 | OS Command Injection | Unescaped consent-prompt renderer (HTML()) enables concealed-approval OS command injection in strands-agents/tools use_computer — RCE |
| [6674](https://hackerone.com/reports/6674) | Yahoo! |  | - | 12 |  | Code Injection | REMOTE CODE EXECUTION/LOCAL FILE INCLUSION/XSPA/SSRF, view-source:http://sb*.geo.sp1.yahoo.com/, 4/6/14, #SpringClean |
| [106802](https://hackerone.com/reports/106802) | Informatica |  | - | 12 |  | Command Injection - Generic | [marketplace.informatica.com] - XXE |
| [106865](https://hackerone.com/reports/106865) | Informatica | high | - | 12 | 2016-12-09 | Command Injection - Generic | [rev-app.informatica.com] - XXE via SAML |
| [289264](https://hackerone.com/reports/289264) | Ubiquiti Inc. | high | - | 12 | 2018-06-19 | Command Injection - Generic | Triggering RCE using XSS to bypass CSRF in PowerBeam M5 300 |
| [299241](https://hackerone.com/reports/299241) | Informatica | critical | - | 12 | 2018-01-02 | Code Injection | [marketplace.informatica.com] -  Template Injection |
| [331752](https://hackerone.com/reports/331752) | Khan Academy | medium | - | 12 | 2019-05-25 | Code Injection | https://mathfacts.khanacademy.org/ includes code from unprivileged localhost port |
| [335447](https://hackerone.com/reports/335447) | Passit |  | - | 12 |  | Command Injection - Generic | CSV-injection in export functionality |
| [384882](https://hackerone.com/reports/384882) | New Relic |  | - | 12 |  | Remote File Inclusion | stamp2-azure-ext.newrelic.com is vulnerable to MS12-020 |
| [415178](https://hackerone.com/reports/415178) | Brave Software | high | - | 12 | 2018-10-23 | Code Injection | chrome://brave can still be navigated to, leading to RCE |
| [461308](https://hackerone.com/reports/461308) | Nextcloud |  | - | 12 | 2019-02-01 | Deserialization of Untrusted Data | Remote attacker can impersonate Social users via ActivityPub API |
| [703659](https://hackerone.com/reports/703659) | Ubiquiti Inc. | high | - | 12 | 2020-06-30 | Command Injection - Generic | RCE in AirOS 6.2.0 Devices with CSRF bypass |
| [943255](https://hackerone.com/reports/943255) | Khan Academy | medium | - | 12 | 2020-08-27 | Code Injection | CSV Injection Via Student Password/Name Leads To Client Side RCE And Reading Client Files |
| [1250307](https://hackerone.com/reports/1250307) | GitHub Security Lab |  | - | 12 |  | Code Injection | [Java] JShell Injection |
| [1317236](https://hackerone.com/reports/1317236) | IBM | critical | - | 12 | 2021-10-18 | Code Injection | Unauthorized Kubernetes to RCE (root) and found TEAMTNT Crypto Miner on it |
| [1360593](https://hackerone.com/reports/1360593) | Informatica | critical | - | 12 | 2021-11-15 | Code Injection | CVE-2021-40870 in [███] |
| [1787810](https://hackerone.com/reports/1787810) | Internet Bug Bounty | medium | - | 12 | 2022-12-14 | Code Injection | Electron CVE-2022-35954 Delimiter Injection Vulnerability in exportVariable |
| [3225565](https://hackerone.com/reports/3225565) | curl | high | - | 12 | 2025-06-28 | OS Command Injection | OS Command Injection in scripts/firefox-db2pem.sh via untrusted certificate nicknames |
| [114476](https://hackerone.com/reports/114476) | VK.com |  | - | 11 | 2016-03-18 | Command Injection - Generic | Внедрение внешних сущностей в функционале импорта пользователей YouTrack |
| [146233](https://hackerone.com/reports/146233) | Internet Bug Bounty |  | - | 11 | 2016-07-28 | Code Injection | Use After Free Vulnerability in PHP's GC algorithm and unserialize |
| [146235](https://hackerone.com/reports/146235) | Internet Bug Bounty |  | - | 11 | 2016-07-28 | Code Injection | ZipArchive class Use After Free Vulnerability in PHP's GC algorithm and unserialize |
| [508894](https://hackerone.com/reports/508894) | Valve | high | - | 11 | 2020-03-25 | Malware | Vulnerability in GoldSource Engine allows to upload and run an arbitrary DLL on client |
| [529371](https://hackerone.com/reports/529371) | 50m-ctf |  | - | 11 |  | Code Injection | Writeup |
| [542670](https://hackerone.com/reports/542670) | Revive Adserver | critical | - | 11 | 2019-04-23 | Deserialization of Untrusted Data | Deserialization of Untrusted Data in www/delivery/dxmlrpc.php |
| [863544](https://hackerone.com/reports/863544) | Node.js third-party modules | critical | - | 11 | 2020-06-15 | Command Injection - Generic | [devcert] Command Injection via insecure command formatting |
| [963155](https://hackerone.com/reports/963155) | Brave Software | medium | - | 11 | 2022-06-30 | Code Injection | Arbitrary file download via "Save .torrent file" option can lead to Client RCE and XSS |
| [1248040](https://hackerone.com/reports/1248040) | U.S. Dept Of Defense | high | - | 11 | 2021-07-29 | Code Injection | Pre-auth RCE in ForgeRock OpenAM (CVE-2021-35464) |
| [1719588](https://hackerone.com/reports/1719588) | Reddit | critical | - | 11 | 2023-05-18 | Remote File Inclusion | HTML injection in API response including request url |
| [1820492](https://hackerone.com/reports/1820492) | ExpressionEngine | high | - | 11 | 2023-03-28 | Command Injection - Generic | PHP Object injection -> Building Custom Gadget chain -> RCE |
| [3744200](https://hackerone.com/reports/3744200) | Revive Adserver | high | - | 11 | 2026-06-03 | Code Injection | PHP code injection via unexpected delivery limitation parameter |
| [3772818](https://hackerone.com/reports/3772818) | Nextcloud | low | - | 11 | 2026-10-24 | Code Injection | Code injection allows unprivileged local attacker to execute arbitrary code in Nextcloud's OAuth/web renderer process |
| [98559](https://hackerone.com/reports/98559) | ownCloud |  | - | 10 | 2015-11-09 | Code Injection | RCE in ci.owncloud.com / ci.owncloud.org |
| [111192](https://hackerone.com/reports/111192) | HackerOne |  | - | 10 | 2016-02-16 | Command Injection - Generic | CSV Injection via the CSV export feature |
| [137631](https://hackerone.com/reports/137631) | Ruby |  | - | 10 | 2016-06-30 | Command Injection - Generic | SMTP command injection |
| [147220](https://hackerone.com/reports/147220) | FantasyTote |  | - | 10 | 2016-06-25 | Command Injection - Generic | Urgent Fix Balance Limit bypass |
| [175403](https://hackerone.com/reports/175403) | Brave Software | medium | - | 10 | 2016-11-03 | Command Injection - Generic | [website] Script injection in newsletter signup https://brave.com/brave_youth_program_signup.html |
| [191243](https://hackerone.com/reports/191243) | U.S. Dept Of Defense | medium | - | 10 | 2017-03-16 | Unrestricted Upload of File with Dangerous Type | File upload vulnerability on a DoD website |
| [218088](https://hackerone.com/reports/218088) | RubyGems | high | - | 10 | 2017-08-30 | Code Injection | Request Hijacking Vulnerability in RubyGems 2.6.11 and earlier |
| [220185](https://hackerone.com/reports/220185) | Skyliner |  | - | 10 | 2017-04-11 | Deserialization of Untrusted Data | Password reset Token not expiring |
| [231926](https://hackerone.com/reports/231926) | U.S. Dept Of Defense | critical | - | 10 | 2017-06-14 | Code Injection | Remote Code Execution (RCE) in a DoD website |
| [274264](https://hackerone.com/reports/274264) | Rockstar Games | medium | - | 10 | 2018-04-10 | Code Injection | Your support community suffers from angularjs injection and must be fixed immediately [CRITICAL] |
| [301458](https://hackerone.com/reports/301458) | Automattic | critical | - | 10 | 2018-04-14 | Code Injection | Remote Code Execution in Wordpress Desktop |
| [389561](https://hackerone.com/reports/389561) | Node.js third-party modules | high | - | 10 | 2019-01-06 | Command Injection - Generic | Command Injection Vulnerability in kill-port Package |
| [394294](https://hackerone.com/reports/394294) | Node.js third-party modules | critical | - | 10 | 2018-09-02 | Command Injection - Generic | [samsung-remote] Command injection |
| [405694](https://hackerone.com/reports/405694) | Node.js third-party modules | critical | - | 10 | 2018-10-18 | Command Injection - Generic | [apex-publish-static-files] Command Injection on connectString |
| [532667](https://hackerone.com/reports/532667) | Node.js third-party modules | high | - | 10 | 2019-10-03 | Code Injection | Server Side JavaScript Code Injection |
| [630903](https://hackerone.com/reports/630903) | Monero | high | - | 10 | 2019-11-18 | Code Injection | Monero Wallet Gui for Windows (Arbitrary Code Execution) |
| [685447](https://hackerone.com/reports/685447) | Node.js third-party modules | critical | - | 10 | 2019-09-13 | OS Command Injection | gitlabhook OS Command Injection |
| [1067291](https://hackerone.com/reports/1067291) | U.S. Dept Of Defense | high | - | 10 | 2021-04-08 | Code Injection | RCE in ██████ subdomain via CVE-2017-1000486 |
| [1175840](https://hackerone.com/reports/1175840) | GitHub Security Lab |  | - | 10 |  | Code Injection | [Java] CWE-094: Query to detect Groovy Code Injections |
| [1332433](https://hackerone.com/reports/1332433) | Nextcloud | critical | - | 10 | 2021-10-20 | Code Injection | RCE on 17 different Docker containers on your network |
| [1350444](https://hackerone.com/reports/1350444) | Concrete CMS | medium | - | 10 | 2021-11-11 | Code Injection | A bypass of adding remote files in concrete5 FIlemanager leads to remote code execution |
| [1092](https://hackerone.com/reports/1092) | Yahoo! |  | - | 9 |  | Code Injection | Directory Traversal |
| [2127](https://hackerone.com/reports/2127) | Yahoo! |  | - | 9 |  | Command Injection - Generic | HK.Yahoo.Net Remote Command Execution |
| [54034](https://hackerone.com/reports/54034) | HackerOne |  | - | 9 | 2016-04-25 | Code Injection | Reflected Filename Download |
| [84374](https://hackerone.com/reports/84374) | ownCloud |  | - | 9 | 2015-09-01 | Code Injection | apps.owncloud.com: Malicious file upload leads to remote code execution |
| [157465](https://hackerone.com/reports/157465) | Gratipay | none | - | 9 | 2016-08-07 | Command Injection - Generic | Host Header Injection/Redirection Attack |
| [159985](https://hackerone.com/reports/159985) | Mail.ru |  | - | 9 |  | Command Injection - Generic | [realty.mail.ru] XSS, SSI Injection |
| [182637](https://hackerone.com/reports/182637) | Pushwoosh | critical | - | 9 | 2016-11-17 | Command Injection - Generic | Administrator Access To Management Console |
| [187542](https://hackerone.com/reports/187542) | Brave Software | critical | - | 9 | 2018-09-18 | Command Injection - Generic | Brave Browser unexpectedly allows to send arbitrary IPC messages |
| [192931](https://hackerone.com/reports/192931) | U.S. Dept Of Defense | high | - | 9 | 2017-07-03 | Code Injection | Server-side include injection vulnerability in a DoD website |
| [218342](https://hackerone.com/reports/218342) | Ruby | medium | - | 9 | 2017-04-05 | Remote File Inclusion | RCE (Remote Code Execution) Vulnerability on Ruby |
| [226783](https://hackerone.com/reports/226783) | Ubiquiti Inc. | low | - | 9 | 2017-06-22 | Code Injection | HTML Injection on airlink.ubnt.com |
| [263913](https://hackerone.com/reports/263913) | GSA Bounty |  | - | 9 | 2020-02-08 | Code Injection | Content injection via URL parameter. |
| [294147](https://hackerone.com/reports/294147) | Internet Bug Bounty | critical | - | 9 | 2019-09-26 | Command Injection - Generic | Mercurial git subrepo lead to arbritary command injection |
| [319476](https://hackerone.com/reports/319476) | Node.js third-party modules | critical | - | 9 | 2018-03-28 | Command Injection - Generic | `whereis` concatenates unsanitized input into exec() command |
| [329376](https://hackerone.com/reports/329376) | U.S. Dept Of Defense | critical | - | 9 | 2019-10-08 | Deserialization of Untrusted Data | Remote Code Execution (RCE) in a DoD website |
| [346575](https://hackerone.com/reports/346575) | Cloudflare Vulnerability Disclosure |  | - | 9 |  | Remote File Inclusion | Remote file inclusion using "/cdn-cgi/pe/bag2?r[]=" |
| [390865](https://hackerone.com/reports/390865) | Node.js third-party modules | medium | - | 9 | 2018-10-14 | Command Injection - Generic | Command Injection Vulnerability in libnmap Package |
| [631227](https://hackerone.com/reports/631227) | Nextcloud | none | - | 9 | 2019-07-26 | Code Injection | Some HTML Tags are Getting Executed in com.nextcloud.client |
| [769998](https://hackerone.com/reports/769998) | Automattic | low | - | 9 | 2020-01-14 | Unrestricted Upload of File with Dangerous Type | Theme Assets uploader allows HTML content |
| [820146](https://hackerone.com/reports/820146) | Nextcloud |  | - | 9 | 2020-06-25 | Code Injection | PHPUnit is included in groupfolders release package potentially causing RCE |
| [823588](https://hackerone.com/reports/823588) | Stripo Inc | medium | - | 9 | 2020-04-13 | Unrestricted Upload of File with Dangerous Type | Unrestricted File Upload on https://my.stripo.email and https://stripo.email |
| [3645415](https://hackerone.com/reports/3645415) | curl |  | - | 9 | 2026-04-06 | Exposed Dangerous Method or Function | # SCURLOPT_SSH_KNOWNHOSTS and host fingerprint pins are silently bypassed when an SSH connection is reused from the connection pool |
| [2106](https://hackerone.com/reports/2106) | Internet Bug Bounty |  | - | 8 | 2013-12-10 | Code Injection | Flash type confusion vulnerability leads to code execution |
| [60058](https://hackerone.com/reports/60058) | Udemy |  | - | 8 | 2015-06-09 | Code Injection | teach.udemy.com log poison vulnerability through wordpress debug.log being publically available |
| [115978](https://hackerone.com/reports/115978) | Imgur |  | - | 8 | 2016-03-14 | Command Injection - Generic | SSRF / Local file enumeration / DoS due to improper handling of certain file formats by ffmpeg |
| [188078](https://hackerone.com/reports/188078) | Brave Software | high | - | 8 | 2017-08-10 | Command Injection - Generic | Command Execution because of extension handling |
| [219323](https://hackerone.com/reports/219323) | Gratipay | medium | - | 8 | 2017-11-03 | Command Injection - Generic | CSV injection in gratipay.com via payment history export feature. |
| [226245](https://hackerone.com/reports/226245) | U.S. Dept Of Defense | critical | - | 8 | 2017-07-05 | Code Injection | Remote code execution (RCE) in multiple DoD websites |
| [313245](https://hackerone.com/reports/313245) | Ubiquiti Inc. | high | - | 8 | 2018-06-19 | Command Injection - Generic | Code Execution in restricted CLI of EdgeSwitch |
| [346516](https://hackerone.com/reports/346516) | Node.js third-party modules | critical | - | 8 | 2019-04-03 | Code Injection | Remote code executio in  NPM package getcookies |
| [350418](https://hackerone.com/reports/350418) | Node.js third-party modules | high | - | 8 | 2018-06-19 | Code Injection | Insecure implementation of deserialization in cryo |
| [390848](https://hackerone.com/reports/390848) | Node.js third-party modules | medium | - | 8 | 2018-09-07 | Command Injection - Generic | Command Injection is ps Package |
| [392311](https://hackerone.com/reports/392311) | RubyGems | critical | - | 8 | 2018-08-09 | Command Injection - Generic | Malware in `active-support` gem |
| [411270](https://hackerone.com/reports/411270) | Informatica | critical | - | 8 | 2018-09-21 | Command Injection - Generic | Cisco RCE |
| [415233](https://hackerone.com/reports/415233) | h1-5411-CTF | critical | - | 8 | 2018-10-22 | Command Injection - Generic | h1-5411-CTF report: LFI / Deserialization / XXE vulnerability, |
| [418308](https://hackerone.com/reports/418308) | 8x8 | critical | - | 8 | 2020-06-09 | Code Injection | [CRITICAL] Remote code execution on http://axa.dxi.eu |
| [660565](https://hackerone.com/reports/660565) | Node.js third-party modules | high | - | 8 | 2020-02-07 | Remote File Inclusion | [jsreport] Remote Code Execution |
| [745921](https://hackerone.com/reports/745921) | Ruby |  | - | 8 | 2021-05-07 | Code Injection | Code Injection Bug Report |
| [767482](https://hackerone.com/reports/767482) | MTN Group | critical | - | 8 | 2020-07-23 | Code Injection | Java Debug Console Provides Command Injection Without Privellage Esclation |
| [858674](https://hackerone.com/reports/858674) | Node.js third-party modules | critical | - | 8 | 2021-04-16 | Command Injection - Generic | [wireguard-wrapper] Command Injection via insecure command concatenation |
| [894872](https://hackerone.com/reports/894872) | GitHub Security Lab |  | - | 8 |  | Code Injection | CodeQL query to detect Server-Side Template Injections (JavaScript) |
| [904672](https://hackerone.com/reports/904672) | Node.js third-party modules | high | - | 8 | 2021-06-28 | Code Injection | Server-side Template Injection in lodash.js |
| [941421](https://hackerone.com/reports/941421) | New Relic |  | - | 8 |  | Code Injection | One Click Remote Code Injection - *.blog.newrelic.com |
| [954398](https://hackerone.com/reports/954398) | U.S. Dept Of Defense | high | - | 8 | 2020-09-03 | Code Injection | Сode injection host  █████████ |
| [1166535](https://hackerone.com/reports/1166535) | Homebrew | medium | - | 8 | 2021-04-30 | Code Injection | Brew bootstrap process is insecure |
| [1249456](https://hackerone.com/reports/1249456) | U.S. Dept Of Defense | high | - | 8 | 2021-07-29 | Code Injection | Pre-auth RCE in ForgeRock OpenAM (CVE-2021-35464) |
| [1415436](https://hackerone.com/reports/1415436) | Django | high | - | 8 | 2022-01-14 | Deserialization of Untrusted Data | Deserialization of potentially malicious data to RCE |
| [3118915](https://hackerone.com/reports/3118915) | curl | high | - | 8 | 2025-06-30 | Code Injection | Potential XSS vector in curl via unsanitized URL parameter handling |
| [3418760](https://hackerone.com/reports/3418760) | curl |  | - | 8 | 2025-11-11 | Command Injection - Generic | Command Injection - CRITICISM |
| [3419617](https://hackerone.com/reports/3419617) | curl | none | - | 8 | 2025-11-11 | Exposed Dangerous Method or Function | Hash exposed in public repository |
| [4836](https://hackerone.com/reports/4836) | Yahoo! |  | - | 7 |  | Command Injection - Generic | From Unrestricted File Upload to Remote Command Execution |
| [14092](https://hackerone.com/reports/14092) | Slack |  | - | 7 | 2014-07-08 | Code Injection | Remote file Inclusion - RFI in upload |
| [116189](https://hackerone.com/reports/116189) | HackerOne |  | - | 7 | 2016-02-23 | Code Injection | Null byte injection |
| [150520](https://hackerone.com/reports/150520) | Informatica | high | - | 7 | 2018-04-30 | Command Injection - Generic | XXE at Informatica sub-domain |
| [158505](https://hackerone.com/reports/158505) | Instacart |  | - | 7 | 2016-10-18 | Command Injection - Generic | Reflected File Download on recipe list search |
| [183458](https://hackerone.com/reports/183458) | Ubiquiti Inc. | high | - | 7 | 2017-12-11 | Command Injection - Generic | Command injection in the process of downloading the latest version of the cloud key firmware through the unifi management software. |
| [212022](https://hackerone.com/reports/212022) | U.S. Dept Of Defense | critical | - | 7 | 2017-06-01 | Code Injection | Remote Code Execution (RCE) in a DoD website |
| [213776](https://hackerone.com/reports/213776) | U.S. Dept Of Defense |  | - | 7 | 2017-04-07 | Code Injection | Remote Command Execution on a DoD website |
| [223344](https://hackerone.com/reports/223344) | Weblate | low | - | 7 | 2017-05-17 | OS Command Injection | CSV Injection with the CSV export feature |
| [228825](https://hackerone.com/reports/228825) | Nextcloud | critical | - | 7 | 2020-03-01 | Code Injection | (Authenticated) RCE by bypassing of the .htaccess blacklist |
| [236607](https://hackerone.com/reports/236607) | ExpressionEngine | medium | - | 7 | 2018-04-04 | Code Injection | Remote Code Execution in the Import Channel function |
| [245228](https://hackerone.com/reports/245228) | Automattic | medium | - | 7 | 2017-09-11 | Code Injection | Object Injection in Woocommerce / Handle PDT Responses from PayPal |
| [302289](https://hackerone.com/reports/302289) | Cloudflare Vulnerability Disclosure |  | - | 7 |  | Code Injection | // (double slash) inside es6 template literals interpreted as an inline comment by the auto-minifier |
| [315773](https://hackerone.com/reports/315773) | Node.js third-party modules | critical | - | 7 | 2018-06-14 | Command Injection - Generic | Remote Command Execution vulnerability in pullit |
| [350401](https://hackerone.com/reports/350401) | Node.js third-party modules | high | - | 7 | 2018-06-15 | Code Injection | Insecure implementation of deserialization in funcster |
| [388936](https://hackerone.com/reports/388936) | Node.js third-party modules | high | - | 7 | 2018-08-19 | Command Injection - Generic | [egg-scripts] Command injection |
| [470553](https://hackerone.com/reports/470553) | Kaspersky | medium | - | 7 | 2019-11-24 | Command Injection - Generic | Unauthorized command execution in Web protection component of Anti-Virus products family [FF, Chrome] |
| [566056](https://hackerone.com/reports/566056) | Node.js third-party modules | medium | - | 7 | 2019-08-20 | Remote File Inclusion | [larvitbase-api] Unintended Require |
| [632721](https://hackerone.com/reports/632721) | U.S. Dept Of Defense | critical | - | 7 | 2019-10-04 | Code Injection | Root Remote Code Execution on https://███ |
| [672243](https://hackerone.com/reports/672243) | Informatica | critical | - | 7 | 2019-08-14 | Code Injection | accounts.informatica.com - RCE due to exposed Groovy console |
| [724599](https://hackerone.com/reports/724599) | Central Security Project | critical | - | 7 | 2020-06-29 | Command Injection - Generic | OS Command Injection in Nexus Repository Manager 2.x -- Bypass for Nexus Repository Manage 2.14.15-01 Command Injection fix |
| [728047](https://hackerone.com/reports/728047) | Node.js third-party modules | medium | - | 7 | 2020-04-25 | Code Injection | [git-promise] RCE via insecure command formatting |
| [772448](https://hackerone.com/reports/772448) | Node.js third-party modules | high | - | 7 | 2020-03-10 | Code Injection | [blamer] RCE via insecure command formatting |
| [950192](https://hackerone.com/reports/950192) | Node.js third-party modules | medium | - | 7 | 2020-09-18 | Command Injection - Generic | [@knutkirkhorn/free-space] - Command Injection through Lack of Sanitization |
| [1161691](https://hackerone.com/reports/1161691) | Ruby | medium | - | 7 | 2021-07-13 | OS Command Injection | OS Command Injection in 'rdoc' documentation generator |
| [1173219](https://hackerone.com/reports/1173219) | New Relic |  | - | 7 |  | Code Injection | HTML Injection In Email In one.newrelic.com |
| [1838674](https://hackerone.com/reports/1838674) | ownCloud | critical | - | 7 | 2023-04-12 | Code Injection | Remote Code Execution on ownCloud instances with ImageMagick installed |
| [3859000](https://hackerone.com/reports/3859000) | Revive Adserver | medium | - | 7 | 2026-11-11 | Code Injection | Formula injection in conversion tracking report export |
| [90131](https://hackerone.com/reports/90131) | Zendesk |  | - | 6 |  | Command Injection - Generic | CSV Excel Macro Injection Vulnerability in export customer tickets |
| [90274](https://hackerone.com/reports/90274) | Zendesk |  | - | 6 |  | Command Injection - Generic | CSV Excel Macro Injection Vulnerability in export chat logs |
| [113831](https://hackerone.com/reports/113831) | Ruby on Rails |  | - | 6 | 2016-03-01 | Code Injection | Regarding [CVE-2016-0752] Possible Information Leak Vulnerability in Action View |
| [114339](https://hackerone.com/reports/114339) | Internet Bug Bounty |  | - | 6 | 2019-10-13 |  | Type Confusion in WDDX Packet Deserialization |
| [147188](https://hackerone.com/reports/147188) | FantasyTote |  | - | 6 | 2016-06-26 | Command Injection - Generic | Stored number of clicks in the Deposits button |
| [149268](https://hackerone.com/reports/149268) | ExpressionEngine |  | - | 6 | 2018-04-04 | Code Injection | Arbitrary file upload when setting an avatar |
| [150375](https://hackerone.com/reports/150375) | Uber |  | - | 6 | 2016-08-22 | Code Injection | newsroom.uber.com is vulnerable to 'SOME' XSS attack via plupload.flash.swf |
| [159213](https://hackerone.com/reports/159213) | Khan Academy |  | - | 6 | 2017-03-01 | Command Injection - Generic | The web app's forgot password page is vulnerable to text injection/content spoofing |
| [175766](https://hackerone.com/reports/175766) | Internet Bug Bounty |  | - | 6 | 2016-12-30 | Code Injection | Remote client memory corruption in ssl_add_clienthello_tlsext() |
| [188561](https://hackerone.com/reports/188561) | Brave Software | critical | - | 6 | 2018-09-18 | Command Injection - Generic | Sending arbitrary IPC messages via overriding Array.prototype.push |
| [192512](https://hackerone.com/reports/192512) | Internet Bug Bounty | critical | - | 6 | 2019-11-12 | Command Injection - Generic | RCE on default Ubuntu Desktop >= 12.10 Quantal |
| [192567](https://hackerone.com/reports/192567) | U.S. Dept Of Defense | high | - | 6 | 2017-06-23 | Code Injection | Remote code execution vulnerability on a DoD website |
| [223999](https://hackerone.com/reports/223999) | Weblate | medium | - | 6 | 2017-05-17 | Command Injection - Generic | CSV export filter bypass leads to formula injection. |
| [273449](https://hackerone.com/reports/273449) | Ubiquiti Inc. | high | - | 6 | 2018-06-19 | OS Command Injection | Authenticated RCE in ToughSwitch |
| [324453](https://hackerone.com/reports/324453) | Node.js third-party modules | critical | - | 6 | 2018-05-11 | Command Injection - Generic | `command-exists` concatenates unsanitized input into exec()/execSync() commands |
| [329399](https://hackerone.com/reports/329399) | U.S. Dept Of Defense | critical | - | 6 | 2019-10-08 | Deserialization of Untrusted Data | Remote Code Execution (RCE) in a DoD website |
| [504355](https://hackerone.com/reports/504355) | 50m-ctf |  | - | 6 |  | Code Injection | Various vulnerabilities ultimately lead to attacker control over FliteThermostat server and access to internal accounting application source code |
| [579560](https://hackerone.com/reports/579560) | Node.js third-party modules | medium | - | 6 | 2019-09-03 | Remote File Inclusion | [larvitbase-www] Unintended Require |
| [661647](https://hackerone.com/reports/661647) | Ubiquiti Inc. | medium | - | 6 | 2020-06-30 | Command Injection - Generic | Local File Disclosure (+XSS+CSRF) in AirOS 6.2.0 devices |
| [809012](https://hackerone.com/reports/809012) | Node.js third-party modules | high | - | 6 | 2020-08-27 | Code Injection | [notevil] - Sandbox Escape Lead to RCE on Node.js and XSS in the Browser |
| [881713](https://hackerone.com/reports/881713) | Node.js third-party modules | high | - | 6 | 2020-11-29 | Command Injection - Generic | [last-commit-log] Command Injection |
| [894308](https://hackerone.com/reports/894308) | Node.js third-party modules | medium | - | 6 | 2020-07-31 | Code Injection | Arbitrary code execution via untrusted schemas in is-my-json-valid |
| [928280](https://hackerone.com/reports/928280) | Nextcloud | medium | - | 6 | 2021-03-04 | Code Injection | Formula Injection vulnerability in CSV export feature |
| [951249](https://hackerone.com/reports/951249) | Node.js third-party modules | medium | - | 6 | 2020-10-14 | Command Injection - Generic | [freespace] Command Injection due to Lack of Sanitization |
| [1121317](https://hackerone.com/reports/1121317) | Acronis | medium | - | 6 | 2021-03-16 | Remote File Inclusion | Unrestricted file upload vulnerability in IMCE |
| [1348154](https://hackerone.com/reports/1348154) | Mail.ru |  | - | 6 |  | Code Injection | RCE в .api/nr/report/{id}/download |
| [1397942](https://hackerone.com/reports/1397942) | GitHub Security Lab |  | - | 6 |  | Code Injection | [GO]: [CWE-090: LDAP Injection All For One] |
| [1537543](https://hackerone.com/reports/1537543) | U.S. Dept Of Defense | critical | - | 6 | 2022-04-29 | Code Injection | ██████████ vulnerable to CVE-2022-22954 |
| [1548535](https://hackerone.com/reports/1548535) | curl | low | - | 6 | 2022-04-24 | Code Injection | --libcurl code injection via trigraphs |
| [5499](https://hackerone.com/reports/5499) | MS-DOS |  | - | 5 | 2014-04-01 | Command Injection - Generic | Arbitrary command execution in MS-DOS |
| [14127](https://hackerone.com/reports/14127) | Slack |  | - | 5 | 2014-12-21 | Command Injection - Generic | SSRF on https://whitehataudit.slack.com/account/photo |
| [31554](https://hackerone.com/reports/31554) | X / xAI |  | - | 5 | 2015-03-22 | Command Injection - Generic | Singup Page HTML Injection Vulnerability |
| [83604](https://hackerone.com/reports/83604) | Khan Academy |  | - | 5 | 2015-12-14 | Command Injection - Generic | Html injection on khanacademy |
| [120219](https://hackerone.com/reports/120219) | Bime |  | - | 5 | 2017-03-18 | Command Injection - Generic | SSRF issue |
| [127032](https://hackerone.com/reports/127032) | New Relic |  | - | 5 |  | Command Injection - Generic | CSV Injection in sub_accounts.csv |
| [145343](https://hackerone.com/reports/145343) | Nextcloud |  | - | 5 | 2018-03-08 | Command Injection - Generic | Possible RCE |
| [160500](https://hackerone.com/reports/160500) | Ian Dunn | low | - | 5 | 2016-10-13 | Command Injection - Generic | Bypassing CSV injection using new line charcter |
| [202652](https://hackerone.com/reports/202652) | U.S. Dept Of Defense | critical | - | 5 | 2017-03-16 | Code Injection | Remote command execution (RCE) vulnerability on a DoD website |
| [223363](https://hackerone.com/reports/223363) | Ruby | medium | - | 5 | 2017-09-15 | Command Injection - Generic | Escape sequence injection vulnerability in WEBrick BasicAuth |
| [246663](https://hackerone.com/reports/246663) | Mail.ru |  | - | 5 |  | Code Injection | [FG-VD-17-115] Mail.ru's Amigo Browser DLL Pre-Loading Vulnerability Notification |
| [274267](https://hackerone.com/reports/274267) | RubyGems | low | - | 5 | 2018-12-08 | Command Injection - Generic | Request Hijacking Vulnerability in RubyGems 2.6.13 and earlier |
| [319467](https://hackerone.com/reports/319467) | Node.js third-party modules | critical | - | 5 | 2018-05-11 | Command Injection - Generic | `macaddress` concatenates unsanitized input into exec() command |
| [341710](https://hackerone.com/reports/341710) | Node.js third-party modules | critical | - | 5 | 2018-06-15 | OS Command Injection | [git-dummy-commit] Command injection on the msg parameter |
| [341869](https://hackerone.com/reports/341869) | Node.js third-party modules | high | - | 5 | 2018-07-18 | Command Injection - Generic | [entitlements] Command injection on the 'path' parameter |
| [390929](https://hackerone.com/reports/390929) | Node.js third-party modules | high | - | 5 | 2019-04-03 | Code Injection | Code Injection Vulnerability in dot Package |
| [415329](https://hackerone.com/reports/415329) | Node.js | medium | - | 5 | 2020-02-13 | Command Injection - Generic | Pull Request #12949 - Security Implications without CVE assignment |
| [534887](https://hackerone.com/reports/534887) | Rocket.Chat | critical | - | 5 | 2021-10-11 | Code Injection | Custom crafted message object in Meteor.Call allows remote code execution and impersonation |
| [660563](https://hackerone.com/reports/660563) | Node.js third-party modules | low | - | 5 | 2020-02-07 | Code Injection | [script-manager] Unintended require |
| [678727](https://hackerone.com/reports/678727) | Nextcloud | high | - | 5 | 2020-04-01 | Code Injection | potential RCE and XSS via file upload requiring user account and default settings |
| [703412](https://hackerone.com/reports/703412) | Node.js third-party modules | high | - | 5 | 2019-12-04 | Code Injection | [node-df] RCE via insecure command concatenation |
| [917843](https://hackerone.com/reports/917843) | Central Security Project | critical | - | 5 | 2020-09-10 | Deserialization of Untrusted Data | Unsafe deserialization in Nexus Repository helm plugin |
| [942103](https://hackerone.com/reports/942103) | Ruby on Rails | none | - | 5 | 2021-02-16 | Command Injection - Generic | Server-side template injection at ujs test server |
| [950853](https://hackerone.com/reports/950853) | QIWI |  | - | 5 |  | Malware | [z.tochka.com] Unlimited file uploads lead to malware executed |
| [972220](https://hackerone.com/reports/972220) | Node.js third-party modules | critical | - | 5 | 2021-01-14 | Code Injection | [arpping] Remote Code Execution |
| [1063039](https://hackerone.com/reports/1063039) | Concrete CMS | medium | - | 5 | 2021-09-24 | Deserialization of Untrusted Data | Phar Deserialization Vulnerability via Logging Settings |
| [1073202](https://hackerone.com/reports/1073202) | Internet Bug Bounty | medium | - | 5 | 2021-07-23 | Code Injection | Canonical Snapcraft vulnerable to remote code execution under certain conditions |
| [1133573](https://hackerone.com/reports/1133573) | GitHub Security Lab |  | - | 5 |  | Code Injection | Java: CWE-652 Improper Neutralization of Data within XQuery Expressions ('XQuery Injection') |
| [1175841](https://hackerone.com/reports/1175841) | GitHub Security Lab |  | - | 5 |  | Code Injection | Java: JSONP Injection |
| [1739099](https://hackerone.com/reports/1739099) | Linux Foundation Decentralized Trust | none | - | 5 | 2022-10-18 |  | CVE-2017-5929: Hyperledger - Arbitrary Deserialization of Untrusted Data |
| [1916285](https://hackerone.com/reports/1916285) | GitLab | low | - | 5 | 2023-06-02 | Command Injection - Generic | Arbitrary escape sequence injection in docker-machine from worker nodes |
| [12583](https://hackerone.com/reports/12583) | Mail.ru |  | - | 4 |  | Command Injection - Generic | XXE and SSRF on webmaster.mail.ru |
| [18371](https://hackerone.com/reports/18371) | jsDelivr |  | - | 4 | 2014-08-20 | Command Injection - Generic | Directory Traversal at http://staging.jsdelivr.net/ |
| [50658](https://hackerone.com/reports/50658) | HackerOne |  | - | 4 | 2015-04-16 | Command Injection - Generic | Reflected File Download attack allows attacker to 'upload' executables to hackerone.com domain |
| [100667](https://hackerone.com/reports/100667) | Shopify |  | - | 4 | 2015-12-01 | Command Injection - Generic | CSV Excel Macro Injection Vulnerability in export list of current users - app.shopify.com |
| [134032](https://hackerone.com/reports/134032) | New Relic |  | - | 4 |  | Code Injection | newrelic.com rails directory traversal vuln |
| [146179](https://hackerone.com/reports/146179) | Nextcloud |  | - | 4 | 2016-06-24 | Command Injection - Generic | REG: Content provider information leakage |
| [159943](https://hackerone.com/reports/159943) | Internet Bug Bounty |  | - | 4 | 2019-10-13 |  | Create an Unexpected Object and Don't Invoke __wakeup() in During Deserialization |
| [164674](https://hackerone.com/reports/164674) | Ian Dunn | low | - | 4 | 2016-10-12 | Command Injection - Generic | CSV Injection in Camptix |
| [179701](https://hackerone.com/reports/179701) | Blockchain |  | - | 4 | 2017-03-08 | Command Injection - Generic | username enumeration |
| [182557](https://hackerone.com/reports/182557) | Brave Software | high | - | 4 | 2017-08-10 | Code Injection | links the user may download can be a malicious files |
| [194564](https://hackerone.com/reports/194564) | Nextcloud | none | - | 4 | 2017-02-18 | Code Injection | Review remote code execution in SwiftMailer |
| [198723](https://hackerone.com/reports/198723) | Internet Bug Bounty | medium | - | 4 | 2019-10-13 |  | Create an Unexpected Object and Don't Invoke __wakeup() in Deserialization |
| [224291](https://hackerone.com/reports/224291) | Weblate | low | - | 4 | 2017-05-17 | Command Injection - Generic | CSV Injection with the CVS export feature - Glossary |
| [226896](https://hackerone.com/reports/226896) | Nextcloud | high | - | 4 | 2017-05-10 | Code Injection | Nextcloud Server Remote Command Execution |
| [231687](https://hackerone.com/reports/231687) | U.S. Dept Of Defense | critical | - | 4 | 2017-07-05 | Code Injection | Remote Code Execution (RCE) vulnerability in multiple DoD websites |
| [263718](https://hackerone.com/reports/263718) | WordPress | high | - | 4 | 2017-10-04 | Code Injection | Wordpress 4.8.1 - Rogue editor leads to RCE. And the risks of same origin frame scripting in general |
| [329400](https://hackerone.com/reports/329400) | U.S. Dept Of Defense | critical | - | 4 | 2019-10-08 | Deserialization of Untrusted Data | Remote Code Execution (RCE) in a DoD website |
| [331032](https://hackerone.com/reports/331032) | Node.js third-party modules | critical | - | 4 | 2018-05-11 | OS Command Injection | [buttle] Remote Command Execution via unsanitized PHP filename when it's run with --php-bin flag |
| [356775](https://hackerone.com/reports/356775) | Open-Xchange |  | - | 4 |  | Command Injection - Generic | command Injection in rawlog binary |
| [459532](https://hackerone.com/reports/459532) | Semrush | medium | - | 4 | 2019-01-11 | Code Injection | Persistent CSV injection |
| [512076](https://hackerone.com/reports/512076) | Revive Adserver | critical | - | 4 | 2019-04-23 | Deserialization of Untrusted Data | Deserialization of Untrusted Data in www/delivery/adxmlrpc.php |
| [630227](https://hackerone.com/reports/630227) | Node.js third-party modules | medium | - | 4 | 2019-10-24 | Command Injection - Generic | Command Injection due to lack of sanitisation of tar.gz filename passed as an argument to pm2.install()  function |
| [634630](https://hackerone.com/reports/634630) | U.S. Dept Of Defense | critical | - | 4 | 2019-10-08 | OS Command Injection | Remote OS command Execution in the 3 more Oracle Weblogic on the ████████, ████, ███████ [CVE-2017-10352] |
| [687325](https://hackerone.com/reports/687325) | Node.js third-party modules | high | - | 4 | 2019-10-04 | Malware | Trojan:JS/CoinMiner in npm files |
| [703415](https://hackerone.com/reports/703415) | Node.js third-party modules | high | - | 4 | 2019-12-04 | Code Injection | [treekill] RCE via insecure command concatenation (only Windows) |
| [728040](https://hackerone.com/reports/728040) | Node.js third-party modules | medium | - | 4 | 2020-01-11 | Code Injection | [meta-git] RCE via insecure command formatting |
| [824925](https://hackerone.com/reports/824925) | GitHub Security Lab |  | - | 4 |  | Code Injection | XPath Injection query in java |
| [904064](https://hackerone.com/reports/904064) | U.S. Dept Of Defense | high | - | 4 | 2021-02-18 | Code Injection | Dashboard sharing enables code injection into ████ emails |
| [983867](https://hackerone.com/reports/983867) | GitHub Security Lab |  | - | 4 |  | Code Injection | Java : add MongoDB injection sinks |
| [1036995](https://hackerone.com/reports/1036995) | Judge.me | none | - | 4 | 2021-12-17 | Command Injection - Generic | HTML injection in review content |
| [1057216](https://hackerone.com/reports/1057216) | Ruby on Rails |  | - | 4 | 2021-06-15 | Code Injection | Regex Injection from request header (Rack::Sendfile, send_file) |
| [1141623](https://hackerone.com/reports/1141623) | Node.js | critical | - | 4 | 2021-06-14 | Use of Inherently Dangerous Function | Unexpected input validation of octal literals in nodejs v15.12.0 and below returns defined values for all undefined octal literals. |
| [1158824](https://hackerone.com/reports/1158824) | Ruby | medium | - | 4 | 2021-07-19 | OS Command Injection | OS Command Injection in '/lib/un.rb -- Utilities to replace common UNIX commands in Makefiles etc' |
| [1241574](https://hackerone.com/reports/1241574) | GitHub Security Lab |  | - | 4 |  | Code Injection | [Java] BeanShell Injection |
| [1241575](https://hackerone.com/reports/1241575) | GitHub Security Lab |  | - | 4 |  |  | [Java]: CWE-502 Add UnsafeDeserialization sinks |
| [1490372](https://hackerone.com/reports/1490372) | GitHub Security Lab |  | - | 4 |  | Code Injection | Java : Add query to detect Server Side Template Injection (SSTI) |
| [1537694](https://hackerone.com/reports/1537694) | U.S. Dept Of Defense | critical | - | 4 | 2022-04-20 | Code Injection | ███ vulnerable to CVE-2022-22954 |
| [1710652](https://hackerone.com/reports/1710652) | Node.js | medium | - | 4 | 2022-12-07 | OS Command Injection | DNS rebinding in --inspect via invalid octal IP address |
| [1781102](https://hackerone.com/reports/1781102) | Rocket.Chat | high | - | 4 | 2022-12-08 | OS Command Injection | Insecure use of shell.openExternal() leads to RCE in Rocket.Chat-Desktop |
| [2904921](https://hackerone.com/reports/2904921) | curl | low | - | 4 | 2025-07-07 | OS Command Injection | OS Command Injection  (subprocess Module Usage) |
| [59663](https://hackerone.com/reports/59663) | Concrete CMS |  | - | 3 | 2015-06-06 | Command Injection - Generic | Sendmail Remote Code Execution Vulnerability in Concrete5 version 5.7.3.1 |
| [73429](https://hackerone.com/reports/73429) | Internet Bug Bounty |  | - | 3 | 2019-10-04 | Code Injection | pngcrush_measure_idat() off-by-one error (CVE-2015-2158) |
| [90415](https://hackerone.com/reports/90415) | Zaption |  | - | 3 | 2015-10-01 | Command Injection - Generic | CSV Excel Macro Injection in Export Response |
| [121863](https://hackerone.com/reports/121863) | Internet Bug Bounty |  | - | 3 | 2016-07-28 | Code Injection | Buffer overflow in HTTP url parsing functions |
| [124223](https://hackerone.com/reports/124223) | HackerOne |  | - | 3 | 2016-04-25 | Command Injection - Generic | CSV Injection via the CSV export feature |
| [130338](https://hackerone.com/reports/130338) | Moneybird |  | - | 3 | 2016-06-13 | Command Injection - Generic | CSV Injection with the CSV export feature |
| [195950](https://hackerone.com/reports/195950) | Internet Bug Bounty | medium | - | 3 | 2017-06-01 | Code Injection | Use of uninitialized memory in unserialize() |
| [203600](https://hackerone.com/reports/203600) | U.S. Dept Of Defense | low | - | 3 | 2017-06-23 | Code Injection | Remote code execution vulnerability on a DoD website |
| [213069](https://hackerone.com/reports/213069) | U.S. Dept Of Defense |  | - | 3 | 2017-05-31 | Code Injection | Remote Code Execution (RCE) in a DoD website |
| [222020](https://hackerone.com/reports/222020) | Internet Bug Bounty | high | - | 3 | 2017-07-12 | Code Injection | Mercurial can be tricked into granting authorized users access to the Python debugger |
| [242119](https://hackerone.com/reports/242119) | Internet Bug Bounty | medium | - | 3 | 2019-11-12 | Command Injection - Generic | Roundcube virtualmin privilege escalation (CVE-2017-8114) |
| [250273](https://hackerone.com/reports/250273) | ExpressionEngine | medium | - | 3 | 2017-09-07 | Code Injection | Image lib - unescaped file path |
| [319473](https://hackerone.com/reports/319473) | Node.js third-party modules | high | - | 3 | 2019-12-13 | Command Injection - Generic | [open] concatenation of unsanitized input into exec() command |
| [326697](https://hackerone.com/reports/326697) | MyCrypto |  | - | 3 | 2018-04-09 | Code Injection | HTML Injection on https://www.mycrypto.com/ |
| [340208](https://hackerone.com/reports/340208) | Node.js third-party modules | medium | - | 3 | 2018-05-29 | Command Injection - Generic | Command injection in 'pdf-image' |
| [413655](https://hackerone.com/reports/413655) | Semmle | low | - | 3 | 2019-07-18 | Command Injection - Generic | Server side includes in https://lgtm-com.pentesting.semmle.net/internal_api/v0.2/savePublicInformation leads to 500 server error and  D-DOS |
| [486502](https://hackerone.com/reports/486502) | Mail.ru |  | - | 3 |  | Code Injection | ICQ Windows Application is Vulnerable to DLL Search Order Hijacking |
| [629879](https://hackerone.com/reports/629879) | Node.js |  | - | 3 | 2020-06-11 | Code Injection | loader.js is not secure |
| [633364](https://hackerone.com/reports/633364) | Node.js third-party modules | medium | - | 3 | 2019-10-24 | Command Injection - Generic | Command Injection in npm module name passed as an argument to pm2.install() function |
| [730121](https://hackerone.com/reports/730121) | Node.js third-party modules | medium | - | 3 | 2020-01-11 | Code Injection | [npm-git-publish] RCE via insecure command formatting |
| [871071](https://hackerone.com/reports/871071) | Node.js third-party modules | critical | - | 3 | 2020-10-27 | Command Injection - Generic | [gfc] Command Injection via insecure command formatting |
| [878181](https://hackerone.com/reports/878181) | Node.js |  | - | 3 | 2020-07-04 | Code Injection | Child process environment injection via prototype pollution |
| [878420](https://hackerone.com/reports/878420) | Node.js third-party modules | critical | - | 3 | 2020-08-24 | Code Injection | [windows-edge] RCE via insecure command formatting |
| [925324](https://hackerone.com/reports/925324) | Node.js third-party modules | critical | - | 3 | 2020-11-16 | Command Injection - Generic | [systeminformation] Command Injection via insecure command formatting |
| [1050706](https://hackerone.com/reports/1050706) | GitHub Security Lab |  | - | 3 |  | Code Injection | [javascript] CWE-90: CodeQL to detect LDAP Injection |
| [1187816](https://hackerone.com/reports/1187816) | Sifchain | none | - | 3 | 2021-12-09 | Code Injection | Dependency Confusion Vulnerability in Sifnode Due to Unclaimed npm Packages. |
| [1189419](https://hackerone.com/reports/1189419) | Ruby | high | - | 3 | 2023-08-01 | Deserialization of Untrusted Data | XMLRPC does not limit deserializable classes. |
| [1193641](https://hackerone.com/reports/1193641) | GlassWire | medium | - | 3 | 2021-11-13 | Code Injection | GlassWire 2.1.167 vulnerability - MSVR 56639 |
| [1196125](https://hackerone.com/reports/1196125) | GitHub Security Lab |  | - | 3 |  | Code Injection | [Java] CWE-078: Add JSch lib OS Command Injection sink |
| [3973249](https://hackerone.com/reports/3973249) | curl |  | - | 3 | 2026-09-14 | Command Injection - Generic | 56: IBM i CL wrapper `parse_command_line()` never enters quote mode |
| [17225](https://hackerone.com/reports/17225) | Uzbey |  | - | 2 | 2014-08-07 | Command Injection - Generic | SQL injection, tile ID |
| [34917](https://hackerone.com/reports/34917) | Block.io |  | - | 2 | 2015-01-01 | Command Injection - Generic | Bypassed or command injection |
| [43988](https://hackerone.com/reports/43988) | X / xAI |  | - | 2 | 2015-04-11 | Command Injection - Generic | twitter android app Fragment Injection |
| [44578](https://hackerone.com/reports/44578) | X / xAI |  | - | 2 | 2015-02-21 | Code Injection | URGENT - SUBDOMAIN TAKEOVER ON TWITTER ACQ. |
| [72976](https://hackerone.com/reports/72976) | Shopify |  | - | 2 | 2015-09-10 | Code Injection | Body injection in mailto link while commenting shop blog |
| [104465](https://hackerone.com/reports/104465) | Square Open Source |  | - | 2 | 2016-01-25 | Command Injection - Generic | git-fastclone allows arbitrary command execution through usage of ext remote URLs in submodules |
| [105190](https://hackerone.com/reports/105190) | Square Open Source |  | - | 2 | 2016-01-25 | Command Injection - Generic | Unsafe usage of Ruby string interpolation enabling command injection in git-fastclone |
| [105980](https://hackerone.com/reports/105980) | ownCloud |  | - | 2 | 2016-01-27 | Command Injection - Generic | XXE at host vpn.owncloud.com |
| [112863](https://hackerone.com/reports/112863) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Code Injection | Trivial age-old heap overflow in 32-bit PHP |
| [118103](https://hackerone.com/reports/118103) | Shopify |  | - | 2 | 2016-03-12 | Code Injection | Injection via CSV Export feature in Admin Orders |
| [163547](https://hackerone.com/reports/163547) | New Relic |  | - | 2 |  | Code Injection | Java RMI (Remote Code Execution) |
| [165969](https://hackerone.com/reports/165969) | Internet Bug Bounty |  | - | 2 | 2019-11-12 | Code Injection | The “Malstaller” Attack, global hijacking of any installation process to achieve RCE with elevated privileges, Windows OS (vendor agnostic) |
| [250587](https://hackerone.com/reports/250587) | ExpressionEngine | medium | - | 2 | 2017-09-07 | Code Injection | Potential code injection in fun delete_directory |
| [272272](https://hackerone.com/reports/272272) | Bitwarden |  | - | 2 | 2017-09-28 | OS Command Injection | Export vault feature is vulnerable to CSV injection |
| [272979](https://hackerone.com/reports/272979) | U.S. Dept Of Defense | critical | - | 2 | 2019-10-08 | Deserialization of Untrusted Data | 2 vulnerabilities of arbitrary code in ████████  - CVE-2017-5929 |
| [282628](https://hackerone.com/reports/282628) | X / xAI | medium | - | 2 | 2017-11-02 | OS Command Injection | OS Command Execution on User's PC via CSV Injection |
| [299034](https://hackerone.com/reports/299034) | RBKmoney | none | - | 2 | 2018-01-29 | Code Injection | Text manipulation in https://checkout.rbk.money |
| [324491](https://hackerone.com/reports/324491) | Node.js third-party modules | critical | - | 2 | 2018-05-11 | Command Injection - Generic | `fs-path` concatenates unsanitized input into exec()/execSync() commands |
| [413388](https://hackerone.com/reports/413388) | Ruby on Rails | high | - | 2 | 2020-05-26 | Deserialization of Untrusted Data | Untrusted strings that are cache fetched with raw option are automatically marshal loaded |
| [694471](https://hackerone.com/reports/694471) | Node.js third-party modules | critical | - | 2 | 2020-10-26 | Code Injection | [create-git] RCE via insecure command formatting |
| [718241](https://hackerone.com/reports/718241) | Node.js third-party modules | medium | - | 2 | 2020-09-24 | Code Injection | [git-lib] RCE via insecure command formatting |
| [730111](https://hackerone.com/reports/730111) | Node.js third-party modules | medium | - | 2 | 2020-09-24 | Code Injection | [gity] RCE via insecure command formatting |
| [864354](https://hackerone.com/reports/864354) | Node.js third-party modules | critical | - | 2 | 2020-07-23 | Command Injection - Generic | [diskstats] Command Injection via insecure command concatenation |
| [901799](https://hackerone.com/reports/901799) | U.S. Dept Of Defense | high | - | 2 | 2020-07-30 | Unrestricted Upload of File with Dangerous Type | Stored XSS on ████████helpdesk |
| [1198203](https://hackerone.com/reports/1198203) | Sifchain | low | - | 2 | 2021-09-06 | Inclusion of Functionality from Untrusted Control Sphere | Bootstrap library is vulnerable |
| [1411867](https://hackerone.com/reports/1411867) | Ruby on Rails | medium | - | 2 | 2023-06-28 | Code Injection | Escape Sequence Injection vulnerability in Rack |
| [1859592](https://hackerone.com/reports/1859592) | Linux Foundation Decentralized Trust | none | - | 2 | 2023-04-27 | OS Command Injection | [indy_node]POOL_UPGRADE command injection, Trustee Node can execute command in any other Node`s system. |
| [14248](https://hackerone.com/reports/14248) | Yahoo! |  | - | 1 |  | Code Injection | Multiple vulnerabilities |
| [57263](https://hackerone.com/reports/57263) | WordPoints |  | - | 1 | 2015-06-04 | Command Injection - Generic | Rank Creation function not validating user inputs. |
| [73242](https://hackerone.com/reports/73242) | Internet Bug Bounty |  | - | 1 | 2015-01-08 | Code Injection | libcurl: URL request injection |
| [92353](https://hackerone.com/reports/92353) | Automattic |  | - | 1 | 2015-11-20 | Code Injection | CSV Injection in polldaddy.com |
| [95804](https://hackerone.com/reports/95804) | Mail.ru |  | - | 1 |  | Command Injection - Generic | [api.allodsteam.com] Authentication Data |
| [103432](https://hackerone.com/reports/103432) | Urban Dictionary |  | - | 1 | 2016-01-04 | Code Injection | URGENT - Subdomain Takeover in support.urbandictionary.com pointing to Zendesk |
| [112855](https://hackerone.com/reports/112855) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Code Injection | EIP control using type confusion in json encoding |
| [114389](https://hackerone.com/reports/114389) | Eternal |  | - | 1 | 2016-03-06 | Code Injection | Remote File Upload Vulnerability in business-blog.zomato.com |
| [116937](https://hackerone.com/reports/116937) | Zendesk |  | - | 1 |  | Command Injection - Generic | Chat History CSV Export Excel Injection Vulnerability |
| [123649](https://hackerone.com/reports/123649) | New Relic |  | - | 1 |  | Command Injection - Generic | Synthetics Xss |
| [139875](https://hackerone.com/reports/139875) | Uber |  | - | 1 | 2016-05-26 | Code Injection | DOM based XSS on |
| [146255](https://hackerone.com/reports/146255) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Code Injection | Double Free Corruption in wddx.c (extension) |
| [146735](https://hackerone.com/reports/146735) | Uber |  | - | 1 | 2016-07-07 | Command Injection - Generic | Command Injection, Information |
| [152278](https://hackerone.com/reports/152278) | Internet Bug Bounty |  | - | 1 | 2019-11-12 | Code Injection | Stack-based buffer overflow vulnerability in php_stream_zip_opener |
| [161290](https://hackerone.com/reports/161290) | Ian Dunn |  | - | 1 | 2016-09-27 | Command Injection - Generic | bypass to csv injection |
| [170748](https://hackerone.com/reports/170748) | RubyGems |  | - | 1 | 2018-02-08 | Command Injection - Generic | RCE,SQL,Vulnerability + Exploit Method. |
| [216998](https://hackerone.com/reports/216998) | Dropbox |  | - | 1 |  | Code Injection | CSV Injection with the CVS export feature |
| [245233](https://hackerone.com/reports/245233) | WakaTime |  | - | 1 | 2021-10-12 | Code Injection | HTML - injection |
| [327512](https://hackerone.com/reports/327512) | Ruby | none | - | 1 | 2019-10-16 | Command Injection - Generic | Potential command injection in `Shell#[]` and `Shell#test` |
| [390871](https://hackerone.com/reports/390871) | Node.js third-party modules | high | - | 1 | 2018-08-10 | Command Injection - Generic | Command Injection Vulnerability in win-fork/win-spawn Packages |
| [661959](https://hackerone.com/reports/661959) | Node.js third-party modules | medium | - | 1 | 2020-01-30 | Command Injection - Generic | Command Injection vulnerability in kill-port-process package |
| [863956](https://hackerone.com/reports/863956) | Node.js third-party modules | critical | - | 1 | 2020-08-22 | Command Injection - Generic | [extra-asciinema] Command Injection via insecure command formatting |
| [897974](https://hackerone.com/reports/897974) | Node.js third-party modules | low | - | 1 | 2020-08-14 | Code Injection | Arbitrary code execution via untrusted schemas in ajv |
| [973386](https://hackerone.com/reports/973386) | Node.js third-party modules | critical | - | 1 | 2021-01-14 | Command Injection - Generic | [curling] Remote Code Execution |
| [1090678](https://hackerone.com/reports/1090678) | Ruby | low | - | 1 | 2021-03-07 | Command Injection - Generic | Command injection in OptionParser.load |
| [1471622](https://hackerone.com/reports/1471622) | GitHub Security Lab |  | - | 1 |  | Code Injection | [Python]: Add shutil module sinks for path injection query |
| [1631364](https://hackerone.com/reports/1631364) | U.S. Dept Of Defense | critical | - | 1 | 2022-09-06 | Code Injection | ██████_log4j - https://██████ |
| [1631370](https://hackerone.com/reports/1631370) | U.S. Dept Of Defense | critical | - | 1 | 2022-09-06 | Code Injection | solr_log4j - http://██████████ |
| [1763343](https://hackerone.com/reports/1763343) | Linux Foundation Decentralized Trust | none | - | 1 | 2023-02-07 | Code Injection | Dependency confusion in https://github.com/hyperledger/aries-mobile-agent-react-native |
| [104010](https://hackerone.com/reports/104010) | Internet Bug Bounty |  | - | 0 | 2015-09-02 | Code Injection | SOAP serialize_function_call() type confusion / RCE |
| [104017](https://hackerone.com/reports/104017) | Internet Bug Bounty |  | - | 0 | 2015-08-04 | Code Injection | Arbitrary code execution in str_ireplace function |
| [511459](https://hackerone.com/reports/511459) | Node.js third-party modules | critical | - | 0 | 2020-02-02 | OS Command Injection | [listening-processes] Command Injection |
| [863944](https://hackerone.com/reports/863944) | Node.js third-party modules | critical | - | 0 | 2020-08-20 | Command Injection - Generic | [extra-ffmpeg] Command Injection via insecure command formatting |
| [864777](https://hackerone.com/reports/864777) | Node.js third-party modules | critical | - | 0 | 2020-08-20 | Command Injection - Generic | [vboxmanage.js] Command Injection via insecure command concatenation |
| [865168](https://hackerone.com/reports/865168) | Node.js third-party modules | critical | - | 0 | 2020-07-23 | Command Injection - Generic | [xps] Command Injection via insecure command concatenation |
| [885031](https://hackerone.com/reports/885031) | Node.js third-party modules | medium | - | 0 | 2020-09-24 | Code Injection | [commit-msg] RCE via insecure command formatting |
| [973245](https://hackerone.com/reports/973245) | Node.js third-party modules | critical | - | 0 | 2021-01-14 | Code Injection | [imagickal] Remote Code Execution |
| [1437942](https://hackerone.com/reports/1437942) | Monero | medium | - | 0 | 2021-12-30 | Code Injection | DLL hijacking in Monero GUI for Windows 0.17.3.0 would allow an attacker to perform remote command execution |
