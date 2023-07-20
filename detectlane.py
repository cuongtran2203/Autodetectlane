import torch
import cv2
import numpy as np 
from YOLO_detector import Detector
from loguru import logger
p1,p2,p3,p4=None,None,None,None
state=0
def get_area_detect(img, points):
    # points = points.reshape((-1, 1, 2))
    mask = np.zeros(img.shape[:2], np.uint8)
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
    dts = cv2.bitwise_and(img, img, mask=mask)
    return dts
def on_mouse(event, x, y, flags, userdata):
    global state, p1, p2,p3,p4
    # Left click
    if event == cv2.EVENT_LBUTTONDOWN:
        # Select first point
        if state == 0:
            p1 = [x,y]
            
            state += 1
        # Select second point
        elif state == 1:
            p2 = [x,y]
            state += 1
          # Select second point
        elif state == 2:
            p3 = [x,y]
            state += 1
          # Select second point
        elif state == 3:
            p4 = [x,y]
            state += 1
    # Right click (erase current ROI)
    if event == cv2.EVENT_LBUTTONDBLCLK:
        p1, p2,p3,p4 = None, None,None,None
        state = 0
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
                # print("Point check org :",check)
                count+=1
                check=point
                # print("Point swap :",check)
                # print('Found {} point '.format(count))
                check_1.append(point)
               
        # print("check 1 :",check_1)
        copy_list=check_1.copy()
        check_ss[str(ss)]=copy_list
        # print("check_ss",check_ss)
        # print("check_ss",check_1)
        for p in check_1:
            center_point.remove(p)
        check_1.clear()
        center_point=list(center_point)
        # print('center point :' ,center_point)
        # print(len(center_point))
        ss+=1
        if len(center_point)<1:
            final=False
        
            
    '''
    Trường hợp detect thiếu lane  
    '''
    list_lane=None
    if len(check_ss)<lane :
        print("không khớp  với đàu vào ")
        # x1,y1,x2,y2=roi
        # y_center=int((y2+y1)/2)
        list_sort_y=sorted(roi,key=lambda x:x[1])
        A=list_sort_y[0]
        B=list_sort_y[1]
        C=list_sort_y[2]
        D=list_sort_y[3]
        x_distance_1=abs(A[0]-B[0])
        y_min=min(A[1],B[1])
        x_distance_2=abs(C[0]-D[0])
        y_max=max(C[1],D[1])
        list_lane=[]
        for i in range(1,lane):
            x1=int(x_distance_1*i/lane)+min(A[0],B[0])
            y1=y_min
            x2=int(x_distance_2*i/lane)+min(C[0],D[0])
            y2=y_max
            list_lane.append([[x1,y1],[x2,y2]])
        logger.info("list lane :{}".format(list_lane))
    if len(check_ss)==lane :
        print("okkk")
    return check_ss,list_lane
        
    
    
        
        
        
    
if __name__=="__main__":
    img=cv2.imread("test2.jpg")
    img=cv2.resize(img,(1280,720))
    cv2.namedWindow('frame')
    cv2.setMouseCallback('frame', on_mouse)
    detector=Detector()
    while True :
        if p1 is not None and p2 is not None and p3 is not None and p4 is not None :
            
            pts=np.array([p1,p2,p3,p4],np.int32)
            list_pts=[p1,p2,p3,p4]
            print(pts)
            #crop frame 
            img_croped=get_area_detect(img,pts)
            cv2.polylines(img,[pts],True,(0,0,142),3)
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
            check_ss,list_lane=auto_lane(img,center_point=center_point,lane=1,threshold=200,roi=list_pts)
            for p in list_lane:
                cv2.line(img,tuple(p[0]),tuple(p[1]),(0,125,47),2)
            for key in check_ss.keys():
                for index, item in enumerate(check_ss[key]): 
                    if index == len(check_ss[key]) -1:
                        break
                    cv2.line(img, tuple(item), tuple(check_ss[key][index + 1]), [127, 255, 0], 2) 
            print("results :",check_ss)
            isClosed=False
            color=(0,0,255)
            # print(center_point)
            thickness=2
        # img=cv2.polylines(img,[np.array(center_point,np.int32)],isClosed,color,thickness)
        cv2.imshow("frame",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()