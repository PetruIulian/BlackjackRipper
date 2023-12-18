from ultralytics import YOLO
from clearml import Task
from ultralytics.utils.plotting import Annotator
import cv2

#task = Task.init(project_name='My Project', task_name='My Experiment')
# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
def start_ai():
    model = YOLO("best.pt")  # load a pretrained model (recommended for training)

    # Use the model
    #results = model.train(data="data.yaml", epochs=1)  # train the model
    #results = model.val()  # evaluate model performance on the validation set
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        _, img = cap.read()
        
        # BGR to RGB conversion is performed under the hood
        # see: https://github.com/ultralytics/ultralytics/issues/2575
        results = model.predict(img)

        for r in results:
            
            annotator = Annotator(img)
            
            boxes = r.boxes
            for box in boxes:
                
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)])
            
        img = annotator.result()  
        return img
    