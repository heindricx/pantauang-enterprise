import os

root_dir = r"D:\satdat 2026\sec\pantauang-enterprise"

render_yaml = os.path.join(root_dir, "render.yaml")
with open(render_yaml, "w") as f:
    f.write('''services:
  - type: web
    name: pantauang-backend
    env: docker
    region: singapore
    plan: free
    dockerContext: ./backend
    dockerfilePath: ./backend/Dockerfile
    healthCheckPath: /
    envVars:
      - key: TIDB_PASSWORD
        sync: false # Set via Render Dashboard
''')

github_dir = os.path.join(root_dir, ".github/workflows")
os.makedirs(github_dir, exist_ok=True)

ci_yml = os.path.join(github_dir, "ci.yml")
with open(ci_yml, "w") as f:
    f.write('''name: PantaUang Enterprise CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.13"
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Backend Tests
      run: |
        cd backend
        # pytest tests/

  frontend-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: "20"
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    - name: Build Next.js
      run: |
        cd frontend
        npm run build
''')

print("Render and GitHub Actions configs scaffolded!")
