{ nixpkgs ? import ./.nix/pinned-nixpkgs.nix {} }:

let

release = import ./release.nix {
  inherit nixpkgs;
};

in

nixpkgs.mkShell {
  buildInputs = [ release ];

  shellHook = ''
    # Bring xdg data dirs of dependencies and current program into the
    # environement. This will allow us to get shell completion if any
    # and there might be other benefits as well.
    xdg_inputs=( "''${buildInputs[@]}" )
    for p in "''${xdg_inputs[@]}"; do
      if [[ -d "$p/share" ]]; then
        XDG_DATA_DIRS="''${XDG_DATA_DIRS}''${XDG_DATA_DIRS+:}$p/share"
      fi
    done
    export XDG_DATA_DIRS
  '';
}
