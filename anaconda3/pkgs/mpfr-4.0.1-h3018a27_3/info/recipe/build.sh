#!/bin/bash

export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH

./configure --prefix=$PREFIX \
            --host=${HOST} \
            --with-gmp=$PREFIX \
            --enable-static
# Flaky parallelism:
make -j${CPU_COUNT} ${VERBOSE_AT} || \
make -j${CPU_COUNT} ${VERBOSE_AT} || \
make -j1 ${VERBOSE_AT}
make check
make install
