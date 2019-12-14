import argparse
from detectron2.demo import demo
#--config-file ../configs/COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml --video-input C:\Users\Goko\Desktop\part1235\videos\scene-0001.mp4 --confidence-threshold 0.6    --opts MODEL.WEIGHTS detectron2://COCO-PanopticSegmentation/panoptic_fpn_R_101_3x/139514519/model_final_cafdb1.pkl MODEL.DEVICE cuda
def create_opt(input, output):
    parser = demo.get_parser()
    args = parser.parse_args(['--config-file','../detectron2/configs/COCO-PanopticSegmentation/panoptic_fpn_R_101_3x.yaml',
                               '--video-input',input,
                               '--output',output,
                               '--confidence-threshold', '0.6',
                               '--opts', 'MODEL.WEIGHTS', 'detectron2://COCO-PanopticSegmentation/panoptic_fpn_R_101_3x/139514519/model_final_cafdb1.pkl', 'MODEL.DEVICE', 'cuda'])
    #args = parser.parse_args()
    return args

class FeatureBearer:
   __instance = None
   @staticmethod
   def getInstance():
      """ Static access method. """
      if FeatureBearer.__instance == None:
          FeatureBearer()
      return FeatureBearer.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if FeatureBearer.__instance != None:
         raise Exception("This class is a singleton!")
      else:
          FeatureBearer.__instance = self
      self.features = []