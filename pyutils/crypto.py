import base64
import hashlib
from binascii import a2b_hex, b2a_hex

from Crypto.Cipher import AES


def get_md5(string, encoding='utf-8'):
    md5 = hashlib.md5()
    md5.update(string.encode(encoding))
    return md5.hexdigest()


def aes_encrypt(plain_text, key, iv=None, mode=AES.MODE_CBC, is_hex_not_b64=True, encoding='utf-8', **kwargs):
    '''
    @desc: AES 加密方法.
    @params:
        plain_text: 明文, str;
        key: 密钥, str or bytes;
        iv: Initialization Vector 初始向量, str or bytes;
        mode: 模式, default CBC;
        is_hex_not_b64: 转码方式, hex if Ture else base64;
        encoding: 编码, default utf-8.
    @return: 密文 encrypt_data.
    '''
    if isinstance(key, str):
        key = key.encode(encoding)
    if isinstance(iv, str):
        iv = iv.encode(encoding)

    def pad(plain_text):
        encoded = plain_text.encode(encoding=encoding)
        mode = AES.block_size - (len(encoded) % AES.block_size)
        text = plain_text + mode * chr(mode)
        return text.encode(encoding=encoding)

    kwargs.update({'key': key, 'iv': iv, 'mode': mode})
    if not iv and mode == AES.MODE_ECB:
        kwargs.pop('iv')

    cipher = AES.new(**kwargs)
    text = pad(plain_text)
    _bytes = cipher.encrypt(text)
    if is_hex_not_b64 == True:
        encrypt_data = b2a_hex(_bytes).decode(encoding)
    else:
        encrypt_data = base64.b64encode(_bytes).decode(encoding)
    return encrypt_data


def aes_decrypt(encrypt_data, key, iv=None, mode=AES.MODE_CBC, is_hex_not_b64=True, encoding='utf-8', **kwargs):
    '''
    @desc: AES 解密方法.
    @params:
        encrypt_data: AES 加密数据;
        key: 密钥, str or bytes;
        iv: Initialization Vector 初始向量, str or bytes;
        mode: 模式, default CBC;
        is_hex_not_b64: 转码方式, hex if Ture else base64;
        encoding: 编码, default utf-8.
    @return： 明文 plain_text.
    '''
    if isinstance(key, str):
        key = key.encode(encoding)
    if isinstance(iv, str):
        iv = iv.encode(encoding)

    def unpad(data):
        return data[:len(data)-ord(data[-1])]

    kwargs.update({'key': key, 'iv': iv, 'mode': mode})
    if not iv:
        kwargs.pop('iv')

    if is_hex_not_b64 == True:
        decoded = a2b_hex(encrypt_data)
    else:
        decoded = base64.b64decode(encrypt_data)
    cipher = AES.new(**kwargs)
    decrypted = cipher.decrypt(decoded)
    plain_text = str(unpad(decrypted), encoding=encoding)
    return plain_text
