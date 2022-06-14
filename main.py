from tkinter import *
from PIL import ImageTk, Image

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
root = Tk()
root.geometry("1000x1000")
canvas = Canvas(root, bg ="white")

global image1, test,imagepath
value_inside = StringVar(root)
value_inside.set("select an opion")
def open_picture():
    global  image1, test, imagepath
    basewidth = 458
    print(value_inside.get())
    imagepath = f"static/pictures/{value_inside.get()}"
    print (imagepath)
    image1 = Image.open(imagepath)
    wpercent = basewidth/float(image1.size[0])
    hsize = int((float(image1.size[1])*float(wpercent)))
    image1 = image1.resize((basewidth, hsize))
    test = ImageTk.PhotoImage(image1)
    canvas.create_image(1,1,image=test,anchor = "nw")

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
            # print(picture)
            pass

        json_object = json.dumps(posedata, indent=2) #this block adds a dictionary for each pic to our json file
        with open("data.json", "w") as outfile:
            outfile.write(json_object)

def mediapipelabel():
    global imagepath, pictureList
    for picture in pictureList:
        # print(picture)
        labelPicture(f"static/pictures/{picture}")


    #for our dictionary we want name of photo, list of angles



class Joint:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.oval = canvas.create_oval((self.x + 4, self.y +4, self.x -4,self.y-4),activeoutline = "yellow", width = 8)

global neck,shoulder, left_arm, right_arme, left_forearm, body, left_thigh, right_thigh, left_leg, right_leg

right_shoulder = Joint(600,100)
left_shoulder = Joint(750,100)
right_waist = Joint(625,250)
left_waist = Joint(725,250)
right_elbow = Joint(570,200)
left_elbow = Joint(780,200)
right_wrist = Joint(570,300)
left_wrist = Joint(780,300)
right_knee = Joint(625,350)
left_knee = Joint(725,350)
right_ankle = Joint(625,500)
left_ankle = Joint(725,500)


shoulders = canvas.create_line(left_shoulder.x, left_shoulder.y, right_shoulder.x, right_shoulder.y)
left_arm = canvas.create_line(left_elbow.x, left_elbow.y, left_shoulder.x, left_shoulder.y)
right_arm = canvas.create_line(right_elbow.x, right_elbow.y, right_shoulder.x, right_shoulder.y)
left_forearm = canvas.create_line(left_elbow.x, left_elbow.y, left_wrist.x, left_wrist.y)
right_forearm = canvas.create_line(right_elbow.x, right_elbow.y, right_wrist.x, right_wrist.y)
left_thigh = canvas.create_line(left_waist.x, left_waist.y, left_knee.x, left_knee.y)
right_thigh = canvas.create_line(right_waist.x, right_waist.y, right_knee.x, right_knee.y)
left_leg = canvas.create_line(left_knee.x, left_knee.y, left_ankle.x, left_ankle.y)
right_leg = canvas.create_line(right_knee.x, right_knee.y, right_ankle.x, right_ankle.y)
left_body = canvas.create_line(left_waist.x,left_waist.y,left_shoulder.x,left_shoulder.y)
right_body = canvas.create_line(right_waist.x,right_waist.y,right_shoulder.x,right_shoulder.y)
hip = canvas.create_line(left_waist.x,left_waist.y,right_waist.x,right_waist.y)

def move_left_shoulder(event):
    global left_arm, shoulders, left_body
    canvas.bind("<B1-Motion>", move_left_shoulder)
    canvas.delete(shoulders,left_body,left_arm,left_shoulder.oval)
    left_shoulder.x,left_shoulder.y = event.x,event.y
    left_shoulder.oval = canvas.create_oval((left_shoulder.x+4,left_shoulder.y+4,left_shoulder.x-4,left_shoulder.y-4),activeoutline = "cyan", width = 8)
    shoulders = canvas.create_line(left_shoulder.x, left_shoulder.y, right_shoulder.x, right_shoulder.y)
    left_arm = canvas.create_line(left_elbow.x, left_elbow.y, left_shoulder.x, left_shoulder.y)
    left_body = canvas.create_line(left_waist.x, left_waist.y, left_shoulder.x,left_shoulder.y)
    canvas.tag_bind(left_shoulder.oval, "<B1-Motion>", move_left_shoulder)

