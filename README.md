Readme
======

Some atlassian admin tools to support [nixos-secure-factory] based projects.


Prerequisites
-------------

 -  A posix system (e.g: Linux, Unix)
 -  [nix](https://nixos.org/nix/download.html)


Building and running
--------------------

```bash
$ nix build -f release.nix
# ..
$ ./result/bin/nixos-sf-bitbucket --help
Usage: nixos-sf-bitbucket [OPTIONS] COMMAND [ARGS]...

  A Bitbucket restapi client.

Options:
  --help  Show this message and exit.

Commands:
  user  Bitbucket user related commands.
```


Entering a user environment
---------------------------

This is an environment that simulates the conditions occurring when this
application is installed on a system. For example it allows one to test packaged
shell completions (bash / zsh / etc).

```bash
$ nix-shell env.nix
# ..
$ nixos-sf-bitbucket --help
# .. (same as above)
$ nixos-sf-bitbucket [Hit Tab Here]
```


Entering a development environment
----------------------------------

```bash
$ cd /this/directory
# ..
$ nix-shell
# ..
$ nixos-sf-bitbucket --help
# .. (same as above)
```


Updating the dependencies
-------------------------

```bash
$ ./update_nix_requirements.sh
# ..
```

Both `requirements.nix` and `requirements_frozen.txt` should have been updated.


[nixos-secure-factory]: https://github.com/jraygauthier/nixos-secure-factory
