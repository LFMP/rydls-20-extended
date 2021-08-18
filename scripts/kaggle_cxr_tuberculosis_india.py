import os
import shutil

import kaggle
import pandas as pd


def build(actual_path):
  kaggle.api.authenticate()
  filename = 'chest-xrays-tuberculosis-from-india.zip'
  outputdir = os.path.join(actual_path,
                           "datasets/chest-xrays-tuberculosis-from-india")
  extractdir = os.path.join(actual_path, "archive")

  if not os.path.exists(extractdir):
    kaggle.api.dataset_download_files(
        'raddar/chest-xrays-tuberculosis-from-india',
        path=extractdir,
        quiet=False,
        unzip=True)

  # Remove output dir if present
  if os.path.isdir(outputdir):
    shutil.rmtree(outputdir)

  csvfile = os.path.join(extractdir, "jaypee_metadata.csv")
  df = pd.read_csv(csvfile)
  df = df[df["findings"] == "Tuberculosis"]

  imagedir = os.path.join(extractdir, "images/images")
  dest_dir = os.path.join(outputdir, "tuberculosis")
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  pid = 0
  for filename in df["study_id"].to_numpy():
    image_path = os.path.join(imagedir, filename)
    # Copy image
    shutil.copy2(image_path, dest_dir)

    offset = 0

    ext = os.path.splitext(filename)[1]
    new_filename_ext = "kaggleTuberculosisIndia-T-" + str(pid) + "_" + str(
        offset) + ext
    old_file = os.path.join(dest_dir, filename)
    new_file = os.path.join(dest_dir, new_filename_ext)
    os.rename(old_file, new_file)
    pid += 1
  shutil.rmtree(extractdir)
