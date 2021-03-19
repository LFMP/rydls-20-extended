import os
import re
import shutil

import kaggle

kaggle.api.authenticate()
actual_path = os.getcwd()
filename = 'chest-xray-pneumonia.zip'
file_path = os.path.join(actual_path, filename)
outputdir = os.path.join(actual_path, "datasets/chest_xray_pneumonia")
extractdir = os.path.join(actual_path, "chest_xray")

if not os.path.exists(extractdir):
  kaggle.api.dataset_download_files('paultimothymooney/chest-xray-pneumonia',
                                    path=actual_path,
                                    quiet=False,
                                    unzip=True)

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

folders = [
    "test/NORMAL", "test/PNEUMONIA", "train/NORMAL", "train/PNEUMONIA",
    "val/NORMAL", "val/PNEUMONIA"
]
pid = 0
for folder in folders:
  # Check if destination folder exists, if not create it
  dest_dir = os.path.join(outputdir, os.path.split(folder)[1])
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  imagedir = os.path.join(extractdir, folder)

  for filename in os.listdir(imagedir):
    image_path = os.path.join(imagedir, filename)

    # Copy image
    shutil.copy2(image_path, dest_dir)

    offset = 0

    ext = os.path.splitext(filename)[1]
    new_filename_ext = "kagglePneumonia-P-" + str(pid) + "_" + str(offset) + ext
    old_file = os.path.join(dest_dir, filename)
    new_file = os.path.join(dest_dir, new_filename_ext)
    os.rename(old_file, new_file)
    pid += 1
shutil.rmtree(extractdir)
