if [[ $(uname) == Darwin ]]; then
  export CONDA_BUILD_SYSROOT=${CONDA_BUILD_SYSROOT:-/opt/MacOSX10.9.sdk}
else
  export LDFLAGS="${LDFLAGS} -Wl,-rpath-link,"${PREFIX}"/lib"
fi
echo "${CC} ${CFLAGS} ${LDFLAGS} -Wl,-rpath,"${PREFIX}"/lib "${RECIPE_DIR}"/test.c -lmpfr -lgmp -o test_exe"
${CC} ${CFLAGS} ${LDFLAGS} -Wl,-rpath,"${PREFIX}"/lib "${RECIPE_DIR}"/test.c -lmpfr -lgmp -o test_exe
./test_exe
