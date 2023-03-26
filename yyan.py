from aip import AipSpeech
import pyaudio
import requests
import hashlib
import urllib.parse

# 设置百度API账号信息
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

# 创建AipSpeech对象
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 设置音频参数
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5

# 创建PyAudio对象
p = pyaudio.PyAudio()

# 打开麦克风并开始录音
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                input=True, frames_per_buffer=CHUNK)
print("正在录音，请说话...")

frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("录音结束！")

# 停止录音
stream.stop_stream()
stream.close()
p.terminate()

# 将录音数据转换成二进制格式
audio_data = bytes().join(frames)

# 发送语音识别请求到百度API
result = client.asr(audio_data, 'pcm', 16000, {
    'dev_pid': 1536,
})

# 输出识别结果
if result['err_no'] == 0:
    print("识别结果: " + result['result'][0])
else:
    print("识别错误，错误代码：" + str(result['err_no']))


def translate(q, from_lang, to_lang):
    appid = ''
    secretKey = ''
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
    #print('data='+str(data))
    response = requests.get(url, params=data)
    #print('response='+str(response))
    #print('response.text='+str(response.text))
    #print('response.status_code='+str(response.status_code))
    result = response.json()['trans_result'][0]['dst']
    #print(result)
    return result

if __name__ == '__main__':
    q = result['result'][0]
    from_lang = 'zh'
    to_lang = 'en'
    result = translate(q, from_lang, to_lang)
    print(result)
