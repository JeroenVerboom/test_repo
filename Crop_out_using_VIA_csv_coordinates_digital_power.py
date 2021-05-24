import re
import os
import cv2
import pandas as pd
# import numpy as np
import matplotlib.pylab as plt

csv_file = r"VIA_format_YOLO_prediction.csv"  # pad naar VGG CSV file met annotaties
image_dir = r'C:\Users\Jeroen\PycharmProjects\Fresh Start\Fracture detection\Iteratie2 _3K_rapporten_niet_nagelopen\PNGS\run2'  # pad naar map met afbeeldingen (niet in submappen!)

radius_f_dir = r".\PNGS\Radius_F"  # pad naar map waar de labels moeten worden opgeslagen, nieuwe map heet output
ulna_f_dir = r'.\PNGS\Ulna_F'
radius_lat_dir = r'.\PNGS\Radius_LAT'
ulna_lat_dir = r'.\PNGS\Ulna_LAT'


try:
    # create output directory
    os.makedirs(radius_f_dir)
    os.makedirs(ulna_f_dir)
    os.makedirs(radius_lat_dir)
    os.makedirs(ulna_lat_dir)

except:
    pass

# create empty dictionary for bounding box coordinates & labels
df = pd.DataFrame(columns=['bone', 'x_center', 'y_center', 'width_norm', 'height_norm', 'file_name'])

# read bounding box csv
with open(csv_file, "r", encoding="utf-8") as csv:
    csv_lines = csv.readlines()
for i, line in enumerate(csv_lines):
    if i == 0:  # skip header
        continue

    elif len(line.split(',')) < 12: # a line for an unusable file looks like this: "2.png,6611951,"{""Unsuable file"":""Rotation""}",0,0,"{}","{}""
        continue


    else:
        # split line
        chuncks = line.split(",")

        # get filename
        file_name = chuncks[0].strip('"')

        # get label of the bone: Radius or ulna
        bone_in_csv = re.findall(r'Radius_F|Ulna_F|Radius_LAT|Ulna_LAT', chuncks[-1])[0]

        if len(chuncks) < 1:
            continue

        else:
            print(line)
            # get bounding box coordinates using regular expressions package
            bbox_x_left = int(re.findall('\d+', chuncks[7])[0])
            bbox_x_right = int(re.findall('\d+', chuncks[9])[0]) + bbox_x_left
            bbox_y_bottom = int(re.findall('\d+', chuncks[8])[0])
            bbox_y_top = int(re.findall('\d+', chuncks[10])[0]) + bbox_y_bottom

            file_path = chuncks[0].strip('"').replace('___', '\\')
            image_path = os.path.join(image_dir, file_name)  # concatenate folder path & image name
            image = cv2.imread(image_path)      # read image
            if image is not None:
                image_height, image_width, image_channels = image.shape
            elif image is None:
                print(file_name, 'is a corrupted image!')
                continue

            # create croppped image
            cropped = image[bbox_y_bottom:bbox_y_top, bbox_x_left:bbox_x_right]

            ## I hashed the plt.show() out for now, but good to have for demonstration purposes
            # plt.imshow(cropped)
            # plt.show()

            # create file specifying the bone it cropped out
            # maximum of 4 radiographs in one
            if bone_in_csv == 'Radius_F':
                new_file_name = file_name.replace('.png', '___Radius_F.png')
                save_path = os.path.join(radius_f_dir, new_file_name)
                if os.path.exists(save_path) == False:
                    cv2.imwrite(save_path, cropped)  # save image to specified directory
                elif os.path.exists(save_path):
                    save_path_2 = save_path.replace('.png', '2.png')
                    cv2.imwrite(save_path_2, cropped)
                elif os.path.exists(save_path_2):
                    save_path_3 = save_path.replace('.png', '3.png')
                    cv2.imwrite(save_path_3, cropped)
                elif os.path.exists(save_path_3):
                    save_path_4 = save_path.replace('.png', '4.png')
                    cv2.imwrite(save_path_4, cropped)
                else:
                    print("Something is going wrong...")

            elif bone_in_csv == 'Ulna_F':
                new_file_name = file_name.replace('.png', '___Ulna_F.png')
                save_path = os.path.join(ulna_f_dir, new_file_name)

                if os.path.exists(save_path) == False:
                    cv2.imwrite(save_path, cropped)  # save image to specified directory
                elif os.path.exists(save_path):
                    save_path_2 = save_path.replace('.png', '2.png')
                    cv2.imwrite(save_path_2, cropped)
                elif os.path.exists(save_path_2):
                    save_path_3 = save_path.replace('.png', '3.png')
                    cv2.imwrite(save_path_3, cropped)
                elif os.path.exists(save_path_3):
                    save_path_4 = save_path.replace('.png', '4.png')
                    cv2.imwrite(save_path_4, cropped)
                else:
                    print("Something is going wrong...")

            elif bone_in_csv == 'Radius_LAT':
                new_file_name = file_name.replace('.png', '___Radius_LAT.png')
                save_path = os.path.join(radius_lat_dir, new_file_name)

                if os.path.exists(save_path) == False:
                    cv2.imwrite(save_path, cropped)  # save image to specified directory
                elif os.path.exists(save_path):
                    save_path_2 = save_path.replace('.png', '2.png')
                    cv2.imwrite(save_path_2, cropped)
                elif os.path.exists(save_path_2):
                    save_path_3 = save_path.replace('.png', '3.png')
                    cv2.imwrite(save_path_3, cropped)
                elif os.path.exists(save_path_3):
                    save_path_4 = save_path.replace('.png', '4.png')
                    cv2.imwrite(save_path_4, cropped)
                else:
                    print("Something is going wrong...")

            elif bone_in_csv == 'Ulna_LAT':
                new_file_name = file_name.replace('.png', '___Ulna_LAT.png')
                save_path = os.path.join(ulna_lat_dir, new_file_name)

                if os.path.exists(save_path) == False:
                    cv2.imwrite(save_path, cropped)  # save image to specified directory
                elif os.path.exists(save_path):
                    save_path_2 = save_path.replace('.png', '2.png')
                    cv2.imwrite(save_path_2, cropped)
                elif os.path.exists(save_path_2):
                    save_path_3 = save_path.replace('.png', '3.png')
                    cv2.imwrite(save_path_3, cropped)
                elif os.path.exists(save_path_3):
                    save_path_4 = save_path.replace('.png', '4.png')
                    cv2.imwrite(save_path_4, cropped)
                else:
                    print("Something is going wrong...")

            else:
                print("Something is going wrong...")

            # create path of new PNG file


