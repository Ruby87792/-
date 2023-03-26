import os
import base64
import json
import requests

# 设置百度翻译 API 的相关信息
APP_ID = '31660408'
API_KEY = 'LdD5TG7hZF2v1DEfyeXM1rYV'
SECRET_KEY = 'sQlN2njuxUz5mkRNN3UCftZR6Z3NGHW6'

# 定义需要翻译的语音文件路径和目标语言代码
audio_file_path = 'path/to/audio/file'
target_lang = 'en'  # 英语

# 将语音文件进行 Base64 编码
with open(audio_file_path, 'rb') as f:
    speech = base64.b64encode(f.read()).decode('utf-8')

# 调用百度翻译 API 进行翻译
url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
params = {
    'q': speech,
    'from': 'zh',
    'to': target_lang,
    'appid': APP_ID,
    'salt': os.urandom(6).hex(),
    'sign': '',
}
sign_str = f"{APP_ID}{speech}{params['salt']}{SECRET_KEY}"
params['sign'] = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
response = requests.get(url, params=params)

# 处理翻译结果
result = json.loads(response.content.decode('utf-8'))
translated_text = result['trans_result'][0]['dst']

# 输出翻译结果
print(translated_text)
