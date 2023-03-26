import requests
import hashlib
import urllib.parse

def translate(q, from_lang, to_lang):
    appid = '20230326001615726'
    secretKey = '_9ueB4DPej_0UcqwWaUj'
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    salt = '12345'
    sign = hashlib.md5((appid + q + salt + secretKey).encode('utf-8')).hexdigest()
    data = {
        'q': q,
        'from': from_lang,
        'to': to_lang,
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    print('data='+str(data))
    response = requests.get(url, params=data)
    print('response='+str(response))
    print('response.text='+str(response.text))
    print('response.status_code='+str(response.status_code))
    result = response.json()['trans_result'][0]['dst']
    print(result)
    return result

if __name__ == '__main__':
    q = 'Hello World!'
    from_lang = 'en'
    to_lang = 'zh'
    result = translate(q, from_lang, to_lang)
    print(result)
