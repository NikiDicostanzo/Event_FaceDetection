import argparse
import os


# rinominare, scalare i video e estrarre frames!
def create_frame(folder, size):
    path_video = folder + 'video/'
    dirs = os.listdir(path_video)
    for d in sorted(dirs):  # ciclo su video

        new_path = folder + 'video_cut/' + d.split('_')[0] + '/'
        if not os.path.exists(new_path):  # crea le cartelle dei frame
            os.makedirs(new_path)

        path_cut = new_path + d.split('_')[0] + '.' + d.split('.')[1]
        path = path_video + d

        print('Cut and scale video: ', d)
        os.system(
            "ffmpeg -i {0} -vf scale={2}:{2} -ss 00:00:01 -t 00:00:30 -async 1 -strict -2 {1}".format(path, path_cut,
                                                                                                      size))
        print('Extract frame: ', d)  # i frame li chiamo video#_##.png
        os.system("ffmpeg -i {0} -filter:v fps=fps=20 {1}/{2}_%14d.png".format(path_cut, new_path, d.split('_')[0]))


# rename video
def rename(folder):
    path_video = folder + 'video/'
    dirs = os.listdir(path_video)
    print(folder)
    count = 1
    for d in sorted(dirs):
        path = path_video + d
        if count < 10:  # video sono meno di 100
            print(folder + 'video0' + str(count) + '.' + d.split('.')[1])
            new_name = path_video + 'video0' + str(count) + '.' + d.split('.')[1]
        else:
            new_name = path_video + 'video' + str(count) + '.' + d.split('.')[1]
        print('rename video: ', d, 'in: ', new_name)
        os.rename(path, new_name)
        count += 1


def rename_event(folder):
    path = folder + 'event/'
    dirs_event = os.listdir(path)
    print('folder', dirs_event)
    for d in sorted(dirs_event):  # cartelle video#
        path_video = path + d + '/'
        print(path, 'd: ', d)
        path_frame = os.listdir(path_video)
        print('folder', path)
        for f in reversed(path_frame):  # cartelle frame, ciclo dall'ultimo
            print('Frame: ', f)
            n = f.split('.')[0]
            num = str(int(n[len(n) - 4:len(n)]) + 2)
            old_name = path_video + f
            new_name = path_video + d + '_' + n[len(n) - 4:len(n) - len(num)] + num + '.' + f.split('.')[1]

            print('new: ', new_name, 'old: ', old_name)
            os.rename(old_name, new_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--size", dest="size", default=768, help="Size of frames")
    args = parser.parse_args()
    print('Rename video')
    rename(args.video)
    create_frame(args.video, args.size)
