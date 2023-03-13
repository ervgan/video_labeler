### Run

**run pip requirements.txt to install dependencies**

**how to run example** `python3 auto_label.py -filePath 'fileName' --className 'label' --frameRate 1 --classId 0`

##Args

-v --filePath
   type=str, path to video file
   
-c --className
   type=str, default="label", class name label
   
-f --frameRate
   type=int, default=1, frame rate
   
-i --classId
   type=int, default=0, Enter your class label id


## Hotkeys
~~~~~~~
+--------------------+----------------------+
| a           | Create/Cancel a rect box    		     
+--------------------+----------------------+
| s           | capture and save frame for background     
+--------------------+----------------------+
| t           | capture and save frame for test       
+--------------------+----------------------+
| Space bar   | Move forward in frames      
+--------------------+----------------------+
| q           | close the video             
+--------------------+----------------------+

                
