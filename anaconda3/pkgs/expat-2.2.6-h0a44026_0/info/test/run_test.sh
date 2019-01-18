

set -ex



xmlwf -h
conda inspect linkages -p $PREFIX expat
conda inspect objects -p $PREFIX expat
exit 0
