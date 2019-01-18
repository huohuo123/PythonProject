#  tests for llvmlite-0.26.0-py37h8c7ce04_0 (this is a generated file);
print('===== testing package: llvmlite-0.26.0-py37h8c7ce04_0 =====');
print('running run_test.py');
#  --- run_test.py (begin) ---
import os
from llvmlite.tests import main

# Enable tests for distribution only
os.environ['LLVMLITE_DIST_TEST'] = '1'
main()
#  --- run_test.py (end) ---

print('===== llvmlite-0.26.0-py37h8c7ce04_0 OK =====');
print("import: 'llvmlite'")
import llvmlite

print("import: 'llvmlite.binding'")
import llvmlite.binding

