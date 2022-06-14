import os

#makes empty string
imageString = ""
#gets every picture name in pictures folder
for pictureName in os.listdir('static/pictures'):
    if "jpg" in pictureName or "png" in pictureName or "jpeg" in pictureName:

    #makes html code for every picture name
        imageString += f'<img src="static/pictures/{pictureName}">\n'

#opens new file to write html code
outfile = open('htmlpics.html', 'w')
outfile.write(imageString)
