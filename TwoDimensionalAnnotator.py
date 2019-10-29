import json
import os

import numpy as np
from nuscenes import NuScenes
from nuscenes.utils.geometry_utils import BoxVisibility
from nuscenes.utils.geometry_utils import view_points

import config


class TwoDimensionalAnnotator:
    def __init__(self, nusc: NuScenes):
        self.nusc = nusc

    def get_the_two_dimensional_annotations(self,
                                            scene_token: str,
                                            channel: str = 'CAM_FRONT'
                                            ):

        # Get records from DB
        scene_rec = self.nusc.get('scene', scene_token)
        sample_rec = self.nusc.get('sample', scene_rec['first_sample_token'])
        sd_rec = self.nusc.get('sample_data', sample_rec['data'][channel])

        scene_list = []
        has_more_frames = True
        while has_more_frames:
            # Get data from DB
            impath, boxes, camera_intrinsic = self.nusc.get_sample_data(sd_rec['token'],
                                                                        box_vis_level=BoxVisibility.ANY)
            reprojections = {}
            annotation_list = []

            for three_d_box in boxes:
                entry = {}
                cs_rec = self.nusc.get('calibrated_sensor', sd_rec['calibrated_sensor_token'])
                camera_intrinsic = np.array(cs_rec['camera_intrinsic'])
                corner_coords = view_points(three_d_box.corners(), camera_intrinsic, True).T[:, :2].tolist()
                boundaries = []
                min_x = int(min(coord[0] for coord in corner_coords))
                min_y = int(min(coord[1] for coord in corner_coords))
                max_x = int(max(coord[0] for coord in corner_coords))
                max_y = int(max(coord[1] for coord in corner_coords))
                boundaries.append((min_x, min_y))
                boundaries.append((max_x, min_y))
                boundaries.append((max_x, max_y))
                boundaries.append((min_x, max_y))
                entry['corners'] = boundaries
                entry['category_name'] = three_d_box.name
                sample_annotation = self.nusc.get('sample_annotation', three_d_box.token)
                entry['instance_token'] = sample_annotation['instance_token']
                annotation_list.append(entry)

            reprojections["annotation_list"] = annotation_list
            reprojections["filename"] = impath
            reprojections['sample_data_token'] = sd_rec['token']
            reprojections['timestamp'] = sd_rec['timestamp']
            reprojections['next'] = sd_rec['next']

            scene_list.append(reprojections)
            if not sd_rec['next'] == "":
                sd_rec = self.nusc.get('sample_data', sd_rec['next'])
            else:
                has_more_frames = False

        return scene_list

    def export_two_dimensional_annotations(self, out_dir: str):
        # Load NuScenes class
        scene_tokens = [s['token'] for s in self.nusc.scene]

        # Create output directory
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        scene_to_annotations = {}
        # Write videos to disk
        for scene_token in scene_tokens:
            scene = self.nusc.get('scene', scene_token)
            scene_to_annotations[scene_token] = self.get_the_two_dimensional_annotations(scene['token'])

        dest_path = os.path.join(config.argument_defaults['dataroot'], config.argument_defaults['version'])
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        if not scene_to_annotations.keys().__len__() == 0:
            with open(os.path.join(config.argument_defaults['dataroot'], config.argument_defaults['version'],
                                   config.argument_defaults['filename']), 'w') as fh:
                json.dump(scene_to_annotations, fh, sort_keys=True, indent=4)

        print("Saved the 2D re-projections under {}".format(
            os.path.join(config.argument_defaults['dataroot'], config.argument_defaults['version'],
                         config.argument_defaults['filename'])))
