{ pkgs ? import ./.nix/pinned-nixpkgs.nix { } }:

{
  default = pkgs.python3Packages.callPackage ./. { };
}
