import requests
from extract_cookies import get_cookie_jar
from requests.utils import dict_from_cookiejar


# I use Tor with privoxy because Twitter is blocked in Iran.
# you can config privoxy
# by adding
#  forward-socks5 / 127.0.0.1:9050 .
# to /etc/privoxy/config
# and finally
# sudo service privoxy restart

proxies = {
    'http': 'http://127.0.0.1:8118',
    'https': 'http://127.0.0.1:8118',
}


class UpdateTwitterBio:
    def __init__(self, cookie_database_path: str):
        self.jar = get_cookie_jar(path_to_db=cookie_database_path, domain='twitter')
        self.csrf_token = dict_from_cookiejar(self.jar)['ct0']
        self.data = {
            'displayNameMaxLength': 50,
            'description': ''
        }

        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
            'x-twitter-active-user': 'yes',
            'x-csrf-token': self.csrf_token,
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'Referer': 'https://twitter.com/settings/profile',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0'
        }

    def update_bio(self):
        req = requests.post(
            'https://api.twitter.com/1.1/account/update_profile.json',
            data=self.data,
            cookies=self.jar,
            headers=self.headers,
            proxies=proxies
        )
        if req.status_code == 200:
            return True
        else:
            raise Exception('Some error. HTTP code:', req.status_code)

    def set_bio_text(self, text):
        self.data['description'] = text

