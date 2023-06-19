from huggingface_hub import HfApi
import json

def init_models():
    api = HfApi()
    models = api.list_models()
    model_dicts = [model.__dict__ for model in models]
    with open("model_index.json", "w") as f:
        json.dump(model_dicts, f)

init_models()