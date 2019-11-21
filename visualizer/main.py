import json

import matplotlib
matplotlib.use('Qt5Agg')

import sklearn as sk
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import _thread
from threading import Thread

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
import json
import config
from proof_of_concept_gui.VideoStatsViewer import VideoStatsViewer
from pyforms import start_app

def pca_data(data):
    print(len(data))

    feature_vector_list = [video["features"] for video in data]
    features = StandardScaler().fit_transform(feature_vector_list)
    pca = PCA(n_components=50)
    principal_components = pca.fit_transform(features).tolist()
    for i in range(len(data)):
        data[i]["features"] = principal_components[i]
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
    return data



def load_data(path=config.argument_defaults['feature_path']):
    # load and create a list
    f = open(path)
    fil = json.load(f)
    # features = np.asarray(fil)
    return fil

def partition_data(fil):
    features = [fil[i]['features'] for i in range(len(fil))]
    names = [fil[i]['video'] for i in range(len(fil))]
    labels=[fil[i]['poc_result'] for i in range(len(fil))]
    return features, names, labels

def tsne(features, names, labels):
    per = 5
    learning_rate = 1000
    early_exaggeration = 30
    n_iter = 7000

    X_embedded = TSNE(n_components=3, perplexity=per,
                      learning_rate=learning_rate,
                      early_exaggeration=early_exaggeration,
                      n_iter=n_iter).fit_transform(features)
    x_vals = [X_embedded[i][0] for i in range(len(X_embedded))]
    y_vals = [X_embedded[i][1] for i in range(len(X_embedded))]
    z_vals = [X_embedded[i][2] for i in range(len(X_embedded))]

    return x_vals, y_vals, z_vals

def plot_tnse(x_vals,y_vals,z_vals, names,labels,mode):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    for i in range(len(labels)):
        if labels[i]== 0:
            labels[i]= 'black'
        else: labels[i] = 'red'
    if mode:
        ax.scatter(x_vals, y_vals, z_vals, 'o', picker=5, c=labels)
    else:
        ax.scatter(x_vals, y_vals, z_vals, 'o', picker=5)
        #ax.annotate(names[i], (x_vals[i], y_vals[i]))
    cid = fig.canvas.mpl_connect('pick_event', lambda event: onpick(event,names))
    plt.show()



def onpick(event,names):
    thisline = event.artist
    ind = event.ind
    #points = tuple(zip(xdata[ind], ydata[ind]))
    scene_name = names[ind[0]]

    config.argument_defaults['selected_scene'] = scene_name
    print(config.argument_defaults['selected_scene'])
    start_app(VideoStatsViewer)

def main():
    file = load_data()
    data = pca_data(file) #uncomment this when needed
    #file = load_data('C:\\Users\\Goko\\Desktop\\data.json')
    features, names, labels=partition_data(data)
    x_vals, y_vals, z_vals = tsne(features, names, labels)
    plot_tnse(x_vals,y_vals,z_vals, names,labels,config.argument_defaults["colored_graph"])




if __name__ == '__main__':
    main()
