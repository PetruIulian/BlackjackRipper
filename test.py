from ultralytics import YOLO

# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8s_playing_cards.pt")  # load a pretrained model (recommended for training)

# Use the model
results = model.train(data="data.yaml", epochs=1)  # train the model
results = model.val()  # evaluate model performance on the validation set
# results = model("files/screenshot.png")  # predict on an image
#success = YOLO("yolov8n.pt").export(format="onnx")  # export a model to ONNX format
print([x for x in results])