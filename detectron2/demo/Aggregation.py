import json
import os
import numpy as np
import pandas as pd
import tqdm
from json import dump
from config import argument_defaults


feature_path = argument_defaults['extractor']
aggregation_path = argument_defaults['aggregation']

with open("input") as f:
    videos = f.readlines()
out = []
for video_name in tqdm.tqdm(videos, total=len(videos)):
    video_name = video_name.replace('\n', '')
    video_name = os.path.splitext(video_name)[0]
    video_path = feature_path + video_name + '.json'

    if not os.path.isfile(video_path):
        continue
    with open(video_path) as f:
        x = json.load(f)

        for key, value in x.items():
            matrix = pd.DataFrame(value)

            #TODO changable aggregation method
            agg = np.max(matrix,axis=0)
            vid = {'video' : key,
                   'features': agg.tolist()}
            out.append(vid)
with open(aggregation_path + 'max_pool' +'.json', 'w') as outfile:
    dump(out, outfile)







