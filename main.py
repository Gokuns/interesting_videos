import argparse
import json
import os.path as osp

from nuscenes import NuScenes

import config
from Dataset import Dataset
from NuscRenderer import NuscRenderer
from TwoDimensionalAnnotator import TwoDimensionalAnnotator
from VideoData import VideoData
from pyforms import start_app
from proof_of_concept_gui.VideoStatsViewer import VideoStatsViewer


def generate_video_data(table, nusc):
    data_list = []
    for key in table.keys():
        name = nusc.get("scene", key)["name"] + ".mp4"
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
    deneme = ['density_based_both', 'number_based_both', 'number_based_one', 'density_based_one',
              'peak_number_both', 'peak_area_both', 'peak_number_one', 'peak_area_one']

    if not osp.exists(osp.join(config.argument_defaults['dataroot'],
                      config.argument_defaults['version'],
                      config.argument_defaults['filename'])):
        annotator = TwoDimensionalAnnotator(nusc)
        annotator.export_two_dimensional_annotations(config.argument_defaults['export_path'])

    if not osp.exists(config.argument_defaults['video_data_path']
                             .format(config.argument_defaults['poc_mode'])+".json"):
        table = json.load(open(osp.join(osp.join(args.dataroot, args.version),
                                        config.argument_defaults['filename'])))
        data_list = generate_video_data(table, nusc)
        dataset = Dataset(name="NuScenes",
                          video_path=config.argument_defaults['export_path'],
                          videos=data_list)
        dataset.label_videos(config.argument_defaults['poc_mode'])
        dataset.save_as_json(config.argument_defaults['video_data_path']
                             .format(config.argument_defaults['poc_mode'])+".json")
    else:
        dataset = Dataset("Nuscenes",
                          json_path=config.argument_defaults['video_data_path'])
    print(config.argument_defaults['video_data_path']
                .format(config.argument_defaults['poc_mode'])+" has {} many interesting cases out of 850"
                .format(sum(video.is_interesting for video in dataset.videos)))
    start_app(VideoStatsViewer)
    print("Done")

    # for elt in deneme:
    #     dataset.label_videos(elt)
    #     dataset.save_as_json(config.argument_defaults['video_data_path'].format(elt) + ".json")
    #     print(config.argument_defaults['video_data_path']
    #           .format(elt) + " has {} many interesting cases out of 850"
    #           .format(sum(video.is_interesting for video in dataset.videos)))
