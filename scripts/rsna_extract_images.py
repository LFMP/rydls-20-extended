import os
import shutil

import cv2
import kaggle
import pandas as pd
import pydicom
import tqdm

kaggle.api.authenticate()
actual_path = os.getcwd()
filename = 'rsna-pneumonia-detection-challenge.zip'
file_path = os.path.join(actual_path, filename)
outputdir = os.path.join(actual_path,
                         "datasets/rsna-pneumonia-detection-challenge")
extractdir = os.path.join(actual_path, "rsna-pneumonia-detection-challenge")

# Remove output dir if present
if os.path.isdir(outputdir):
  shutil.rmtree(outputdir)

metadata_train = os.path.join(outputdir, "stage_2_train_labels.csv")
metadata_detailed = os.path.join(outputdir, "stage_2_detailed_class_info.csv")

if not os.path.exists(file_path):
  kaggle.api.competition_download_files('rsna-pneumonia-detection-challenge',
                                        path=actual_path,
                                        quiet=False)
shutil.unpack_archive(file_path, extractdir)
os.remove(file_path)

df = pd.read_csv(metadata_train)
df_detailed = pd.read_csv(metadata_detailed)

x_ray_view = ["PA", "AP"]

global_pid = 0

for target in ["Normal", "No Lung Opacity / Not Normal", "Lung Opacity"]:
  positive_target = df_detailed["class"] == target
  local_df = df_detailed[positive_target]
  local_df.reset_index(inplace=True)
  nrows = local_df.shape[0]

  # Check if destination folder exists, if not create it
  if target == "No Lung Opacity / Not Normal":
    dest_dir = os.path.join(outputdir, "Not normal")
  else:
    dest_dir = os.path.join(outputdir, target)

  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  for pid in trange(nrows):
    full_pid = local_df["patientId"][pid]
    dcm_file = os.path.join(extractdir,
                            "stage_2_train_images/%s.dcm" % full_pid)
    dcm_data = pydicom.read_file(dcm_file)

    if dcm_data.ViewPosition not in x_ray_view:
      continue
    global_pid += 1
    image = dcm_data.pixel_array
    file_path = os.path.join(dest_dir, "rsna-P" + str(global_pid) + "_0.png")
    cv2.imwrite(file_path, image)
shutil.rmtree(extractdir)
