import cv2 #OpenCV library
import sys 
import argparse
from pathlib import Path
import numpy as np
from datetime import datetime

"""
Video Labeler class facilitating labeling of an object through different frames with openCV CSRT tracking algorithm
Created: 23.01.2023
"""

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--filePath", type=str,
        help="path to input video file")
    parser.add_argument("-c", "--className", type=str, default="label",
        help="Enter your class label name")
    parser.add_argument("-f", "--frameRate", type=int, default=1,
        help="save per frame")
    parser.add_argument("-i", "--classId", type=int, default=0,
        help="Enter your class label id")
    return parser

#converts bounding box coordinates into yolo data format
def convert_to_yolo(tracker_box, image, class_id):
    (x, y, w, h) = [int(dimension) for dimension in tracker_box]
    image_height, image_width = image.shape[:2]

    #normalizes box coordinates w/r to image size and find center of box
    x = x / image_width
    y = y / image_height
    w = w / image_width
    h = h / image_height
    x_center = x + (w/2)
    y_center = y + (h/2)
    #TODO double check YOLO data format
    yolo_data = [[class_id, x_center, y_center, w, h]]
    return yolo_data

#saves label in text file for corresponding image
def save_label(image, tracker_box, class_id, image_name, dataset_path):
    yolo_data = convert_to_yolo(tracker_box, image, class_id)
    label_train_path = Path(dataset_path / "raw_data/labels")
    label_train_path.mkdir(parents=True, exist_ok=True)
    file_path = label_train_path.joinpath(image_name + ".txt")

    with open(file_path, 'w') as f:
        np.savetxt(
            f,
            yolo_data,
            fmt=["%d", "%f", "%f", "%f", "%f"]
        )

def save_img(image, image_name, dataset_path, type):
    if type == "nonTest":
        image_train_path = Path(dataset_path / "raw_data/images")
    elif type == "test":
        image_train_path = Path(dataset_path / "images/test")
    
    image_train_path.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(image_train_path.joinpath(image_name + ".jpg")), image)

#Prints info on bottom left of screen and shows if it is background image or a detection image
def print_info_screen(type, image_count, frame):
    info = [
        ("Image type: ", type),
        ("Saved images: ", f'{image_count}')
    ]   
    frame_height = frame.shape[0]
    for (i, (type, saved_images)) in enumerate(info):
        text = "{}: {}".format(type, saved_images)
        cv2.putText(frame, text, (10, frame_height - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

class VideoLabeler:
    def __init__(self, file_name, class_name, frame_rate, class_id):
        self.file_name = file_name # video filename
        self.class_name = class_name # your class label name
        self.frame_rate = frame_rate # save per frame
        self.class_id = class_id # your class label id

        self.frame_count = 0 #counts number of frames 
        self.detect_image_count = 0 #counts number of saved detection images
        self.test_image_count = 0 #counts number of saved testing images
        self.back_image_count = 0 #counts number of saved background images
        self.bounding_box = None #bounding_box object
        self.bounding_box_toggle = False #activate/deactivate bounding_box
        self.tracker = cv2.TrackerCSRT_create()

    def start(self):
        video_capture = cv2.VideoCapture(self.file_name) #get video object
        #create output folder with class name
        dataset_path = Path("Datasets")
        dataset_path.mkdir(parents=True, exist_ok=True)
        class_file = dataset_path.joinpath("classes.txt")
        with open(class_file, 'w') as file:
            file.write(self.class_name)

        if not video_capture.isOpened():
            print("Error opening video stream or file. Try again")
            sys.exit()
        else:    
            cv2.namedWindow('Frame',cv2.WINDOW_NORMAL)
            cv2.resizeWindow('Frame',800,800)

            while video_capture.isOpened():
                retval, frame = video_capture.read()
                #if no more frame
                if not retval:
                    sys.exit()
                    break
                self.frame_count +=1
                image = frame.copy()
                
                if self.bounding_box is not None:
                    (success, tracker_box) = self.tracker.update(frame)
                    #checks if tracking is successful
                    if success:
                        (x, y, w, h) = [int(dimension) for dimension in tracker_box] #tracker box dimensions
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
                        if self.frame_count % self.frame_rate == 0:
                            self.detect_image_count +=1
                            image_name = f'{self.class_name}{self.detect_image_count}_' + datetime.now().strftime("%d.%m.%Y_%H.%M.%S") 
                            save_img(image, image_name, dataset_path, "nonTest")
                            save_label(image, tracker_box, self.class_id, image_name, dataset_path)
                    
                    print_info_screen("detection", self.detect_image_count, frame)
                
                cv2.imshow("Frame", frame)
                key = cv2.waitKey(0) & 0xFF

                #Press a to select/unselect bounding box, saving will take place automatically at the frame rate specified
                if key == ord("a"): 
                    self.bounding_box_toggle = not self.bounding_box_toggle
                    if self.bounding_box_toggle: 
                        try:
                            self.bounding_box = cv2.selectROI(
                                "Frame", frame, fromCenter=False, showCrosshair=True)
                            self.tracker.init(frame, self.bounding_box)
                        except:
                            print("Issue with ROI selection. Tracker cannot initialize")
                    else:
                        self.bounding_box = None
                
                #press s to save a frame as background image
                elif key == ord("s"):
                    self.back_image_count += 1
                    image_name = f'Background {self.back_image_count}_' + datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
                    print_info_screen("background", self.back_image_count, frame) 
                    save_img(image, image_name, dataset_path, "nonTest")
                    cv2.imshow("Frame", frame)
                    cv2.waitKey(500) #reshow frame with the information printed on the bottom left for 0.5seconds

                #press t to save a frame for the test dataset
                elif key == ord("t"):
                    self.test_image_count += 1
                    image_name = f'Background {self.test_image_count}_' + datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
                    print_info_screen("test", self.test_image_count, frame)
                    save_img(image, image_name, dataset_path, "test")
                    cv2.imshow("Frame", frame)
                    cv2.waitKey(500) #reshow frame with the information printed on the bottom left for 0.5seconds

                #exit 
                elif key == ord("q"):
                    break
                    
        
        video_capture.release()

    def stop(self):
        print("Exiting...")
        cv2.destroyAllWindows()


def main():
    parser = create_parser()
    args = vars(parser.parse_args())
    video_labeler = VideoLabeler(args["filePath"], args["className"], 
                                args["frameRate"], args["classId"])
    video_labeler.start()
    video_labeler.stop()


if __name__ == '__main__':
    main()

