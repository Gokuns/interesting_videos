import argparse
import json
import os.path as osp

from nuscenes import NuScenes

import config
from Dataset import Dataset
from NuscRenderer import NuscRenderer
from TwoDimensionalAnnotator import TwoDimensionalAnnotator
from VideoData import VideoData


def generate_video_data(table, nusc):
    data_list = []
    for key in table.keys():
        name = nusc.get("scene", key)["name"]
        path = osp.join(config.argument_defaults['export_path'], name)
        data = VideoData(table[key], path)
        data_list.append(data)
    return data_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export 2D annotations from reprojections to a .json file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dataroot', type=str, default=config.argument_defaults['dataroot'],
                        help="Path where nuScenes is saved.")
    parser.add_argument('--version', type=str, default=config.argument_defaults['version'], help='Dataset version.')
    parser.add_argument('--filename', type=str, default=config.argument_defaults['filename'], help='Output filename.')
    parser.add_argument('--visibilities', type=str, default=['', '1', '2', '3', '4'],
                        help='Visibility bins, the higher the number the higher the visibility.', nargs='+')
    parser.add_argument('--image_limit', type=int, default=-1, help='Number of images to process or -1 to process all.')
    args = parser.parse_args()

    nusc = NuScenes(dataroot=args.dataroot, version=args.version)
    # renderer = NuscRenderer(nusc)
    # renderer.export_videos_and_two_dimensional_annotations(config.argument_defaults['export_path'])
    # annotator = TwoDimensionalAnnotator(nusc)
    # annotator.export_two_dimensional_annotations(config.argument_defaults['export_path'])

    table = json.load(open(osp.join(osp.join(args.dataroot, args.version), config.argument_defaults['filename'])))
    data_list = generate_video_data(table, nusc)

    # dataset = Dataset(name="NuScenes", video_path=config.argument_defaults['export_path'], videos=data_list)
    dataset = Dataset("loaded dataset",
                      json_path=config.argument_defaults['video_data_path'])
    dataset.label_videos(data_list, config.argument_defaults['poc_mode'])
    # with open(os.path.join(args.dataroot, args.version, config.argument_defaults['dataset_path']), 'w') as fh:
    #     json.dump(dataset.videos, fh, sort_keys=True, indent=4)

    print("Done")
