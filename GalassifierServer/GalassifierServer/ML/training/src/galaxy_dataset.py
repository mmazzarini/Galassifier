import config
import numpy as np
import pandas as pd
import os
import zipfile
import config
from tensorflow import keras
import shutil

config_data = config.load_project_config()

MOUNT_REMOTE_IMAGES = config_data["training_stages"]["mount_remote_images"]
LOAD_REMOTE_DATASET = config_data["training_stages"]["load_and_mount_remote_dataset"]


#method to define galaxy table, from a csv file converting it into an array
def  create_galaxy_table(in_galaxy_file):
    galaxies_np_file = in_galaxy_file.to_numpy()
    galaxies_table = []
    classes = config_data["classification"]["classes"]
    classification_keywords = config_data["classification"]["keyword_search_for_classes_in_data"]
    for line in galaxies_np_file:
        galaxy_type = 0 # means uncertain type
        galaxy_id = line[0]
        galaxy_type_str = str(line[6])
        for class_key in classification_keywords:
            if(class_key in galaxy_type_str):
                galaxy_type = classification_keywords.index(class_key)
                break
        galaxies_table.append([galaxy_id, galaxy_type])
    return galaxies_table

def load_remote_dataset():

    #catalog: lets get galaxies
    #using https://data.galaxyzoo.org/?_ga=2.107268992.360088703.1763919279-669604038.1763591364
    #see also https://zenodo.org/records/3565489#.Y3vFKS-l0eY for the images
    galaxies_CSV_filename = 'gz2_hart16.csv.gz'
    galaxies_CSV_file_path = 'https://gz2hart.s3.amazonaws.com/gz2_hart16.csv.gz'
    galaxies_CSV_zip_file = keras.utils.get_file(galaxies_CSV_filename, galaxies_CSV_file_path)
    print(galaxies_CSV_zip_file)
    # Read the CSV file from the zip archive directly
    galaxies_file = pd.read_csv(galaxies_CSV_zip_file)
    galaxies_datatable = create_galaxy_table(galaxies_file)

    galaxies_images_file = []
    galaxies_image_filename = 'images_gz2_v2.zip'
    #here we load and read the images
    if(MOUNT_REMOTE_IMAGES == True):
        galaxies_images_file_path = 'https://zenodo.org/records/3565489/files/images_gz2.zip'
        galaxies_images_file = keras.utils.get_file(galaxies_image_filename, galaxies_images_file_path)
        print(galaxies_images_file)
        #copy images to drive
        
        shutil.copy(galaxies_images_file, '/content/drive/MyDrive/Galaxies_Zoo')
        galaxies_images_file = keras.utils.get_file(galaxies_image_filename, galaxies_images_file_path)
        print(galaxies_images_file)
    else:
        galaxies_images_file = os.path.join('/content/drive/MyDrive/Galaxies_Zoo', galaxies_image_filename)
        print(galaxies_images_file)
        if not os.path.exists(galaxies_images_file):
            print("Warning! The file does not exist in drive directory!")

    if(LOAD_REMOTE_DATASET == True):

        extract_dir = './galaxy_images_truncated'
        os.makedirs(extract_dir, exist_ok=True)

        galaxies_datatable_np = np.array(galaxies_datatable)

        try:
            with zipfile.ZipFile(galaxies_images_file, 'r') as zip_ref:
                all_files_in_zip = zip_ref.namelist()
                print(len(all_files_in_zip))
                extract_count = 0

                for file_name in all_files_in_zip:
                    if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                        zip_ref.extract(file_name, extract_dir)
                        extract_count += 1

        except FileNotFoundError:
            print(f"Error: Zip file not found at '{galaxies_images_file}'. Please ensure it was downloaded correctly.")
        except zipfile.BadZipFile:
            print(f"Error: '{galaxies_images_file}' is not a valid zip file or is corrupted. It might have been an incomplete download.")
        except Exception as e:
            print(f"An unexpected error occurred during extraction: {e}")

        #print(extract_dir)

        galaxies_CSV_map_filename = 'gz2_filename_mapping.csv'
        galaxies_CSV_map_file_path = 'https://zenodo.org/records/3565489/files/gz2_filename_mapping.csv'
        galaxies_CSV_map_file = keras.utils.get_file(galaxies_CSV_map_filename, galaxies_CSV_map_file_path)
        print(galaxies_CSV_map_file)
        # Read the CSV file from the zip archive directly
        galaxies_map = pd.read_csv(galaxies_CSV_map_file)
        print(galaxies_map.to_numpy().shape)
        galaxy_map_np = np.empty((0,2), dtype=np.int64)
        index = 0
        for galaxy_data in galaxies_map.to_numpy():
            index += 1
            galaxy_id = int(galaxy_data[0])
            galaxy_asset_id = int(galaxy_data[2]) # Renamed for clarity: this is asset_id, not galaxy_type
            galaxy_map_np = np.append(galaxy_map_np, np.array([[galaxy_id, galaxy_asset_id]],dtype=np.int64), axis=0)

        print(galaxy_map_np.shape)
        print(np.array(galaxies_datatable).shape)
        galaxies_datatable_np = np.array(galaxies_datatable)
        print(galaxies_datatable_np.shape, type(galaxies_datatable_np))
    
    return galaxies_datatable_np, galaxy_map_np

