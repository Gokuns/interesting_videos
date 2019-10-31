rareCategories = ["pushable_pullable",
                  "debris",
                  "ambulance",
                  "police",
                  "police_officer",
                  "personal_mobility",
                  "child"]


class VideoData:
    _instance_tokens = set()
    _total_people_area = 0.0
    _total_vehicle_area = 0.0

    video_path = ""
    is_interesting = False
    density_of_people = -1.0
    density_of_vehicles = -1.0
    number_of_people = 0
    number_of_vehicles = 0
    number_of_rare_objects = 0

    def __init__(self, scene, video_path):
        self.video_path = video_path
        if scene is not None:
            for sample in scene:
                ann_list = sample["annotation_list"]
                self.evaluate_anns(ann_list)
            self.density_of_people = \
                self._total_people_area / len(scene) / 1600 / 900
            self.density_of_vehicles = \
                self._total_vehicle_area / len(scene) / 1600 / 900

    def _calculate_area(self, corners):
        x_dif = corners[2][0] - corners[0][0]
        y_dif = corners[2][1] - corners[0][1]
        return x_dif * y_dif

    def evaluate_anns(self, ann_list):
        for ann in ann_list:
            if not ann["instance_token"] in self._instance_tokens:
                self._instance_tokens.add(ann["instance_token"])
                category = ann["category_name"]
                corners = ann["corners"]
                category = category.split(".")
                general_category = category[0]
                sub_category = category[-1]
                if general_category == "human":
                    self.number_of_people += 1
                    self._total_people_area += self._calculate_area(corners)
                if general_category == "vehicle":
                    self.number_of_vehicles += 1
                    self._total_vehicle_area += self._calculate_area(corners)
                if sub_category in rareCategories:
                    self.number_of_rare_objects += 1


