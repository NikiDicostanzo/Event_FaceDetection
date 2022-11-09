import argparse
import os

# /video01_0002.png
# /video01_0000.png
#  ...
# /video1_0600.png
# /video02_0002.png
# ...
# /video70_0600.png

def create_txt(fol_event, fol_yolo):
    train, test, val = split(fol_event)
    dirs = os.listdir(fol_yolo) #/YOLO../.. /images/..
    for d in sorted(dirs):  # cartelle dei video
        path = fol_yolo + d # path_image
        #dirs_im = os.listdir(path)
        if d.split('_') in train: # h
            print('image: ', d)

        #if

#val: 10%, train: 60%, test : 30%
def split(folder):
    path_video = folder #+ 'images/'
    dirs = os.listdir(path_video)

    len_train = round((60 * 30129) / 100)
    len_val = round((10 * 30129) / 100)
    len_test = 30129 - (len_val + len_train)

    #train = dirs[:len_train]
    #val = dirs[len_train: len_train + len_val]
    #test = dirs[len_train + len_val :]
    # print(folder)
    # count = 1
    sum = 0
    sum_val = 0
    print('train: ', len_train, 'val: ', len_val, 'test: ', len_test)
    train = []
    val = []
    test = []
    for d in sorted(dirs):  # ciclo su frame -> YOLO... /images
        path = folder + d

        dirs1 = os.listdir(path)
        #print(d, 'len:', len(dirs1))
        sum = sum + len(dirs1)

        if sum <= len_train  :
            #print('Train', d, 'len:', len(dirs1), sum)
            train.append(d)
        elif len_train < sum < len_train + len_val:
            sum_val = sum_val + len(dirs1)
            val.append(d)
            #print('Val', d, 'len:', len(dirs1), sum_val)
        else:
            test.append(d)

    print(sum, '\n')
    print('test: ', test)
    print('train: ', train)
    print('val: ', val)
    return train, test, val
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--dest", dest="dest", default=None, help="Path of the video")

    args = parser.parse_args()
    print('Video: ', args.video)
    create_txt(args.video, args.dest)

#capire quanti sono i video da - di 600 frame