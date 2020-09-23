Readme
======

Some atlassian admin tools to support [nixos-secure-factory] based projects.

Features
--------

### User account ssh key management

 -  Authorizing a ssh key to the user account:

    ```bash
    $ ssh_key="$(cat /path/to/my/ssh-key.pub)"
    $ nsf-bitbucket user ssh authorize -v --label my-ssh-key-label "$ssh_key"
    Username: my-user-name@gmail.com
    Password:
    INFO:nsf_atlassian_tools.bitbucket_cli:Authorized ssh key 'my-ssh-key-label' to ' my-user-name@gmail.com' user account.`{key_uuid: {6088bce9-75ec-4e36-8c05-973cea379cff}}`
    ```

 -  Listing ssh keys authorized to the user account:

    ```bash
    $ nsf-bitbucket user ssh ls -v
    Username: my-user-name@gmail.com
    Password:
    label: my-ssh-key-label, uuid: {6088bce9-75ec-4e36-8c05-973cea379cff}
    label: my-other-ssh-key-label, uuid: {1a35d6d6-e828-4ff4-8808-ab64785cd81d}
    # ..
    ```

 -  Listing ssh keys filtered by label:

    ```bash
    $ nsf-bitbucket user ssh ls -v --label my-ssh-key
    Username: my-user-name@gmail.com
    Password:
    label: my-ssh-key-label, uuid: {6088bce9-75ec-4e36-8c05-973cea379cff}
    ```

 -  Deauthorizing a ssh key from the user account:

    ```bash
    $ nsf-bitbucket user ssh deauthorize -v --label my-ssh-key-label
    Username: jraygauthier@gmail.com
    Password:
    INFO:nsf_atlassian_tools.bitbucket_cli:Deauthorized ssh key 'my-ssh-key-label' from 'my-user-name@gmail.com' user account.`{key_uuid: {6088bce9-75ec-4e36-8c05-973cea379cff}}`
    ```


Prerequisites
-------------

 -  A posix system (e.g: Linux, Unix)
 -  [nix](https://nixos.org/nix/download.html)


Building and running
--------------------

```bash
$ nix build -f release.nix default
# ..
$ ./result/bin/nsf-bitbucket --help
Usage: nsf-bitbucket [OPTIONS] COMMAND [ARGS]...

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
$ nsf-bitbucket --help
# .. (same as above)
$ nsf-bitbucket [Hit Tab Here]
```


Entering a development environment
----------------------------------

```bash
$ cd /this/directory
# ..
$ nix-shell
# ..
$ nsf-bitbucket --help
# .. (same as above)
```


Updating the dependencies
-------------------------

```bash
$ ./update_nix_requirements.sh
# ..
```

Both `requirements.nix` and `requirements_frozen.txt` should have been updated.


Todo
----

See [Todo](./TODO.md) file.


Contributing
------------

Contributing implies licensing those contributions under the terms of [LICENSE](./LICENSE), which is an *Apache 2.0* license.


[nixos-secure-factory]: https://github.com/jraygauthier/nixos-secure-factory


Acknowledgements
----------------

Thanks to [Zilia Health] for being the first innovative corporate user /
supporter of this project allowing it to grow both in quality and features.

[Zilia Health]: https://ziliahealth.com/
