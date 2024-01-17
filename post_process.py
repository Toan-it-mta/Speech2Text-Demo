from models.xlm_roberta_capu.gec_model import GecBERTModel

model = GecBERTModel(
    vocab_path="models/xlm_roberta_capu/vocabulary",
    model_paths="models/xlm_roberta_capu",
    split_chunk=True
)

def capitalize_and_add_punctuation(text):
    # start = time.time()
    result = model(text)
    result_str = ''.join(result)
    return result_str


