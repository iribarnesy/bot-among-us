import os
import random
import time
import io
import scipy.misc
import numpy as np
import copy
import csv
import pathlib
import matplotlib
import matplotlib.pyplot as plt
from six import BytesIO
from PIL import Image
from tqdm import tqdm

import tensorflow as tf

from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder


ROOT_FOLDER = "."
DATA_FOLDER = f"{ROOT_FOLDER}/src/players_recognition"
train_image_dir = f"{DATA_FOLDER}/positive_small"
test_image_dir = train_image_dir
annotation_file = "full-pos.txt"
annotation_file_path = f"{DATA_FOLDER}/{annotation_file}"

MODEL_PATH = f"{ROOT_FOLDER}/models/all_boxes_model_40_batches"
MODEL_CHECKPOINT_PATH = f"{MODEL_PATH}/ckpt-1-1"

MIN_SCORE_THRESHOLD = 0.6
label_id_offset = 1
category_index = {1: {'id': 1, 'name': 'player'}}

plt.rcParams['axes.grid'] = False
plt.rcParams['xtick.labelsize'] = False
plt.rcParams['ytick.labelsize'] = False
plt.rcParams['xtick.top'] = False
plt.rcParams['xtick.bottom'] = False
plt.rcParams['ytick.left'] = False
plt.rcParams['ytick.right'] = False
plt.rcParams['figure.figsize'] = [14, 7]


class PlayersDetector:
  def __init__(self, checkpoint_path=MODEL_CHECKPOINT_PATH):
    self.detection_model = None
    self.load_model(checkpoint_path)

  def load_model(self, checkpoint_path):
    tf.keras.backend.clear_session()

    print('Building model and restoring weights for fine-tuning...', flush=True)
    num_classes = 1
    pipeline_config = f"{MODEL_PATH}/ssd_resnet50_v1_fpn_640x640_coco17_tpu-8.config"

    # Load pipeline config and build a detection model.
    configs = config_util.get_configs_from_pipeline_file(pipeline_config)
    model_config = configs['model']
    model_config.ssd.num_classes = num_classes
    model_config.ssd.freeze_batchnorm = True
    detection_model = model_builder.build(
          model_config=model_config, is_training=False)

    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
    ckpt.restore(checkpoint_path).expect_partial()

    # Run model through a dummy image so that variables are created
    image, shapes = detection_model.preprocess(tf.zeros([1, 640, 640, 3]))
    prediction_dict = detection_model.predict(image, shapes)
    _ = detection_model.postprocess(prediction_dict, shapes)
    print('Weights restored!')
    self.detection_model = detection_model
    return detection_model

  @tf.function
  def detect(self, input_tensor):
    """Run detection on an input image.

    Args:
      input_tensor: A [1, height, width, 3] Tensor of type tf.float32.
        Note that height and width can be anything since the image will be
        immediately resized according to the needs of the model within this
        function.

    Returns:
      A dict containing 3 Tensors (`detection_boxes`, `detection_classes`,
        and `detection_scores`).
    """
    preprocessed_image, shapes = self.detection_model.preprocess(input_tensor)
    prediction_dict = self.detection_model.predict(preprocessed_image, shapes)
    return self.detection_model.postprocess(prediction_dict, shapes)

  def detect_from_np_array(self, img_np):
    if len(img_np.shape) == 3:
      img_np = np.expand_dims(img_np, axis=0)
    input_tensor = tf.convert_to_tensor(img_np, dtype=tf.float32)
    return self.detect(input_tensor)
  
  # Note that the first frame will trigger tracing of the tf.function, which will
  # take some time, after which inference should be fast.

    
  def detect_and_plot(self, images_np, image_index_offset=0):
    """ Detect players in 6 images given in parameters.
    You can pass more than 6 images and precise an offset.
    """
    plt.figure(figsize=(30, 15))

    nb_images_to_plot = 6
    for i in tqdm(range(nb_images_to_plot)):
      idx = i + image_index_offset
      detections = self.detect_from_np_array(images_np[idx])
      plt.subplot(2, 3, i+1)
      plot_prediction(images_np[idx], detections)
    plt.show()

# Utils functions but hard-coded for this class
    
