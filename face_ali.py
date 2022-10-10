import face_alignment
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from skimage import io
import collections
import numpy as np
import argparse
import os
import csv


def get_coord(path_image):
    # Optionally set detector and some additional detector parameters
    face_detector = 'sfd'
    face_detector_kwargs = {
        "filter_threshold": 0.8
    }
    # Run the 3D face alignment on a test image, without CUDA.
    fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._3D, device='cpu', flip_input=True,
                                      face_detector=face_detector, face_detector_kwargs=face_detector_kwargs)
    input_img = io.imread(path_image)
    preds = fa.get_landmarks(input_img)[-1]
    return preds


def plot_bb(path_image, path_event):
    event_img = io.imread(path_event)
    bb = bounding_box(path_image)
    fig = plt.figure(figsize=plt.figaspect(.5))
    ax = fig.add_subplot(1, 2, 1)
    ax.imshow(event_img)
    ax.plot(bb[:, 0], bb[:, 1])
    ax.axis('off')
    plt.show()


def bounding_box(path_image):
    preds = get_coord(path_image)
    bb = [[max(preds[:, 0]), max(preds[:, 1])],
          [min(preds[:, 0]), max(preds[:, 1])],
          [min(preds[:, 0]), min(preds[:, 1])],
          [max(preds[:, 0]), min(preds[:, 1])]]
    bb = np.array(bb)
    return bb

# folder = /home/ndicostanzo/event
def create_csv(folder):  # path -> (??) / frame/video#/frame#.png
    dirs = os.listdir(folder)
    for d in sorted(dirs):  # video
        if d != 'event':
            path = folder + d
            #todo
            csv_path = folder + 'event/' + d + '/video.csv'  # devo salvarlo dentro event
            with open(csv_path, 'w') as csvfile:
                filewriter = csv.writer(csvfile)
                frame = os.listdir(path)
                for f in sorted(frame):  # frame
                    if 'png' == f.split('.')[1]:
                        path_image = path + '/' + f
                        print('Frame: ', path_image)
                        bb = bounding_box(path_image)
                        print('Finish bb: ', bb)

                        path_image_save = folder + 'event/' + d + '/' + f  # metto path macchina?
                        lines = [path_image_save, bb]
                        filewriter.writerow(lines)


# creo csv con coordinate bb e path al frame (attenzione al path! quando metti nella macchina-> stesse cartelle)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    args = parser.parse_args()
    print('Video: ', args.video)
    create_csv(args.video)
