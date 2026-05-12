from utils.helpers import RandomDataUtil
import json
from utils.constants import FilePaths


class RandomTestData:
    @staticmethod
    def get_user():
        random_data = RandomDataUtil()
        password = random_data.get_password()

        return {
            "firstName": random_data.get_first_name(),
            "lastName": random_data.get_last_name(),
            "email": random_data.get_email(),
            "telephone": random_data.get_phone_number(),
            "password": password,
        }


def update_registered_user(registered_user, updated_user):
    """Update cached registered user data after account update."""

    registered_user["firstName"] = updated_user["firstName"]
    registered_user["lastName"] = updated_user["lastName"]
    registered_user["email"] = updated_user["email"]
    registered_user["telephone"] = updated_user["telephone"]

    FilePaths.AUTH_USER_PATH.write_text(json.dumps(registered_user, indent=2), encoding="utf-8")
