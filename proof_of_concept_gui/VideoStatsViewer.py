from pyforms.basewidget import BaseWidget
import pyforms.controls as pc
import Dataset
import config



class VideoStatsViewer(BaseWidget):

    def __init__(self):

        super().__init__('VideoAnalyzer')
        dataset = Dataset.Dataset(name= '', json_path=config.argument_defaults['video_data_path'])

        self.set_margin(10)

        #Definition of the forms fields
        self._videofile  = pc.ControlCombo('Select Video')
        for videoData in dataset.videos:
            self._videofile.add_item(videoData.video_path)
        self._outputfile = pc.ControlText('Results output file')
        self._player     = pc.ControlPlayer('Player')
        self._person_bar = pc.ControlButton('asd')
        self._vehicle_bar = pc.ControlButton()
        self._empty = pc.ControlEmptyWidget('asdd')

        self._lala = pc.ControlLabel('what what')

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
        asd = [
            '_person_bar',
            '_vehicle_bar',
            '_empty',




        ]

        self._formset = ['_videofile', (player_part,asd)]


    def __videoFileSelectionEvent(self):
        """
        When the videofile is selected instanciate the video in the player
        """
        self._player.value = self._videofile.value


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

