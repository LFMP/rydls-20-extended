import os
import re
import shutil

import pandas as pd

# I'm assuming that this repo does not contain repeated images from Cohen

actual_path = os.getcwd()
if not os.path.exists(
    os.path.join(actual_path, "Figure1-COVID-chestxray-dataset")):
  os.system(
      "git clone https://github.com/agchung/Figure1-COVID-chestxray-dataset.git"
  )
metadata = os.path.join(actual_path,
                        "Figure1-COVID-chestxray-dataset/metadata.csv")
imagedir = os.path.join(actual_path, "Figure1-COVID-chestxray-dataset/images")
outputdir = os.path.join(actual_path, "datasets/Figure1")

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

mask_dir = os.path.join(outputdir, "Masks")
if not os.path.isdir(mask_dir):
  os.makedirs(mask_dir)

# Check if destination folder exists, if not create it
dest_dir = os.path.join(outputdir, "COVID-19")
if not os.path.isdir(dest_dir):
  os.makedirs(dest_dir)

metadata_csv = pd.read_csv(metadata, encoding='ISO-8859-1')

for (i, row) in metadata_csv.iterrows():

  if row["finding"] != "COVID-19":
    continue

  filename = row["patientid"]

  if os.path.isfile(os.path.join(imagedir, filename + ".png")):
    ext = ".png"
  else:
    ext = ".jpg"

  image_path = os.path.join(imagedir, filename + ext)

  # Copy image
  shutil.copy2(image_path, dest_dir)

  _, pid = re.split("-", row["patientid"])
  offset = row["offset"]

  try:
    offset = int(offset)
  except:
    offset = 0

  new_filename_ext = "figure1-P" + str(pid) + "_" + str(offset)
  old_file = os.path.join(dest_dir, filename + ext)
  new_file = os.path.join(dest_dir, new_filename_ext + ext)
  if os.path.exists(new_file):
    os.remove(new_file)

  # Check if there are any mask provided for this image
  mask_filename = filename + ".png"
  mask_filepath = os.path.join("Masks", mask_filename)
  if os.path.exists(mask_filepath):
    shutil.copy2(mask_filepath, mask_dir)
    old_file = os.path.join(mask_dir, mask_filename)
    new_file = os.path.join(mask_dir, new_filename_ext + ".png")
    os.rename(old_file, new_file)
shutil.rmtree(os.path.join(actual_path, "Figure1-COVID-chestxray-dataset"))
