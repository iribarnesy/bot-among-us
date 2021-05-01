# Among Us Bot
## Requirements

- Python3
- Tesseract
- OpenCV
- Numpy
- PyAutoGUI
- Among Us (Steam)

## Execute

To run, use the command ``` python bot.py``` and use the menu to do your desired function!

## Google Cloud Vision

You must have the key JSON file placed in th environments/ folder.
Then you must declare the GOOGLE_APPLICATION_CREDENTIALS as the path of the key file.
You can do it by running the first cell of the notebook.

## Download OpenCV 3.4 for image annotation

[Download link](https://sourceforge.net/projects/opencvlibrary/files/3.4.14/opencv-3.4.14-vc14_vc15.exe/download)

## Download Object Detection API

You must have `protoc` installed locally. Follow this link to install [protoc-3.15.8-win64](https://github.com/protocolbuffers/protobuf/releases/download/v3.15.8/protoc-3.15.8-win64.zip). The `protoc` command should work then, if not please verify that the binary is in your path (Add the bin/ folder to your PATH, go to environment variables in Windows).

Then, execute these commands:

```bash
cd models/research/
protoc object_detection/protos/*.proto --python_out=.
cp object_detection/packages/tf2/setup.py .
python -m pip install -U .
```

You can then run `python object_detection/builders/model_builder_tf2_test.py` to verify that the installation is fine.

Copy the model (download it from [the google drive folder](https://drive.google.com/drive/u/1/folders/1-JZd1OF8aOJ08qXstt6wx8AOytp1LtSM)) to a new models/ folder at the root of the project. It should be as below :

```bash
models/
└───all_boxes_model_40_batches/
    ├───assets/
    ├───variables/
    ├───checkpoint
    ├───ckpt-1-1.data-00000-of-00001
    ├───ckpt-1-1.index
    ├───saved_model.pb
    └───ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.config
```

Then, you can run `python src/players_recognition/main.py` to vizualize the players detection loop.