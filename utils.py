from requests.structures import CaseInsensitiveDict
from user_agent import generate_user_agent


def default_headers():
    """
    :rtype: requests.structures.CaseInsensitiveDict
    """
    return CaseInsensitiveDict({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Connection': 'keep-alive',
    })


def gen_ua(os=None, device_type=None, navigator=None, platform=None):
    '''
    @params:
        os: ("win", "mac", "linux")
        device_type: ("desktop", "smartphone", "tablet", "all")
        platform: like "Windows NT 5.1; WOW64"
    '''
    return generate_user_agent(os, device_type=device_type, navigator=navigator, platform=platform)
