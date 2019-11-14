from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import json

with open("datasets/nuscenes/output_averages_18.json") as f:
    data = json.load(f)
    feature_vector_list = [video["features"] for video in data]
    video_names = [video["video"] for video in data]
    features = StandardScaler().fit_transform(feature_vector_list)
    pca = PCA(n_components=20)
    principal_components = pca.fit_transform(features).tolist()
    pca_dict = dict(zip(video_names, principal_components))
    print(pca_dict)
    with open('data.json', 'w') as outfile:
        json.dump(pca_dict, outfile)