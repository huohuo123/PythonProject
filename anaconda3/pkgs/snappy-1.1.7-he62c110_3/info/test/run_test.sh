

set -ex



test -e $PREFIX/include/snappy.h
test -e $PREFIX/include/snappy-stubs-public.h
test -e $PREFIX/lib/libsnappy$SHLIB_EXT
test -e $PREFIX/lib/libsnappy.a
exit 0
