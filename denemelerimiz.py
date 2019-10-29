import os.path as osp

import cv2
from nuscenes.utils.geometry_utils import view_points, box_in_image, BoxVisibility
from nuscenes.utils.geometry_utils import view_points

import numpy as np
import json
import argparse
import os

from typing import List, Tuple, Union
from nuscenes import NuScenes


def render_scene_channel_new(nusc: NuScenes,
                             scene_token: str,
                             channel: str = 'CAM_FRONT',
                             freq: float = 10,
                             imsize: Tuple[float, float] = (640, 360),
                             out_path: str = None) -> list:
    valid_channels = ['CAM_FRONT_LEFT', 'CAM_FRONT', 'CAM_FRONT_RIGHT',
                      'CAM_BACK_LEFT', 'CAM_BACK', 'CAM_BACK_RIGHT']

    assert imsize[0] / imsize[1] == 16 / 9, "Aspect ratio should be 16/9."
    assert channel in valid_channels, 'Input channel {} not valid.'.format(channel)

    if out_path is not None:
        assert osp.splitext(out_path)[-1] == '.avi'

    # Get records from DB
    scene_rec = nusc.get('scene', scene_token)
    sample_rec = nusc.get('sample', scene_rec['first_sample_token'])
    sd_rec = nusc.get('sample_data', sample_rec['data'][channel])

    # Open CV init
    name = '{}: {} (Space to pause, ESC to exit)'.format(scene_rec['name'], channel)
    cv2.namedWindow(name)
    cv2.moveWindow(name, 0, 0)

    if out_path is not None:
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(out_path, fourcc, freq, imsize)
    else:
        out = None

    scene_list = []

    has_more_frames = True
    while has_more_frames:
        # Get data from DB
        impath, boxes, camera_intrinsic = nusc.get_sample_data(sd_rec['token'],
                                                               box_vis_level=BoxVisibility.ANY)

        # Load and render
        if not osp.exists(impath):
            raise Exception('Error: Missing image %s' % impath)

        im = cv2.imread(impath)
        reprojections = {}
        annotation_list = []

        for three_d_box in boxes:
            entry = {}
            c = nusc.explorer.get_color(three_d_box.name)
            cs_rec = nusc.get('calibrated_sensor', sd_rec['calibrated_sensor_token'])
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
            entry['instance_token'] = three_d_box.token

            annotation_list.append(entry)
            for i in range(4):
                cv2.line(im, boundaries[i], boundaries[(i + 1) % 4], c, 2)

        reprojections["annotation_list"] = annotation_list
        reprojections["filename"] = impath
        reprojections['sample_data_token'] = sd_rec['token']
        reprojections['timestamp'] = sd_rec['timestamp']
        reprojections['next'] = sd_rec['next']

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
        scene_list.append(reprojections)
        if not sd_rec['next'] == "":
            sd_rec = nusc.get('sample_data', sd_rec['next'])
        else:
            has_more_frames = False

    cv2.destroyAllWindows()
    if out_path is not None:
        out.release()
    return scene_list


def export_videos_and_two_dimensional_annotations(nusc: NuScenes, out_dir: str):
    # Load NuScenes class
    scene_tokens = [s['token'] for s in nusc.scene]

    # Create output directory
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    scene_to_annotations = {}
    # Write videos to disk
    for scene_token in scene_tokens:
        scene = nusc.get('scene', scene_token)
        print('Writing scene %s' % scene['name'])
        out_path = os.path.join(out_dir, scene['name']) + '.avi'
        if not os.path.exists(out_path):
            scene_to_annotations[scene_token] = render_scene_channel_new(nusc, scene['token'],
                                                                               channel='CAM_FRONT',
                                                                                freq= 10,
                                                                         imsize=(640, 360),
                                                                               out_path=out_path)
    dest_path = os.path.join(args.dataroot, args.version)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    with open(os.path.join(args.dataroot, args.version, args.filename), 'w') as fh:
        json.dump(scene_to_annotations, fh, sort_keys=True, indent=4)

    print("Saved the 2D re-projections under {}".format(os.path.join(args.dataroot, args.version, args.filename)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export 2D annotations from reprojections to a .json file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dataroot', type=str, default='/Users/Asli/Desktop/train',
                        help="Path where nuScenes is saved.")
    parser.add_argument('--version', type=str, default='v1.0-mini', help='Dataset version.')
    parser.add_argument('--filename', type=str, default='hadi_ins.json', help='Output filename.')
    parser.add_argument('--visibilities', type=str, default=['', '1', '2', '3', '4'],
                        help='Visibility bins, the higher the number the higher the visibility.', nargs='+')
    parser.add_argument('--image_limit', type=int, default=-1, help='Number of images to process or -1 to process all.')
    args = parser.parse_args()

    nusc = NuScenes(dataroot=args.dataroot, version=args.version)
    export_videos_and_two_dimensional_annotations(nusc, "exports/2d_anns")
    deneme = nusc.__load_table__("hadi_ins")
    print("oldu mu")