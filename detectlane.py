import torch
import cv2
import numpy as np 
from YOLO_detector import Detector
def auto_lane(img,lane=None,center_point=None,roi=None,threshold=200):
    final=True
    check_ss={}
    ss=0
    while final :
        check=center_point[0]
       
        count=1
        check_1=[]
        check_1.append(check)
        for point in center_point :
            
            if abs(check[0]-point[0])<threshold and check[1]<point[1]:
                # cv2.circle(img,tuple(check),10,(0,0,255),-1)
                print("Point check org :",check)
                count+=1
                check=point
                print("Point swap :",check)
                print('Found {} point '.format(count))
                check_1.append(point)
               
        print("check 1 :",check_1)
        copy_list=check_1.copy()
        check_ss[str(ss)]=copy_list
        print("check_ss",check_ss)
        print("check_ss",check_1)
        for p in check_1:
            center_point.remove(p)
        check_1.clear()
        center_point=list(center_point)
        print('center point :' ,center_point)
        print(len(center_point))
        ss+=1
        if len(center_point)<1:
            final=False
    if len(check_ss)<lane :
        print("không khớp  với đàu vào ")
        x1,y1,x2,y2=roi
        y_center=int((y2+y1)/2)
        
    if len(check_ss)==lane :
        print("okkk")
    

       
    return check_ss
        
    
    
        
        
        
    
if __name__=="__main__":
    img=cv2.imread("test1.jpg")
    img=cv2.resize(img,(1280,720))
    detector=Detector()
    bbox,label=detector.detect(img)
    # print(label)
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
    check_ss=auto_lane(img,center_point=center_point,lane=2)
    print("results :",check_ss)
    isClosed=False
    color=(0,0,255)
    # print(center_point)
    thickness=2
    # img=cv2.polylines(img,[np.array(center_point,np.int32)],isClosed,color,thickness)
    # cv2.imshow("result",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()