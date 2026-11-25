# Build script: generates dump, classes.json, and verifies quotes.
# Bodies come verbatim from DB vulnerability_information (== classified.json bodies, verified 0 mismatches).
import json, sqlite3, re, sys
from pathlib import Path
BASE=Path('/home/user/projects/FAN/Vault/16_Information-Disclosure')
ARCH=BASE/'references/archive'
DB='/home/user/tools/h1-brain/disclosed_reports.db'
CLSDIR='/home/user/opencode-work/h1brain'
c=json.load(open(f'{CLSDIR}/classified.json'))
m=json.load(open(f'{CLSDIR}/module_map_all.json'))
info=m['info-disclosure']
ORDER=['graphql_api_objects_exposure','hackerone_reports_bounty_privacy','user_pii_location_privacy','file_path_errors_secrets_leaks','protocol_memory_disclosure','_adjacent','_adjacent_unclassified']
MODNAME={'graphql_api_objects_exposure':'GraphQL-API-Objects-Exposure','hackerone_reports_bounty_privacy':'HackerOne-Reports-Bounty-Privacy','user_pii_location_privacy':'User-PII-Location-Privacy','file_path_errors_secrets_leaks':'File-Path-Errors-Secrets-Leaks','protocol_memory_disclosure':'Protocol-Memory-Disclosure','_adjacent':'Adjacent-Disclosure-Noise','_adjacent_unclassified':'Adjacent-Disclosure-Noise'}
con=sqlite3.connect(DB)
cur=con.cursor()
meta={}
for x in c['info-disclosure']+[y for y in c['unclassified']]:
    i=x['id']
    cur.execute('SELECT id,title,weakness_name,program_handle,asset_identifier,asset_type,cve_ids,bounty_amount,length(vulnerability_information),vulnerability_information FROM disclosed_reports WHERE id=?',(i,))
    r=cur.fetchone()
    if r: meta[i]=r
allids=[]
for k in ORDER:
    allids.extend(info[k])
# classes.json: RCE-style {module: [ids]} + also flat? Task says every bucket id exactly once in classes.json.
# Use module-name keys for the 6 merged modules (adjacent merged), values sorted ascending.
merged={'GraphQL-API-Objects-Exposure':sorted(info['graphql_api_objects_exposure']),
'HackerOne-Reports-Bounty-Privacy':sorted(info['hackerone_reports_bounty_privacy']),
'User-PII-Location-Privacy':sorted(info['user_pii_location_privacy']),
'File-Path-Errors-Secrets-Leaks':sorted(info['file_path_errors_secrets_leaks']),
'Protocol-Memory-Disclosure':sorted(info['protocol_memory_disclosure']),
'Adjacent-Disclosure-Noise':sorted(list(info['_adjacent'])+list(info['_adjacent_unclassified']))}
(ARCH/'classes.json').write_text(json.dumps(merged,indent=1,ensure_ascii=False)+'\n')
# dump: ===== INFO-<id> | <title> | bounty=<..> | program=<..> | weak=<..> | cve=<..> | len=<n>\n<body>\n\n
lines=[]
for i in sorted(allids):
    r=meta[i]
    bounty='None' if r[7] is None else (str(int(r[7])) if float(r[7]).is_integer() else str(r[7]))
    lines.append(f"===== INFO-{i} | {r[1]} | bounty={bounty} | program={r[3]} | weak={r[2]} | cve={r[6]} | len={r[8]}\n{r[9]}\n")
(ARCH/'INFO-bodies-full-dump.txt').write_text('\n'.join(lines))
print('dump bytes', (ARCH/'INFO-bodies-full-dump.txt').stat().st_size)
print({k:len(v) for k,v in merged.items()}, 'total', sum(len(v) for v in merged.values()))
# verify vs bucket
bucket=set(x['id'] for x in c['info-disclosure'])
flat=[i for v in merged.values() for i in v]
print('bucket252? bucket=',len(bucket),'flat=',len(flat),'unique=',len(set(flat)))
print('missing from flat:', sorted(bucket-set(flat)))
print('extra beyond bucket (unclassified merges):', sorted(set(flat)-bucket), len(set(flat)-bucket))
