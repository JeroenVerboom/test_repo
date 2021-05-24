import cv2
import os
import pandas as pd


# specify input directories
im_dir = r'.\PNGS' # LET OP: verander dit naar het pad waar je de images hebt gedownload
lab_dir = r".\YOLO_predictions" # LET OP: verander dit naar het pad waar je de txt files hebt gedownload

# specify output directories
csv_dir = r'.\VIA_format_YOLO_prediction.csv'
radius_f_dir = r".\PNGS\Radius_F"
ulna_f_dir = r'.\PNGS\Ulna_F'
radius_lat_dir = r'.\PNGS\Radius_LAT'
ulna_lat_dir = r'.\PNGS\Ulna_LAT'


# If you want to crop the predicted image imediately, change the value to True
cropping = True

# create empty dataframe to fill with YOLO predictions in VIA format
df = pd.DataFrame()


print("Cropping images and creating new csv file with VIA coordinates. This might take a minute or two...")
# loop over images names
for image_name in sorted(os.listdir(im_dir)):
    if '.png' not in image_name: # skip if file is not an image
        continue
    elif image_name.replace('.png', '.txt') not in os.listdir(lab_dir): # check if image has a corresponding YOLO prediciton
        continue
    else: # read image, extract image size and recreate path
        im_path = os.path.join(im_dir, image_name)
        im_array = cv2.imread(im_path)
        im_size = os.path.getsize(im_path)

        #  skip corrupted files
        if im_array is None:
            print("corrupted file!", image_name)
            continue
        else:
            image_height, image_width, image_channels = im_array.shape # extract width & height from image
            txt = image_name.replace('png', 'txt') # replace the suffix with txt to find the corresponding txt file with bbox coordinates

            # open file and create a list for each bone annotated: [class, x, y, width, height, conf]
            with open(os.path.join(lab_dir, txt), "r") as myfile:
                data = myfile.readlines()
                annotations_raw = [line.split(' ') for line in data]



                # extract the YOLO format coordinates (these are normalized coordinates)
                for line in annotations_raw:
                    x_center = float(line[1])
                    y_center = float(line[2])
                    width_norm = float(line[3])
                    height_norm = float(line[4].strip("\n"))

                    # transform to boundig box coordinates for VIA
                    bbox_x_left = int((x_center * image_width) - (width_norm * image_width/2))
                    bbox_x_right = int((x_center * image_width) + (width_norm * image_width/2))
                    bbox_y_bottom = int((y_center * image_height) - (height_norm * image_height/2))
                    bbox_y_top = int((y_center * image_height) + (height_norm * image_height/2))

                    bbox_width_VIA = bbox_x_right - bbox_x_left
                    bbox_height_VIA = bbox_y_top - bbox_y_bottom
                    rect = '"rect"' # specify bbox shape

                    # extract the bone-projection combination of the bounding box
                    # These combinations were encoded by the YOLO model (0 = Radius_F, 1 = Ulna_F, 2 = Radius_LAT etc.)
                    if line[0] == '0':
                        region_attribute = '{"bone":"Radius_F"}'
                    elif line[0] == '1':
                        region_attribute = '{"bone":"Ulna_F"}'
                    elif line[0] == '2':
                        region_attribute = '{"bone":"Radius_LAT"}'
                    elif line[0] == '3':
                        region_attribute = '{"bone":"Ulna_LAT"}'

                    # create a row for the dataframe using a dictionary
                    dict = {
                        'filename': image_name, 'file_size': im_size, 'file_attributes': '"{}"', 'region_count': 1,
                        'region_id': int(line[0]),
                        'region_shape_attributes': '{{"name":{},"x":{},"y":{},"width":{},"height":{}}}'.format(
                            rect, bbox_x_left, bbox_y_bottom, bbox_width_VIA, bbox_height_VIA),
                        'region_attributes': region_attribute}

                    # transform dictionary to dataframe and concatenate it with existing df.
                    df_subset = pd.DataFrame(dict, index=[0])
                    df = pd.concat([df, df_subset])




                    # Crop bone out of the image and save to new dir:
                    if cropping == True:

                        # create output directories for crops
                        try:
                            os.makedirs(radius_f_dir)
                            os.makedirs(ulna_f_dir)
                            os.makedirs(radius_lat_dir)
                            os.makedirs(ulna_lat_dir)

                        except:
                            pass

                        # Crop ouut the image using the transformed coordinates.
                        cropped = im_array[bbox_y_bottom:bbox_y_top, bbox_x_left:bbox_x_right]

                        # Create file specifying the bone-projection combination it cropped out:
                        # NOTE: Some PNGS from the hospital contained multiple radiographs (maximum of 4) meaning multiple
                        # instances of the radius and ulna might occur in one PNG. The code below renames cropped
                        # image if the file already exists.
                        if 'Radius_F' in region_attribute:
                            new_file_name = image_name.replace('.png', '___Radius_F.png')
                            save_path = os.path.join(radius_f_dir, new_file_name)  # e.g  ....REUMA_AP_-CR-1___1new___Radius_F.png
                            if os.path.exists(save_path) == False:  # check if image already exissts, otherwise rename
                                cv2.imwrite(save_path, cropped)
                            elif os.path.exists(save_path):
                                save_path_2 = save_path.replace('.png','2.png')  # e.g  ....REUMA_AP_-CR-1___1new___Radius_F2.png
                                cv2.imwrite(save_path_2, cropped)
                            elif os.path.exists(save_path_2):
                                save_path_3 = save_path.replace('.png', '3.png')
                                cv2.imwrite(save_path_3, cropped)
                            elif os.path.exists(save_path_3):
                                save_path_4 = save_path.replace('.png', '4.png')
                                cv2.imwrite(save_path_4, cropped)
                            else:
                                print("Something is going wrong...")

                        elif 'Ulna_F' in region_attribute:
                            new_file_name = image_name.replace('.png', '___Ulna_F.png')
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

                        elif 'Radius_LAT' in region_attribute:
                            new_file_name = image_name.replace('.png', '___Radius_LAT.png')
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

                        elif 'Ulna_LAT' in region_attribute:
                            new_file_name = image_name.replace('.png', '___Ulna_LAT.png')
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
                    else:
                        continue


print(len(df), "bounding boxes generated.")

# Sort and save the dataframe
df = df.sort_values('filename')
print("saving data frame...")
df.to_csv(csv_dir, header=True, index=False)













