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

def rename(folder):
    dirs = os.listdir(folder)
    # print(folder)
    count = 1
    for d in sorted(dirs):
        if d != '720':
            path = folder + d
            new_name = folder + 'video' + str(count) + '.' + d.split('.')[1]
            print('rename video: ', d, 'in: ', new_name)
            os.rename(path, new_name)
            count += 1


def cut_video(folder):
    path_video = folder + '/'
    dirs = os.listdir(path_video)
    # print(folder)
    new_path = folder + 'cut_video/'
    #count = 1
    if not os.path.exists(new_path):  # crea le cartelle dei frame
        os.makedirs(new_path)

    for d in sorted(dirs): # ciclo su video
        if d != 'a':
            #if len(d.split('.')) > 1:
            # new_name = new_path + '.' + d.split('.')[1]
            path_cut = new_path + d.split('_')[0] + '_cut.' + d.split('.')[1]
            path = path_video + d

            print('Cut video: ', d)
            os.system("ffmpeg -i {0} -ss 00:00:01 -t 00:00:30 -async 1 -strict -2 {1}".format(path, path_cut))
            # print('rename video: ',d,'in: ','video'+d.split('.')[1])
    print('Remove frames:', path_video)
    shutil.rmtree(path_video)  # elimino cartella con file rgb per problemi di spazio

# Resize video
def scale(folder):
    video_path = folder + 'cut/'
    dirs = os.listdir(video_path)
    print('folder', folder)
    for d in sorted(dirs):
        name = video_path + d
        print(name, 'd: ', d)
        new_name = folder + 'video_scale/' + d.split('.')[0] + '_scale.' + d.split('.')[1]
        print('new' , new_name)
        new_folder = folder + 'video_scale/'
        if not os.path.exists(new_folder):  # crea le cartelle dei frame
            os.makedirs(new_folder)
        os.system("ffmpeg -i {0} -vf scale=1280:720 -strict -2 {1}".format(name, new_name))

        #dest = '/home/ndicostanzo/data/video_scale/'
        #os.system('mv {0} {1}'.format(name, dest))

#r
# # Resize event frame    name: video70_0598
def scale_frame(folder , dest):
    dirs = folder + 'event/'
    dirs_event = os.listdir(dirs)
    print('folder', dirs_event)

    for d in sorted(dirs_event):  # cartelle video#
        path = dirs + d
        print(path, 'd: ', d)
        path_frame = os.listdir(path)
        print('folder', path)
        if d!= '720':
            for f in sorted(path_frame):  # cartelle frame#
                #la cartella event_scale la voglio fuori da event
                # new_folder = dest + d
                # if not os.path.exists(new_folder):  # crea le cartelle dei frame
                #     os.makedirs(new_folder)
                print('Frame: ', f)
                n = f.split('.')[0]
                num = str(int(n[len(n) - 4:len(n)]) + 2)  # il # parte da 0002 ( 1° frame rgb non c'è)
                new_name = dest + d + '_' + n[len(n)-4:len(n)-len(num)] + num + '.' + f.split('.')[1]
                print('new: ', new_name)

                frame = path + '/' + f
                img = cv2.imread(frame)
                print('Frame: ', frame)
                img = cv2.resize(img, (1280, 720), interpolation=cv2.INTER_NEAREST)
                cv2.imwrite(new_name, img)
                # dest = '/home/ndicostanzo/data/video_scale/'
                # os.system('mv {0} {1}'.format(name, dest))



if __name__ == '__main__':
    print('gggggg')
    # parser = argparse.ArgumentParser(description="Create event frame")
    # parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    # #parser.add_argument("--dest", dest="dest", default=None, help="Path of the video")
    # args = parser.parse_args()
    #create_frame(args.video)
    #scale_frame(args.video,args.dest)
    #scale(args.video)
    #cut_video(args.video)
    # rename(args.video)
# main()
#
#
# sp = False
# for d in dirs:
#         if d == 'video94.mp4':
#             sp = True
#         if sp == True:
#              path = '~/tmp/batch2/' + d
#              dest = '/tmp/batch2/rim'
#              #print(path)
#              os.system('mv path dest')
