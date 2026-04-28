"""Update widget data URLs to Selectel bucket.
Usage: python3 update_urls.py <bucket-url>
Example: python3 update_urls.py https://glukhova-photos.storage.selectel.ru
"""
import json, base64, glob, sys

BUCKET = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else ""

with open("api/widgets-combined.json") as f:
    raw = f.read()

raw = raw.replace('"i-p.rmcdn.net/', f'"{BUCKET}/glukhova-dasha/originals/')
raw = raw.replace("https://c-p.rmcdn.net/", f"{BUCKET}/glukhova-dasha/originals/")

with open("api/widgets-combined.json", "w") as f:
    f.write(raw)

widgets = json.loads(raw)
b64_data = base64.b64encode(raw.encode("utf-8")).decode("ascii")

ServerData = json.loads(
    open("index.html").read()
    .split("window.ServerData =")[1].split("</script>")[0].strip().rstrip(";")
)
page_wids = {p["_id"]: p.get("wids", []) for p in ServerData["mags"]["mag"]["pages"]}

interceptor = """<script>
(function(){
var B='B64_DATA',W=JSON.parse(decodeURIComponent(escape(atob(B))));
var PW=PAGE_WIDS_MAP;
var F=window.fetch.bind(window);
window.fetch=function(u,o){
var U=(typeof u=='string'?u:(u&&u.url))||'';
if(U.indexOf('/api/viewer/project/')>-1&&U.indexOf('widgets')>-1){
var m=U.match(/pageId=([a-f0-9]+)/);var p=m?m[1]:null;var w=PW[p]||[];var f=W.filter(function(x){return w.indexOf(x.wid)>=0});
return Promise.resolve(new Response(JSON.stringify(f),{status:200,headers:{'Content-Type':'application/json'}}))}
if(U.indexOf('/api/countview/')>-1||U.indexOf('/api/proxy/')>-1)
return Promise.resolve(new Response('ok',{status:200}));
return F(u,o)};window.XMLHttpRequest=void 0})();
</script>"""
interceptor = interceptor.replace("B64_DATA", b64_data)
interceptor = interceptor.replace("PAGE_WIDS_MAP", json.dumps(page_wids, ensure_ascii=False))

for fname in sorted(glob.glob("*.html")):
    content = open(fname).read()
    for marker in ["var B64_DATA", "var WIDGETS", "var WIDGETS_STR"]:
        while True:
            idx = content.find(marker)
            if idx < 0: break
            s = content.rfind("<script>", 0, idx)
            e = content.find("</script>", idx)
            if s >= 0 and e > 0: content = content[:s] + content[e+9:]
            else: break
    content = content.replace("</body>", interceptor + "\n</body>")
    open(fname, "w").write(content)

print(f"URLs updated to: {BUCKET}/glukhova-dasha/originals/")
