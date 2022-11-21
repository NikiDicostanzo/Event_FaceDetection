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

    im = fol_yolo + 'images/'
    dirs = os.listdir(im)  #/YOLO../.. /images/..
    name = fol_yolo + 'valid.txt'
    with open(name, 'w') as f:
        for d in sorted(dirs):  # cartelle dei video
            path = 'data/custom/images/' + d  # path_image
            if d.split('_')[0] in val:  # h
                print('Scrive,', d)
                f.writelines(path)
                f.write('\n')


#val: 10%, train: 60%, test : 30%
def split(folder):
    path_images = folder #+ 'images/'
    dirs = os.listdir(path_images)
    num = len(dirs)
    len_train = round((60 * num) / 100)
    len_val = round((10 * num) / 100)
    len_test = num - (len_val + len_train)

    # print(folder)
    # count = 1
    sum = 0
    sum_val = 0
    print('train: ', len_train, 'val: ', len_val, 'test: ', len_test)
    train = []
    val = []
    test = []
    fold_video = []
    count_a = []
    count = 0
    for d in sorted(dirs):  # ciclo su frame -> YOLO... /images
        if d.split('_')[0] not in fold_video: # salvo il nome dei video che ho
            if count > 0:
                count_a.append(count)
            fold_video.append(d.split('_')[0])
            count = 0
        else:
            count += 1
    count_a.append(count) # ultimo altrimenti non si salva
    index_train = 0
    index_val = 0
    sum = 0
    for d in count_a:
        if index_train + d <= len_train :
            index_train = index_train + d
            index_val = index_train
        elif len_train < index_val + d <= len_val + len_train:
            index_val = index_val + d


    dirs = sorted(dirs)
    train = dirs[:index_train]
    val = dirs[index_train + 1: index_val]
    test = dirs[index_val + 1:]

    #
    # for v in range(len(dirs)):
    #     imm = dirs[v]
    #     if v <= index_train:
    #         train.append(imm)
    #     elif index_train < v <= index_val:
    #         val.append(imm)
    #     else:
    #         test.append(imm)
    # print(sum, '\n')
    print('test: ', len(test))
    print('train: ', len(train))
    print('val: ', len(val))
    return train, test, val
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--dest", dest="dest", default=None, help="Path of the video")

    args = parser.parse_args()
    print('Video: ', args.video)
    split(args.video)#, args.dest)

#capire quanti sono i video da - di 600 frame