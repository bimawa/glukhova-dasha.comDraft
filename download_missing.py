import json, re, subprocess, os

data = json.load(open("api/widgets-combined.json"))
raw = json.dumps(data)
all_files = set(re.findall(r'upload-([a-f0-9-]+)\.webp', raw))

dl_dir = "originals"
os.makedirs(dl_dir, exist_ok=True)

existing = set()
for f in os.listdir(dl_dir):
    if f.endswith(".webp"):
        existing.add(f.replace(".webp", ""))

missing = sorted(all_files - existing)
print(f"Всего: {len(all_files)}, уже есть: {len(existing)}, скачать: {len(missing)}")

downloaded = 0
for i, base in enumerate(missing):
    local_path = f"{dl_dir}/{base}.webp"
    
    for ext in [".jpg", ".png"]:
        url = f"https://i-p.rmcdn.net/5479c8026bbe3ca75cc0a82e/3936815/{base}{ext}"
        tmp = f"/tmp/{base}{ext}"
        
        result = subprocess.run(
            f'curl -sL --connect-timeout 15 --max-time 60 -o "{tmp}" "{url}" -H "User-Agent: Mozilla/5.0" -w "%{{http_code}}"',
            shell=True, capture_output=True, text=True, timeout=70
        )
        if result.stdout.strip() == "200" and os.path.exists(tmp) and os.path.getsize(tmp) > 100:
            sz = os.path.getsize(tmp)
            subprocess.run(f'cwebp -q 85 -quiet "{tmp}" -o "{local_path}"', shell=True, timeout=20)
            os.remove(tmp)
            downloaded += 1
            print(f"✓ [{i+1}/{len(missing)}] {base[:30]} ({sz/1024:.0f}KB)")
            break
    
    if (i + 1) % 20 == 0:
        print(f"— {i+1}/{len(missing)}: {downloaded} OK —")

print(f"\nСкачано: {downloaded}")
print(f"Всего: {sum(1 for f in os.listdir(dl_dir) if f.endswith('.webp'))}/{len(all_files)}")
