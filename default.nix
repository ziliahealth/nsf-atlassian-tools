{ pkgs, buildPythonPackage, atlassian-python-api, click, mypy, pytest }:

buildPythonPackage rec {
  pname = "nsf-atlassian-tools";
  version = "0.1.0";
  name = "${pname}-${version}";
  src = pkgs.nix-gitignore.gitignoreSourcePure ./.gitignore ./.;
  buildInputs = [ ];
  checkInputs = [
    mypy
    pytest
  ];
  propagatedBuildInputs = [
    atlassian-python-api
    click
  ];

  postInstall = ''
    click_exes=( "nsf-bitbucket" )

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

  # Allow nix-shell inside nix-shell.
  # See `pkgs/development/interpreters/python/hooks/setuptools-build-hook.sh`
  # for the reason why.
  shellHook = ''
    setuptoolsShellHook
  '';
}
