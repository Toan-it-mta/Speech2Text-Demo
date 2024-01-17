from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
from post_process import capitalize_and_add_punctuation
from operator import itemgetter

device = "cuda" if torch.cuda.is_available() else "cpu"


class Whisper_Model:
    def __init__(self) -> None:
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.MODEL_ID = "/mnt/wsl/PHYSICALDRIVE0p1/toan/Speech2TextDemo/models/whisper-medium-vi-aia-27-12-2023/checkpoint-6658"
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            self.MODEL_ID, torch_dtype=self.torch_dtype, low_cpu_mem_usage=True, use_safetensors=True,cache_dir="/mnt/wsl/PHYSICALDRIVE0p1/toan/Speech2TextDemo/models",
        )
        self.model.to(device)
        self.processor = AutoProcessor.from_pretrained("openai/whisper-medium",cache_dir='/mnt/wsl/PHYSICALDRIVE0p1/toan/Speech2TextDemo/models')
        
    def infer(self,audiopath:str) -> str:
        print("=== Process input ===")
        pipe = pipeline(
        "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            chunk_length_s=20,
            batch_size=16,
            return_timestamps=True,
            torch_dtype=self.torch_dtype,
            device=device,
            generate_kwargs={"task": "transcribe","language":'vi'}
        )
        prediction = pipe(audiopath)
        result_string = " ".join(map(itemgetter('text'), prediction["chunks"]))
        return result_string