import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier  # MLP is an NN
from sklearn import svm
import numpy as np
import argparse
import cv2
import os
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
import pickle
import math
import sys

symbol_output_dict = {

}


random_seed = 42
random.seed(random_seed)
np.random.seed(random_seed)


classifiers = {
    'SVM': svm.LinearSVC(random_state=random_seed, max_iter=20000,dual=False),
    'KNN': KNeighborsClassifier(n_neighbors=7),
    'NN': MLPClassifier(solver='sgd', random_state=random_seed, hidden_layer_sizes=(500,), max_iter=20, verbose=1)
}


def ORB_feature(img):
    orb = cv.ORB_create()
    # find the keypoints with ORB
    kp = orb.detect(img, None)
    # compute the descriptors with ORB
    kp, des = orb.compute(img, kp)
    # draw only keypoints location,not size and orientation
    img2 = cv.drawKeypoints(img, kp, None, color=(0, 255, 0), flags=0)
    plt.imshow(img2), plt.show()


def extract_hog_features(img, target_img_size=(32, 32)):

    img = cv2.resize(img, target_img_size)
    win_size = (32, 32)
    cell_size = (4, 4)
    block_size_in_cells = (2, 2)

    block_size = (block_size_in_cells[1] * cell_size[1],
                  block_size_in_cells[0] * cell_size[0])
    block_stride = (cell_size[1], cell_size[0])
    nbins = 9  # Number of orientation bins
    hog = cv2.HOGDescriptor(win_size, block_size,
                            block_stride, cell_size, nbins)
    h = hog.compute(img)
    h = h.flatten()
    return h.flatten()


def extract_hist_features(img, histmode='hist', target_img_size=(32, 32)):

    if(len(img.shape)==3):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, target_img_size)
    img = img > 127
    hist_hor = np.sum(img, axis=0)
    hist_ver = np.sum(img, axis=1)
    if histmode == 'vhist':
        return hist_ver
    if histmode == 'hhist':
        return hist_ver
    if histmode == 'hist' or histmode == 'all':
        return np.concatenate((hist_ver, hist_hor))

def extract_huMoments_features(img, target_img_size = (32,32)):
    
    if(len(img.shape)==3):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, target_img_size)
    _,img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    features = cv.moments(img)
    hufeats = cv.HuMoments(features)
    for i in range(0,7):
        if hufeats[i] != 0:
            hufeats[i] = -1* math.copysign(1.0, hufeats[i]) * math.log10(abs(hufeats[i]))
    return hufeats.flatten()

def extract_features(img, feature_set='hog'):

    if feature_set == 'hog':
        hog = extract_hog_features(img)
        aspectRatio = img.shape[0] / img.shape[1]
        hog = np.append(hog, aspectRatio)
        return hog

    elif feature_set == 'hist' or feature_set == 'vhist' or feature_set == 'hhist':
        return extract_hist_features(img, feature_set)

    elif feature_set == 'moments':
        return extract_huMoments_features(img)

    elif feature_set == 'all':
        hog = extract_hog_features(img)
        aspectRatio = img.shape[0] / img.shape[1]
        hog = np.append(hog, aspectRatio)
        histfeatures = extract_hist_features(img, feature_set)
        allFeature = np.concatenate((hog, histfeatures))
        moments = extract_huMoments_features(img)
        allFeature = np.concatenate((allFeature,moments))
        return allFeature


def load_dataset(path_to_dataset, feature_set='hog'):
    features = []
    labels = []
    path_to_dataset = os.path.join(os.getcwd(), path_to_dataset)
    directoriesNames = os.listdir(path_to_dataset)
    print(directoriesNames)
    for directory in directoriesNames:
        print(directory)
        img_filenames = os.listdir(os.path.join(path_to_dataset, directory))
        for i, fn in enumerate(img_filenames):

            labels.append(directory)

            path = os.path.join(path_to_dataset, directory, fn)
            img = cv2.imread(path)
            features.append(extract_features(img, feature_set))

            # show an update every 1,000 images
            if i > 0 and i % 500 == 0:
                print("[INFO] processed {}/{}".format(i, len(img_filenames)))

    return features, labels


def train_classifier(path_to_dataset, feature_set):

    # Load dataset with extracted features
    print('Loading dataset. This will take time ...')
    features, labels = load_dataset(path_to_dataset, feature_set)
    print('Finished loading dataset.')

    # Since we don't want to know the performance of our classifier on images it has seen before
    # we are going to withhold some images that we will test the classifier on after training
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, random_state=random_seed, stratify=labels, shuffle=True)

    print('############## Training', " SVM ", "##############")
    # Train the model only on the training features
    model = classifiers['SVM']
    model.fit(train_features, train_labels)

    # Test the model on images it hasn't seen before
    accuracy = model.score(test_features, test_labels)

    print("SVM ", 'accuracy:', accuracy*100, '%')



def main():
    # Testing the function

    if(len(sys.argv) >= 2):
        data_path = sys.argv[1]
    else:
        data_path = "Dataset"

    train_classifier(data_path, 'all')
    classifier = classifiers['SVM']
    # save the model to disk
    filename = 'Model.sav'
    pickle.dump(classifier, open(filename, 'wb'))



if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
