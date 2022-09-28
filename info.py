import argparse
import glob
import os
from PIL import Image

#simulatore esim
path_ros = '/home/ninad/sim_ws/src/rpg_esim/event_camera_simulator/esim_ros'
#home\ninad\sim_ws\src\rpg_esim\event_camera_simulator\esim_ros\scripts
#folder = '/tmp/cheetah_example/esmi_frame!=/'
#folder = '/mnt/e/frame'

def ros_info(folder):
    dirs = os.listdir(folder)
    for d in sorted(dirs):  # cartelle dei video
        if d != 'event':
            path = folder + d
            os.system("rosbag info {0}/video.bag".format(path))
            print('p :', path)

def black_image(folder):
    dirs = os.listdir(folder) #path alle cartelle con tutti i frames
    for d in sorted(dirs): #dirs
        if d != 'event':
            path = folder + d + '/'
            frames = os.listdir(path)
            for f in sorted(frames): #frame

                if 'launch' != f.split('.')[1] and 'csv' != f.split('.')[1] and 'video' not in f.split('.')[0]:
                    path_frames = path + f
                    print(path_frames)
                    for filename in glob.glob(path_frames):
                        im = Image.open(filename)
                        pix = list(im.getdata())
                        if set(pix) == {(0,0,0)}:
                            os.remove(path_frames)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    args = parser.parse_args()
    black_image(args.video)
    print('Info event')
    #ros_info(args.video)
   # main()

