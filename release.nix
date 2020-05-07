{ pkgs ? import ./.nix/pinned-nixpkgs.nix {} }:

{
  default = pkgs.callPackage ./. { inherit pkgs; };
}
