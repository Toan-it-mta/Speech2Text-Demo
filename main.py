import gradio as gr
import requests
from pydub import AudioSegment
from asr_model import Whisper_Model


whisper_model = Whisper_Model()
   
def convert2mono(file_path):
    sound = AudioSegment.from_wav(file_path)
    sound = sound.set_channels(1)
    sound.export(file_path, format="wav")

def call_api(file_path):
    try:
        asr_text = whisper_model.infer(file_path)
        return asr_text
    except requests.RequestException as e:
        return "Error making the API request:", e
  
def speech_to_text(path):
    if path is not None:
        text = call_api(path)
        result = capitalize_and_add_punctuation(text)
        return result
    else:
        return "Đầu vào sai"

path = gr.Audio(type="filepath", label="Thực hiện Upload file cần kiểm thử")
iface = gr.Interface(
    fn=speech_to_text,
    inputs=[path],
    outputs=gr.Textbox(label="Speech-to-Text Output"),
    title="Speech-To-Text"
)

iface.launch(share=False,debug=True,server_name="0.0.0.0",server_port=1510,ssl_verify=False)

    


