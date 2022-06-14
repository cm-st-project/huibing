import numpy as np
from database import *
from sklearn.neighbors import NearestNeighbors,KNeighborsClassifier
import json

knn=KNeighborsClassifier(1)
#knn.fit()


keqingFeatures = []




keqingFeatures = [[8.5,0.06060606060606061,-3.1875, 8.083333333333334, 0.2535211267605634,8.473684210526315,
                  18.666666666666668,-0.5344827586206896,0.5106382978723404, 0.3253968253968254,5.5,
                  -1.1595092024539877],[15.333333333333334, 0.2,-2.911764705882353, 6.928571428571429,
                    0.23943661971830985,78.0, -42.0,-0.19696969696969696,0.5405405405405406, 0.2631578947368421,
                7.130434782608695, -1.065040650406504  ],[20], [8]]
keqingLabel= [0,0,20,8]
# np.reshape(keqingLabel, (-1,1))

picture4 = np.array([picture4aAngles,picture4bAngles,picture4cAngles])
picture4labels = np.array([3,3,3])

datafeatures = np.array([picture4aAngles, picture4bAngles,picture4cAngles,
                         picture13Angles, picture13bAngles, picture13cAngles,
                         picture14aAngles, picture14bAngles,picture14cAngles])
labels = np.array([4,4,4,13,13,13,14,14,14])

#
knn.fit(datafeatures, labels)

def classifier(angles):
    data = np.array(angles)

    prediction = knn.predict([data])

    print(prediction)
    print(type(prediction[0]))
    return str(prediction[0])

def classifier2():
    f = open('data.json')
    data = json.load(f)
    print(data)
