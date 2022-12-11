import argparse
import os
import glob
import csv
import numpy as np
# estrarre bb e calcolare centro e poi scalare tra [0, 1], path ?
from matplotlib import pyplot as plt

from ast import literal_eval

# Aonnotations file
#crea annotazioni con file csv
# dimension image: # x # -> scalare tra [0,1]
def create_ann(folder, dest):
    path = folder + 'csv/'   #folder +
    #path = 'csv/'  # folder +

    dirs = os.listdir(path)
    print('folder', dirs)
    path_no_bb = []
    for d in sorted(dirs):  # cartelle video#
        path_csv = path + d
        print('CSV: ', d)
        with open(path_csv, 'r') as csv_file:
            data = csv.reader(csv_file)
            for row in data:
                # coord = literal_eval(row[1].replace('.', '').replace(' ', ','))

                #print(row[1].replace('. ', ', ').replace('.', '').replace(' [', ',['))
                coord = literal_eval(row[1].replace('. ', ', ').replace('.', '').replace(' [', ',['))

                # Aonnotations file : label_idx x_center y_center width height
                if coord == -1 :
                    center = [' ', ' ']
                    w = ' '
                    h = ' '
                    path_no_bb.append(row[0])
                    #mi salvo i path di questi

                else:
                    center = [((coord[0][0] + coord[1][0]) / 2) / 1280, ((coord[0][1] + coord[2][1]) / 2) / 720]
                    w = (coord[0][0] - coord[1][0]) / 1280  # (xmax - xmin)
                    h = (coord[0][1] - coord[2][1]) / 720  # (ymax - ymin)
                    # print(center, 'w: ', w, 'h: ', h, '\n')

                # path frame #dest +
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
    path_txt_no = folder + 'bb_no_detected.csv'
    # with open(path_txt_no, 'w') as f:
    #     f.write(write)
    with open(path_txt_no, 'w') as csvfile:
        filewriter = csv.writer(csvfile)
        
        filewriter.writerow(path_no_bb)
    print(path_no_bb)

def mov_bb_null(folder):
    dirs = os.listdir(folder)
    print('folder', dirs)
    for d in sorted(dirs):  # c
        path_txt = folder + d
        with open(path_txt, 'r') as file:
            text = file.read()
            if len(text) <= 10:
                os.system('mv {0} /home/ndicostanzo/PyTorch-YOLOv3/pytorchyolo/data/custom/lab_zero/'.format(path_txt))


def mov_image_null(folder):
    fol_text = folder + 'lab_zero/'
    dirs = os.listdir(fol_text)
    print('folder', dirs)
    for d in sorted(dirs):  # ciclo su cartella bb_nul
        path_image = folder + 'images/' + d.split('.')[0] + '.jpg'
        os.system('mv {0} /home/ndicostanzo/PyTorch-YOLOv3/pytorchyolo/data/custom/image_zero/'.format(path_image))

def check_file(folder):
    path = folder + '/data/cut_video_scale/'
    dirs = os.listdir(path)
    event = folder + 'event/'
    dirs_event = os.listdir(event)
    #print('folder', dirs)
    for d in sorted(dirs):
        if d.split('_')[0] not in dirs_event:
            print(d)

def remove_file(folder):
    #video_no = ['video32', 'video33', 'video35','video54','video69']
    path_image = folder + 'event/'
    dirs_image = os.listdir(path_image)

    path_csv = '/home/ndicostanzo/PyTorch-YOLOv3/pytorchyolo/data/custom/image_no.csv'
    with open(path_csv, 'r') as csvfile:
        for i in csvfile:
            image = (i.split(','))

    for d in sorted(dirs_image): # ciclo sulle immagini
        name = d.split('.')[0] + '.txt'
        if d in image:
            path_name = path_image + d
            #print(path_name)
            d_save.append(d)
            os.remove(path_image)

    # path_txt_no = folder + 'image_no.csv'
    # with open(path_txt_no, 'w') as csvfile:
    #     filewriter = csv.writer(csvfile)
    #     filewriter.writerow(d_save)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--dest", dest="dest", default=None, help="Path to save annotation")
    args = parser.parse_args()
    print('Video: ', args.video)
    remove_file(args.video)
