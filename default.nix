{ nixpkgs, fromNixShell ? false }:

let
  lib = nixpkgs.lib;
  appPythonOverrides = {pkgs, python}: self: super: {
  };

  appPython = import ./requirements.nix {
    pkgs = nixpkgs;
    overrides = appPythonOverrides;
  };

  app = appPython.mkDerivation {
    name = "nixos-sf-atlassian-tools";
    src = ./.;
    buildInputs = [];
    checkInputs =  with appPython.packages; [
      mypy
      pytest
      # flake
    ] ++ lib.optionals fromNixShell [
      ipython
    ];
    propagatedBuildInputs = with appPython.packages; [
      atlassian-python-api
      click
    ];

    # dontUseSetuptoolsShellHook = true;
  };

in

app
# nixpkgs.python3Packages.toPythonApplication app
# appPython.packages.toPythonApplication app
