#!/bin/bash

pip install --no-deps .

if [ `uname` == Darwin ]
then
    chmod +x $RECIPE_DIR/jupyter_mac.command 
    cp $RECIPE_DIR/jupyter_mac.command $PREFIX/bin
fi
