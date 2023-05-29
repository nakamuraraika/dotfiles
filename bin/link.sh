#!/bin/bash -eu

BASEDIR=$(pwd)
cd $BASEDIR

for dotfile in $BASEDIR/.??* ; do
    [[ "$dotfile" == "${BASEDIR}/.git" ]] && continue
    [[ "$dotfile" == "${BASEDIR}/.gitignore" ]] && continue
    [[ "$dotfile" == "${BASEDIR}/.github" ]] && continue
    [[ "$dotfile" == "${BASEDIR}/.DS_Store" ]] && continue

    ln -fnsv "$dotfile" "$HOME"
done