import cv2
import os
import sys 

while True:
    # Get a list of all the text files in the directory
    label_path = "Datasets/raw_data/labels/"
    image_path = "Datasets/raw_data/images/"
    text_files = [f for f in os.listdir(label_path) if f.endswith(".txt")]
    for text_file in text_files:
        # Get the image name
        image_name = image_path + text_file.replace(".txt", ".jpg")

        # Load the image
        img = cv2.imread(image_name)
        #cv2.resize(img, None, fx=0.5, fy=0.5)
        # Read the YOLO detection data from the text file
        text_file = label_path + text_file
        with open(text_file) as f:
            lines = f.readlines()
        # Parse the detection data
        detections = []
        for line in lines:
            data = line.strip().split()
            class_id = int(data[0])
            x_center = float(data[1])
            y_center = float(data[2])
            width = float(data[3])
            height = float(data[4])
            detections.append([class_id, x_center, y_center, width, height])
        # Loop through the detections
        for detection in detections:
            class_id, x_center, y_center, width, height = detection
            # Convert the center coordinates and width/height to bounding box coordinates
            xmin = int((x_center - width/2) * img.shape[1])
            ymin = int((y_center - height/2) * img.shape[0])
            xmax = int((x_center + width/2) * img.shape[1])
            ymax = int((y_center + height/2) * img.shape[0])

            # Draw the bounding box on the image
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            # Display the class label and confidence score
            cv2.putText(img, f"{class_id}", (xmin, ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Show the image
        cv2.imshow(image_name, img)
        key = cv2.waitKey(0)
        if key == ord("q"):
            sys.exit()
        cv2.destroyAllWindows()
    # Sleep for a while before checking for new text files
    #time.sleep(3)