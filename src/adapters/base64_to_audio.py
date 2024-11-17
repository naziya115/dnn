import base64
import os


def base64_to_audio(base64_string, output_audio_file):
    """
    Converts a Base64 string directly to an audio file.

    Parameters:
    - base64_string (str): The Base64 encoded string of the audio file.
    - output_audio_file (str): The path to save the decoded audio file (e.g., 'output.mp3').
    """
    try:
        # Decode Base64 string to binary data
        audio_data = base64.b64decode(base64_string)
        output_audio_file = "src/handlers/" + output_audio_file
        # Write the binary data directly to the audio file
        with open(output_audio_file, "wb") as audio_file:
            audio_file.write(audio_data)
        
        print(f"Audio file saved at: {os.path.abspath(output_audio_file)}")
    except Exception as e:
        print(f"Error converting Base64 to audio: {e}")

def hex_to_base64(hex_string: str) -> str:
    # Конвертируем hex-строку в байты
    byte_data = bytes.fromhex(hex_string)
    # Кодируем байты в Base64
    base64_data = base64.b64encode(byte_data)
    # Возвращаем строку в формате Base64
    return base64_data.decode('utf-8')


# path = "audio (3).txt"
# with open(path, "r") as file:  # Open the file in read mode
#     my_file = file.read()
#
# b64_file = hex_to_base64(my_file)
#
# final_audio_file = "output1.mp3"  # Can also be "output.wav" or other formats
#
# # Convert Base64 to audio
# base64_to_audio(b64_file, final_audio_file)