def load_image_into_numpy_array(path):
  """Load an image from file into a numpy array.

  Puts image into numpy array to feed into tensorflow graph.
  Note that by convention we put it into a numpy array with shape
  (height, width, channels), where channels=3 for RGB.

  Args:
    path: a file path.

  Returns:
    uint8 numpy array with shape (img_height, img_width, 3)
  """
  img_data = tf.io.gfile.GFile(path, 'rb').read()
  image = Image.open(BytesIO(img_data))
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def plot_detections(image_np,
                    boxes,
                    classes,
                    scores,
                    category_index,
                    figsize=(12, 16),
                    image_name=None,
                    min_score_thresh=MIN_SCORE_THRESHOLD):
  """Wrapper function to visualize detections.

  Args:
    image_np: uint8 numpy array with shape (img_height, img_width, 3)
    boxes: a numpy array of shape [N, 4]
    classes: a numpy array of shape [N]. Note that class indices are 1-based,
      and match the keys in the label map.
    scores: a numpy array of shape [N] or None.  If scores=None, then
      this function assumes that the boxes to be plotted are groundtruth
      boxes and plot all boxes as black with no classes or scores.
    category_index: a dict containing category dictionaries (each holding
      category index `id` and category name `name`) keyed by category indices.
    figsize: size for the figure.
    image_name: a name for the image file.
  """
  if len(image_np.shape) == 4:
    image_np = image_np[0]
  image_np_with_annotations = image_np.copy()
  viz_utils.visualize_boxes_and_labels_on_image_array(
      image_np_with_annotations,
      boxes,
      classes,
      scores,
      category_index,
      use_normalized_coordinates=True,
      min_score_thresh=min_score_thresh)
  if image_name:
        plt.imsave(image_name, image_np_with_annotations)
  else:
        plt.imshow(image_np_with_annotations)

def plot_prediction(image_np, predictions):
      plot_detections(
      image_np,
      predictions['detection_boxes'][0].numpy(),
      predictions['detection_classes'][0].numpy().astype(np.uint32)
      + label_id_offset,
      predictions['detection_scores'][0].numpy(),
      # image_name="gif_frame_" + ('%02d' % i) + ".jpg",
      category_index, figsize=(15, 20))

def get_annotations_from_file(annotation_file_path):
  def get_box(row, index):
    """ a row is as below :
      image_path nb_boxes x1 y1 w1 h1 x2 y2 w2 h2...
    """
    xmin, ymin = int(row[index*4 + 2]), int(row[index*4 + 3])
    xmax, ymax = xmin + int(row[index*4 + 4]), ymin + int(row[index*4 + 5])
    xmin, ymin, xmax, ymax = xmin / 1920, ymin / 1080, xmax / 1920, ymax / 1080
    return [ymin, xmin, ymax, xmax]

  gt_boxes = []
  img_paths = []
  with open(annotation_file_path) as annot_csv_file:
      csv_reader = csv.reader(annot_csv_file, delimiter=' ')
      line_count = 0
      for row in csv_reader:
        img_path = row[0].split('\\')[1]
        img_path = f"{train_image_dir}/{img_path}"
        nb_boxes = int(row[1])
        img_paths.append(img_path)
        boxes = np.array([get_box(row, i_box) for i_box in range(nb_boxes)], dtype=np.float32)
        gt_boxes.append(boxes)
        # print(f"img:{img_path}, nb_boxes:{nb_boxes}, boxes:{boxes}")
        line_count += 1
      print(f'Processed {line_count} lines.')
  return img_paths, gt_boxes

def load_images_from_folder(img_dir, subset):
  img_np = []
  for filename in tqdm(os.listdir(img_dir)):
    img_path = os.path.join(img_dir +"/"+ filename)
    if subset == 'test':
      img_np.append(np.expand_dims(
          load_image_into_numpy_array(img_path), axis=0))
    elif subset == 'train':
          img_np.append(np.expand_dims(
          load_image_into_numpy_array(img_path), axis=0))
  print(f"Loaded {len(img_np)} images for {subset}")
  return img_np


def plot_annotations(images_np, gt_boxes):
  plt.figure(figsize=(30, 15))
  for idx in range(6):
    plt.subplot(2, 3, idx+1)
    plot_detections(
        images_np[idx],
        gt_boxes[idx],
        np.ones(shape=[gt_boxes[idx].shape[0]], dtype=np.int32),
        np.ones(shape=[gt_boxes[idx].shape[0]], dtype=np.float32), 
        category_index)
  plt.show()


# Main function to demonstrate how to use the model

def main():
  matplotlib.use('tkagg')
  img_paths, gt_boxes = get_annotations_from_file(annotation_file_path)

  test_images_np = []
  for img_path in tqdm(img_paths[:10]):
    test_images_np.append(np.expand_dims(
          load_image_into_numpy_array(img_path), axis=0))
          
  # train_images_np = load_images_from_folder(train_image_dir, 'train')
  # test_images_np = load_images_from_folder(test_image_dir, 'test')
  plot_annotations(test_images_np, gt_boxes)

  detect_model = PlayersDetector()
  detect_model.detect_and_plot(test_images_np, image_index_offset=0)


if __name__ == '__main__':
  main()