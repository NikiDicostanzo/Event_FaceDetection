## Recommended Directory Structure for preprocessing video
### Dataset: 
Es. folder = */home/ndicostanzo/data/*
```
../folder/
    └── video
         ├──video01.mp4
         ├──video02.mp4
         └── ...   
 ```
note: non usare video con immagini nere/scritte!

## Run
Andare al path: */home/ndicostanzo/vmr/*

### Processare i video: 
Es. *folder = /home/ndicostanzo/data/*
```
python preprocessing.py --video 'folder'
```
### Creare i file bag: 
Es. path_folder_esim = *'/home/ninad/sim_ws/src/rpg_esim/event_camera_simulator/esim_ros'*
```
python create_bag.py --video 'folder' --ros 'path_folder_esim'
```
Dopo aver eseguito **preprocessing.py** e **create_bag.py** si ottiene: 
```
../folder/
     ├── video
     ├── video_cut
     └── event
```
### Split dataset:
Es. *-- path_yolo = /home/ndicostanzo/PyTorch-YOLOv3/pytorchyolo/*
```
python split_dataset.py --yolo 'path_yolo' 
```
### Creare annotazioni:
```
python annotation.py --video 'folder' --yolo 'path_yolo' 
```
## PyTorch-YOLOv3
Andare al path *"path_yolo"*
### Eseguire train: 
```
python train.py --d config/custom.data --pretrained_weights weights/darknet53.conv.74 -e 100 --n_cpu 1
```
### Eseguire test.py:
```
python test.py -d config/custom.data -w checkpoints/yolov3_ckpt_82.pth --n_cpu 1 --img_size 768 
```
### Inference: 
Es. path_data = */home/ndicostanzo/data/vr/event/video01/*
```
python detect.py -i 'path_data' -w checkpoints/yolov3_ckpt_82.pth -c data/classes.names --img_size 768 --conf_thres 0.3
```
Nota: l'output viene salvato al path : */home/ndicostanzo/PyTorch-YOLOv3/pytorchyolo/output/*
