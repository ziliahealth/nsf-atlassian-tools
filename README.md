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

  Click cli app entry point.

Options:
  -v, --verbose
  --username TEXT
  --password TEXT
  --help           Show this message and exit.

Commands:
  user  Cli app `user` sub command group.
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
