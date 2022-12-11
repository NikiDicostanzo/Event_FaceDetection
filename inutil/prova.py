import argparse
import os
from face_ali import bounding_box
import csv
# tagliare i video e estrarre i frame rgb
import shutil
import cv2


def create_frame(folder):
    path_video = folder + 'video_scale/'
    dirs = os.listdir(path_video)
    # print(folder)
    #count = 1
    for d in sorted(dirs): # ciclo su video
        if d != 'a':
            new_path = folder + d.split('_')[0] + '/'
            #if len(d.split('.')) > 1:
            # new_name = new_path + '.' + d.split('.')[1]
            path_cut = new_path + d.split('_')[0] + '_cut.' + d.split('.')[1]
            path = path_video + d

            if not os.path.exists(new_path):  # crea le cartelle dei frame
                os.makedirs(new_path)

            print('Cut video: ', d)
            os.system("ffmpeg -i {0} -ss 00:00:01 -t 00:00:30 -async 1 -strict -2 {1}".format(path, path_cut))
            # print('rename video: ',d,'in: ','video'+d.split('.')[1])

            # os.rename(path, new_name)
            print('Extract frame: ', d)
            os.system("ffmpeg -i {0} -filter:v fps=fps=20 {1}/{2}_%14d.png".format(path_cut, new_path, d.split('_')[0]))

            print('Calculate bouding box: ', d)
            dirs_frame = os.listdir(new_path)

            csv_path = folder + 'bb/' + d.split('_')[0] + '.csv'  # devo salvarlo dentro event

            with open(csv_path, 'w') as csvfile:
                filewriter = csv.writer(csvfile)
                for f in sorted(dirs_frame):
                    if 'png' == f.split('.')[1]:
                        path_image = new_path + f
                        print('Frame: ', path_image)
                        bb = bounding_box(path_image)
                        print('Finish bb: ', bb)
                        path_image_save = 'event/' + d + '/' + f  # metto path macchina?
                        if bb == 'NoneType':
                            bb = -1
                        lines = [path_image_save, bb]
                        filewriter.writerow(lines)
            print('Remove frames:', d)
            shutil.rmtree(new_path) # elimino cartella con file rgb per problemi di spazio


# # Resize event frame    name: video70_0598
def scale_event(folder, dest):
    dirs = folder + 'event/'
    dirs_event = os.listdir(dirs)
    print('folder', dirs_event)

    for d in sorted(dirs_event):  # cartelle video#
        if d != 'rin':
            path = dirs + d
            print(path, 'd: ', d)
            path_frame = os.listdir(path)
            print('folder', path)
            #num_v = int(d[len(d)-2:len(d)])
            #if 1 < num_v < 10 :
                #print(d)
            for f in sorted(path_frame):  # cartelle frame#
                #la cartella event_scale la voglio fuori da event
                # new_folder = dest + d
                # if not os.path.exists(new_folder):  # crea le cartelle dei frame
                #     os.makedirs(new_folder)
                print('Frame: ', f)
                n = f.split('.')[0]
                if 'video' not in n:
                    num = str(int(n[len(n) - 4:len(n)]) + 2)
                    new_name = dest + d + '_' + n[len(n)-4:len(n)-len(num)] + num + '.' + f.split('.')[1]

                else:
                    new_name = dest + f
                frame = path + '/' + f
                print('new: ', new_name)
                img = cv2.imread(frame)
               # print('Frame: ', frame)
                img = cv2.resize(img, (768, 768), interpolation=cv2.INTER_NEAREST)
                cv2.imwrite(new_name, img)
            #     # dest = '/home/ndicostanzo/data/video_scale/'
            #     # os.system('mv {0} {1}'.format(name, dest))
            #


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--dest", dest="dest", default=None, help="Path of the video")
    args = parser.parse_args()
    scale_event(args.video, args.dest)

