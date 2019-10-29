import json

rareCategories = ["pushable_pullable",
                  "debris",
                  "ambulance",
                  "police",
                  "police_officer",
                  "personal_mobility",
                  "child"]


class VideoData:
    _instance_tokens = set()

    video_path = ""
    is_interesting = False
    density_of_people = -1.0
    density_of_vehicles = -1.0
    number_of_people = 0
    number_of_vehicles = 0
    number_of_rare_objects = 0

    def __init__(self, scene, video_path):
        self.video_path = video_path
        for sample in scene:
            ann_list = sample["annotation_list"]
            self.evaluate_anns(ann_list)
            sample_token = sample["next"]

    def evaluate_anns(self, ann_list):
        for ann in ann_list:
            if not ann["instance_token"] in self._instance_tokens:
                self._instance_tokens.add(ann["instance_token"])
                category = ann["category_name"]
                category = category.split(".")
                general_category = category[0]
                sub_category = category[-1]
                if general_category == "human":
                    self.number_of_people += 1
                if general_category == "vehicle":
                    self.number_of_vehicles += 1
                if sub_category in rareCategories:
                    self.number_of_rare_objects += 1
