from ColorBarStats import ColorBarStats


class Dataset:
    number_of_people = ColorBarStats(0, 0, 0)
    number_of_vehicles = ColorBarStats(0, 0, 0)
    density_of_people = ColorBarStats(0, 0, 0)
    density_of_vehicles = ColorBarStats(0, 0, 0)

    def __init__(self, name: str, video_path: str, videos: list):
        """

        :param name: the name of the Dataset (Nuscenes, Berkeley etc.)
        :param video_path: the path to the videos
        :param videos: the list of VideoData
        """
        self.name = name
        self.video_path = video_path
        self.videos = videos
        self.number_of_people = ColorBarStats(maximum=max(video.number_of_people for video in videos),
                                              minimum=min(video.number_of_people for video in videos),
                                              average=sum(
                                                  video.number_of_people for video in videos) / videos.__len__())

        self.number_of_vehicles = ColorBarStats(maximum=max(video.number_of_vehicles for video in videos),
                                                minimum=min(video.number_of_vehicles for video in videos),
                                                average=sum(
                                                    video.number_of_vehicles for video in videos) / videos.__len__())

        self.density_of_people = ColorBarStats(maximum=max(video.density_of_people for video in videos),
                                               minimum=min(video.density_of_people for video in videos),
                                               average=sum(
                                                   video.density_of_people for video in videos) / videos.__len__())

        self.density_of_vehicles = ColorBarStats(maximum=max(video.density_of_vehicles for video in videos),
                                                 minimum=min(video.density_of_vehicles for video in videos),
                                                 average=sum(
                                                     video.density_of_vehicles for video in videos) / videos.__len__())

    def label_videos(self, videos: list, poc_mode: str):
        if poc_mode == 'density_based':
            for video in videos:
                video.is_interesting = (video.density_of_people > self.density_of_people.average) \
                                       and (video.density_of_vehicles > self.density_of_vehicles.average)
        else:
            for video in videos:
                video.is_interesting = (video.number_of_people > self.number_of_people.average) \
                                       and (video.number_of_vehicles > self.number_of_vehicles.average)
