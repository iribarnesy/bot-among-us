# Among Us Bot
## Requirements

- Python3
- Tesseract
- OpenCV
- Numpy
- PyAutoGUI
- Among Us (Steam)
- FFMPEG
- shapely (install with conda)

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
git clone https://github.com/tensorflow/models.git tensorflow_models
cd tensorflow_models/research/
protoc object_detection/protos/*.proto --python_out=.
cp object_detection/packages/tf2/setup.py .
python -m pip install -U .
```

If the last command exit with error please try to run `python -m pip install --user .`

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

If you have some errors due to matplotlib or opencv please uninstall and reinstall the packages

```bash
pip uninstall opencv-python matplotlib
pip install opencv-python matplotlib
```
## Download Text Summarization model.

Copy the model (download it from [the google drive folder](A changer !!)) to a new models/ folder at the root of the project. It should be as below :

```bash
models/
└───A changer /
    ├───config.json
    └───pytorch_model.bin
```

## Add dependencies to make the bot speak

First install the python dependencies with `pip install -r requirements.txt` (if not done before)

Then, it's necessary to have ffmpeg installed, just run `ffmpeg` in shell to verify it. If you have not, you can [download ffmpeg for windows](https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-05-05-12-34/ffmpeg-n4.4-10-g75c3969292-win64-gpl-4.4.zip) and add it to your PATH.

Finally you have to add some secrets to a `.env` file at the root of the project.

```bash
DISCORD_TOKEN = <DISCORD_TOKEN>
GUILD = <GUILD>
CHANNEL = <CHANNEL>
TEXT_CHANNEL_ID = <TEXT_CHANNEL_ID>
VOICE_CHANNEL_ID = <VOICE_CHANNEL_ID>
```

Then you can instantiate the bot and make him say something. It will connect to the discord server/guild, join the "among" channel and speak.

```python
from src.bot import Bot
bot = Bot()
bot.discord_bot.say("something")
```