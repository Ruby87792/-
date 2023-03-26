from flask import Flask, request, jsonify
from aip import AipSpeech
import requests
import hashlib

# 设置百度API账号信息
APP_ID = '31660408'
API_KEY = 'LdD5TG7hZF2v1DEfyeXM1rYV'
SECRET_KEY = 'sQlN2njuxUz5mkRNN3UCftZR6Z3NGHW6'

# 创建AipSpeech对象
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

app = Flask(__name__)

@app.route('/api/translate_speech', methods=['POST'])
def translate_speech():
    # 从请求中获取语音数据
    audio_data = request.data

    # 发送语音识别请求到百度API
    result_asr = client.asr(audio_data, 'pcm', 16000, {
        'dev_pid': 1536,
    })

    # 输出识别结果
    if result_asr['err_no'] == 0:
        print("识别结果: " + result_asr['result'][0])
    else:
        error_msg = "识别错误，错误代码：" + str(result_asr['err_no'])
        print(error_msg)
        return jsonify({'error': error_msg}), 400

    # 翻译识别结果
    q = result_asr['result'][0]
    from_lang = 'zh'
    to_lang = 'en'
    result_trans = translate(q, from_lang, to_lang)

    # 返回翻译结果
    result = {'translation': result_trans}
    return jsonify(result)


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
    response = requests.get(url, params=data)
    result = response.json()['trans_result'][0]['dst']
    return result


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
