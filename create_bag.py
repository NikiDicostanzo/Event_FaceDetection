import argparse
import os
import glob

path_ros = '/home/ninad/sim_ws/src/rpg_esim/event_camera_simulator/esim_ros'
#home\ninad\sim_ws\src\rpg_esim\event_camera_simulator\esim_ros\scripts
#folder = '/tmp/cheetah_example/esmi_frame!=/'
#folder = '/mnt/e/frame'

def create_csv(folder):
    dirs = os.listdir(folder)
    for d in dirs: #cartelle dei video
        path = folder + d + '/'
        os.system("python {0}/scripts/generate_stamps_file.py -i {1} -r 30.0".format(path_ros, path))

def create_bag(folder):
    dirs = os.listdir(folder)
    for d in dirs: #cartelle dei video
        path = folder + d #cartella ai frame
        print(path)
        #os.system("rostopic list")
        os.system("rosrun esim_ros esim_node --data_source=2 "
                  "--path_to_output_bag={0}/video.bag "
                  "--path_to_data_folder={0} "
                  "--ros_publisher_frame_rate=30 --exposure_time_ms=10.0 "
                  "--use_log_image=1 --log_eps=0.1 --contrast_threshold_pos=0.15 "
                  "--contrast_threshold_neg=0.15".format(path))

def create_lunch():
    f = open("demofile3.lunch", "w")
    f.write("<launch>"
            "<node pkg='rosbag' type='play' name='rosbag' required='true' args='/tmp/cheetah_example/out91.bag'/> "
            "<node name='extract' pkg='image_view' type='extract_images' respawn='false' required='true' output='screen' cwd='ROS_HOME'> "
            "<remap from='image' to='/dvs_rendering'/> "
            "<param name='sec_per_frame' value='0.1'/> </node> "
            "</launch> ")
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create event frame")
    parser.add_argument("--video", dest="video", default=None, help="Path of the video")
    args = parser.parse_args()
    #create_csv(args.video)
    #create_bag(args.video)
    create_lunch()

   # main()

