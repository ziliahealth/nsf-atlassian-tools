from typing import Optional, Dict, Iterator, Any
from atlassian.rest_client import AtlassianRestAPI
import argparse
import logging
import itertools
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)


class BitbucketRestAPIError(Exception):
    pass

@dataclass(frozen=True)
class SshKeyEntry:
    uuid: str
    label: str
    key: str


class BitbucketRestAPI:
    def __init__(
            self,
            username: str,
            password: str,
            url: Optional[str] = None,
            **kwargs
    ) -> None:
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
            assert key_info is not None
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



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', action="store", type=str, required=True)
    parser.add_argument('--password', action="store", type=str, required=True)
    parser.add_argument('--ssh-key-label', action="store",
                        type=str, required=True)
    parser.add_argument('--ssh-key', action="store", type=str, required=True)
    parser.add_argument('-v', '--verbose', action='count', default=0)

    args = parser.parse_args()

    key_label = args.ssh_key_label
    key = args.ssh_key
    username = args.username
    password = args.password
    verbosity_lvl = args.verbose

    verbosity_mapping = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }
    logging.basicConfig(
        level=verbosity_mapping.get(verbosity_lvl, logging.DEBUG))

    client = BitbucketRestAPI(
        username=username,
        password=password
    )

    key_entry = client.set_ssh_user_key(key_label, key)
    LOGGER.info(
        "Added / updated ssh key to '%s' user account."
        "{key_label: %s, key_uuid: %s}",
        username, key_entry.label, key_entry.uuid)


if __name__ == "__main__":
    main()
