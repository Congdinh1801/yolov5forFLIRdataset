#  <div align="center">Tutorial to train YOLOv5 for FLIRdataset</div>

## Download FLIR dataset using the link below
https://www.kaggle.com/deepnewbie/flir-thermal-images-dataset

## Convert FLIR dataset to yolov5 format
Copy my createFLIR.py to your current dataset folder and run it to convert FLIR dataset to yolov5 format
```
python3 createFLIR.py
```

## Installation
```
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```

## Copy data.yaml and custom_yolov5s.yaml 
Edit my data.yaml where you need to change /home/user/ to whatever path you have on your local machine and put it in ./yolov5 

Copy my custom_yolov5s.yaml and put it in ./yolov5/models

## Train
Run the code below to start training YOLOv5 on FLIR dataset for 300 epochs using cuda device

Change /home/user/ to whatever path you have on your local machine
```
python3 train.py --img 640 --batch 16 --epochs 300 --data '/home/user/yolov5/data.yaml' --cfg /home/user/FLIRyolov5/yolov5/models/custom_yolov5s.yaml --weights '/home/user/yolov5/runs/train/yolov5s_results2/weights/best.pt' --name yolov5s_results  --cache --device 0 
```

## Contact
Feel free to contact me if you have any issue. 

## Reference
Link to the original YOLOv5 github https://github.com/ultralytics/yolov5