def move_right_shoulder(event):
    global right_arm, shoulders, right_body
    canvas.bind("<B1-Motion>", move_right_shoulder)
    canvas.delete(shoulders,right_body,right_arm,right_shoulder.oval)
    right_shoulder.x,right_shoulder.y = event.x,event.y
    right_shoulder.oval = canvas.create_oval((right_shoulder.x+4,right_shoulder.y+4,right_shoulder.x-4,right_shoulder.y-4),activeoutline = "red", width = 8)
    shoulders = canvas.create_line(left_shoulder.x, left_shoulder.y, right_shoulder.x, right_shoulder.y)
    right_arm = canvas.create_line(right_elbow.x, right_elbow.y, right_shoulder.x, right_shoulder.y)
    right_body = canvas.create_line(right_waist.x, right_waist.y, right_shoulder.x, right_shoulder.y)
    canvas.tag_bind(right_shoulder.oval, "<B1-Motion>", move_right_shoulder)

def move_left_elbow(event):
    global left_arm,left_forearm
    canvas.bind("<B1-Motion>",move_left_elbow)
    canvas.delete(left_arm,left_forearm,left_elbow.oval)
    left_elbow.x,left_elbow.y = event.x,event.y
    left_arm = canvas.create_line(left_shoulder.x,left_shoulder.y,left_elbow.x,left_elbow.y)
    left_forearm = canvas.create_line(left_elbow.x,left_elbow.y, left_wrist.x,left_wrist.y)
    left_elbow.oval = canvas.create_oval((left_elbow.x+4,left_elbow.y+4,left_elbow.x-4,left_elbow.y-4),activeoutline = "cyan", width = 8)
    canvas.tag_bind(left_elbow.oval, "<B1-Motion>", move_left_elbow)

def move_right_elbow(event):
    global right_arm,right_forearm
    canvas.bind("<B1-Motion>",move_right_elbow)
    canvas.delete(right_arm,right_forearm,right_elbow.oval)
    right_elbow.x,right_elbow.y = event.x,event.y
    right_arm = canvas.create_line(right_shoulder.x,right_shoulder.y,right_elbow.x,right_elbow.y)
    right_forearm = canvas.create_line(right_elbow.x,right_elbow.y, right_wrist.x,right_wrist.y)
    right_elbow.oval = canvas.create_oval((right_elbow.x+4,right_elbow.y+4,right_elbow.x-4,right_elbow.y-4),activeoutline = "red", width = 8)
    canvas.tag_bind(right_elbow.oval, "<B1-Motion>", move_right_elbow)

def move_left_waist(event):
    global left_body,left_thigh,hip
    canvas.bind("<B1-Motion>",move_left_waist)
    canvas.delete(left_body,left_thigh,left_waist.oval,hip)
    left_waist.x,left_waist.y = event.x,event.y
    left_waist.oval = canvas.create_oval((left_waist.x+4,left_waist.y+4,left_waist.x-4,left_waist.y-4),activeoutline = "cyan", width = 8)
    left_body = canvas.create_line(left_shoulder.x,left_shoulder.y,left_waist.x,left_waist.y)
    left_thigh = canvas.create_line(left_waist.x,left_waist.y,left_knee.x,left_knee.y)
    hip = canvas.create_line(left_waist.x,left_waist.y,right_waist.x,right_waist.y)
    canvas.tag_bind(left_waist.oval,"<B1-Motion>",move_left_waist)

def move_right_waist(event):
    global right_body,right_thigh,hip
    canvas.bind("<B1-Motion>",move_right_waist)
    canvas.delete(right_body,right_thigh,right_waist.oval,hip)
    right_waist.x,right_waist.y = event.x,event.y
    right_waist.oval = canvas.create_oval((right_waist.x+4,right_waist.y+4,right_waist.x-4,right_waist.y-4),activeoutline = "red", width = 8)
    right_body = canvas.create_line(right_shoulder.x,right_shoulder.y,right_waist.x,right_waist.y)
    right_thigh = canvas.create_line(right_waist.x,right_waist.y,right_knee.x,right_knee.y)
    hip = canvas.create_line(left_waist.x,left_waist.y,right_waist.x,right_waist.y)
    canvas.tag_bind(right_waist.oval,"<B1-Motion>",move_right_waist)




