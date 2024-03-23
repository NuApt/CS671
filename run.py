# -*- coding: utf-8 -*-
"""SAM_CS671.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ITybPISi0AbKfZUqbstKI-QCTimB408T
"""

# !!pip install -q git+https://github.com/huggingface/transformers


import cv2 
from tensorflow import keras
from transformers import TFSamModel, SamProcessor
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.python.ops.numpy_ops import np_config
from PIL import Image
import requests
import glob
import os
import os
import glob
import cv2  # OpenCV
import numpy as np
import os
import csv


import os
import glob

# main_folder = os.path.join(main_folder, '/Iris_Segmentation/Iris_Segmentation/CASIA-V4-Lamp_mask_similar')

image_folder = 'Iris_Segmentation/Iris_Segmentation/CASIA-V4-Lamp_images_L_R_ALL'
mask_folder = 'Iris_Segmentation/Iris_Segmentation/CASIA-V4-Lamp_mask_similar'

# List to store masks and corresponding images
mask_list = []
image_list = []

# Get list of mask files
mask_files = glob.glob(os.path.join(mask_folder, '*.jpg'))  # Assuming masks are PNG files

# Iterate through mask files
i=0
for mask_file in mask_files:
    i+=1
    if(i==1501):
      break
    # Extract file name without extension
    mask_name = os.path.splitext(os.path.basename(mask_file))[0]

    # Search for corresponding image file
    image_file = os.path.join(image_folder, mask_name + '.jpg')  # Assuming images are JPEG files

    # Check if image file exists
    if os.path.exists(image_file):
        # Load mask and image as NumPy arrays
        mask = cv2.imread(mask_file,cv2.IMREAD_UNCHANGED)
        image = cv2.imread(image_file)

        binary_image =(np.mean(mask,axis=-1) > 128).astype(int)


        # Append mask and image arrays to lists
        mask_list.append(binary_image)
        image_list.append(image)

# Convert lists to NumPy arrays
mask_list = np.array(mask_list)
image_list = np.array(image_list)

# Print the shapes of arrays
print("Shape of Masks Array:", mask_list.shape)
print("Shape of Images Array:", image_list.shape)
with open("print.txt", mode = 'a', newline = "") as file:
        file.write("Shape of Masks Array:", mask_list.shape, "\n")
        file.write("Shape of Images Array:", image_list.shape, "\n")


model = TFSamModel.from_pretrained("facebook/sam-vit-base")
processor = SamProcessor.from_pretrained("facebook/sam-vit-base")

np_config.enable_numpy_behavior()


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)


def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(
        plt.Rectangle((x0, y0), w, h, edgecolor="green", facecolor=(0, 0, 0, 0), lw=2)
    )


def show_boxes_on_image(raw_image, boxes):
    plt.figure(figsize=(10, 10))
    plt.imshow(raw_image)
    for box in boxes:
        show_box(box, plt.gca())
    plt.axis("on")
    plt.show()


