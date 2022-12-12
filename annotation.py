import glob
import csv
import numpy as np
from matplotlib import pyplot as plt
import argparse
import os
from face_ali import bounding_box, plot_bb
import csv
# tagliare i video e estrarre i frame rgb
import shutil
import cv2
from ast import literal_eval


# cambio -> creo frame(togliendo il primo), ridimensiono, calcolo bb e salvo direttamente bb
def data_yolo(folder, dest, size_im):
    path_video = folder + 'video_cut/'
    dirs = os.listdir(path_video)
    no_bb = []
    for d in sorted(dirs):  # ciclo su video
        new_path = folder + d.split('.')[0] + '/'  # dove salvo frame
        path = path_video + d
        if not os.path.exists(new_path):  # crea le cartelle dei frame
            os.makedirs(new_path)

        print('Extract frame RGB: ', d)
        os.system("ffmpeg -i {0} -filter:v fps=fps=20 {1}/{2}_%04d.png".format(path, new_path, d.split('_')[0]))
        dirs_frame = os.listdir(new_path)
        for f in sorted(dirs_frame):
            path_image = new_path + f
            if f.split('.')[0] != 'video0001':  # non voglio il 1° frame perche non ho l'event
                print('Calculate bb')
                bb = bounding_box(path_image)
                print('Finish bb: ', bb)
                if len(bb) != 0:  # non salvo se non c'è bb
                    name_file = f.split('.')[0]  # chiamo i file video#.txt
                    create_ann(bb, name_file, dest, size_im)
                else:
                    no_bb.append(path_image)
                    # spostare imm. senza bb
                    print('Move images: ', f)
                    mv_image = dest + 'images/' + f
                    image_zero = dest + 'image_zero/'
                    if not os.path.exists(image_zero):  # crea le cartelle dei frame_zero
                        os.makedirs(image_zero)
                    os.system('mv {0} {1}'.format(mv_image, image_zero))

        print('Remove frames:', d)
        shutil.rmtree(new_path)  # elimino cartella con file rgb per problemi di spazio

    path_txt_no = folder + 'bb_no_detected.csv'
    with open(path_txt_no, 'w') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(no_bb)


# uso video scalati ! non serve
def scale_image(frame, new_name, size_im):
    img = cv2.imread(frame)
    print('Frame: ', frame)
    img = cv2.resize(img, (size_im, size_im), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(new_name, img)

# dimension image: 768 x 768 -> scalare tra [0,1]
def create_ann(coord, row, dest, size_im):
    center = [((coord[0][0] + coord[1][0]) / 2) / size_im, ((coord[0][1] + coord[2][1]) / 2) / size_im]
    w = (coord[0][0] - coord[1][0]) / size_im  # (xmax - xmin)
    h = (coord[0][1] - coord[2][1]) / size_im  # (ymax - ymin)
    # print(center, 'w: ', w, 'h: ', h, '\n')
    print(coord)
    write = '0' + ' ' + str(center[0]) + ' ' + str(center[1]) + ' ' + str(w) + ' ' + str(h)

    name_frame = dest + 'labels/' + row + '.txt'  #/../PyTorch-YOLOv3/pytorchyolo/data/custom/
    print(write)
    # label_idx x_center y_center width height
    with open(name_frame, 'w') as f:
        f.write(write)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--dest", dest="dest", default=None, help="Path to save annotation")
    parser.add_argument("--size_im", dest="size_im", default=768, help="Size of image")
    args = parser.parse_args()
    print('Video: ', args.video)
    data_yolo(args.video, args.dest, args.size_im)
