import requests
import base64
from pydub import AudioSegment

#
# API_KEY = "ZUYSmX4d.LWFgp19Dun5zUUaqJlpWWisLnZnSaXuk"
#
# url = "https://apikazllm.nu.edu.kz/assistant/"
#
# headers = {
#     "accept": "application/json",
#     "Authorization": f"Api-Key {API_KEY}"
# }
#
# response = requests.get(url, headers=headers)
#
#
# if response.status_code == 200:
#     print("Response data:")
#     print(response.json())
# else:
#     print(f"Request failed with status code {response.status_code}")
#     print(response.text)


def post_request_kazllm(text: str):

    API_KEY = "ZUYSmX4d.LWFgp19Dun5zUUaqJlpWWisLnZnSaXuk"
    # assistant/{assistant_id}/interactions/
    url = "https://apikazllm.nu.edu.kz/assistant/83/interactions/"

    headers = {
        "accept": "application/json",
        "Authorization": f"Api-Key {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "name": "Sample Chat",
        "text_prompt": text,
        "file_prompt": None
    }

    response = requests.post(url, headers=headers, json=data)

    return response.json()


def translate_text(text):

    API_KEY = "6-9gxEpWQR0syeu9DGk1Jw"

    url = "https://soyle.nu.edu.kz/external-api/v1/translate/text/?output_format=text"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }


    data = {
        "source_language": "eng",
        "target_language": "kaz",
        "text": text,
    }

    response = requests.post(url, headers=headers, json=data)
    # print(response.json())

    return response.json()


def get_audio(text):

    API_KEY = "6-9gxEpWQR0syeu9DGk1Jw"

    url = "https://soyle.nu.edu.kz/external-api/v1/translate/text/"

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "source_language": "kaz",
        "target_language": "kaz",
        "text": text,
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json()["text"])

    base64_audio = response.json()['audio']

    return base64_audio

# print(get_audio("С"))
