import os

peta_file = r"D:\satdat 2026\sec\pantauang-enterprise\frontend\src\app\peta\PetaClient.tsx"

with open(peta_file, "r") as f:
    content = f.read()

# Fix 1: Ensure Map has explicit style dimensions
content = content.replace(
    '<Map\n          initialViewState',
    '<Map\n          style={{ width: "100%", height: "100%", position: "absolute", inset: 0 }}\n          initialViewState'
)

# Fix 2: Ensure PetaClient root container has explicit height instead of just h-full which can collapse
content = content.replace(
    'className="h-full w-full flex flex-col bg-slate-50 relative"',
    'className="min-h-[calc(100vh-4rem)] w-full flex flex-col bg-slate-50 relative"'
)

# Fix 3: Ensure map container is flex-1 with a strict minimum height
content = content.replace(
    'className="flex-1 w-full relative min-h-[400px]"',
    'className="flex-1 w-full relative min-h-[60vh]"'
)

with open(peta_file, "w") as f:
    f.write(content)

print("PetaClient patched for height visibility")
