from user_agent import generate_user_agent


def gen_ua(os=None, device_type=None, navigator=None, platform=None):
    '''
    @params:
        os: ("win", "mac", "linux")
        device_type: ("desktop", "smartphone", "tablet", "all")
        platform: like "Windows NT 5.1; WOW64"
    '''
    return generate_user_agent(os, device_type=device_type, navigator=navigator, platform=platform)
