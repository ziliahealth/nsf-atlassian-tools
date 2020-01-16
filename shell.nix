{ nixpkgs ? import ./.nix/pinned-nixpkgs.nix {} }:

nixpkgs.callPackage ./. {
  inherit nixpkgs;
  fromNixShell = true;
}