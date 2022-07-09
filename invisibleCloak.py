import os
import cv2
import time
import argparse
import numpy as np


def useCloak(color,save,out):
    '''
    Python program to simulate invisibility cloak (using opencv library)
    '''

    cap = cv2.VideoCapture(0)
    if save:
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        if out!="":
            path = os.path.join(out,f'vid_{time.time()}.avi')
        else:
            path = f'Videos/vid_{time.time()}.avi'
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(path, fourcc, 20.0, (frame_width,frame_height))

    time.sleep(1)

    for i in range(20):
        ret , background_img = cap.read()

    if cap.isOpened():
        # print("\nCapturing..")

        while True:
            
            ret, frame = cap.read()
            if not ret:
                continue

            frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)  ## Hue Saturation Value
            
            if color=='blue':
                ## Mask 1 : Taking frame captured, finding the place where cloak is, and getting that area
                blue_min = np.array([100,50,45]) 
                blue_max = np.array([135,255,255])
                mask = cv2.inRange(frame_hsv, blue_min,blue_max)

                ## Final Cloak Mask
                cloak_mask = mask

            if color=='green':
                ## Mask 1 : Taking frame captured, finding the place where cloak is, and getting that area
                green_min = np.array([45,50,50]) 
                green_max = np.array([80,255,255])
                mask = cv2.inRange(frame_hsv, green_min,green_max)

                ## Final Cloak Mask
                cloak_mask = mask

            if color=='red':
                ## Mask 1 : Taking frame captured, finding the place where cloak is, and getting that area
                red_min1 = np.array([0,220,50]) 
                red_max1 = np.array([9,245,255])
                mask1 = cv2.inRange(frame_hsv, red_min1,red_max1)
                
                ## Mask 2 : Taking frame captured, finding the place where cloak is, and getting that area
                red_min2 = np.array([170,220,50]) 
                red_max2 = np.array([179,255,255])
                mask2 = cv2.inRange(frame_hsv, red_min2, red_max2)
                
                ## Final Cloak Mask
                cloak_mask = mask1 + mask2
   


            # removing noise from the mask
            cloak_mask = cv2.morphologyEx(cloak_mask, cv2.MORPH_OPEN,np.ones((3,3),np.uint8),iterations=2)
            cloak_mask = cv2.morphologyEx(cloak_mask, cv2.MORPH_DILATE,np.ones((4,4),np.uint8),iterations=1)
            
            cloak_mask_inv = cv2.bitwise_not(cloak_mask)
            
            background_cloak_mask = cv2.bitwise_and(background_img,background_img,mask=cloak_mask)
            new_frame = cv2.bitwise_and(frame,frame,mask=cloak_mask_inv)
            
            final_frame = cv2.addWeighted(background_cloak_mask,1,new_frame,1,0)
            
            cv2.namedWindow('Invisible Cloak',cv2.WINDOW_NORMAL)

            cv2.resizeWindow('Invisible Cloak', 960,640)

            if save:
                out.write(final_frame)

            cv2.imshow("Invisible Cloak",final_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        print("Your camera is not working\n Exiting..")

    if save:
        out.release()    
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-c","--color", help="set color of the cloak", type=str, choices=['red', 'green', 'blue'],default='red')
    parser.add_argument("--save", help="save your video", action="store_true")
    parser.add_argument("-out","--output",type=str , help="path to the directory where you want to save the video", default="")
    
    args = parser.parse_args()

    print("\nPlease use --color or -c argument to choose color of your cloak (default='red').\nUse -h to check other options.")
    print("\npress 'q' to exit.")

    useCloak(args.color,args.save,args.output)