def load_dataset_from_tables(galaxies_datatable_np, galaxy_map_np):
    
    train_images = []
    train_labels = []
    val_images = []
    val_labels = []
    train_num = math.floor(galaxies_datatable_np.shape[0]*0.70)
    val_num = galaxies_datatable_np.shape[0] - train_num
    total_set_num = train_num + val_num
    extract_dir = './galaxy_images_truncated'
    dir_images_root = extract_dir + '/' + 'images' + '/'
    print('dir images root: ' + dir_images_root)
    counter = 0
    for galaxy_mapdata in galaxy_map_np:
        if(counter >= total_set_num):
            break
        galaxy_id = galaxy_mapdata[0]
        galaxy_img_num = galaxy_mapdata[1]
        # path
        galaxy_img_path = os.path.join(dir_images_root, str(galaxy_img_num) + '.jpg')

        if not os.path.exists(galaxy_img_path):
              print (f"Warning: path {galaxy_img_path} does not exist!")
        try:
            # 1) load img; 2) array-fy image; 3) normalize it
            img = keras.utils.load_img(galaxy_img_path, color_mode="grayscale", target_size=(IMG_SIZE_X, IMG_SIZE_Y))
            img_array = keras.utils.img_to_array(img)
            img_normalized = img_array / 255.0
            print(f"SUCCESS: image {galaxy_img_path} found!")
        except Exception as e:
            print(f"Error: could not properly load image at path {galaxy_img_path}: {e}")
            continue
        #galaxy type
        gal_type_line_num = (galaxies_datatable_np[:,0] == galaxy_id).nonzero()
        if(gal_type_line_num[0].size == 0):
            continue
        galaxy_type_idx = gal_type_line_num[0][0]
        galaxy_type = galaxies_datatable_np[galaxy_type_idx][1]
        #fill arrays
        if(counter < train_num):
            # train imgs
            train_images.append(img_normalized)
            train_labels.append(galaxy_type)
        else:
            #val imgs
            val_images.append(img_normalized)
            val_labels.append(galaxy_type)
        counter += 1

    #after doing all: let's make numpy-arrays out of our dataset
    train_images = np.array(train_images)
    train_labels = np.array(train_labels)
    val_images = np.array(val_images)
    val_labels = np.array(val_labels)
    print(f'Done processing. Train images len: {len(train_images)}; validation images len: {len(val_images)}.')

    return {
        'train_images' : train_images, 
        'train_labels' : train_labels, 
        'val_images' : val_images, 
        'val_labels' : val_labels 
    }
    