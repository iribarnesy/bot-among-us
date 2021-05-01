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