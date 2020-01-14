{ nixpkgs, fromNixShell ? false }:

let
  lib = nixpkgs.lib;
  appPythonOverrides = {pkgs, python}: self: super: {
  };

  appPython = import ./requirements.nix {
    pkgs = nixpkgs;
    overrides = appPythonOverrides;
  };

  app = appPython.mkDerivation rec {
    pname = "nixos-sf-atlassian-tools";
    version = "0.0.0";
    name = "${pname}-${version}";
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

    postInstall = ''
      click_exes=( "nixos-sf-bitbucket" )

      # Install click application bash completions.
      bash_completion_dir="$out/share/bash-completion/completions"
      mkdir -p "$bash_completion_dir"
      for e in "''${click_exes[@]}"; do
        click_exe_path="$out/bin/$e"
        click_complete_env_var_name="_$(echo "$e" | tr "[a-z-]" "[A-Z_]")_COMPLETE"
        # TODO: For some reason, running this return a non zero (1) status code. This might
        # be a click library bug. Fill one if so.
        env "''${click_complete_env_var_name}=source_bash" "$click_exe_path" > "$bash_completion_dir/$e" || true
        # Because of the above, check that we got some completion code in the file.
        cat "$bash_completion_dir/$e" | grep "$e" > /dev/null
      done
    '';
  };

in

app
# nixpkgs.python3Packages.toPythonApplication app
# appPython.packages.toPythonApplication app