def move_left_knee(event):
    global left_thigh,left_leg
    canvas.bind("<B1-Motion>",move_left_knee)
    canvas.delete(left_thigh,left_leg,left_knee.oval)
    left_knee.x,left_knee.y = event.x,event.y
    left_thigh = canvas.create_line(left_waist.x,left_waist.y,left_knee.x,left_knee.y)
    left_leg = canvas.create_line(left_knee.x, left_knee.y,left_ankle.x,left_ankle.y)
    left_knee.oval = canvas.create_oval((left_knee.x+4,left_knee.y+4,left_knee.x-4,left_knee.y-4), activeoutline="cyan", width=8)
    canvas.tag_bind(left_knee.oval,"<B1-Motion>",move_left_knee)

def move_right_knee(event):
    global right_thigh,right_leg
    canvas.bind("<B1-Motion>",move_right_knee)
    canvas.delete(right_thigh,right_leg,right_knee.oval)
    right_knee.x,right_knee.y = event.x,event.y
    right_thigh = canvas.create_line(right_waist.x,right_waist.y,right_knee.x,right_knee.y)
    right_leg = canvas.create_line(right_knee.x, right_knee.y,right_ankle.x,right_ankle.y)
    right_knee.oval = canvas.create_oval((right_knee.x+4,right_knee.y+4,right_knee.x-4,right_knee.y-4), activeoutline="red", width=8)
    canvas.tag_bind(right_knee.oval,"<B1-Motion>",move_right_knee)

def move_left_wrist(event):
    global left_forearm
    canvas.bind("<B1-Motion>",move_left_wrist)
    canvas.delete(left_forearm,left_wrist.oval)
    left_wrist.x,left_wrist.y = event.x,event.y
    left_forearm = canvas.create_line(left_elbow.x,left_elbow.y,left_wrist.x,left_wrist.y)
    left_wrist.oval = canvas.create_oval((left_wrist.x+4,left_wrist.y+4,left_wrist.x-4,left_wrist.y-4), activeoutline="cyan", width=8)
    canvas.tag_bind(left_wrist.oval, "<B1-Motion>", move_left_wrist)

def move_right_wrist(event):
    global right_forearm
    canvas.bind("<B1-Motion>",move_right_wrist)
    canvas.delete(right_forearm,right_wrist.oval)
    right_wrist.x,right_wrist.y = event.x,event.y
    right_forearm = canvas.create_line(right_elbow.x,right_elbow.y,right_wrist.x,right_wrist.y)
    right_wrist.oval = canvas.create_oval((right_wrist.x+4,right_wrist.y+4,right_wrist.x-4,right_wrist.y-4), activeoutline="red", width=8)
    canvas.tag_bind(right_wrist.oval, "<B1-Motion>", move_right_wrist)

def move_left_ankle(event):
    global left_leg
    canvas.bind("<B1-Motion>",move_left_ankle)
    canvas.delete(left_leg,left_ankle.oval)
    left_ankle.x,left_ankle.y = event.x,event.y
    left_leg = canvas.create_line(left_knee.x,left_knee.y,left_ankle.x,left_ankle.y)
    left_ankle.oval = canvas.create_oval((left_ankle.x+4,left_ankle.y+4,left_ankle.x-4,left_ankle.y-4), activeoutline="cyan", width=8)
    canvas.tag_bind(left_ankle.oval,"<B1-Motion>",move_left_ankle)

def move_right_ankle(event):
    global right_leg
    canvas.bind("<B1-Motion>",move_right_ankle)
    canvas.delete(right_leg,right_ankle.oval)
    right_ankle.x,right_ankle.y = event.x,event.y
    right_leg = canvas.create_line(right_knee.x,right_knee.y,right_ankle.x,right_ankle.y)
    right_ankle.oval = canvas.create_oval((right_ankle.x+4,right_ankle.y+4,right_ankle.x-4,right_ankle.y-4), activeoutline="red", width=8)
    canvas.tag_bind(right_ankle.oval,"<B1-Motion>",move_right_ankle)

