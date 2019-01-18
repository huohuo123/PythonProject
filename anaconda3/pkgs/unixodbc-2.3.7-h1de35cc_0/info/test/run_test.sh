

set -ex



test -f $PREFIX/lib/libodbc.2.dylib
test -f $PREFIX/lib/libodbc.dylib
test -f $PREFIX/lib/libodbcinst.2.dylib
test -f $PREFIX/lib/libodbcinst.dylib
isql --help
iusql --help
exit 0
