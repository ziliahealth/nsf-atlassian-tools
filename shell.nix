{ pkgs ? import ./.nix/pinned-nixpkgs.nix { } }:

import ./release.nix {
  inherit pkgs;
}
