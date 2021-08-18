import os
import shutil

import kaggle


def build(actual_path):
  kaggle.api.authenticate()
  filename = 'tbx-11.zip'
  outputdir = os.path.join(actual_path, "datasets/tbx-11")
  extractdir = os.path.join(actual_path, "tbx-11")

  if not os.path.exists(extractdir):
    kaggle.api.dataset_download_files('usmanshams/tbx-11',
                                      path=extractdir,
                                      quiet=False,
                                      unzip=True)

  # Remove output dir if present
  if os.path.isdir(outputdir):
    shutil.rmtree(outputdir)

  pid = 0
  dest_dir = os.path.join(outputdir, "Tuberculosis")
  if not os.path.isdir(dest_dir):
    os.makedirs(dest_dir)

  imagedir = os.path.join(extractdir, "TBX11K/imgs/tb")

  for filename in os.listdir(imagedir):
    image_path = os.path.join(imagedir, filename)

    # Copy image
    shutil.copy2(image_path, dest_dir)

    offset = 0

    ext = os.path.splitext(filename)[1]
    new_filename_ext = "kaggleTBX11-T-" + str(pid) + "_" + str(offset) + ext
    old_file = os.path.join(dest_dir, filename)
    new_file = os.path.join(dest_dir, new_filename_ext)
    os.rename(old_file, new_file)
    pid += 1
  shutil.rmtree(extractdir)
