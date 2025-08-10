import sys
import subprocess

REQUIRED = [
    'chromadb==0.4.15',
    'sentence-transformers==2.2.2',
    'numpy==1.24.3',
    'pandas==2.0.3',
    'tiktoken==0.5.1',
    'openai==0.27.8',
    'langchain==0.0.324'
]

def main():
    for pkg in REQUIRED:
        subprocess.call([sys.executable, '-m', 'pip', 'install', pkg])
    print('[INFO] All dependencies installed')

if __name__ == '__main__':
    main()