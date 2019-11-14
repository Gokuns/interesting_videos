import json
import sklearn as sk
import numpy as np


def load_data(path='C:\\Users\\Goko\\Desktop\\data.json'):
    # load and create a list
    f = open(path)
    fil = json.load(f)

    features = [fil[i]['features'] for i in range(len(fil))]
    names = [fil[i]['video'] for i in range(len(fil))]
    labels=None #TODO: 5 fll this when you get labels in json
    # features = np.asarray(fil)
    return features,names,labels



def main():


    from sklearn.manifold import TSNE


if __name__ == '__main__':
    main()