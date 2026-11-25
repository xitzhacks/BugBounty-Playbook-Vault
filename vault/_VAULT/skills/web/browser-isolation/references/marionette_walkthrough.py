from marionette_driver.marionette import Marionette
from marionette_driver import Wait

# Connect to OUR isolated Firefox (Marionette port, never the user's browser).
# Launch that instance first:
#   firefox --no-remote --new-instance --profile /tmp/ff-iso --no-sync --marionette 2828 about:blank
client = Marionette(host='127.0.0.1', port=2828)
client.start_session()

links = [
    ("home",      "http://www.evil.com/"),
    ("Lies",      "http://www.evil.com/projectX.htm"),
    ("Shouts",    "http://www.evil.com/shoutout.htm"),
    ("Archives",  "http://www.evil.com/archives/index.htm"),
    ("Static",    "http://www.evil.com/static.html"),
    ("Financials","https://evil.com/lucre/index.html"),
]

for name, url in links:
    try:
        client.navigate(url)
        Wait(client, timeout=20).until(
            lambda m: m.execute_script("return document.readyState") == "complete")
    except Exception as ex:
        print(f"\n### {name} -> {url}\n  NAV ERROR: {ex}")
        continue

    info = client.execute_script("""
      const r={};
      r.url=location.href;
      r.title=document.title;
      r.text=(document.body? document.body.innerText : '').trim().slice(0,600);
      r.h1=(document.querySelector('h1')? document.querySelector('h1').innerText : '');
      r.links=[];
      document.querySelectorAll('a').forEach(a=>{
        const b=a.getBoundingClientRect();
        if(b.width>0||b.height>0 || a.href) r.links.push({t:(a.textContent||'').trim().slice(0,50), h:a.href});
      });
      r.forms=document.querySelectorAll('form').length;
      r.inputs=document.querySelectorAll('input,button,select,textarea').length;
      r.scripts=document.querySelectorAll('script').length;
      return r;
    """)

    print(f"\n{'='*70}")
    print(f"PAGE: {name}")
    print(f"URL : {info['url']}")
    print(f"TITLE: {info['title']}")
    print(f"H1  : {info['h1']}")
    print(f"forms={info['forms']} inputs/buttons={info['inputs']} scripts={info['scripts']} links_on_page={len(info['links'])}")
    print("--- body text (first 600 chars) ---")
    print(info['text'])
    print(f"--- links found on this page ({len(info['links'])}) ---")
    for l in info['links'][:15]:
        print(f"   - '{l['t']}' -> {l['h']}")

client.delete_session()
print("\n\nWALK COMPLETE — all links interacted with.")
