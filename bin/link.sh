#!/bin/bash -eu

BASEDIR=$(pwd)
cd $BASEDIR

ln -fnsv $(readlink -f ".ssh") "$HOME"
ln -fnsv $(readlink -f ".config") "$HOME"
ln -fnsv $(readlink -f ".zshenv") "$HOME"