

set -ex



test -f ${PREFIX}/lib/libzmq.a
test -f ${PREFIX}/lib/libzmq.dylib
test -f ${PREFIX}/lib/libzmq.5.dylib
test -f ${PREFIX}/share/cmake/ZeroMQ/ZeroMQConfig.cmake
test -f ${PREFIX}/share/cmake/ZeroMQ/ZeroMQConfigVersion.cmake
${PREFIX}/bin/curve_keygen
exit 0
