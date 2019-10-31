from pyforms.basewidget import BaseWidget
import pyforms.controls as pc
import Dataset

class VideoStatsViewer(BaseWidget):

    def __init__(self,dataset:Dataset):

        super().__init__('Computer vision algorithm example')

        self.set_margin(10)

        #Definition of the forms fields
        self._videofile  = pc.ControlCombo()
        self._outputfile = pc.ControlText('Results output file')
        self._threshold  = pc.ControlSlider('Threshold', default=114, minimum=0, maximum=255)
        self._blobsize   = pc.ControlSlider('Minimum blob size', default=110, minimum=100, maximum=2000)
        self._player     = pc.ControlPlayer('Player')
        self._runbutton  = pc.ControlButton('Run')
        self._lala = pc.ControlText('what what')

        #Define the function that will be called when a file is selected
        self._videofile.changed_event     = self.__videoFileSelectionEvent
        #Define the event that will be called when the run button is processed
        self._runbutton.value       = self.__runEvent
        #Define the event called before showing the image in the player
        self._player.process_frame_event    = self.__process_frame

        #Define the organization of the Form Controls
        self._formset = [
            ('_videofile', '_outputfile'),
            '_threshold',
            ('_blobsize', '_runbutton'),
            '_player'
        ]
        self._formset = [(self._formset,'_lala')]


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


if __name__ == '__main__':

    from pyforms import start_app
    start_app(VideoStatsViewer)