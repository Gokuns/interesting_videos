from json import load
from json import dump
import numpy as np
import Dataset
import config


def change_poc(database_path, feature_path, output_path):
    with open(feature_path) as f:
        f = load(f)
        with open(output_path, 'w') as out:
            dataset = Dataset.Dataset(name="nuscenes",
                                      json_path=database_path)
            for video in f:
                video_data = dataset.find_video_from_path(video["video"])
                video["poc_result"] = video_data.is_interesting
            dump(f, out)


def aggregate_features(base_feature_path, database_path, mode, opt):
    with open(base_feature_path) as f:
        outputs = load(f)
        dataset = Dataset(json_path=database_path)

        average_output = []
        for scene in outputs:
            res = {'video': scene['video']}
            scene_full_path = scene['video']
            videodata = dataset.find_video_from_path(scene_full_path)
            res['poc_result'] = int(videodata.is_interesting)
            a = [i['features'] for i in scene['clips']]
            if mode == 'average':
                deneme = np.sum(a, 0) / len(a)
            elif mode == 'maximum':
                deneme = np.maximum(a, 0)
            else:
                deneme = np.sum(a, 0) / len(a)

            res['features'] = deneme.tolist()
            average_output.append(res)

        with open("output_{}_{}_{}.json".format(mode, opt.model_depth,
                                                config.argument_defaults[
                                                    'poc_mode']), 'w') as f:
            dump(average_output, f)


poc_modes = ['density_based_both', 'number_based_both', 'number_based_one', 'density_based_one',
              'peak_number_both', 'peak_area_both', 'peak_number_one', 'peak_area_one']
for mode in poc_modes:
    change_poc(config.argument_defaults['video_data_path']
                             .format(mode),
               "./output_averages_50.json",
               "./output_averages_50_{}.json".format(mode))
