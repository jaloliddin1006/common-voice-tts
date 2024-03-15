import requests


# Audio faylini yuborish
def send_audio(audio_path=None, caption='', id=None, group_id=1):
    # Bot API tokenini yozing
    TOKEN = "6463249109:AAESqnRtpa1TBMNS1fON3HYzDvfXO3-Z6sQ"

    # Chat ID ni yozing
    CHAT_ID = "-1002115614399"

    url = f"https://api.telegram.org/bot{TOKEN}/sendAudio"
    files = {"audio": open(audio_path, "rb")}
    data = {"chat_id": CHAT_ID,
            "reply_to_message_id": group_id,
            "caption": f"#{id} - {caption}"}
    response = requests.post(url, files=files, data=data)
    
    if response.status_code != 200:
        print("Audio bo'sh yuborildi")
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID,
                "reply_to_message_id": 1,
                "text": f"#{id} -<b> {caption} </b> - Audio guruhga yetib kelmadi ",
                "parse_mode": "HTML"
                }
        response = requests.post(url, json=data)

    # print(response.json())


# send_audio('media/voices/click.wav', 'Bu mening test xabaringiz')