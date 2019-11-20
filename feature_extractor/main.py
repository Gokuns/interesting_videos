import os
import sys
import json
import subprocess
import numpy as np
import torch
from torch import nn

from opts import parse_opts
from model import generate_model
from mean import get_mean
from classify import classify_video

import Dataset
import config

def main():
    opt = parse_opts()
    opt.mean = get_mean()
    opt.arch = '{}-{}'.format(opt.model_name, opt.model_depth)
    opt.sample_size = 112
    opt.sample_duration = 16
    opt.n_classes = 400

    model = generate_model(opt)
    print('loading model {}'.format(opt.model))
    model_data = torch.load(opt.model)
    assert opt.arch == model_data['arch']
    model.load_state_dict(model_data['state_dict'], strict = False)
    model.eval()
    dataset = Dataset.Dataset(name='', json_path=config.argument_defaults['video_data_path']
                             .format(config.argument_defaults['poc_mode'])+".json")

    if opt.verbose:
        print(model)

    input_files = []
    with open(opt.input, 'r') as f:
        for row in f:
            input_files.append(row[:-1])

    class_names = []
    with open('class_names_list') as f:
        for row in f:
            class_names.append(row[:-1])

    ffmpeg_loglevel = 'quiet'
    if opt.verbose:
        ffmpeg_loglevel = 'info'

    if os.path.exists('tmp'):
        subprocess.call('rm -rf tmp', shell=True)

    outputs = []
    for input_file in input_files:
        video_path = os.path.join(opt.video_root, input_file)
        if os.path.exists(video_path):
            print(video_path)
            subprocess.call('mkdir tmp', shell=True)
            subprocess.call('ffmpeg -i {} tmp/image_%05d.jpg'.format(video_path),
                            shell=True)

            result = classify_video('tmp', input_file, class_names, model, opt)

            outputs.append(result)

            subprocess.call('rm -rf tmp', shell=True)
        else:
            print('{} does not exist'.format(input_file))

    if os.path.exists('tmp'):
        subprocess.call('rm -rf tmp', shell=True)

    average_output = []
    for scene in outputs:
        res = {'video': scene['video']}
        scene_full_path = scene['video']
        videodata = dataset.find_video_from_path(scene_full_path)
        res['poc_result'] = int(videodata.is_interesting)
        a = [i['features'] for i in scene['clips']]
        deneme = np.sum(a, 0) / len(a)
        res['features'] = deneme.tolist()
        average_output.append(res)

    with open(opt.output, 'w') as f:
        json.dump(outputs, f)

    with open("output_averages_{}_{}.json".format(opt.model_depth, config.argument_defaults['poc_mode']), 'w') as f:
        json.dump(average_output, f)

if __name__ == "__main__":
    main()
