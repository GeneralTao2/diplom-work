# C:\Users\gener\OneDrive\Documents\Python\images-to-stl\patients\tmp\DICOM\PA0\ST0\SE1
from io import BytesIO
from pydicom import dcmread
import os
import cv2 
import matplotlib.pyplot as plt
from pydicom_PIL import show_PIL
from pydicom.pixel_data_handlers.util import apply_color_lut
from pydicom.pixel_data_handlers.util import apply_modality_lut

path_to_dicom = 'C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\patients\\tmp\\DICOM\\PA0\\ST0\\SE2\\'
path_to_images = 'C:\\Users\\gener\\OneDrive\\Documents\\Python\\images-to-stl\\pa0st0se2-images-ex\\'

""" test_file_name = "IM28"
from pydicom.pixel_data_handlers.util import apply_voi_lut
ds = dcmread(path_to_dicom+test_file_name)
print(apply_color_lut(ds.pixel_array, palette='PET'))
arr=ds.pixel_array
plt.imshow(apply_voi_lut(arr, ds, index=0)) 

plt.show() """
""" ds = dcmread(path_to_dicom+test_file_name)
show_PIL(ds) """

sorted_ds = []
for file in os.listdir(path_to_dicom):
    ds = dcmread(path_to_dicom+file)
    sorted_ds.append(ds)

sorted_ds.sort(key=lambda x: x.ImagePositionPatient[2])

i=0
for ds in sorted_ds:
    image = ds.pixel_array
    image = (image -1024)*4
    image_format = '.png' # or '.png'
    gray_three = cv2.merge([image,image,image])
    
    cv2.imwrite(path_to_images + "IM" + str(i) + image_format, gray_three)
    i+=1

for i in range(len(sorted_ds)-1):
    print(sorted_ds[i+1].ImagePositionPatient[2]-sorted_ds[i].ImagePositionPatient[2])


