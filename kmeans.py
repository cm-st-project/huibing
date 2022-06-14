from sklearn.neighbors import NearestNeighbors

import json

f = open('data.json')
data = json.load(f)

pic_names = []
pic_frames =[]
for name, angles in data.items():
    if angles:
        pic_names.append(name)
        pic_frames.append(angles)
        print(name, angles)

neigh = NearestNeighbors(n_neighbors=3)
neigh.fit(pic_frames)

pred = neigh.kneighbors([[-0.0, 1.2793395323170296, 0.8056656581096698, -1.2793395323170296, -0.9346557580492049, -1.4056476493802699, 1.4056476493802699, -0.0, 1.5708, 1.5708, 1.5708, 1.5708]])

pic_list = pred[1][0]

for i in pic_list:
    print(pic_names[i])