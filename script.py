import subprocess
import sys

subprocess.run([
    sys.executable, "-m", "fastapi",
    "dev",
    "app/main.py"
])