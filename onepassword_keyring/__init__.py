from typing import Optional

from keyring.backend import KeyringBackend
from keyring.util import properties
from onepassword import OnePassword


class OnePasswordKeyring(KeyringBackend):
    """PyCrypto File Keyring"""

    @properties.ClassProperty
    @classmethod
    def priority(self):
        try:
            import onepassword
        except ImportError:  # pragma: no cover
            raise RuntimeError("Requires the onepassword-client-v2 package install: pip install onepassword-client-v2")
        return 0.6

    def __init__(self):
        super().__init__()
        self.op = OnePassword()

    def _check_onepassword_connection(self):
        """
        Check if the file exists and has the expected password reference.
        """
        self.op.sign_in_if_needed()
        vaults = self.op.list_vaults()
        assert(bool(vaults))

    def _unlock(self):
        """
        Unlock this keyring by getting the password for the keyring from the
        user.
        """
        self._check_onepassword_connection()

    def _lock(self):
        """
        Remove the keyring key from this instance.
        """
        self._check_onepassword_connection()

    def _get_matching_uuid(self, service: str, username: str, vault: Optional[str] = None) -> Optional[str]:
        """
        Get the item fields matching this most closely.

        This will be slower than possible, but will disambiguate logins for you.
        For instance, my 1password has Airbnb twice with two different usernames.
        The CLI will fail, but this handles it pre-emptively.
        :return:
        """
        return self.op.get_first_uuid_with_hint(title=service, hint=username, vault=vault)

    def get_password(self, service: str, username: str) -> Optional[str]:
        '''
        Get the login matching this title and username, and return its password.
        '''
        self._check_onepassword_connection()
        uuid = self._get_matching_uuid(service, username)
        if uuid is None:
            return 'not found'

        response_dict = self.op.get_item_fields(uuid=uuid, fields=['username', 'password'])
        if response_dict.get('username') == username:
            return response_dict.get('password')
        return 'not found'

    def set_password(self, service: str, username: str, password: str) -> None:
        self._check_onepassword_connection()
        uuid = self._get_matching_uuid(service, username)
        if uuid is None:
            self.op.create_login(
                username, password, service
            )
            return

        self.op.edit_item_username(uuid=uuid, value=username)
        self.op.edit_item_password(uuid=uuid, value=password)

    def delete_password(self, service: str, username: str) -> None:
        self._check_onepassword_connection()
        uuid = self._get_matching_uuid(service, username)
        if uuid is None:
            print("Could not match that service and username, not deleting.")
            return None

        self.op.delete_item(uuid=uuid)
