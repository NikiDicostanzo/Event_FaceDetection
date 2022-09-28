import argparse
import os

#tagliare i video e estrarre i frame rgb

def create_frame(folder):
    dirs = os.listdir(folder)
    #print(folder)
    count=1
    for d in sorted(dirs):
        new_path = folder + 'video' + str(count)
        if len(d.split('.'))> 1:
            new_name = new_path + '.' + d.split('.')[1]
            path_cut = new_path + '/video' + str(count) + '_cut.' + d.split('.')[1]
            path = folder + d

            if not os.path.exists(new_path):#crea le cartelle dei frame
               os.makedirs(new_path)

            print('Cut video: ',d)
            os.system("ffmpeg -i {0} -ss 00:00:00 -t 00:00:30 -async 1 -strict -2 {1}".format(path, path_cut))
            print('rename video: ',d,'in: ','video'+d.split('.')[1])

            os.rename(path, new_name)
            print('Extract frame: ', d)
            os.system("ffmpeg -i {0} -filter:v fps=fps=20 {1}/frames{2}_%010d.png".format(path_cut,new_path, count))
            count += 1

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


