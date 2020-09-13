import sqlite3
from http import cookiejar
from decrypt_cookie import main_decryption


def get_cookie_jar(path_to_db: str, domain: str):
    """
    :param path_to_db: the path to the Browsers Cookie sqlite database
    :param domain: domain of the website that you want to cookies from
    :return: A CookieJar object
    """
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    # in my own browser (Opera) cookie values are encrypted
    # if your's is not you can skip using the `main_decryption` function
    sql = f"SELECT host_key, name, encrypted_value, expires_utc, is_secure, path \
            FROM cookies WHERE host_key LIKE '%{domain}%'"
    query_res = cur.execute(sql)
    jar = cookiejar.CookieJar()

    for i, val in enumerate(query_res):
        host = val[0]
        name = val[1]
        value = main_decryption(val[2])
        expires_at = val[3]
        is_secure = val[4]
        path = val[5]
        cookie = cookiejar.Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=host,
            domain_specified=True,
            domain_initial_dot=host.startswith('.'),
            path=path,
            path_specified=False,
            secure=is_secure,
            expires=expires_at,
            discard=expires_at == '',
            comment=None,
            comment_url=None,
            rest={}
        )

        jar.set_cookie(cookie)
    return jar
