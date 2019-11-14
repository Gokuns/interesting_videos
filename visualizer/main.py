import json
import sklearn as sk
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


def load_data(path='C:\\Users\\Goko\\Desktop\\data.json'):
    # load and create a list
    f = open(path)
    fil = json.load(f)

    features = [fil[i]['features'] for i in range(len(fil))]
    names = [fil[i]['video'] for i in range(len(fil))]
    labels=None #TODO: 5 fll this when you get labels in json
    # features = np.asarray(fil)
    return features,names,labels

def tsne(features, names, labels):
    per = 15
    learning_rate = 150
    early_exaggeration = 5
    n_iter = 1500

    X_embedded = TSNE(n_components=2, perplexity=per,
                      learning_rate=learning_rate,
                      early_exaggeration=early_exaggeration,
                      n_iter=n_iter).fit_transform(features)
    x_vals = [X_embedded[i][0] for i in range(len(X_embedded))]
    y_vals = [X_embedded[i][1] for i in range(len(X_embedded))]

    return x_vals, y_vals

def plot_tnse(x_vals,y_vals,names,labels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_vals, y_vals)
    for i in range(len(x_vals)):
        ax.annotate(names[i], (x_vals[i], y_vals[i]))

    def onclick(event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()





def main():
    features, names, labels = load_data()
    x_vals, y_vals = tsne(features, names, labels)
    plot_tnse(x_vals,y_vals,names,labels)


if __name__ == '__main__':
    main()