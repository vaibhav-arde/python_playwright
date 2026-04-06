from utils.helpers import RandomDataUtil


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
