import gradio as gr
import os
import requests
from pydub import AudioSegment

def convert2mono(file_path):
    sound = AudioSegment.from_wav(file_path)
    sound = sound.set_channels(1)
    sound.export(file_path, format="wav")

def call_api(url, file_path):
    try:
        file_name = "_".join(file_path.split('/')[-2:])
        new_file_path = os.path.join('./recordings',file_name)

        # Prepare the API request with the file parameter
        with open(file_path,'rb') as f:
            wav = f.read()

        with open(new_file_path,'wb') as f:
            f.write(wav)

        convert2mono(new_file_path)

        payload = {'file': open(new_file_path, 'rb')}

        # Make the POST request to the API
        response = requests.post(url, files=payload)

        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            return response.text
        else:
            print(f"API request failed with status code {response.status_code}.")
            return f"API request failed with status code {response.status_code}."
    except requests.RequestException as e:
        print("Error making the API request:", e)
        return "Error making the API request:", e

    
def speech_to_text(mic_path,load_path):
    try:
        if mic_path is not None:
            api_url = 'https://asr.hpda.vn/listen_file'
            text = call_api(api_url,mic_path)
            return text

        elif load_path is not None:
            api_url = 'https://asr.hpda.vn/listen_file'
            text = call_api(api_url,load_path)
            return text
        else:
            return ""
    except:
        return ""

mic = gr.Audio(source="microphone", type="filepath", label="Nhấn vào nút record để bắt đầu ghi âm.")
path = gr.Audio(type="filepath", label="Thực hiện Upload file cần kiểm thử")
iface = gr.Interface(
    fn=speech_to_text,
    inputs=[mic,path],
    outputs=[gr.Textbox(label="Speech-to-Text Output")],
    title="Kiểm thử Speech-To-Text",
    description="",
)

iface.launch(share=True, debug=True)