def search():
    global pictureList
    Angles = [angle(left_wrist, left_elbow), angle(right_wrist,right_elbow),
                          angle(left_shoulder, left_elbow), angle(right_shoulder, right_elbow),
                          angle(left_shoulder,right_shoulder), angle(left_waist, left_shoulder),
                          angle(right_waist,right_shoulder), angle(left_waist, right_waist),
                          angle(left_knee, left_waist), angle(right_knee, right_waist),
                          angle(left_knee,left_ankle), angle(right_knee, right_ankle)]
    result = classifier(Angles)
    for picture in pictureList:
        if result in picture:
            print("Result")
            basewidth = 458
            image2 = Image.open(f"static/pictures/{picture}")
            wpercent = basewidth / float(image2.size[0])
            hsize = int((float(image2.size[1]) * float(wpercent)))
            image2 = image2.resize((basewidth, hsize))
            test2 = ImageTk.PhotoImage(image2)
            canvas.create_image(1, 1, image=test2, anchor="nw")
        else:
            print(result+picture)

def search2():
    f = open('data.json')
    data = json.load(f)
    for key in data:
        for i,val in enumerate(data[key]):
            if abs(val) > 1.3:
                data[key][i] = abs(val)

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
    for key in data:
        # print(len(data[key]))
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
    # for i in sum_of_diff:
        # print (i,sum_of_diff[i])
    # print(result, min(sum_of_diff.values()))

    global  image1, test, imagepath
    basewidth = 458
    print(value_inside.get())
    imagepath = f"static/pictures/{result}"
    # print (imagepath)
    image1 = Image.open(imagepath)
    wpercent = basewidth/float(image1.size[0])
    hsize = int((float(image1.size[1])*float(wpercent)))
    image1 = image1.resize((basewidth, hsize))
    test = ImageTk.PhotoImage(image1)
    canvas.create_image(1,1,image=test,anchor = "nw")


def angle(joint1,joint2):
    try:
        slope = (joint2.y-joint1.y)/(joint2.x-joint1.x)
        angle = numpy.arctan(slope)
        return angle
    except ZeroDivisionError:
        return 1.5708 #pi/2 radians

def save(): #Maybe use absolute value?
    global unnamed_pose_count,imagepath
    # PoseDictionary = {"picture": imagepath, "left_shoulder": (left_shoulder.x, left_shoulder.y),
    #         "left_elbow": (left_elbow.x, left_elbow.y), "left_wrist": (left_wrist.x, left_wrist.y),
    #         "left_waist": (left_waist.x, left_waist.y), "left_knee": (left_knee.x, left_knee.y),
    #         "left_ankle": (left_ankle.x, left_ankle.y), "right_shoulder": (right_shoulder.x, right_shoulder.y),
    #         "right_elbow": (right_elbow.x, right_elbow.y), "right_wrist": (right_wrist.x, right_wrist.y),
    #         "right_waist": (right_waist.x, right_waist.y), "right_knee": (right_knee.x, right_knee.y),
    #         "right_ankle": (right_ankle.x, right_ankle.y)}
    # print(str(PoseDictionary))
    #
    # Angles = [angle(left_wrist, left_elbow), angle(right_wrist,right_elbow),
    #                       angle(left_shoulder, left_elbow), angle(right_shoulder, right_elbow),
    #                       angle(left_shoulder,right_shoulder), angle(left_waist, left_shoulder),
    #                       angle(right_waist,right_shoulder), angle(left_waist, right_waist),
    #                       angle(left_knee, left_waist), angle(right_knee, right_waist),
    #                       angle(left_knee,left_ankle), angle(right_knee, right_ankle)]
    # x = databaseEntry.get()
    # file = open("database.py","a")
    # if x == "":
    #     x = f"unnamedPose{unnamed_pose_count}"
    #     unnamed_pose_count += 1
    #     file.write(f"\nunnamed_pose_count = {unnamed_pose_count}")
    #
    #
    # file.write(f"\n{x}= " +str(PoseDictionary))
    # file.write(f"\n{x}Angles= " +str(Angles
    #                                  ))
    f = open('data.json')
    data = json.load(f)
    pic = value_inside.get()
    data[pic] = [angle(left_shoulder, right_shoulder), angle(left_shoulder, left_elbow),
              angle(left_elbow, left_wrist), angle(right_shoulder, right_elbow),
              angle(right_elbow, right_wrist), angle(left_shoulder, left_waist),
              angle(right_shoulder, right_waist), angle(left_waist, right_waist),
              angle(left_waist, left_knee), angle(left_knee, left_ankle),
              angle(right_waist, right_knee), angle(right_knee, right_ankle)]
    json_object = json.dumps(data, indent=2)  # this block adds a dictionary for each pic to our json file
    with open("data.json", "w") as outfile:
        outfile.write(json_object)



