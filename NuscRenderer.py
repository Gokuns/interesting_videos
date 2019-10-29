import os.path as osp

import os
import os.path as osp
from typing import Tuple

import cv2
import numpy as np
from nuscenes import NuScenes
from nuscenes.utils.geometry_utils import BoxVisibility
from nuscenes.utils.geometry_utils import view_points

import config


class NuscRenderer:
    def __init__(self, nusc: NuScenes):
        self.nusc = nusc

    def render_scene_channel_with_two_dimensional_boxes(self,
                                                        scene_token: str,
                                                        channel: str = 'CAM_FRONT',
                                                        freq: float = 10,
                                                        imsize: Tuple[float, float] = (640, 360),
                                                        out_path: str = None):

        if out_path is not None:
            assert osp.splitext(out_path)[-1] == '.avi'

        # Get records from DB
        scene_rec = self.nusc.get('scene', scene_token)
        sample_rec = self.nusc.get('sample', scene_rec['first_sample_token'])
        sd_rec = self.nusc.get('sample_data', sample_rec['data'][channel])

        # Open CV init
        name = '{}: {} (Space to pause, ESC to exit)'.format(scene_rec['name'], channel)
        cv2.namedWindow(name)
        cv2.moveWindow(name, 0, 0)

        if out_path is not None:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(out_path, fourcc, freq, imsize)
        else:
            out = None

        has_more_frames = True
        while has_more_frames:
            # Get data from DB
            impath, boxes, camera_intrinsic = self.nusc.get_sample_data(sd_rec['token'],
                                                                        box_vis_level=BoxVisibility.ANY)

            # Load and render
            if not osp.exists(impath):
                raise Exception('Error: Missing image %s' % impath)

            im = cv2.imread(impath)

            for three_d_box in boxes:
                c = self.nusc.explorer.get_color(three_d_box.name)
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

                for i in range(4):
                    cv2.line(im, boundaries[i], boundaries[(i + 1) % 4], c, 2)

            # Render
            im = cv2.resize(im, imsize)
            cv2.imshow(name, im)
            if out_path is not None:
                out.write(im)

            key = cv2.waitKey(10)  # Images stored at approx 10 Hz, so wait 10 ms.
            if key == 32:  # If space is pressed, pause.
                key = cv2.waitKey()

            if key == 27:  # if ESC is pressed, exit
                cv2.destroyAllWindows()
                break

            if not sd_rec['next'] == "":
                sd_rec = self.nusc.get('sample_data', sd_rec['next'])
            else:
                has_more_frames = False

        cv2.destroyAllWindows()
        if out_path is not None:
            out.release()
        # return scene_list

    def export_videos_and_two_dimensional_annotations(self, out_dir: str):
        # Load NuScenes class
        scene_tokens = [s['token'] for s in self.nusc.scene]

        # Create output directory
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        # Write videos to disk
        for scene_token in scene_tokens:
            scene = self.nusc.get('scene', scene_token)
            print('Writing scene %s' % scene['name'])
            out_path = os.path.join(out_dir, scene['name']) + '.avi'
            if not os.path.exists(out_path):
                self.render_scene_channel_with_two_dimensional_boxes(scene['token'],
                                                                     freq=10,
                                                                     imsize=(640, 360),
                                                                     out_path=out_path)
        dest_path = os.path.join(config.argument_defaults['dataroot'], config.argument_defaults['version'])
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
