#!/usr/bin/env nix-shell
#!nix-shell -i bash
#!nix-shell -I "pypi2nixSrc=https://github.com/nix-community/pypi2nix/archive/0811de9fabe00b898cd200158ddc059cbae9d4e1.tar.gz"
#!nix-shell -I "nixpkgs=https://github.com/NixOS/nixpkgs/archive/96c9578020133fe64feab90c00f3cb880d53ad0d.tar.gz"
#!nix-shell -p "(import <pypi2nixSrc>) {pkgs = import <nixpkgs> {};}"

pypi2nix -vvv -V python3 -r ./requirements.txt --default-overrides
