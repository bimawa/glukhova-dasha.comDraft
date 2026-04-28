import json, re, base64, glob

WIDGETS = json.load(open("api/widgets-combined.json"))
widgets_json = json.dumps(WIDGETS, ensure_ascii=False)
b64_data = base64.b64encode(widgets_json.encode("utf-8")).decode("ascii")
print(f"Widget data: {len(WIDGETS)} total, {len(b64_data)} bytes base64")

ServerData = json.loads(
    open("index.html").read()
    .split("window.ServerData =")[1]
    .split("</script>")[0].strip().rstrip(";")
)
PAGES = ServerData["mags"]["mag"]["pages"]

# Build pageId → wids mapping
page_wids = {}
for p in PAGES:
    pid = p["_id"]
    wids = p.get("wids", [])
    page_wids[pid] = wids
    label = p.get("label", "?")
    print(f"  Page {label:20s} ({pid[:12]}...): {len(wids)} widgets")

page_wids_json = json.dumps(page_wids, ensure_ascii=False)

interceptor = """<script>
(function(){
var B='B64_DATA',W=JSON.parse(decodeURIComponent(escape(atob(B))));
var PW=PAGE_WIDS_MAP;
function gU(u){return typeof u=='string'?u:(u&&u.url)||''}
function eP(u){var m=u.match(/pageId=([a-f0-9]+)/);return m?m[1]:null}
var F=window.fetch.bind(window);
window.fetch=function(u,o){
var U=gU(u);
if(U.indexOf('/api/viewer/project/')>-1&&U.indexOf('widgets')>-1){
var p=eP(U);var w=PW[p]||[];var f=W.filter(function(x){return w.indexOf(x.wid)>=0});
return Promise.resolve(new Response(JSON.stringify(f),{status:200,headers:{'Content-Type':'application/json'}}))}
if(U.indexOf('/api/countview/')>-1||U.indexOf('/api/proxy/')>-1)
return Promise.resolve(new Response('ok',{status:200}));
return F(u,o)};window.XMLHttpRequest=void 0})();
</script>"""
interceptor = interceptor.replace("B64_DATA", b64_data)
interceptor = interceptor.replace("PAGE_WIDS_MAP", page_wids_json)

import subprocess, tempfile, os
with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as f:
    js = interceptor.replace("<script>\n", "").replace("\n</script>", "")
    f.write(js)
    temp_path = f.name
result = subprocess.run(["node", "--check", temp_path], capture_output=True, text=True)
if result.returncode == 0:
    print(f"\nInterceptor JS: VALID ({len(interceptor)} bytes)")
else:
    print(f"\nINTERCEPTOR INVALID: {result.stderr[:200]}")
os.unlink(temp_path)

for fname in sorted(glob.glob("*.html")):
    content = open(fname).read()

    for marker in ["var B64_DATA", "var WIDGETS", "var WIDGETS_STR"]:
        while True:
            idx = content.find(marker)
            if idx < 0:
                break
            script_start = content.rfind("<script>", 0, idx)
            script_end = content.find("</script>", idx)
            if script_start >= 0 and script_end > 0:
                content = content[:script_start] + content[script_end + 9:]
            else:
                break

    content = content.replace("https://st-p.rmcdn1.net/", "st-p.rmcdn1.net/")

    content = re.sub(
        r'<script[^>]*src="https://www\.youtube\.com/iframe_api"[^>]*>\s*</script>',
        "", content,
    )
    content = re.sub(
        r"<script>window\.youTubeApiIsReady.*?</script>",
        "<script>window.youTubeApiIsReady=false;</script>",
        content, flags=re.DOTALL,
    )
    content = re.sub(
        r'<link[^>]*href="https://fonts\.googleapis\.com/[^"]*"[^>]*/?>',
        "", content,
    )

    content = content.replace("</body>", interceptor + "\n</body>")

    open(fname, "w").write(content)
    size_kb = len(content) / 1024
    print(f"{fname}: {size_kb:.0f}KB")

print("\nDone! GitVerse-ready HTML files generated.")
