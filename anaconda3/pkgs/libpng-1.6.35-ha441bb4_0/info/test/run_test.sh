

set -ex



test -f ${PREFIX}/lib/libpng.a
test -f ${PREFIX}/lib/libpng.dylib
libpng-config --version
conda inspect linkages -p $PREFIX libpng
conda inspect objects -p $PREFIX libpng
exit 0
