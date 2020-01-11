"""Command line interface to interact with the Bitbucket rest api."""
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


def setup_verbose(
        verbose: int) -> None:
    verbosity_mapping = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }
    assert verbose >= 0
    logging.basicConfig(
        level=verbosity_mapping.get(verbose, logging.DEBUG))


def composed(*decs):
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def shared_cmd_options(func):
    return composed(
        click.option(
            '-v', '--verbose', default=0, count=True,
            help="Verbosity level."),
        click.option(
            '--username', envvar='NIXOS_SF_BITBUCKET_USERNAME',
            prompt=True,
            help="Username of the Bitbucket account this tool will operate on."),
        click.option(
            '--password', envvar='NIXOS_SF_BITBUCKET_PW',
            prompt=True, hide_input=True,
            help="Password of the Bitbucket account this tool will operate on.")
    )(func)


def setup_shared_cmd_options(
        verbose: int,
        username: str,
        password: str
) -> CliContext:
    setup_verbose(verbose)
    client_builder = BitbucketRestAPIClientBuilder(
        username=username,
        password=password
    )
    return CliContext(
        client_builder=client_builder,
        username=username)


@click.group()
# @click.pass_context
def cli(
        # ctx: click.Context,
) -> None:
    """A Bitbucket restapi client."""
    pass


@cli.group()
def user():
    """Bitbucket user related commands."""
    pass


@user.group()
def ssh():
    """Commands for managing a Bitbucket user's authorized ssh keys."""
    pass


@ssh.command()
@shared_cmd_options
@click.option(
    '--label',
    help="Filter results by ssh key label.")
# @click.pass_obj
def ls(
        # obj: CliContext,
        verbose: int,
        username: str,
        password: str,
        label: Optional[str]
) -> None:
    """List ssh key authorized to the specified user account."""
    obj = setup_shared_cmd_options(verbose, username, password)
    client_builder = obj.client_builder
    client = client_builder.build_client()
    for v in client.get_ssh_user_keys(label):
        click.echo("label: {}, uuid: {}".format(v.label, v.uuid))


@ssh.command()
@click.argument('key', default=None, required=False)
@shared_cmd_options
@click.option(
    '--label', required=True,
    help="A unique label for this ssh key.")
@click.pass_obj
def authorize(
        # obj: CliContext,
        verbose: int,
        username: str,
        password: str,
        label: str,
        key: str
) -> None:
    """Authorize ssh key to the specified user account."""
    obj = setup_shared_cmd_options(verbose, username, password)
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
@shared_cmd_options
@click.option(
    '--label', required=True,
    help="The label of the ssh key to be deauthorized.")
@click.pass_obj
def deauthorize(
        # obj: CliContext,
        verbose: int,
        username: str,
        password: str,
        label: str
) -> None:
    """Deauthorize ssh key from the specified user account."""
    obj = setup_shared_cmd_options(verbose, username, password)
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
