import sys
import os
print(f"CWD: {os.getcwd()}")
print(f"sys.path: {sys.path}")
try:
    from app.main import app
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
