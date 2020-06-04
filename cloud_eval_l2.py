#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#### Module import
import keras.backend as K
import keras
from keras import backend
from keras.models import load_model
import tensorflow as tf

from cleverhans.utils_keras import KerasModelWrapper
from cleverhans import utils
import csv
import scipy.io
import glob
import numpy as np
import sys
from numpy import genfromtxt
import time

#### Funtion definition
def preprocess(x, maxlen):
    # Replace Nan data with numerical zeros and infinity
    x =  np.nan_to_num(x)
#    x =  x[0, 0:min(maxlen,len(x))]
    # clip the data with maxlen (9000) data points
    x =  x[0, 0:maxlen]
    # subtract each data with mean
    x = x - np.mean(x)
    # divide each data with std
    x = x / np.std(x)

    # zeros of size 1x9000
    tmp = np.zeros((1, maxlen))
#    print(x.shape)
    #len(x) is again either 9000 or less than that,
    tmp[0, :len(x)] = x.T  # padding sequence?

    #x was a row matrix earlier, now it is a column after the transpose
    x = tmp
#    print(x.shape)
# axis 0,1,2 somehow keras requires data to be in 3 dimensions [[[2],[3],[4]..]]
    x = np.expand_dims(x, axis=2)  # required by Keras
#    print(x.shape)
    del tmp

    return x

def zero_mean(x):
    x = x - np.mean(x)
    x = x / np.std(x)
    return x

#### Main Program

#--- parameters
dataDir = './training2017/'
FS = 300
WINDOW_SIZE = 30*FS     # padding window for CNN
classes = ['A', 'N', 'O','~']

file = sys.argv[1]
fid_from = int(sys.argv[2])
fid_to = int(sys.argv[3])
data_select = genfromtxt(file, delimiter=',')

#--- loading model and prepare wrapper

#A boolean that when value is set at 0 means testing phase
keras.layers.core.K.set_learning_phase(0)

# In tensorflow 1, you are first required to create a graph that defines all the computaions that are required to be performed
# The graph does not compute anything by itself (we just define the operations that are to be performed)
# A session is where the graph or a part of the graph is implemented
# A variables' value is only valid through that session, if a variable initialized in one session is called in another session it will have to be initialized again
sess = tf.Session()
K.set_session(sess)
print("Loading model")
model = load_model('ResNet_30s_34lay_16conv.hdf5')

# Model wrapper = without any additional computation, just represent the model (hide the underlying details of the operation)
#wrap = KerasModelWrapper(model, nb_classes=4)
wrap = KerasModelWrapper(model)


# A session in tf is an encapsulation with its own variables, objects
# A placeholder is a 'placeholder' for a tensor that is fed later
# x is a tensor for feeding input (hence size 9000x1)
# y is a tensor for output hence 4 classes
x = tf.placeholder(tf.float32, shape=(None, 9000, 1))
y = tf.placeholder(tf.float32, shape=(None, 4))

# predictions are the result of input when fed to the model
preds = model(x)

#--- load groundTruth File
print("Loading ground truth file")
# Revised Labels file
csvfile = list(csv.reader(open('REFERENCE-v3.csv')))
# Files now contains all the matlab data file paths (all 8528 of them) sorted
files = sorted(glob.glob(dataDir+"*.mat"))

#--- Attacker

# Import the attack which uses l2 metric
from myattacks_l2 import ECGadvL2

# Instantiate an object passing wrapped model and current session
ecgadvL2 = ECGadvL2(wrap, sess=sess)

print('Attack l2-norm is running...')

#--- loop on file including data_select[:,3] from fid_from-th row to fid_to-th row

eval_result = np.zeros((4*(fid_to-fid_from), 4)) # fid, ground_truth, target, adv_result

num = fid_from
while (num < fid_to):

    #--- Loading
    fid = int(data_select[num, 3])
    record = "A{:05d}".format(fid)
    local_filename = dataDir+record
    print('Loading record {}'.format(record))
    mat_data = scipy.io.loadmat(local_filename)
    #data = mat_data['val'].squeeze()
    data = mat_data['val']
    print(data.shape)

    #--- Processing data
    data = preprocess(data, WINDOW_SIZE)
    X_test=np.float32(data)

    #--- Read the ground truth label, Change it to one-shot form
    ground_truth_label = csvfile[fid-1][1]
    ground_truth = classes.index(ground_truth_label)
    print('Ground truth:{}'.format(ground_truth))

    Y_test = np.zeros((1, 1))
    Y_test[0,0] = ground_truth
    Y_test = utils.to_categorical(Y_test, num_classes=4)

    #--- Prepare the target labels for targeted attack
    for i in range(4):
        if (i == ground_truth):
            continue

        target = np.zeros((1, 1))
        target[0,0] = i
        target = utils.to_categorical(target, num_classes=4)
        target = np.float32(target)

        #--- Attacking...
        ecgadvL2_params = {'y_target': target}
        start_time = time.time()
        adv_x = ecgadvL2.generate(x, **ecgadvL2_params)
        adv_x = tf.stop_gradient(adv_x) # Consider the attack to be constant
        feed_dict = {x: X_test}
        adv_sample = adv_x.eval(feed_dict=feed_dict, session=sess)
        print("--- %s seconds ---" % (time.time() - start_time))

        #--- Attack result
#        adv_sample = zero_mean(adv_sample)
        prob = model.predict(adv_sample)
        ann = np.argmax(prob)
#        ann_label = classes[ann]
        print('Adv result:{}'.format(ann))

        idx = num - fid_from
        eval_result[4*idx+i, 0] = fid
        eval_result[4*idx+i, 1] = ground_truth
        eval_result[4*idx+i, 2] = i
        eval_result[4*idx+i, 3] = ann

        #--- Save adv_sample to file
        file_sample = './cloud_model/l2_eval/R' + str(fid)+ '_' + str(ground_truth) + '_' + str(i) + '_' + str(ann) + '.csv'
        np.savetxt(file_sample, adv_sample[0,:], delimiter=",")

    num = num+1

file_result = './cloud_model/l2_eval/res'+ '_' + str(fid_from) + '_' + str(fid_to) + '.csv'
np.savetxt(file_result, eval_result, delimiter=",")
