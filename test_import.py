import importlib
import sys

try:
    importlib.import_module('src.app')
    print('imported src.app ok')
except Exception as e:
    print('import failed:', type(e).__name__, e)
    sys.exit(1)
