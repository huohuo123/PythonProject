

set -ex



test -f "${PREFIX}/lib/libgfortran.dylib"
test -f "${PREFIX}/lib/libgfortran.3.dylib"
test -f "${PREFIX}/lib/libquadmath.dylib"
test -f "${PREFIX}/lib/libquadmath.0.dylib"
test -f "${PREFIX}/lib/libgcc_s.1.dylib"
test -f "${PREFIX}/lib/libgcc_s_ppc64.1.dylib"
test -f "${PREFIX}/lib/libgcc_s_x86_64.1.dylib"
exit 0
