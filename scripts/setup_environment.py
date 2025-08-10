import os
import sys

if not (sys.version_info.major == 3 and sys.version_info.minor >= 8):
    print('[ERROR] Python 3.8+ is required.')
    sys.exit(1)

if not os.path.isdir('.venv'):
    os.system('python3 -m venv .venv')
    print('[INFO] Created virtual environment at .venv')
print('[INFO] Python environment check done.')