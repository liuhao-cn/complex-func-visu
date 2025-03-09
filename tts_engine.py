#coding=utf-8

'''
requires Python 3.6 or later
pip install requests
'''
import base64
import json
import uuid
import os
import requests
from pydub import AudioSegment

def get_audio_duration(mp3_file):
    audio = AudioSegment.from_mp3(mp3_file)
    return audio.duration_seconds


def tts_engine_bytedance(text, mp3_file, speed_ratio=1.0, volume_ratio=1.0, pitch_ratio=1.0):
    appid        = "3018995978"
    access_token = os.environ.get("ByteDanceAPI", "")
    cluster      = "volcano_tts"
    voice_type   = "BV001_streaming"
    api_url      = f"https://openspeech.bytedance.com/api/v1/tts"
    header       = {"Authorization": f"Bearer;{access_token}"}
    request_json = {
        "app": {
            "appid": appid,
            "token": "access_token",
            "cluster": cluster
        },
        "user": {
            "uid": "388808087185088"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": speed_ratio,
            "volume_ratio": volume_ratio,
            "pitch_ratio": pitch_ratio,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"
        }
    }
    resp = requests.post(api_url, json.dumps(request_json), headers=header)
    if "data" in resp.json():
        data_base64 = resp.json()["data"]
    else:
        print(f"Fail to get speech response")
        return
    
    fop = open(mp3_file, "wb")
    fop.write(base64.b64decode(data_base64))
    fop.close()

    audio_duration = get_audio_duration(mp3_file)

    print(f"生成的语音时长: {audio_duration:.2f}秒")
    return audio_duration



def tts_engine_aliyun(text, mp3_file, role="longmiao"):
    import dashscope
    from dashscope.audio.tts_v2 import SpeechSynthesizer
    model = "cosyvoice-v1"
    voice = role
    # 从系统环境变量中获取阿里云API密钥
    dashscope.api_key = os.environ.get("ALIYUNAPI", "")

    synthesizer = SpeechSynthesizer(model=model, voice=voice)
    audio = synthesizer.call(text)

    with open(mp3_file, 'wb') as f:
        f.write(audio)

    audio_duration = get_audio_duration(mp3_file)
    print(f"生成的语音时长: {audio_duration:.2f}秒")

    return audio_duration


# 当直接运行该文件时，执行测试
if __name__ == "__main__":
    # 测试参数
    test_file = "test_speech.mp3"
    test_text = "今天天气怎么样？"
    
    print("开始测试语音合成引擎...")
    print(f"测试文本: '{test_text}'")
    
    # 调用TTS引擎生成语音
    try:
        duration = tts_engine_aliyun(test_text, test_file)
        print(f"语音生成成功，时长为: {duration:.2f}秒")
        print(f"请检查输出文件: {test_file}")
    except Exception as e:
        print(f"测试失败: {e}")


