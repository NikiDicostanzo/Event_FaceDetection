import argparse
import os
from preprocessing import rename_event
#simulatore esim
#path_ros = '/home/ninad/sim_ws/src/rpg_esim/event_camera_simulator/esim_ros'


def create_csv(folder, path_ros):
    fol = folder + 'image/'
    dirs = os.listdir(fol)
    for d in sorted(dirs):
        path = fol + d + '/'
        os.system("python {0}/scripts/generate_stamps_file.py -i {1} -r 20.0".format(path_ros, path))


def create_bag(folder):
    fol = folder + 'image/'
    dirs = os.listdir(fol)
    for d in sorted(dirs): #cartelle con cartelle dei frame
        path = fol + d #cartella ai frame
        print(path)
        os.system("rosrun esim_ros esim_node --data_source=2 "
                  "--path_to_output_bag={0}/video.bag "
                  "--path_to_data_folder={0} "
                  "--ros_publisher_frame_rate=60 --exposure_time_ms=10.0 "
                  "--use_log_image=1 --log_eps=0.1 --contrast_threshold_pos=0.15 "
                  "--contrast_threshold_neg=0.15".format(path))


def create_lunch(folder):
    fol = folder + 'image/'
    dirs = os.listdir(fol)
    for d in sorted(dirs):  # cartelle dei video
        path = fol + d
        print(path)
        path_file = path + "/file.launch"
        f = open(path_file, "w")
        f.write("<launch> \n"
                "   <node pkg='rosbag' type='play' name='rosbag' required='true' args='--rate=0.1 {0}/video.bag'/> \n"
                "   <node name='extract' pkg='image_view' type='extract_images' respawn='false' required='true' output='screen' cwd='ROS_HOME'> \n"
                "   <remap from='image' to='/dvs_rendering'/> \n"
                "   <param name='sec_per_frame' value='0.02'/></node> \n"
                "</launch> ".format(path))    #0.02 per estrarre 20 fps
        f.close()


def extract_event(folder):
    fol = folder + 'image/'
    dirs = os.listdir(fol)
    path_event = folder + 'event/'
    for d in sorted(dirs):  # cartelle di carelle
        path = fol + d
        os.system("roslaunch {0}/file.launch".format(path))
        print('p :', path)
        new_path = path_event + d
        if not os.path.exists(new_path):  # crea le cartelle dei frame
            os.makedirs(new_path)
        os.system('mv ~/.ros/frame*.jpg {0}'.format(new_path))
    rename_event(path_event)  # rinomino i frame0002 in poi


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    parser.add_argument("--ros", dest="path_ros", default=None, help="Path of esim_ros")
    args = parser.parse_args()
    print('Video: ', args.video)
    print('Create csv')
    create_csv(args.video, args.path_ros)
    print('Create bag')
    create_bag(args.video)
    print('Create file lunch')
    create_lunch(args.video)
    print('Extract event')
    extract_event(args.video)