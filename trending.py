#main script for getting trending models
print("Starting the script...")
from huggingface_hub import HfApi
import json

class Trending():
    def __init__(self, x):
        print("Initializing Trending class...")
        self.x = x
        self.remove_invalid_json()
        self.compare_models()
        self.sort_models()
        
    def remove_invalid_json(self):
        print("Removing invalid JSON...")
        with open("model_index.json", "r") as f:
            models = f.readlines()
        valid_models = []
        for model in models:
            try:
                json.loads(model)
                valid_models.append(model)
            except json.JSONDecodeError:
                continue
        with open("model_index.json", "w") as f:
            f.writelines(valid_models)
        
    def compare_models(self):        
        print("Comparing models...")
        api = HfApi()
        current_models = api.list_models()
        with open("model_index.json", "r") as f:
            previous_model_index = json.load(f)
        previous_model_dict = {model["id"]: model for model in previous_model_index}
        for current_model in current_models:
            current_model_dict = current_model.__dict__
            try:
                json.dumps(current_model_dict)
            except json.JSONDecodeError:
                continue
            previous_model = previous_model_dict.get(current_model_dict["id"])
            if previous_model:
                current_model_dict["downloads"] = current_model_dict["downloads"] - previous_model["downloads"]
                previous_model_dict[current_model_dict["id"]] = current_model_dict
            else:
                previous_model_dict[current_model_dict["id"]] = current_model_dict
        with open("model_index.json", "w") as f:
            json.dump(list(previous_model_dict.values()), f)
            
    def sort_models(self):
        print("Sorting models...")
        with open("model_index.json", "r") as f:
            models = json.load(f)
        sorted_models = sorted(models, key=lambda x: x["downloads"], reverse=True)
        with open("model_index.json", "w") as f:
            json.dump(sorted_models, f)

    def get_models(self):
        print("Getting top models...")
        with open("model_index.json", "r") as f:
            sorted_models = json.load(f)
        top_x_models = sorted_models[:self.x]
        return top_x_models
    
#example code of getting top ten models:
'''x = 10
print("Getting the top {} models...".format(x))
trending = Trending(x)
top_x_models = trending.get_models()
print("Top {} models:".format(x))
for model in top_x_models:
    print(model["id"])
    print("ID: {}, Downloads: {}".format(model["id"], model["downloads"]))'''
    
