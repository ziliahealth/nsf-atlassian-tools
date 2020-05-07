{ pkgs ? import ./.nix/pinned-nixpkgs.nix {} }:

pkgs.callPackage ./. {
  inherit pkgs;
  fromNixShell = true;
}