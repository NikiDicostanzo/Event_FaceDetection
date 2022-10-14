import argparse
import os
import glob
import csv
import numpy as np
# estrarre bb e calcolare centro e poi scalare tra [0, 1], path ?
from matplotlib import pyplot as plt

from ast import literal_eval


# dimension image: 1280 x 720 -> scalare tra [0,1]
def create_ann(folder, dest):
    path = folder + 'csv/'   #folder +
    dirs = os.listdir(path)
    print('folder', dirs)

    for d in sorted(dirs):  # cartelle video#
        path_csv = path + d
        with open(path_csv, 'r') as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                coord = literal_eval(row[1].replace('.', '').replace(' ', ','))
                # print(coord, '\n')

                # Aonnotations file : label_idx x_center y_center width height
                center = [((coord[0][0] + coord[1][0]) / 2) / 1280, ((coord[0][1] + coord[2][1]) / 2) / 720]
                w = (coord[0][0] - coord[1][0]) / 1280  # (xmax - xmin)
                h = (coord[0][1] - coord[2][1]) / 720  # (ymax - ymin)
                # print(center, 'w: ', w, 'h: ', h, '\n')

                # path frame
                name_frame = dest + 'labels/' + row[0].split('/')[2].split('.')[0] + '.txt'
                # print(name_frame)
                # label_idx x_center y_center width height
                write = '0' + ' ' + str(center[0]) + ' ' + str(center[1]) + ' ' + str(w) + ' ' + str(h)
                with open(name_frame, 'w') as f:
                    f.write(write)

            # for i in range(len(coord)):
            #     plt.scatter(coord[i][0], coord[i][1])
            #     print(coord[i][0],coord[i][1], '\n')
            # plt.scatter((coord[0][0] + coord[1][0])/2, (coord[0][1] + coord[2][1])/2)
            # plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--dest", dest="dest", default=None, help="Path to save annotation")
    args = parser.parse_args()
    print('Video: ', args.video)
    create_ann(args.video, args.dest)
