from nuscenes.nuscenes import NuScenes

rareCategories = ["pushable_pullable",
                  "debris",
                  "ambulance",
                  "police",
                  "police_officer",
                  "personal_mobility",
                  "child"]

class VideoData:
    densityOfPeople = -1.0
    densityOfVehicles = -1.0
    numberOfPeople = 0
    numberOfVehicles = 0
    numberOfRareObjects = 0

    def __init__(self, video, nusc):
        sample_token = video["first_sample_token"]
        while sample_token != "":
            sample = nusc.get("sample", sample_token)
            ann_list = sample["anns"]
            self.evaluate_anns(ann_list, nusc)
            sample_token = sample["next"]

    def evaluate_anns(self, ann_list, nusc):
        for ann_tok in ann_list:
            ann = nusc.get("sample_annotation", ann_tok)
            category = ann["category_name"]
            category = category.split(".")
            general_category = category[0]
            sub_category = category[-1]
            if general_category == "human":
                self.numberOfPeople += 1
            if general_category == "vehicle":
                self.numberOfVehicles += 1
            if sub_category in rareCategories:
                self.numberOfRareObjects += 1


nusc = NuScenes(version='v1.0-mini',
                dataroot='datasets/nuscenes/mini_raw',
                verbose=True)
for video in nusc.scene:
    data = VideoData(video, nusc)
    print("Number of People: {}".format(
        data.numberOfPeople))
    print("Number of Vehicles: {}".format(
        data.numberOfVehicles))
    print("Number of Rare Objects: {}".format(
        data.numberOfRareObjects))

for category in nusc.category:
    print(category)

