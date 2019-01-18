#!/bin/bash

export LD_LIBRARY_PATH=$PREFIX/lib:$LD_LIBRARY_PATH

./configure --prefix=$PREFIX \
            --host=${HOST} \
            --with-gmp=$PREFIX \
            --with-mpfr=$PREFIX
make -j${CPU_COUNT} ${VERBOSE_AT}
make check
make install
