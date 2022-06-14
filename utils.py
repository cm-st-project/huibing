
from mpPose import mpPose, labelPicture
import os
import numpy
from machineLearning import *
import json
classifier2()

global pictureList
pictureList = []
for picture in os.listdir("static/pictures"):
    pictureList.append(picture)
print(pictureList)
print(os.listdir("static/pictures"))


def mediapipe():
    global imagepath, pictureList
    # with open("data.json","r+") as file:
    #     file.truncate(0)
    posedata = {}
    for picture in pictureList: #this block gets angles for each pic and appends it to dictionary
        posedata[picture] = []
        try:
            for joint1,joint2 in mpPose(f"static/pictures/{picture}"):
                posedata[picture].append(angle(joint1,joint2))
            print(posedata)
        except UnboundLocalError:
            print(picture)
            pass

        json_object = json.dumps(posedata, indent=2) #this block adds a dictionary for each pic to our json file
        with open("data.json", "w") as outfile:
            outfile.write(json_object)

def mediapipelabel():
    global imagepath, pictureList
    for picture in pictureList:
        print(picture)
        labelPicture(f"static/pictures/{picture}")


    #for our dictionary we want name of photo, list of angles

def search2(joints):
    f = open('data.json')
    data = json.load(f)
    for key in data:
        for i,val in enumerate(data[key]):
            if abs(val) > 1.3:
                data[key][i] = abs(val)

    right_shoulder = Joint(joints['right_shoulder']['x'],joints['right_shoulder']['y'])
    left_shoulder = Joint(joints['left_shoulder']['x'],joints['left_shoulder']['y'])
    right_waist = Joint(joints['right_waist']['x'],joints['right_waist']['y'])
    left_waist = Joint(joints['left_waist']['x'],joints['left_waist']['y'])
    right_elbow = Joint(joints['right_elbow']['x'],joints['right_elbow']['y'])
    left_elbow = Joint(joints['left_elbow']['x'],joints['left_elbow']['y'])
    right_wrist = Joint(joints['right_wrist']['x'],joints['right_wrist']['y'])
    left_wrist = Joint(joints['left_wrist']['x'],joints['left_wrist']['y'])
    right_knee = Joint(joints['right_knee']['x'],joints['right_knee']['y'])
    left_knee = Joint(joints['left_knee']['x'],joints['left_knee']['y'])
    right_ankle = Joint(joints['right_ankle']['x'],joints['right_ankle']['y'])
    left_ankle = Joint(joints['left_ankle']['x'],joints['left_ankle']['y'])

    Angles = [angle(left_shoulder, right_shoulder), angle(left_shoulder, left_elbow),
              angle(left_elbow, left_wrist), angle(right_shoulder, right_elbow),
              angle(right_elbow, right_wrist), angle(left_shoulder, left_waist),
              angle(right_shoulder, right_waist), angle(left_waist, right_waist),
              angle(left_waist, left_knee), angle(left_knee, left_ankle),
              angle(right_waist, right_knee), angle(right_knee, right_ankle)]
    # for a in Angles:
    #     print(a)
    print(Angles)
    differences = {}
    sum_of_diff = {}
    # a = np.array(Angles)
    #
    # for key in data:
    #     if len(data[key])>0:
    #         b = np.array(data[key])
    #         dist = np.linalg.norm(a - b)
    #         sum_of_diff[key]=dist

    for key in data:
        if len(data[key]) > 0:
            differences[key] = []
            for i in range(len(data[key])):
                if i in [1,2,3,4,8,10]:
                    differences[key].append(abs(Angles[i]-data[key][i])*2)
                else:
                    differences[key].append(abs(Angles[i] - data[key][i]))

    for key in differences:
        sum_of_diff[key] = 0
        for diff in differences[key]:
            sum_of_diff[key] += diff
    result = min(sum_of_diff, key=sum_of_diff.get)
    scores = sum_of_diff
    top3=[]
    for i in range(3):
        minimum = min(scores, key=scores.get)
        del scores[minimum]
        top3.append(minimum)
    imagepath = f"static/pictures/{result}"
    imagepath2= f"static/pictures/{top3[1]}"
    imagepath3 = f"static/pictures/{top3[2]}"
    top3 = [imagepath, imagepath2, imagepath3]
    print(imagepath)
    return top3



def angle(joint1,joint2):
    try:
        slope = (joint2.y-joint1.y)/(joint2.x-joint1.x)
        angle = numpy.arctan(slope)
        return  angle
    except ZeroDivisionError:
        return 1.5708 #pi/2 radians
# mediapipe()
# def save(): #Maybe use absolute value?
#     global unnamed_pose_count,imagepath
#     # PoseDictionary = {"picture": imagepath, "left_shoulder": (left_shoulder.x, left_shoulder.y),
#     #         "left_elbow": (left_elbow.x, left_elbow.y), "left_wrist": (left_wrist.x, left_wrist.y),
#     #         "left_waist": (left_waist.x, left_waist.y), "left_knee": (left_knee.x, left_knee.y),
#     #         "left_ankle": (left_ankle.x, left_ankle.y), "right_shoulder": (right_shoulder.x, right_shoulder.y),
#     #         "right_elbow": (right_elbow.x, right_elbow.y), "right_wrist": (right_wrist.x, right_wrist.y),
#     #         "right_waist": (right_waist.x, right_waist.y), "right_knee": (right_knee.x, right_knee.y),
#     #         "right_ankle": (right_ankle.x, right_ankle.y)}
#     # print(str(PoseDictionary))
#     #
#     # Angles = [angle(left_wrist, left_elbow), angle(right_wrist,right_elbow),
#     #                       angle(left_shoulder, left_elbow), angle(right_shoulder, right_elbow),
#     #                       angle(left_shoulder,right_shoulder), angle(left_waist, left_shoulder),
#     #                       angle(right_waist,right_shoulder), angle(left_waist, right_waist),
#     #                       angle(left_knee, left_waist), angle(right_knee, right_waist),
#     #                       angle(left_knee,left_ankle), angle(right_knee, right_ankle)]
#     # x = databaseEntry.get()
#     # file = open("database.py","a")
#     # if x == "":
#     #     x = f"unnamedPose{unnamed_pose_count}"
#     #     unnamed_pose_count += 1
#     #     file.write(f"\nunnamed_pose_count = {unnamed_pose_count}")
#     #
#     #
#     # file.write(f"\n{x}= " +str(PoseDictionary))
#     # file.write(f"\n{x}Angles= " +str(Angles
#     #                                  ))
#     f = open('data.json')
#     data = json.load(f)
#     pic = value_inside.get()
#     data[pic] = [angle(left_shoulder, right_shoulder), angle(left_shoulder, left_elbow),
#               angle(left_elbow, left_wrist), angle(right_shoulder, right_elbow),
#               angle(right_elbow, right_wrist), angle(left_shoulder, left_waist),
#               angle(right_shoulder, right_waist), angle(left_waist, right_waist),
#               angle(left_waist, left_knee), angle(left_knee, left_ankle),
#               angle(right_waist, right_knee), angle(right_knee, right_ankle)]
#     json_object = json.dumps(data, indent=2)  # this block adds a dictionary for each pic to our json file
#     with open("data.json", "w") as outfile:
#         outfile.write(json_object)

class Joint:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def print(self):
        return self.x, self.y
