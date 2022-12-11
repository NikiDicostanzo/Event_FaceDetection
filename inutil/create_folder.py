import argparse
import os
import glob

def create_frame(folder):
    dirs = os.listdir(folder)
    list = []
    for d in dirs: #prendo i numeri dei video
        d1 = d.split('_')[0]
        num = d1[len(d1)-2:len(d1)]
        if num.isdigit() and num not in list:
            list.append(num)
            print(num)
    for n in list:
        frame = folder+ '*'+ n + '_*.png'
        images = glob.glob(frame)
        for i in images:
            path = folder + 'video'+ n + '/'
            if not os.path.exists(path):
                os.makedirs(path)
                print('boh')
            os.system("mv {0} {1}".format(i, path))
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


