import torch
import cv2
import numpy as np 
from YOLO_detector import Detector
def auto_lane(lane=None,center_point=None,threshold=50):
    center_point=sorted(center_point)
    check=0
    
    
        
        
        
    
if __name__=="__main__":
    img=cv2.imread("test1.jpg")
    img=cv2.resize(img,(1280,720))
    detector=Detector()
    bbox,label=detector.detect(img)
    print(label)
    center_point=[]
    # print(np.sort(bbox))
    # auto_lane(lane=0,bbox=bbox)
    for box,l in zip(bbox,label) :
        box=list(map(int,box))
        if int(l)==0:
            mid_point=[int((box[0]+box[2])/2),int((box[1]+box[3])/2)]
            center_point.append(mid_point)
            
            img=cv2.rectangle(img,(box[0],box[1]),(box[2],box[3]),(255,0,0),1)
    center_point=sorted(center_point)
    isClosed=False
    color=(0,0,255)
    thickness=2
    img=cv2.polylines(img,[np.array(center_point,np.int32)],isClosed,color,thickness)
    cv2.imshow("result",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()