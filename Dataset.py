from videoData import VideoData

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

        self.min_number_of_people = int(min(video.number_of_people for video in videos))
        self.max_number_of_people = int(max(video.number_of_people for video in videos))
        self.average_number_of_people = sum(video.number_of_people for video in videos) / videos.__len__()

        self.min_number_of_vehicles = int(min(video.number_of_vehicles for video in videos))
        self.max_number_of_vehicles = int(max(video.number_of_vehicles for video in videos))
        self.average_number_of_vehicles = sum(video.number_of_vehicles for video in videos) / videos.__len__()

        self.min_number_of_rare_objects = int(min(video.number_of_rare_objects for video in videos))
        self.max_number_of_rare_objects = int(max(video.number_of_rare_objects for video in videos))
        self.average_number_of_rare_objects = sum(video.number_of_rare_objects for video in videos) / videos.__len__()

    def label_videos(self, videos: list):
        for video in videos:
            video.is_interesting = (video.number_of_rare_objects > self.average_number_of_rare_objects) \
                                  or ((video.number_of_people > self.average_number_of_people)
                                      and (video.number_of_vehicles > self.average_number_of_vehicles))


