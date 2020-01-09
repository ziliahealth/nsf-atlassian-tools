"""Command line interface to interact with the bitbucket rest api."""
from typing import Optional
import logging
import click
from dataclasses import dataclass
from .bitbucket import (
    BitbucketRestAPIClientBuilder,
    BitbucketRestAPISshKeyDoesNotExistsError
)

LOGGER = logging.getLogger(__name__)


@dataclass
class CliContext:
    """Click cli app context."""

    client_builder: BitbucketRestAPIClientBuilder
    username: str


@click.group()
@click.option('-v', '--verbose', default=0, count=True)
@click.option(
    '--username', envvar='NIXOS_SF_BITBUCKET_USERNAME',
    prompt=True)
@click.option(
    '--password', envvar='NIXOS_SF_BITBUCKET_PW',
    prompt=True, hide_input=True)
@click.pass_context
def cli(
        ctx: click.Context,
        verbose: int,
        username: str,
        password: str
) -> None:
    """Click cli app entry point."""
    verbosity_mapping = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }
    assert verbose >= 0
    logging.basicConfig(
        level=verbosity_mapping.get(verbose, logging.DEBUG))

    client_builder = BitbucketRestAPIClientBuilder(
        username=username,
        password=password
    )

    ctx.obj = CliContext(
        client_builder=client_builder,
        username=username)


@cli.group()
def user():
    """Cli app `user` sub command group."""
    pass


@user.group()
def ssh():
    """Cli app `user ssh` sub command group."""
    pass


@ssh.command()
@click.option('--label')
@click.pass_obj
def ls(
        obj: CliContext,
        label: Optional[str]
) -> None:
    """Cli app `user ssh ls` sub command."""
    client_builder = obj.client_builder
    client = client_builder.build_client()
    for v in client.get_ssh_user_keys(label):
        click.echo("label: {}, uuid: {}".format(v.label, v.uuid))


@ssh.command()
@click.argument('key', default=None, required=False)
@click.option('--label', required=True)
@click.pass_obj
def authorize(
        obj: CliContext,
        label,
        key
) -> None:
    """Cli app `user ssh authorize` sub command."""
    client_builder = obj.client_builder
    username = obj.username

    if key is None:
        # When key argument is not provided, read its value from stdin.
        stdin_text = click.get_text_stream('stdin')
        key = stdin_text.read()

    client = client_builder.build_client()
    key_entry = client.set_ssh_user_key(label, key)
    LOGGER.info(
        "Authorized ssh key '%s' to '%s' user account."
        "`{key_uuid: %s}`",
        key_entry.label, username, key_entry.uuid)


@ssh.command()
@click.option('--label', required=True)
@click.pass_obj
def deauthorize(
        obj: CliContext,
        label
) -> None:
    """Cli app `user ssh deauthorize` sub command."""
    client_builder = obj.client_builder
    username = obj.username

    client = client_builder.build_client()
    try:
        key_entry = client.delete_ssh_user_key(label)
    except BitbucketRestAPISshKeyDoesNotExistsError:
        LOGGER.info(
            "Ssh key '%s' already deauthorized from '%s' user account.",
            label, username)
    else:
        LOGGER.info(
            "Deauthorized ssh key '%s' from '%s' user account."
            "`{key_uuid: %s}`",
            key_entry.label, username, key_entry.uuid)


if __name__ == "__main__":
    cli()
