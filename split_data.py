import random
from pathlib import Path


def split_data():
    pre_images_path = Path("Datasets/raw_data/images")
    pre_labels_path = Path("Datasets/raw_data/labels")
    train_images_path = Path('Datasets/images/train')
    val_images_path = Path('Datasets/images/val')
    train_labels_path = Path('Datasets/labels/train')
    val_labels_path = Path('Datasets/labels/val')    

    #shuffling images and random split between 10% and 20% goes to validation set
    image_files = [img for img in pre_images_path.iterdir() if img.is_file() and img.suffix == '.jpg']
    random.shuffle(image_files)
    split = random.uniform(0.1, 0.2)
    #create directories if no created yet
    train_images_path.mkdir(parents=True, exist_ok=True)
    val_images_path.mkdir(parents=True, exist_ok=True)
    train_labels_path.mkdir(parents=True, exist_ok=True)
    val_labels_path.mkdir(parents=True, exist_ok=True)

    #split the data into the two sets
    images_count = len(image_files)
    print("Images in total: ", images_count)
    train_images = image_files[: int(images_count - (images_count*split))]
    val_images = image_files[int(images_count - (images_count*split)):]
    print("Training images: ", len(train_images))
    print("Validation images: ", len(val_images))

    for image in train_images:
        #move images and labels used for training in the correct folders
        source_image_path = Path(image)
        source_image_path.rename(train_images_path / image.name)
        label_file_name = image.name.replace('.jpg', '.txt')
        source_label_path = Path(pre_labels_path / label_file_name)
        #if the image is a background then there will be no label associated
        if source_label_path.exists():
            source_label_path.rename(train_labels_path / label_file_name)

    for image in val_images:
        #move images and labels used for validation in the correct folders
        source_image_path = Path(image)
        source_image_path.rename(val_images_path / image.name)
        label_file_name = image.name.replace('.jpg', '.txt')
        source_label_path = Path(pre_labels_path / label_file_name)
        #if the image is a background then there will be no label associated
        if source_label_path.exists():
            source_label_path.rename(val_labels_path / label_file_name)

    print("ALl files moved in the correct folders")

if __name__ == '__main__':
    split_data()