{ nixpkgs ? import ../../../pinned/nixpkgs.nix {} }:

nixpkgs.callPackage ./. { inherit nixpkgs; }
