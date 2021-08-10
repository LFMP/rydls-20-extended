import os
import shutil

actual_path = os.getcwd()
datasets_path = os.path.join(actual_path, 'datasets')
datasets = os.listdir(datasets_path)
images_path = os.path.join(actual_path, 'images')

actualmed = os.path.join(datasets_path, 'Actualmed')
chest_xray_pneumonia = os.path.join(datasets_path, 'chest_xray_pneumonia')
cohen = os.path.join(datasets_path, 'cohen')
COVID19_R_Dataset = os.path.join(datasets_path, 'COVID-19_Radiography_Dataset')
figure1 = os.path.join(datasets_path, 'Figure1')
rsna = os.path.join(datasets_path, 'rsna-pneumonia-detection-challenge')
cvo19_nii = os.path.join(datasets_path, 'v2_cov19_nii')

if not os.path.isdir(images_path):
  os.makedirs(images_path)

covid_path = os.path.join(images_path, 'COVID-19')
if not os.path.isdir(covid_path):
  os.makedirs(covid_path)

covid_datasets_path = [
    os.path.join(actualmed, 'COVID-19'),
    os.path.join(cohen, 'Pneumonia/Viral/COVID-19'),
    os.path.join(figure1, 'COVID-19'),
    os.path.join(COVID19_R_Dataset, 'COVID'),
    os.path.join(cvo19_nii, 'COVID-19')
]
for folder in covid_datasets_path:
  if os.path.exists(folder):
    for filename in os.listdir(folder):
      shutil.move(os.path.join(folder, filename), covid_path)

normal_path = os.path.join(images_path, 'Normal')
if not os.path.isdir(normal_path):
  os.makedirs(normal_path)

normal_datasets_path = [
    os.path.join(chest_xray_pneumonia, 'NORMAL'),
    os.path.join(cohen, 'Normal'),
    os.path.join(COVID19_R_Dataset, 'Normal'),
    os.path.join(rsna, 'Normal'),
]

for folder in normal_datasets_path:
  for filename in os.listdir(folder):
    shutil.move(os.path.join(folder, filename), normal_path)

if os.path.exists(os.path.join(cohen, 'Pneumonia')):
  shutil.move(os.path.join(cohen, 'Pneumonia'), images_path)
pneumo_path = os.path.join(images_path, 'Pneumonia')
if not os.path.isdir(pneumo_path):
  os.makedirs(pneumo_path)

pneumo_datasets_path = [
    os.path.join(chest_xray_pneumonia, 'PNEUMONIA'),
]

for folder in pneumo_datasets_path:
  for filename in os.listdir(folder):
    shutil.move(os.path.join(folder, filename), pneumo_path)

for filename in os.listdir(os.path.join(COVID19_R_Dataset, 'Viral Pneumonia')):
  shutil.move(os.path.join(COVID19_R_Dataset, 'Viral Pneumonia', filename),
              os.path.join(images_path, 'Pneumonia', 'Viral'))

if os.path.exists(os.path.join(cohen, 'Tuberculosis')):
  shutil.move(os.path.join(cohen, 'Tuberculosis'), images_path)

opacity_path = os.path.join(images_path, 'Opacity')
if not os.path.isdir(opacity_path):
  os.makedirs(opacity_path)

opacity_datasets_path = [
    os.path.join(COVID19_R_Dataset, 'Lung_Opacity'),
    os.path.join(rsna, 'Lung Opacity'),
]

for folder in opacity_datasets_path:
  for filename in os.listdir(folder):
    shutil.move(os.path.join(folder, filename), opacity_path)

unknown_path = os.path.join(images_path, 'Unknown')
if not os.path.isdir(unknown_path):
  os.makedirs(unknown_path)

unknown_datasets_path = [
    os.path.join(cohen, 'Unknown'),
    os.path.join(rsna, 'Not normal'),
]

for folder in unknown_datasets_path:
  for filename in os.listdir(folder):
    shutil.move(os.path.join(folder, filename), unknown_path)

shutil.rmtree(os.path.join(actual_path, "datasets"))
