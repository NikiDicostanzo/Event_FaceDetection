import argparse
import os

def create_frame(folder):
    dirs = os.listdir(folder)
    for d in dirs:
        w = d.split('.')[0]
        w2 = w.split('_')[0]
        count = w2[len(w2)-2:len(w2)]
        path = folder + '/' + d
        os.system("ffmpeg -i {0} -filter:v fps=fps=24 /mnt/e/frame/frames{1}_%010d.png".format(path, count))
#ffmpeg -i {0} -filter:v fps=fps=24 /tmp/frames/frames{1}_%010d.png

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    args = parser.parse_args()
    create_frame(args.video)
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


