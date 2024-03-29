import os
import shutil

import pandas as pd

# I'm assuming that this repo does not contain repeated images from Cohen


def build(actual_path):
  if not os.path.exists(
      os.path.join(actual_path, "Actualmed-COVID-chestxray-dataset")):
    os.system(
        "git clone https://github.com/agchung/Actualmed-COVID-chestxray-dataset.git"
    )
  metadata = os.path.join(actual_path,
                          "Actualmed-COVID-chestxray-dataset/metadata.csv")
  imagedir = os.path.join(actual_path,
                          "Actualmed-COVID-chestxray-dataset/images")
  outputdir = os.path.join(actual_path, "datasets/Actualmed")

  # Remove output dir if present
  if os.path.isdir(outputdir):
    shutil.rmtree(outputdir)

  # Check if destination folder exists, if not create it
  dest_dir = os.path.join(outputdir, "COVID-19")
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  mask_dir = os.path.join(outputdir, "Masks")
  if not os.path.isdir(mask_dir):
    os.makedirs(mask_dir)

  metadata_csv = pd.read_csv(metadata)

  for (i, row) in metadata_csv.iterrows():
    if row["finding"] != "COVID-19":
      continue

    filename = row["imagename"]

    image_path = os.path.join(imagedir, filename)

    # Copy image
    shutil.copy2(image_path, dest_dir)

    pid = row["patientid"].replace("ANON", "")
    offset = row["offset"]

    try:
      offset = int(offset)
    except:
      offset = 0

    ext = os.path.splitext(filename)[-1]
    new_filename = "actualmed-P" + str(pid) + "_" + str(offset)
    old_file = os.path.join(dest_dir, filename)
    new_file = os.path.join(dest_dir, new_filename + ext)
    if os.path.exists(new_file):
      os.remove(new_file)
    os.rename(old_file, new_file)

    # Check if there are any mask provided for this image
    mask_filename = os.path.splitext(filename)[0] + ".png"
    mask_filepath = os.path.join("Masks", mask_filename)
    if os.path.exists(mask_filepath):
      shutil.copy2(mask_filepath, mask_dir)
      old_file = os.path.join(mask_dir, mask_filename)
      new_file = os.path.join(mask_dir, new_filename + ".png")
      os.rename(old_file, new_file)
  shutil.rmtree(os.path.join(actual_path, "Actualmed-COVID-chestxray-dataset"))
