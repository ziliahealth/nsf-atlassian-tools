{}:
let
  nixpkgs = rec {
    rev = "refs/tags/22.05";
    sha256 = "0d643wp3l77hv2pmg2fi7vyxn4rwy0iyr8djcw1h5x72315ck9ik";
    url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
    src = builtins.fetchTarball {
      inherit url;
      inherit sha256;
    };
  };
in
import nixpkgs.src {
  overlays = [ ];
  config = {
    allowUnfree = true;
  };
}
