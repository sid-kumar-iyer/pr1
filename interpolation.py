import os
import random
import matplotlib.image as mpimg
import numpy as np
import cv2
import math as m
import random as r
import json




def bnd(x_rand,y_rand,img,angl):
    y_max,x_max= img.shape
    j=0
    theta=[]
    limit=[]
    dist=[]

    for i in angl:
        j+=1
        x, y, r=fnd(i,x_rand,y_rand,img)
        l=(y, x)
        theta.append(i)
        limit.append(l)
        dist.append(r)
    return theta,limit,dist




def fnd(theta,or_x,or_y,img):
    r=1
    y_max,x_max= img.shape
    
    while True:
        p_x=or_x + r * m.cos(theta)
        p_y=or_y + r * m.sin(theta)
        
        #print((p_y, p_x))
        
        if(p_x > x_max - 1 or p_y > y_max - 1 or p_x < 0 or p_y < 0):
            return m.inf,m.inf,r
       
        v=value(p_x,p_y,img)
        r+=1
        if(v>.9):
            return p_x,p_y,r



def value(x,y,img):
    
    dy, dx = y - m.floor(y), x - m.floor(x)
    y0, x0 = y, x
    y1, x1 = y0 + m.ceil(dy), x0 + m.ceil(dx)
    
    p1_x,p1_y=m.floor(x0),m.floor(y0)
    p2_x,p2_y=m.floor(x0),m.floor(y1)
    p3_x,p3_y=m.floor(x1),m.floor(y0)
    p4_x,p4_y=m.floor(x1),m.floor(y1)
    
    v_00 = img[p1_y, p1_x]
    v_01 = img[p3_y, p3_x]
    v_10 = img[p2_y, p2_x]
    v_11 = img[p4_y, p4_x]
    v = np.array([
        v_00, v_01, v_10, v_11
    ])
    
    f_00 = dy * dx
    f_01 = dy * (1 - dx)
    f_10 = (1 - dy) * dx
    f_11 = (1 - dy) * (1 - dx)
    f = np.array([
        f_00, f_01, f_10, f_11
    ])
    f = 1 / (f + 1e-8)
    f /= np.sum(f)
    return np.dot(v, f)

if __name__ == "__main__":
    box_img='/home/bvr/data/grapheks/box_thresh/dda031-lvl2-li-bl-lg.png'
    img=mpimg.imread(box_img)
    y_max,x_max= img.shape
    angl=[]
    res=[]
    k=1000
    for i in range(k):
        theta=(2 * m.pi)/k*i
        angl.append(theta)
    for j in range(1):
        origins=[]
        x_rand= r.randint(1,x_max-1)
        y_rand= r.randint(1,y_max-1)
        origins.extend((y_rand,x_rand))
        th,p0,r= bnd(x_rand,y_rand,img,angl)
        p= [(y, x) for y, x in p0 if x is not np.inf and y is not np.inf]
        l=len(p)
        p=np.array(p)
        jj,ii=np.nonzeo(np.where(p!=m.inf))
        
        result={'origin':'origin','theta':'th','r':'r','p':'p','num_points':'l'}
        res.append(result)
    with open('test.json', 'w') as outfile:
        json.dump(res, outfile)
    

        