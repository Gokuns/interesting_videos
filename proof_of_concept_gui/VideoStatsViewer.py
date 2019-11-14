from pyforms.basewidget import BaseWidget
import pyforms.controls as pc
import Dataset
import config
import ntpath
import matplotlib



class VideoStatsViewer(BaseWidget):

    def __init__(self):

        super().__init__('VideoAnalyzer')
        dataset = Dataset.Dataset(name= '', json_path=config.argument_defaults['video_data_path'])

        self.set_margin(10)

        #Definition of the forms fields
        self._videofile  = pc.ControlCombo('Select Video')
        self._selected_video = None
        for videoData in dataset.videos:
            path = videoData.video_path
            name = ntpath.basename(path)
            self._videofile.add_item(name,path)
        self._player     = pc.ControlPlayer('Player')
        self._person_bar = pc.ControlLabel("Number of People")
        self._vehicle_bar = pc.ControlLabel('Number of Vehicles')
        self._empty = pc.ControlEmptyWidget('asdd')

        self._min_people = pc.ControlLabel('Min:' + str(dataset.number_of_people.minimum))
        self._avg_people = pc.ControlLabel('Avg:' + str(dataset.number_of_people.average))
        self._max_people = pc.ControlLabel('Max:' + str(dataset.number_of_people.maximum))
        self._curr_people_lb = pc.ControlLabel('Total number of people:')
        self._curr_people = pc.ControlLabel()

        self._min_cars = pc.ControlLabel('Min' + str(dataset.number_of_vehicles.minimum))
        self._avg_cars = pc.ControlLabel('Avg:' + str(dataset.number_of_vehicles.average))
        self._max_cars = pc.ControlLabel('Max:' + str(dataset.number_of_vehicles.maximum))
        self._curr_vehicle_lb = pc.ControlLabel('Total number of vehicles:')
        self._curr_vehicle = pc.ControlLabel()

        self._interesting_lb = pc.ControlLabel('Is it interesting?')
        self._interesting = pc.ControlLabel()

        #Define the function that will be called when a file is selected
        self._videofile.changed_event     = self.__videoFileSelectionEvent
        #Define the event that will be called when the run button is processed
        #self._runbutton.value       = self.__runEvent
        #Define the event called before showing the image in the player
        self._player.process_frame_event    = self.__process_frame

        #Define the organization of the Form Controls
        player_part = [
            '_player',
        ]

        num_people = [            '_person_bar',
            ('_min_people', '_avg_people', '_max_people'),]
        num_veh = [            '_vehicle_bar',
            ('_min_cars', '_avg_cars', '_max_cars'),
        ]

        asd = [
            num_people,
            num_veh,
            '_curr_people_lb',
            '_curr_people',
            '_curr_vehicle_lb',
            '_curr_vehicle',
            '_interesting_lb',
            '_interesting',
            '_empty',
            '_empty',
            '_empty',
        ]

        defy = [
            '_empty',
        ]

        right_column = [
            asd, defy
        ]

        self._formset = ['_videofile', (player_part,right_column)]


    def __videoFileSelectionEvent(self):
        """
        When the videofile is selected instanciate the video in the player
        """
        dataset = Dataset.Dataset(name='', json_path=config.argument_defaults[
            'video_data_path'])

        self._player.value = self._videofile.value
        selected_video =  dataset.find_video_from_path(self._videofile.value)
        self._curr_people.value = str(selected_video.number_of_people)
        self._curr_vehicle.value = str(selected_video.number_of_vehicles)
        self._interesting.value = str(selected_video.is_interesting)


    def __process_frame(self, frame):
        """
        Do some processing to the frame and return the result frame
        """
        return frame

    def __runEvent(self):
        """
        After setting the best parameters run the full algorithm
        """
        pass

