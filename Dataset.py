import videoData.VideoData as VideoData


class Dataset:
    max_number_of_people = 0
    min_number_of_people = 0
    average_number_of_people = 0.0
    max_number_of_vehicles = 0
    min_number_of_vehicles = 0
    average_number_of_vehicles = 0.0

    max_number_of_rare_objects = 0
    min_number_of_rare_objects = 0
    average_number_of_rare_objects = 0.0

    def __init__(self, name: str, video_path: str, videos: list):
        self.name = name
        self.video_path = video_path
        self.videos = videos

        self.min_number_of_people = int(min(video.numberOfPeople for video in videos))
        self.max_number_of_people = int(max(video.numberOfPeople for video in videos))
        self.average_number_of_people = sum(video.numberOfPeople for video in videos) / videos.__len__()

        self.min_number_of_vehicles = int(min(video.numberOfVehicles for video in videos))
        self.max_number_of_vehicles = int(max(video.numberOfVehicles for video in videos))
        self.average_number_of_vehicles = sum(video.numberOfVehicles for video in videos) / videos.__len__()

        self.min_number_of_rare_objects = int(min(video.numberOfRareObjects for video in videos))
        self.max_number_of_rare_objects = int(max(video.numberOfRareObjects for video in videos))
        self.average_number_of_rare_objects = sum(video.numberOfRareObjects for video in videos) / videos.__len__()

    def label_videos(self, videos: list):
        for video in videos:
            video.isInteresting = (video.numberOfRareObjects > self.average_number_of_rare_objects) \
                                  or ((video.numberOfPeople > self.average_number_of_people)
                                      and (video.numberOfVehicles > self.average_number_of_vehicles))


