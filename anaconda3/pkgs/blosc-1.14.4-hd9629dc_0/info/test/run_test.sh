

set -ex



test -e $PREFIX/include/blosc.h
test -e $PREFIX/include/blosc-export.h
test -e $PREFIX/lib/libblosc.dylib
conda inspect linkages -p $PREFIX $PKG_NAME
conda inspect objects -p $PREFIX $PKG_NAME
exit 0
