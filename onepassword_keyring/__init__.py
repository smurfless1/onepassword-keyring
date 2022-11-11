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

    def get_password(self, service: str, username: str) -> Optional[str]:
        self._check_onepassword_connection()
        response_dict = self.op.get_item_fields(uuid=service, fields=['username', 'password'])
        if response_dict.get('username') == username:
            return response_dict.get('password')
        return 'not found'

    def set_password(self, service: str, username: str, password: str) -> None:
        self._check_onepassword_connection()
        found = self.op.get_item_fields(uuid=service, fields='username')
        if 'username' in found:
            self.op.edit_item_username(uuid=service, value=username)
            self.op.edit_item_password(uuid=service, value=password)
            return
        self.op.create_login(
            username, password, service
        )

    def delete_password(self, service: str, username: str) -> None:
        self._check_onepassword_connection()
        response_dict = self.op.get_item_fields(uuid=service, fields=['username', 'password'])
        if response_dict.get('username') == username:
            self.op.delete_item(uuid=service)
            return
        print("Could not match that service and username, not deleting.")
