import json
import os
import numpy as np
import pandas as pd
import tqdm
from json import dump
from config import argument_defaults


feature_path = argument_defaults['extractor']
aggregation_path = argument_defaults['aggregation']

# with open("input") as f:
#     videos = f.readlines()
# maxer = []
# avger = []
# for video_name in tqdm.tqdm(videos, total=len(videos)):
#     video_name = video_name.replace('\n', '')
#     video_name = os.path.splitext(video_name)[0]
#     video_path = feature_path + video_name + '.json'
#
#     if not os.path.isfile(video_path):
#         continue
#     with open(video_path) as f:
#         x = json.load(f)
#
#         for key, value in x.items():
#             matrix = pd.DataFrame(value)
#
#             #TODO changable aggregation method
#             agg = np.mean(matrix,axis=0)
#             vid = {'video' : key,
#                    'features': agg.tolist()}
#             avger.append(vid)
#
#             agg2 = np.max(matrix,axis=0)
#             vid = {'video' : key,
#                    'features': agg2.tolist()}
#             maxer.append(vid)
# with open(aggregation_path + 'average2' +'.json', 'w') as outfile:
#     dump(avger, outfile)
#
# with open(aggregation_path + 'max_pool2' + '.json', 'w') as outfile:
#     dump(maxer, outfile)
#


def aggregate_vid(feat_list,mode):
    agg = []
    if mode ==1:
        agg = np.mean(feat_list, axis=0)
    elif mode == 2:
        agg = np.max(feat_list, axis=0)
    return agg








