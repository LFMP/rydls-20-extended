import os
import re
import shutil

import kaggle
import pandas as pd


def build(actual_path):
  kaggle.api.authenticate()
  actual_path = os.getcwd()
  filename = 'covid19-radiography-database.zip'
  outputdir = os.path.join(actual_path, "datasets/COVID-19_Radiography_Dataset")
  extractdir = os.path.join(actual_path, "COVID-19_Radiography_Dataset")

  if not os.path.exists(extractdir):
    kaggle.api.dataset_download_files(
        'tawsifurrahman/covid19-radiography-database',
        path=actual_path,
        quiet=False,
        unzip=True)

  # Remove output dir if present
  if os.path.isdir(outputdir):
    shutil.rmtree(outputdir)

  metadatas = ["COVID", "Lung_Opacity", "Normal", "Viral Pneumonia"]

  for meta in metadatas:
    # Check if destination folder exists, if not create it
    dest_dir = os.path.join(outputdir, meta)
    if not os.path.isdir(dest_dir):
      os.makedirs(dest_dir)

    metadata = os.path.join(extractdir, meta + ".metadata.xlsx")
    imagedir = os.path.join(extractdir, meta)

    metadata_csv = pd.read_excel(metadata)

    for (i, row) in metadata_csv.iterrows():

      filename = row["FILE NAME"]
      if not os.path.isfile(os.path.join(imagedir, filename + ".png")):
        filename = row["FILE NAME"].replace("(", " (")

      if meta == "Normal":
        filename = filename.capitalize()
      image_path = os.path.join(imagedir, filename + ".png")

      # Copy image
      shutil.copy2(image_path, dest_dir)

      pid = re.split("[()]", filename)[0]
      offset = 0

      ext = os.path.splitext(filename)[1]
      new_filename_ext = "kaggleCRD-P-" + str(pid) + "_" + str(offset) + ext
      old_file = os.path.join(dest_dir, filename + ".png")
      new_file = os.path.join(dest_dir, new_filename_ext + ".png")
      os.rename(old_file, new_file)
  shutil.rmtree(extractdir)
