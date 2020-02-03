#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 14:38:43 2019

@author: gabin
"""

import cv2
import matplotlib.pyplot as plt
import space as sp
from data_extracter import json_extracter
import json

#print('Récupération de la vidéo frame par frame')
#vidcap = cv2.VideoCapture('../data/thompson_shot1280x720.mp4')
#fps = vidcap.get(cv2.CAP_PROP_FPS) # getting video framerate
#success,image = vidcap.read()
#count = 0
#success = True
#while success:
#    cv2.imwrite("../data/video_frames/frame%d.jpg" % count, image,[int(cv2.IMWRITE_JPEG_QUALITY), 90])     # save frame as JPEG file
#    success,image = vidcap.read()
#    #print ('Read a new frame: ', success)
#    count += 1
    
def animation_video(path,event_ind,eventId=None):
    print('Tracé animation frame par frame')
    with open(path) as json_file:  
        data = json.load(json_file)
        events=data['events']
    
    if eventId==None:
        moments=events[event_ind]['moments']
    else :
        j=0
        while j<len(events) and events[j]['eventId']!=eventId:
            j+=1
    
    if j==len(events):
        return('event non trouvé')
    moments=events[j]['moments']
    n=len(moments)-40
    #n=150
    os.chdir('D:\Documents\MecaSportCo\python_files')
    # Tracer frame par frame de l'animation
    fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,figsize=(50,30)) # rajouter autant d'axes que souhaité et ajuster figsize
    ax3bis=ax3.twinx()
    ax4bis=ax4.twinx()
    
    field = plt.imread("../Images/fullcourt.png")
    #ax1.imshow(field, extent=[0,94,0,50])
    print(n)
    d=[]
    t=[]
    time=[]
    d2=[]
    t2=[]
    shot_time=539.54
    catch_time=moments[258][2]
    window=5
    for k in range(n):
        print(k)
        field = plt.imread("../Images/fullcourt.png")
        ax1.imshow(field, extent=[0,94,0,50])
        ax1.axis('off')
        ax1.set_ylim((50,0))
        moment1=moments[k]
        moment2=moments[k+1]
        sp.animation_print_court_teams_occupation_inertia(fig,ax1,moment1,moment2,n=50,p=94)
        
        d.append(sp.distance_closest_def(moments,k,202691)[0])
        t.append(sp.time_closest_def(moments,k,202691))
        time.append(moments[k][2])
        #ax3bis.set_yticks([])
        ax3.plot(time[1:],d[1:],'r',linewidth=5)
        ax3.set_ylim((0,16))
        ax3.tick_params(labelsize=30,width=2,length=10)
        ax3bis.tick_params(labelsize=30,width=2,length=10)
        ax3.set_xlabel(r'Time [s]',fontsize=40)
        ax3.set_ylabel(r'$\delta_{space}^*(t)$ [s]',fontsize=40,color='red')
        ax3bis.set_ylabel(r'$\delta_{time}^*(t)$ [s]',fontsize=40,color='blue')
        if moments[k][2]>(moments[0][2]-window+1):
            ax3.set_xlim((moments[0][2],moments[0][2]-5))
            ax4.set_xlim((moments[0][2],moments[0][2]-5))
            
        else :
            ax3.set_xlim((moments[k][2]+4,moments[k][2]-1))
            ax4.set_xlim((moments[k][2]+4,moments[k][2]-1))
        ax3bis.plot(time[1:],sp.running_mean(t,2),'b',linewidth=5)
        ax3bis.set_ylim((0,1.5))
        
        if (k-188)*2.4<500 and k>188: #synchronization
            img = cv2.imread('D:/Documents/MecaSportCo/data/video_frames/frame%d.jpg' % int((k-188)*2.4))
            RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im1=ax2.imshow(RGB_img)
        ax2.axis('off')
        
        if k>257:
            ax3.axvline(catch_time,linestyle='dashed',linewidth=3)
            ax4.axvline(catch_time,linestyle='dashed',linewidth=3)
            #ax3.annotate('catch time',(catch_time,15),fontsize=40)
            #ax4.annotate('catch time',(catch_time,15),fontsize=40)
                
            #if moments[k][2]<shot_time:
            ax3.axvline(shot_time,linestyle='dashed',linewidth=3)
            ax4.axvline(shot_time,linestyle='dashed',linewidth=3)
            #ax3.annotate('shot time',(shot_time,15),fontsize=40)
            #ax4.annotate('shot time',(shot_time,15),fontsize=40)
            ax3.annotate("",xy=(catch_time,12.5),xytext=(shot_time,12.5),arrowprops=dict(arrowstyle="<->",linewidth=5))
            ax3.annotate("release time="+str(round(catch_time-shot_time,2))+'s',xy=(catch_time-0.25,13),fontsize=40,horizontalalignment='center')
            ax4.annotate("",xy=(catch_time,12.5),xytext=(shot_time,12.5),arrowprops=dict(arrowstyle="<->",linewidth=5))
            ax4.annotate("release time="+str(round(catch_time-shot_time,2))+'s',xy=(catch_time-0.25,13),fontsize=40,horizontalalignment='center')
        
        for i in range(1,11):
            p=moments[k][5][i][1]
            pos_player=moments[k][5][i][2:4]
            pos_closest_def=sp.distance_closest_def(moments,k,p)[1]
            ax1.plot([pos_player[0],pos_closest_def[0]],[pos_player[1],pos_closest_def[1]],'green',linewidth=4)
        
        player2=sp.player_with_ball(moments,k)
        if player2!=0:
            player=player2
        d2.append(sp.distance_closest_def(moments,k,player)[0])
        t2.append(sp.time_closest_def(moments,k,player))
        
        ax4.set_xlabel(r'Time [s]',fontsize=40)
        ax4.set_ylabel(r'$\delta_{space}^*(t)$ [s]',fontsize=40,color='red')
        ax4bis.set_ylabel(r'$\delta_{time}^*(t)$ [s]',fontsize=40,color='blue')
        ax4.set_ylim((0,16))
        ax4.tick_params(labelsize=30,width=2,length=10)
        ax4bis.tick_params(labelsize=30,width=2,length=10)
        ax4bis.set_ylim((0,1.5))
        #ax4.set_xlim((moments[0][2],moments[-1][2]))
        ax4.plot(time[1:],d2[1:],'r',linewidth=5)
        
        ax4bis.plot(time[1:],sp.running_mean(t2,2),'b',linewidth=5)
        
        ax3.set_title("Thompson's free space evolution",fontsize=50)
        ax4.set_title("Ball owner's free space evolution",fontsize=50)
            
        plt.savefig('../data/animation_frames/frame%d.jpg' % k)
        ax1.clear()
        ax2.clear()
        ax3.clear()
        ax3bis.clear()
        ax4.clear()
        ax4bis.clear()

        
    print('écriture de la vidéo')
    # création vidéo à partir des frames précédentes
    
    ## taille des images
    img=cv2.imread('../data/animation_frames/frame1.jpg')
    height, width, channels = img.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter('../data/video.avi', fourcc, float(25), (width, height)) # mettre le chemin où on souhaite enregistrer l'animation
    
    for i in range(n):
        frame = cv2.imread('../data/animation_frames/frame%d.jpg' % i)
        video.write(frame)
    video.release()

    
def quick_animation(path,event_ind,eventId=None):
    print('Tracé animation frame par frame')
    with open(path) as json_file:  
        data = json.load(json_file)
        events=data['events']
    
    if eventId==None:
        moments=events[event_ind]['moments']
    else :
        j=0
        while j<len(events) and events[j]['eventId']!=eventId:
            j+=1
    
    if j==len(events):
        return('event non trouvé')
    moments=events[j]['moments']
    n=len(moments)-1
    os.chdir('D:\Documents\MecaSportCo\python_files')
    # Tracer frame par frame de l'animation
    fig, ax = plt.subplots(1,1,figsize=(15,8)) # rajouter autant d'axes que souhaité et ajuster figsize
    field = plt.imread("../Images/fullcourt.png")
    ax.imshow(field, extent=[0,94,0,50])
    print(n)
    for k in range(n):
        field = plt.imread("../Images/fullcourt.png")
        ax.imshow(field, extent=[0,94,0,50])
        ax.set_ylim((50,0))
        
        sp.print_court_players(fig,ax,events,j,k,n=50,p=94)
    
        plt.savefig('../data/animation_frames/frame%d.jpg' % k)
        plt.cla()
    
    print('écriture de la vidéo')
    # création vidéo à partir des frames précédentes
    
    ## taille des images
    img=cv2.imread('../data/animation_frames/frame1.jpg')
    height, width, channels = img.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter('../data/video.avi', fourcc, float(25), (width, height)) # mettre le chemin où on souhaite enregistrer l'animation
    
    for i in range(n):
        frame = cv2.imread('../data/animation_frames/frame%d.jpg' % i)
        video.write(frame)
    video.release()
