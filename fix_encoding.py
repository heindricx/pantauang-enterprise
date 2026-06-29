with open('patch_v4_4_infografis.py', encoding='utf-8') as f:
    c = f.read()

with open('patch_v4_5_data.py', encoding='utf-8') as f:
    c2 = f.read()

c2 = c2.replace(') as f:\n    f.write(', ', encoding="utf-8") as f:\n    f.write(')
with open('patch_v4_5_data.py', 'w', encoding='utf-8') as f:
    f.write(c2)

print("Done patching encoding")
