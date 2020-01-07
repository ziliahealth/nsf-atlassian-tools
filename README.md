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
$ ./result/bin/nixos-sf-bitbucket-user-authorize-ssh-key --help
usage: nixos-sf-bitbucket-user-authorize-ssh-key [-h] --username USERNAME
                                                 --password PASSWORD
                                                 --ssh-key-label SSH_KEY_LABEL
                                                 --ssh-key SSH_KEY

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME
  --password PASSWORD
  --ssh-key-label SSH_KEY_LABEL
  --ssh-key SSH_KEY
```


Entering a development environment
----------------------------------

```bash
$ cd /this/directory
# ..
$ nix-shell
# ..
$ nixos-sf-bitbucket-user-authorize-ssh-key --help
# .. (same as above)
usage: nixos-sf-bitbucket-user-authorize-ssh-key [-h] --username USERNAME
                                                 --password PASSWORD
                                                 --ssh-key-label SSH_KEY_LABEL
                                                 --ssh-key SSH_KEY

optional arguments:
  -h, --help            show this help message and exit
  --username USERNAME
  --password PASSWORD
  --ssh-key-label SSH_KEY_LABEL
  --ssh-key SSH_KEY
```


Updating the dependencies
-------------------------

```bash
$ ./update_nix_requirements.sh
# ..
```

Both `requirements.nix` and `requirements_frozen.txt` should have been updated.


[nixos-secure-factory]: https://github.com/jraygauthier/nixos-secure-factory
