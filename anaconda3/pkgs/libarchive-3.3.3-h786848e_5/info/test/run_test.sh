

set -ex



test -f "${PREFIX}/lib/pkgconfig/libarchive.pc"
test -f "${PREFIX}/include/archive.h"
test -f "${PREFIX}/include/archive_entry.h"
test -f "${PREFIX}/lib/libarchive.a"
test -f "${PREFIX}/lib/libarchive.dylib"
bsdcat --version
bsdcpio --version
bsdtar --version
bsdtar -tf test/hello_world.xar
exit 0
