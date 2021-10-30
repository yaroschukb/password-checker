import requests
import hashlib
import sys


def request_api_data(query_char):
    url = f'https://api.pwnedpasswords.com/range/{query_char}'
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check the api and try again.')
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return count


def pwned_api_check(password):
    sha1password = hashlib.sha1(
        password.encode('utf-8')).hexdigest().upper()
    response = request_api_data(sha1password[:5])
    return get_password_leaks_count(response, sha1password[5:])


def main():
    args = input('Enter password or passwords to check: ').split(" ")
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(
                f'{password} was found {count} times... you should probably change your password!')
        else:
            print(f'{password} was NOT found. Carry on!')
    return 'Done!'


if __name__ == '__main__':
    sys.exit(main())
