### Recommended Directory Structure for preprocessing video
Dataset:
```
../folder/
    └── video
         ├──video01.mp4
         ├──video02.mp4
         └── ...   
 ```
note: non usare video con immagini nere/scritte!

## Run
(Andare al path: /home/ndicostanzo/vmr/)

(--video = /home/ndicostanzo/data/) 

Processare i video: 
```
python preprocessing.py --video 'folder'
```
Creare i file bag:
```
python create_bag.py --video 'folder' --ros 'path_folder_esim'
```
Dopo aver eseguito preprocessing.py e create_bag.py si ottiene: 
```
../folder/
     ├── video
     ├── video_cut
     └── event
```

split dataset:
```
python split_dataset.py --yolo 'path_folder_yolo' 
```
Creare annotazioni:
```
python annotation.py --video 'folder' --yolo 'path_folder_yolo' 
```
#### 
(-- path_yolo = /home/ndicostanzo/PyTorch-YOLOv3/pytorchyolo/)

Eseguire train:(andare al path path_yolo)
```
python train.py --d config/custom.data --pretrained_weights weights/darknet53.conv.74 -e 100 --n_cpu 1
```
Eseguire test.py:
```
python test.py -d config/custom.data -w checkpoints/yolov3_ckpt_82.pth --n_cpu 1 --img_size 768 
```
Inference:
```
python detect.py -i 'path_data' -w checkpoints_darknet/yolov3_ckpt_94.pth -c data/classes.names --img_size 768 --conf_thres 0.3
```
####
