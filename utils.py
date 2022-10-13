import argparse
import os
import glob
import csv
import numpy as np
#estrarre bb e calcolare centro e poi scalare tra [0, 1], path ?
from matplotlib import pyplot as plt
# AQnnotations file : label_idx x_center y_center width height
from ast import literal_eval
# dimension image: 1280 x 720
def create_ann():
    with open('video02.csv', 'r') as csv_file:
        data = csv.reader(csv_file)
        for row in data:
            coord = literal_eval(row[1].replace('.', '').replace(' ', ','))
           # print(coord, '\n')
            #print(coord)
            #fig = plt.figure()
            center = [((coord[0][0] + coord[1][0]) /2) /1280, ((coord[0][1] + coord[2][1]) /2) /720]
            w = (coord[0][0] - coord[1][0]) /1280  # (xmax - xmin)
            h = (coord[0][1] - coord[2][1]) /720  # (ymax - ymin)
            print(center, 'w: ', w, 'h: ', h, '\n')
        # for i in range(len(coord)):
        #     plt.scatter(coord[i][0], coord[i][1])
        #     print(coord[i][0],coord[i][1], '\n')
        # plt.scatter((coord[0][0] + coord[1][0])/2, (coord[0][1] + coord[2][1])/2)
        # plt.show()
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    args = parser.parse_args()
    print('Video: ', args.video)
    create_ann()