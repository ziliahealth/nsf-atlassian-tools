from typing import Optional, Dict, Iterator, Any
from atlassian.rest_client import AtlassianRestAPI
import argparse
import logging
import itertools
import click
from dataclasses import dataclass


class BitbucketRestAPIError(Exception):
    pass


class BitbucketRestAPISshKeyDoesNotExistsError(BitbucketRestAPIError):
    pass


@dataclass(frozen=True)
class SshKeyEntry:
    uuid: str
    label: str
    key: str


@dataclass
class BitbucketRestAPIClientBuilder:
    """Builder for the bitbucket rest api client."""

    username: str
    password: str
    url: Optional[str] = None

    def build_client(self):
        """Build method for the client."""
        return BitbucketRestAPIClient(self.username, self.password, self.url)


class BitbucketRestAPIClient:
    """Bitbucket rest api client specialized for this application's needs."""

    def __init__(
            self,
            username: str,
            password: str,
            url: Optional[str] = None,
            **kwargs
    ) -> None:
        """Cstor."""
        default_url = "https://api.bitbucket.org/"
        if url is None:
            url = default_url

        self._client = AtlassianRestAPI(url, username, password, **kwargs)
        self._user_uuid = self._get_user_uuid()

    def _get_user_uuid(self) -> str:
        url = "2.0/user"
        response = self._client.get(url, params={})

        if response["type"] == "error":
            msg = response["error"]["message"]
            raise BitbucketRestAPIError(msg)

        return response["uuid"]

    @staticmethod
    def _make_ssh_key_entry_from_json(in_json: Dict[str, Any]) -> SshKeyEntry:
        assert "ssh_key" == in_json["type"]

        return SshKeyEntry(
            label=in_json["label"],
            uuid=in_json["uuid"],
            key=in_json["key"]
        )

    def get_ssh_user_keys(
            self, label=None, exact_match=False) -> Iterator[SshKeyEntry]:
        url = "2.0/users/{0}/ssh-keys".format(self._user_uuid)

        for page in itertools.count(1):
            params: Dict = {"page": page, "pagelen": "5"}
            if label is not None:
                if exact_match:
                    params["q"] = "label=\"{}\"".format(label)
                else:
                    params["q"] = "label~\"{}\"".format(label)

            response = self._client.get(url, params=params)

            for v in response["values"]:
                assert "ssh_key" == v["type"]
                yield self._make_ssh_key_entry_from_json(v)

            if response.get("next") is None:
                break

    def get_ssh_user_keys_by_label(self, label=None) -> Dict[str, SshKeyEntry]:
        out: Dict[str, SshKeyEntry] = dict()

        for v in self.get_ssh_user_keys(label):
            assert out.get(v.label) is None
            out[v.label] = v

        return out

    def get_ssh_user_key_from_label(self, label: str) -> Optional[SshKeyEntry]:
        out = None
        for v in self.get_ssh_user_keys(label=label, exact_match=True):
            # If not the case, it means we received more than a single result
            # which shouldn't be possible.
            assert out is None
            out = v

        return out

    @classmethod
    def _process_ssh_user_key_changed_response(
            cls, response: Dict[str, Any]
    ) -> SshKeyEntry:
        if response["type"] == "error":
            msg = response["error"]["message"]
            raise BitbucketRestAPIError(msg)
        else:
            return cls._make_ssh_key_entry_from_json(response)

    def post_ssh_user_key(
            self, label: str, key: str
    ) -> SshKeyEntry:
        data = {
            "label": label,
            "key": key
        }
        url = "2.0/users/{0}/ssh-keys".format(self._user_uuid)
        response = self._client.post(url, data=data)
        return self._process_ssh_user_key_changed_response(response)

    def put_ssh_user_key(
            self, label: str, key: str, key_uuid: Optional[str] = None
    ) -> SshKeyEntry:
        if key_uuid is None:
            key_info = self.get_ssh_user_key_from_label(label)
            try:
                assert key_info is not None
            except AssertionError as e:
                raise BitbucketRestAPISshKeyDoesNotExistsError(
                    "Ssh key for label '{}' does not exists.".format(
                        label)) from e
            key_uuid = key_info.uuid

        data = {
            "label": label,
            "key": key
        }
        url = "2.0/users/{}/ssh-keys/{}".format(self._user_uuid, key_uuid)
        response = self._client.put(url, data=data)

        return self._process_ssh_user_key_changed_response(response)

    def set_ssh_user_key(
            self, label: str, key: str
    ) -> SshKeyEntry:
        existing_keys = self.get_ssh_user_keys_by_label(label)

        existing_key = existing_keys.get(label)
        if existing_key is None:
            return self.post_ssh_user_key(label, key)
        else:
            return self.put_ssh_user_key(label, key, key_uuid=existing_key.uuid)

    @classmethod
    def _process_ssh_user_key_removed_response(
            cls, response: Optional[Dict[str, Any]]
    ) -> None:
        if response is None:
            return  # Successful removal.

        if response["type"] == "error":
            msg = response["error"]["message"]
            raise BitbucketRestAPIError(msg)

    def delete_ssh_user_key(
            self, label: str, key_uuid: Optional[str] = None
    ) -> SshKeyEntry:
        if key_uuid is None:
            key_info = self.get_ssh_user_key_from_label(label)
            try:
                assert key_info is not None
            except AssertionError as e:
                raise BitbucketRestAPISshKeyDoesNotExistsError(
                    "Ssh key for label '{}' does not exists.".format(
                        label)) from e
            key_uuid = key_info.uuid

        url = "2.0/users/{}/ssh-keys/{}".format(self._user_uuid, key_uuid)
        response = self._client.delete(url, data={})
        self._process_ssh_user_key_removed_response(response)
        return SshKeyEntry(
            label=label,
            uuid=key_uuid,
            key="")
