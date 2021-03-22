import json
import os
import shutil

import cv2
import numpy as np
import pandas as pd

# We are going to use PA, AP and AP Supine view, right now we are not interested in lateral x-ray
x_ray_view = ["PA", "AP", "AP Supine", "AP semi erect", "AP erect"]

actual_path = os.getcwd()
if not os.path.exists(os.path.join(actual_path, "covid-chestxray-dataset")):
  os.system("git clone https://github.com/ieee8023/covid-chestxray-dataset.git")
if not os.path.exists(os.path.join(actual_path, "covid-19-xray-dataset")):
  os.system("git clone https://github.com/v7labs/covid-19-xray-dataset.git")

v7dir = os.path.join(actual_path, "covid-19-xray-dataset")

v7imageszip = os.path.join(v7dir, "annotations/all-images.zip")
v7semanticzip = os.path.join(v7dir, "annotations/all-images-semantic-png.zip")
v7semanticdir = os.path.join(v7dir, "annotations/all-images-semantic-png")
v7imagespath = os.path.join(v7dir, "annotations/all-images")
shutil.unpack_archive(v7imageszip, v7imagespath)
shutil.unpack_archive(v7semanticzip, v7semanticdir)

cohendir = os.path.join(actual_path, "covid-chestxray-dataset")
metadata = os.path.join(cohendir, "metadata.csv")
imagedir = os.path.join(cohendir, "images")
outputdir = os.path.join(actual_path, "datasets/cohen")
v7semanticimages = os.path.join(v7semanticdir, "masks")
lungVAEmasksdir = os.path.join(cohendir, "annotations/lungVAE-masks")
manualmasksdir = os.path.join(cohendir, "annotations/manual_masks")

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

mask_dir = os.path.join(outputdir, "Masks")
if not os.path.isdir(mask_dir):
  os.makedirs(mask_dir)

# Open the v7labs JSON that contains information about the segmentation masks
v7labs_mask_dict = {}
for json_filename in os.listdir(v7imagespath):
  with open(os.path.join(v7imagespath, json_filename)) as json_file:
    data = json.load(json_file)
    v7labs_filename = os.path.splitext(json_filename)[0]
    cohen_filename = data["image"]["original_filename"]
    v7labs_mask_dict[cohen_filename] = v7labs_filename

metadata_csv = pd.read_csv(metadata)
for (i, row) in metadata_csv.iterrows():
  # Only use X-ray with PA (frontal) view
  if row["view"] not in x_ray_view:
    continue

  # Split the images by its finding
  fndg = row["finding"]
  if fndg == "todo":
    fndg = "Unknown"
  elif fndg == "No Finding":
    fndg = "Normal"

  filename = row["filename"].split(os.path.sep)[-1]
  image_path = os.path.sep.join([imagedir, filename])

  # Check if destination folder exists, if not create it
  dest_dir = os.path.join(outputdir, fndg)
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  # Copy image
  shutil.copy2(image_path, dest_dir)

  # Rename the file to a more representative name
  pid = row["patientid"]
  offset = row["offset"]

  try:
    offset = int(offset)
  except:
    offset = 0

  ext = os.path.splitext(filename)[1]
  new_filename = "P" + str(pid) + "_" + str(offset)
  new_filename_ext = "P" + str(pid) + "_" + str(offset) + ext
  old_file = os.path.join(dest_dir, filename)
  new_file = os.path.join(dest_dir, new_filename_ext)
  os.rename(old_file, new_file)

  # Check if there are any mask provided for this image
  # First, lets check the v7labs mask
  if filename in v7labs_mask_dict:
    mask_filename = v7labs_mask_dict[filename] + ".png"
    mask_filepath = os.path.join(v7semanticimages, mask_filename)
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)

    # Remove the mask with pixels containing 127
    img = cv2.imread(new_file, 0)
    img = np.uint8(img == 255) * 255
    cv2.imwrite(new_file, img)
    continue

  # Then, check the VAE provided masks
  mask_filename = os.path.splitext(filename)[0] + "_mask.png"
  mask_filepath = os.path.join(lungVAEmasksdir, mask_filename)
  if os.path.exists(mask_filepath):
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)
    continue

  # Finally, check for cohen manually created masks
  mask_filename = os.path.splitext(filename)[0] + "_mask.png"
  mask_filepath = os.path.join(manualmasksdir, mask_filename)
  if os.path.exists(mask_filepath):
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename + ".png")
    os.rename(old_file, new_file)
    continue
shutil.rmtree(cohendir)
shutil.rmtree(v7dir)