def show_points_on_image(raw_image, input_points, input_labels=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(raw_image)
    input_points = np.array(input_points)
    if input_labels is None:
        labels = np.ones_like(input_points[:, 0])
    else:
        labels = np.array(input_labels)
    show_points(input_points, labels, plt.gca())
    plt.axis("on")
    plt.show()


def show_points_and_boxes_on_image(raw_image, boxes, input_points, input_labels=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(raw_image)
    input_points = np.array(input_points)
    if input_labels is None:
        labels = np.ones_like(input_points[:, 0])
    else:
        labels = np.array(input_labels)
    show_points(input_points, labels, plt.gca())
    for box in boxes:
        show_box(box, plt.gca())
    plt.axis("on")
    plt.show()


def show_points_and_boxes_on_image(raw_image, boxes, input_points, input_labels=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(raw_image)
    input_points = np.array(input_points)
    if input_labels is None:
        labels = np.ones_like(input_points[:, 0])
    else:
        labels = np.array(input_labels)
    show_points(input_points, labels, plt.gca())
    for box in boxes:
        show_box(box, plt.gca())
    plt.axis("on")
    plt.show()


def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels == 1]
    neg_points = coords[labels == 0]
    ax.scatter(
        pos_points[:, 0],
        pos_points[:, 1],
        color="green",
        marker="*",
        s=marker_size,
        edgecolor="white",
        linewidth=1.25,
    )
    ax.scatter(
        neg_points[:, 0],
        neg_points[:, 1],
        color="red",
        marker="*",
        s=marker_size,
        edgecolor="white",
        linewidth=1.25,
    )


def show_masks_on_image(raw_image, masks, scores):
    if len(masks[0].shape) == 4:
        final_masks = tf.squeeze(masks[0])
    if scores.shape[0] == 1:
        final_scores = tf.squeeze(scores)

    nb_predictions = scores.shape[-1]
    fig, axes = plt.subplots(1, nb_predictions, figsize=(15, 15))

    for i, (mask, score) in enumerate(zip(final_masks, final_scores)):
        mask = tf.stop_gradient(mask)
        axes[i].imshow(np.array(raw_image))
        show_mask(mask, axes[i])
        axes[i].title.set_text(f"Mask {i+1}, Score: {score.numpy().item():.3f}")
        axes[i].axis("off")

    # Save the figure as img1.png
    plt.savefig("img1.png")
    # Close the figure to prevent it from being displayed
    plt.close()

image = image_list[112]
plt.imshow(image)
plt.show()

mask = mask_list[112]
plt.imshow(mask)
plt.show()

mask = mask_list[115]
plt.imshow(mask)
plt.show()

input_box = np.array([[200, 150, 500, 400]])

# Preprocess the input image.
inputs = processor(image, return_tensors="tf")

# Predict for segmentation with the prompt.
outputs = model(**inputs)

outputs.pred_masks.shape

masks = processor.image_processor.post_process_masks(
    outputs.pred_masks,
    inputs["original_sizes"],
    inputs["reshaped_input_sizes"],
    return_tensors="tf",
)

show_masks_on_image(image, masks, outputs.iou_scores)

masks[0].shape

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30 / 255, 144 / 255, 255 / 255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)

class Generator:
    """Generator class for processing the images and the masks for SAM fine-tuning."""

    def __init__(self, image_list, mask_list, processor):
        self.image_list = image_list
        self.mask_list = mask_list
        self.processor = processor

    def __call__(self):
        for image_, mask_ in zip(self.image_list, self.mask_list):
            image = image_
            ground_truth_mask = mask_

            # get bounding box prompt
            prompt = self.get_bounding_box(ground_truth_mask)

            # prepare image and prompt for the model
            inputs = self.processor(image, input_boxes=[[prompt]], return_tensors="np")

            # remove batch dimension which the processor adds by default
            inputs = {k: v.squeeze(0) for k, v in inputs.items()}

            # add ground truth segmentation
            inputs["ground_truth_mask"] = ground_truth_mask

            yield inputs

    def get_bounding_box(self, ground_truth_map):
        # get bounding box from mask
        y_indices, x_indices = np.where(ground_truth_map > 0)
        x_min, x_max = np.min(x_indices), np.max(x_indices)
        y_min, y_max = np.min(y_indices), np.max(y_indices)

        # add perturbation to bounding box coordinates
        H, W = ground_truth_map.shape
        x_min = max(0, x_min - np.random.randint(0, 20))
        x_max = min(W, x_max + np.random.randint(0, 20))
        y_min = max(0, y_min - np.random.randint(0, 20))
        y_max = min(H, y_max + np.random.randint(0, 20))
        bbox = [x_min, y_min, x_max, y_max]

        return bbox

# Define the output signature of the generator class.
output_signature = {
    "pixel_values": tf.TensorSpec(shape=(3, None, None), dtype=tf.float32),
    "original_sizes": tf.TensorSpec(shape=(None,), dtype=tf.int64),
    "reshaped_input_sizes": tf.TensorSpec(shape=(None,), dtype=tf.int64),
    "input_boxes": tf.TensorSpec(shape=(None, None), dtype=tf.float64),
    "ground_truth_mask": tf.TensorSpec(shape=(None, None), dtype=tf.int32),
}

# Prepare the dataset object.
train_dataset_gen = Generator(image_list[:1500], mask_list[:1500], processor)
train_ds = tf.data.Dataset.from_generator(
    train_dataset_gen, output_signature=output_signature
)

auto = tf.data.AUTOTUNE
batch_size = 2
shuffle_buffer = 4

train_ds = (
    train_ds.cache()
    .shuffle(shuffle_buffer)
    .batch(batch_size)
    .prefetch(buffer_size=auto)
)

train_ds

sample = next(iter(train_ds))
for k in sample:
    print(k, sample[k].shape, sample[k].dtype, isinstance(sample[k], tf.Tensor))

import tensorflow as tf

def dice_loss(y_true, y_pred, smooth=1e-5):
    y_pred = tf.sigmoid(y_pred)
    reduce_axis = list(range(2, len(y_pred.shape)))
    if batch_size > 1:
        # reducing spatial dimensions and batch
        reduce_axis = [0] + reduce_axis
    intersection = tf.reduce_sum(y_true * y_pred, axis=reduce_axis)
    y_true_sq = tf.math.pow(y_true, 2)
    y_pred_sq = tf.math.pow(y_pred, 2)

    ground_o = tf.reduce_sum(y_true_sq, axis=reduce_axis)
    pred_o = tf.reduce_sum(y_pred_sq, axis=reduce_axis)
    denominator = ground_o + pred_o
    # calculate DICE coefficient
    loss = 1.0 - (2.0 * intersection + 1e-5) / (denominator + 1e-5)
    loss = tf.reduce_mean(loss)
    return loss

def focal_loss(y_true, y_pred, alpha=0.25, gamma=2.0):
    """
    Focal loss for multi-class segmentation tasks.

    Args:
        y_true: Ground truth masks (one-hot encoded).
        y_pred: Predicted masks.
        alpha: Weighting factor for the rare class.
        gamma: Focusing parameter.

    Returns:
        Focal loss value.
    """
    y_pred = tf.clip_by_value(y_pred, 1e-7, 1.0 - 1e-7)  # Avoiding division by zero and numerical instabilities
    pt = tf.where(tf.equal(y_true, 1), y_pred, 1 - y_pred)  # Select predicted probabilities for true classes
    focal_loss =  -((alpha) * ((1-pt) ** gamma) * (y_true) * tf.math.log(pt))-((1 - alpha) * (pt ** gamma) * (1 - y_true) * tf.math.log(1 - pt)) # Compute focal loss
    return tf.reduce_mean(focal_loss)  # Return mean focal loss over all classes

# initialize SAM model and optimizer
sam = TFSamModel.from_pretrained("facebook/sam-vit-base")
optimizer = keras.optimizers.Adam(1e-5)

for layer in sam.layers:
    if layer.name in ["vision_encoder", "prompt_encoder"]:
        layer.trainable = False


@tf.function
def train_step(inputs):
    with tf.GradientTape() as tape:
        # pass inputs to SAM model
        outputs = sam(
            pixel_values=inputs["pixel_values"],
            input_boxes=inputs["input_boxes"],
            multimask_output=False,
            training=True,
        )
        predicted_masks = tf.squeeze(outputs.pred_masks, 1)
        predicted_masks = tf.transpose(predicted_masks, [0, 2, 3, 1])
        predicted_masks = tf.image.resize(
              predicted_masks,
              (480,640),
              method=tf.image.ResizeMethod.BILINEAR,
              preserve_aspect_ratio=False,
              antialias=False,
              name=None
          )
        predicted_masks = tf.transpose(predicted_masks, [0, 3, 1, 2])
        ground_truth_masks = tf.cast(inputs["ground_truth_mask"], tf.float32)

        # calculate loss over predicted and ground truth masks
        loss = focal_loss(tf.expand_dims(ground_truth_masks, 1), predicted_masks)
        # update trainable variables
        trainable_vars = sam.trainable_variables
        grads = tape.gradient(loss, trainable_vars)
        optimizer.apply_gradients(zip(grads, trainable_vars))

        return loss

# run training
for epoch in range(10):
    for inputs in train_ds:
        loss = train_step(inputs)
        with open("print.txt", mode = 'a', newline = "") as file:
            file.write()
    print(f"Epoch {epoch + 1}: Loss = {loss}")
    with open("print.txt", mode = 'a', newline = "") as file:
        file.write()

raw_image_inference = image_list[0]

# process the image and infer
preprocessed_img = processor(raw_image_inference)
outputs = sam(preprocessed_img)

masks = processor.image_processor.post_process_masks(
    outputs.pred_masks,
    preprocessed_img["original_sizes"],
    preprocessed_img["reshaped_input_sizes"],
    return_tensors="tf",
)

show_masks_on_image(image, masks, outputs.iou_scores)

outputs.pred_masks

