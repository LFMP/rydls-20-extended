import os
import shutil

import pandas as pd

# I'm assuming that this repo does not contain repeated images from Cohen

actual_path = os.getcwd()
if not os.path.exists(os.path.join(actual_path, "covid-19-image-repository")):
  os.system(
      "git clone https://github.com/ml-workgroup/covid-19-image-repository.git")

imagedir = os.path.join(actual_path, "covid-19-image-repository/png")
metadata = os.path.join(actual_path, "covid-19-image-repository/data.csv")
outputdir = os.path.join(actual_path, "datasets/v2_cov19_nii")

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

# Check if destination folder exists, if not create it
dest_dir = os.path.join(outputdir, "COVID-19")
if not os.path.isdir(dest_dir):
  os.makedirs(dest_dir)

metadata_csv = pd.read_csv(metadata)

for (i, row) in metadata_csv.iterrows():

  filename = row["image_id"]
  ext = ".png"

  if row["projection"] != "pa":
    continue

  image_path = os.path.join(imagedir, filename + ext)

  # Copy image
  shutil.copy2(image_path, dest_dir)
  offset = row["patient_id"]

  try:
    offset = int(offset)
  except:
    offset = 0

  new_filename_ext = "cov19_nii-P" + str(i) + "_" + str(offset)
  old_file = os.path.join(dest_dir, filename + ext)
  new_file = os.path.join(dest_dir, new_filename_ext + ext)
  if os.path.exists(new_file):
    os.remove(new_file)
  os.rename(old_file, new_file)
shutil.rmtree(os.path.join(actual_path, "covid-19-image-repository"))
