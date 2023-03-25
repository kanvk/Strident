import os
from hashlib import md5

from dotenv import load_dotenv
import requests
import time
import webbrowser

load_dotenv()
API_KEY = os.getenv('API_KEY')
SHARED_SECRET = os.getenv('SHARED_SECRET')
API_ROOT = "https://ws.audioscrobbler.com/2.0"
API_TOKEN = ""
API_TOKEN_EXPIRY = 0


def get_token() -> str:
    """
    Returns singleton instance of token

    :return: Token
    :rtype: str
    """
    global API_TOKEN, API_TOKEN_EXPIRY
    if API_TOKEN and time.time() < API_TOKEN_EXPIRY:
        return API_TOKEN

    api_signature = md5(f"api_key{API_KEY}methodauth.getToken{SHARED_SECRET}".encode()).hexdigest()
    response = requests.get(f"{API_ROOT}?method=auth.gettoken&api_key={API_KEY}&api_sig={api_signature}&format=json")
    API_TOKEN_EXPIRY = time.time() + 59 * 60  # Tokens expire in 60 minutes, change them in 59

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code} getting token.")

    API_TOKEN = response.json()['token']
    return API_TOKEN


def get_auth() -> None:
    token = get_token()
    api_signature = md5(f"api_key{API_KEY}methodauth.getSessiontoken{token}{SHARED_SECRET}".encode()).hexdigest()
    url = f"https://www.last.fm/api/auth/?api_key=f{API_KEY}&token={token}&api_sig={api_signature}"
    webbrowser.get().open(url)
