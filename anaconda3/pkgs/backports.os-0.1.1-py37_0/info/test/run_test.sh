

set -ex



export "PYTHONIOENCODING=utf8"
python -m unittest discover tests
exit 0