canvas.tag_bind(left_shoulder.oval,"<Button-1>",move_left_shoulder)
canvas.tag_bind(left_shoulder.oval, "<B1-Motion>", move_left_shoulder)
canvas.tag_bind(right_shoulder.oval,"<Button-1>",move_right_shoulder)
canvas.tag_bind(right_shoulder.oval, "<B1-Motion>", move_right_shoulder)
canvas.tag_bind(left_elbow.oval,"<Button-1>",move_left_elbow)
canvas.tag_bind(left_elbow.oval, "<B1-Motion>", move_left_elbow)
canvas.tag_bind(right_elbow.oval,"<Button-1>",move_right_elbow)
canvas.tag_bind(right_elbow.oval, "<B1-Motion>", move_left_elbow)
canvas.tag_bind(left_waist.oval,"<Button-1>",move_left_waist)
canvas.tag_bind(left_waist.oval, "<B1-Motion>", move_left_waist)
canvas.tag_bind(right_waist.oval,"<Button-1>",move_right_waist)
canvas.tag_bind(right_waist.oval, "<B1-Motion>", move_right_waist)
canvas.tag_bind(left_knee.oval,"<Button-1>",move_left_knee)
canvas.tag_bind(left_knee.oval,"<B1-Motion>",move_left_knee)
canvas.tag_bind(right_knee.oval,"<Button-1>",move_right_knee)
canvas.tag_bind(right_knee.oval,"<B1-Motion>",move_right_knee)
canvas.tag_bind(left_wrist.oval,"<Button-1>",move_left_wrist)
canvas.tag_bind(left_wrist.oval,"<B1-Motion>",move_left_wrist)
canvas.tag_bind(right_wrist.oval,"<Button-1>",move_right_wrist)
canvas.tag_bind(right_wrist.oval,"<B1-Motion>",move_right_wrist)
canvas.tag_bind(right_ankle.oval,"<Button-1>",move_right_ankle)
canvas.tag_bind(right_ankle.oval,"<B1-Motion>",move_right_ankle)
canvas.tag_bind(left_ankle.oval,"<Button-1>",move_left_ankle)
canvas.tag_bind(left_ankle.oval,"<B1-Motion>",move_left_ankle)


searchLabel = Label(root, text ="Search for a pose by dragging pose creator")
searchLabel.pack()
SearchButton = Button(root,text = "Search", command = search2)
SearchButton.pack()
saveLabel = Label(root, text = "Save pose to database")
saveLabel.pack()
#databaseEntry = Entry(root)
#databaseEntry.pack()
saveButton = Button(root, text = "Save", command = save)
saveButton.pack()
value_inside = StringVar(root)
value_inside.set("select an opion")
pictureMenu = OptionMenu(root,value_inside,*pictureList)
pictureMenu.pack()
openButton = Button(root, text = "open", command = open_picture)
openButton.pack()
mediapipeButton = Button(root, text = "mediapip", command = mediapipe)
mediapipeButton.pack()
# mediapipelabelButton = Button(root, text = "mplable", command = mediapipelabel)
# mediapipelabelButton.pack()
canvas.pack(anchor = 'ne',fill = 'both',expand = '1')




root.mainloop()
