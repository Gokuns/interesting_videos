from ColorBarStats import ColorBarStats
import json
from VideoData import VideoData

class Dataset:
    number_of_people = ColorBarStats(0, 0, 0)
    number_of_vehicles = ColorBarStats(0, 0, 0)
    density_of_people = ColorBarStats(0, 0, 0)
    density_of_vehicles = ColorBarStats(0, 0, 0)

    def __init__(self, name: str, video_path: str = None, videos: list = None,
                 json_path: str = None):
        """

        :param name: the name of the Dataset (Nuscenes, Berkeley etc.)
        :param video_path: the path to the videos
        :param videos: the list of VideoData
        """
        self.name = name
        self.video_path = video_path
        self.videos = videos
        if json_path is not None:
            self.load_from_json(json_path)
        else:
            self._initialize_color_bars(videos)

    def _initialize_color_bars(self, videos):
        self.number_of_people = ColorBarStats(
            maximum=max(video.number_of_people for video in videos),
            minimum=min(video.number_of_people for video in videos),
            average=sum(
                video.number_of_people for video in videos) / videos.__len__())

        self.number_of_vehicles = ColorBarStats(
            maximum=max(video.number_of_vehicles for video in videos),
            minimum=min(video.number_of_vehicles for video in videos),
            average=sum(
                video.number_of_vehicles for video in
                videos) / videos.__len__())

        self.density_of_people = ColorBarStats(
            maximum=max(video.density_of_people for video in videos),
            minimum=min(video.density_of_people for video in videos),
            average=sum(
                video.density_of_people for video in
                videos) / videos.__len__())

        self.density_of_vehicles = ColorBarStats(
            maximum=max(video.density_of_vehicles for video in videos),
            minimum=min(video.density_of_vehicles for video in videos),
            average=sum(
                video.density_of_vehicles for video in
                videos) / videos.__len__())

    def label_videos(self, poc_mode: str):
        if poc_mode == 'density_based':
            for video in self.videos:
                video.is_interesting = (video.density_of_people > self.density_of_people.average) \
                                       and (video.density_of_vehicles > self.density_of_vehicles.average)
        else:
            for video in self.videos:
                video.is_interesting = (video.number_of_people > self.number_of_people.average) \
                                       and (video.number_of_vehicles > self.number_of_vehicles.average)

    def save_as_json(self, path):
        with open(path, 'w+') as outfile:
            fields = self.__dict__.copy()
            fields['videos'] = [v.__dict__ for v in
                                fields['videos']]
            fields['number_of_people'] = fields['number_of_people'].__dict__
            fields['number_of_vehicles'] = fields['number_of_vehicles'].__dict__
            fields['density_of_people'] = fields['density_of_people'].__dict__
            fields['density_of_vehicles'] = fields['density_of_vehicles'].__dict__
            json.dump(fields, outfile)

    def load_from_json(self, path):
        with open(path, 'r') as infile:
            fields = json.load(infile)
            v_list = []
            for v_dict in fields['videos']:
                video = VideoData(None, None)
                video.__dict__ = v_dict
                v_list.append(video)
            fields['videos'] = v_list
            number_of_people = ColorBarStats(0,0,0)
            number_of_people.__dict__ = fields['number_of_people']
            fields['number_of_people'] = number_of_people
            number_of_vehicles = ColorBarStats(0,0,0)
            number_of_vehicles.__dict__ = fields['number_of_vehicles']
            fields['number_of_vehicles'] = number_of_vehicles
            density_of_people = ColorBarStats(0,0,0)
            density_of_people.__dict__ = fields['density_of_people']
            fields['density_of_people'] = density_of_people
            density_of_vehicles = ColorBarStats(0,0,0)
            density_of_vehicles.__dict__ = fields['density_of_vehicles']
            fields['density_of_vehicles']
            self.__dict__ = fields

    def find_video_from_path(self,path):
        result = None
        for video in self.videos:
            if video.video_path == path:
                result = video
        return result