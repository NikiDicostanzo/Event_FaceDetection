import argparse
import os

# /video01_0002.png
# /video01_0000.png
#  ...
# /video1_0600.png
# /video02_0002.png
# ...
# /video70_0600.png


def create_txt(fol_event, fol_yolo, split_val, split_train):
    train, test, val = split(fol_event, split_val, split_train)

    im = fol_yolo + 'images/'
    dirs = os.listdir(im)  #/YOLO../.. /images/..
    name1 = fol_yolo + 'train.txt'
    name2 = fol_yolo + 'valid.txt'
    name3 = fol_yolo + 'test.txt'

    write_file(name1, dirs, train)
    write_file(name2, dirs, val)
    write_file(name3, dirs, test)


def write_file(name, dirs, data):
    with open(name, 'w') as f:
        for d in sorted(dirs):  # cartelle dei video
            path = 'data/custom/images/' + d  # path_image
            if d.split('_')[0] in data:  # h
                #print(name, d)
                f.writelines(path)
                f.write('\n')


#val: 10%, train: 60%, test : 30%
def split(folder, split_val, split_train):
    path_images = folder + 'images/'
    dirs = os.listdir(path_images)
    num = len(dirs)
    print(split_train, split_val)
    len_train = round((split_train * num) / 100)
    len_val = round((split_val * num) / 100)
    len_test = num - (len_val + len_train)
    print('train: ', len_train, 'val: ', len_val, 'test: ', len_test)

    fold_video = []
    count_a = []
    count = 0
    for d in sorted(dirs):  # ciclo su frame -> YOLO... /images
       # print(d)
        if d.split('_')[0] not in fold_video:  # salvo il nome dei video che ho
            if count > 0: #metto il count precedente
                count_a.append(count)
            fold_video.append(d.split('_')[0])
            count = 0
        else:
            count += 1
    count_a.append(count)  # ultimo altrimenti non si salva
    print(count_a)
    index_train = 0
    index_val = 0
    tol = num / 100
    for d in count_a:  # conta da 0_ vorrei che immaggini dello stesso video stanno insieme
        if index_train + d <= len_train + tol:
            index_train = index_train + d
            index_val = index_train
        elif len_train < index_val + d <= len_val + len_train + tol:
            index_val = index_val + d
    print('Tol: ',tol)

    if index_train == 0 or index_val == index_train:
        # 60:100 = x : len(dirs)
        index_train = round((len(dirs) * split_train)/100)
        index_val = round((len(dirs) * split_val) / 100) + index_train  # prima ci sono quelli del train, va in ordine
    dirs = sorted(dirs)

    train = dirs[:index_train]
    val = dirs[index_train: index_val]
    test = dirs[index_val:]

    print('test: ', len(test))
    print('train: ', len(train))
    print('val: ', len(val))
    return train, test, val


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--dest", dest="dest", default=None, help="Path of the video")
    parser.add_argument("--val", dest="split_val", default=10, help="Split dataset")
    parser.add_argument("--train", dest="split_train", default=60, help="Split dataset")
    args = parser.parse_args()
    print('Video: ', args.video)
    create_txt(args.video, args.dest, args.split_val, args.split_train)
