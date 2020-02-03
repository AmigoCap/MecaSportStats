#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:39:29 2019

@author: gabin
"""

import numpy as np
import matplotlib.pyplot as plt
import math as m
from scipy.spatial import Voronoi, voronoi_plot_2d

def voronoi(events,event_id,mom_id):
    event=events[event_id]
    moment=event['moments'][mom_id][5] # we only take the five index of moment info because it contains players' and ball's position
    points = np.array([[player[2],player[3]] for player in moment[1:]])
    vor = Voronoi(points)
    fig = voronoi_plot_2d(vor, show_vertices=False, line_colors='black',line_width=1, line_alpha=0.6, point_size=0)
    plt.xlim(0,94) #force the plt.show to adapt the size
    plt.ylim(0,50)
    plt.xlabel('x in feet')
    plt.ylabel('y in feet')

def players_ball_speed_position(moment1,moment2):
    
    dt=moment1[2]-moment2[2]
    mom_infos={}
    mom_infos['ball']={}
    mom_infos['team1']={}
    mom_infos['team2']={}
    for i in range(11) :
        if i==0:
            mom_infos['ball']['xy']=np.array(moment1[5][i][2:4])
            mom_infos['ball']['z']=moment1[5][i][4]
            if dt==0.0:
                mom_infos['ball']['v']=np.array([0,0])
            else:
                mom_infos['ball']['v']=np.array([(moment2[5][i][2]-moment1[5][i][2])/dt,(moment2[5][i][3]-moment1[5][i][3])/dt])
        if 6<=i<=11:
            if dt==0.0:
                mom_infos['team2'][str(moment1[5][i][1])]={'xy':np.array(moment1[5][i][2:4]),'v':np.array([0,0])}
            else:
                mom_infos['team2'][str(moment1[5][i][1])]={'xy':np.array(moment1[5][i][2:4]),'v':np.array([(moment2[5][i][2]-moment1[5][i][2])/dt,(moment2[5][i][3]-moment1[5][i][3])/dt])}
        if 1<=i<=5:
            if dt==0.0:
                mom_infos['team1'][str(moment1[5][i][1])]={'xy':np.array(moment1[5][i][2:4]),'v':np.array([0,0])}
            else :
                mom_infos['team1'][str(moment1[5][i][1])]={'xy':np.array(moment1[5][i][2:4]),'v':np.array([(moment2[5][i][2]-moment1[5][i][2])/dt,(moment2[5][i][3]-moment1[5][i][3])/dt])}
    return(mom_infos)

def distance(a,b):      #a = (x,y) departure point ; b = (i,j) arrival point
    return m.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def distance_difference(mom_infos,b):
    'distance difference between closest player of each team to the point b'
    
    dmin1=np.inf
    
    for player in mom_infos['team1'].keys():
        a=mom_infos['team1'][player]['xy']
        d=distance(a,b)
        if d<dmin1:
            dmin1=d
            
    dmin2=np.inf
            
    for player in mom_infos['team2'].keys():
        a=mom_infos['team2'][player]['xy']
        d=distance(a,b)
        if d<dmin2:
            dmin2=d
            
    return(dmin1-dmin2)
    
def print_court_players(fig,ax,events,event_id,mom_id,n=50,p=94):
    event=events[event_id]
    moment=event['moments'][mom_id]
    team1=moment[5][1][0]
    team2=moment[5][-1][0]
    
    for k in range(len(moment[5])):
        if moment[5][k][0]==-1:
            ax.plot(moment[5][k][2],moment[5][k][3],'yo')
        if moment[5][k][0]==team1:
            ax.plot(moment[5][k][2],moment[5][k][3],'ro',markersize=12,alpha=0.6)
            ax.annotate(str(moment[5][k][1]),(moment[5][k][2],moment[5][k][3]),xytext=(3,3),textcoords='offset points')
        if moment[5][k][0]==team2:
            ax.plot(moment[5][k][2],moment[5][k][3],'bo',markersize=12,alpha=0.6)
            ax.annotate(str(moment[5][k][1]),(moment[5][k][2],moment[5][k][3]),xytext=(3,3),textcoords='offset points')
    
        

def print_court_teams_occupation(events,event_id,mom_id,voronoi_cut=False,value=False,player_info=False,n=50,p=94):
    "This function return a visualization of the court for the moment mom_id of the event event_id. If voronoi_cut=True, voronoi cutting is plotted. Then, if value=True, a heat-map giving a value to space occupation is drawn."
    if voronoi_cut:
        voronoi(events,event_id,mom_id)
    event=events[event_id]
    moment=event['moments'][mom_id]
    moment1=moment
    moment2=event['moments'][mom_id+1]
    
    # separation of ball, team1 and team2 and calculation of the speed
    mom_infos=players_ball_speed_position(moment1,moment2)
    
    ind=1
    for player in mom_infos['team2'].keys():
        x=mom_infos['team2'][player]['xy'][0]
        y=mom_infos['team2'][player]['xy'][1]
        vx=mom_infos['team2'][player]['v'][0]
        vy=mom_infos['team2'][player]['v'][1]
        plt.plot(x,y,'bo',markersize=12,alpha=0.6)
        plt.arrow(x,y,vx,vy,shape='full',lw=1.5,head_width=1)
        if player_info:
            plt.annotate(str(ind),(x,y),xytext=(3,3),textcoords='offset points')
            ind+=1
    
    for player in mom_infos['team1'].keys():
        x=mom_infos['team1'][player]['xy'][0]
        y=mom_infos['team1'][player]['xy'][1]
        vx=mom_infos['team1'][player]['v'][0]
        vy=mom_infos['team1'][player]['v'][1]
        plt.plot(x,y,'ro',markersize=12,alpha=0.6)
        plt.arrow(x,y,vx,vy,shape='full',lw=1.5,head_width=1)
        if player_info:
            plt.annotate(str(ind),(x,y),xytext=(3,3),textcoords='offset points')
            ind+=1
    if value:
        court=np.zeros((n,p))
        for i in range(n):
            for j in range(p):
                b=np.array([j,i]) # point d'arrivée
            
                dmin_1=np.inf
                for player in mom_infos['team1'].keys():
                    a=mom_infos['team1'][player]['xy']
                    d=distance(a,b)
                    if d<dmin_1:
                        dmin_1=d
                    
                dmin_2=np.inf
                for player in mom_infos['team2'].keys():
                    a=mom_infos['team2'][player]['xy']
                    d=distance(a,b)
                    if d<dmin_2:
                        dmin_2=d
                court[i,j]=dmin_1-dmin_2
        im=plt.imshow(court,origin='lower', cmap='RdBu')
        #plt.colorbar(orientation='vertical')
        
    plt.plot(mom_infos['ball']['xy'][0],mom_infos['ball']['xy'][1],'yo')
    plt.xlabel('x in feet')
    plt.ylabel('y in feet')
    field = plt.imread("Images/fullcourt.png")
    plt.imshow(field, extent=[0,94,0,50])
    plt.show()

def time_to_point(a,b,v,F=10*3.281):   
    "time to go from a to b with initial speed v, F is the force parameter in feet/s-2"
    x0,y0=a
    xf,yf=b
    X=x0-xf
    Y=y0-yf
    k4=1
    k3=0
    k2=4*(v[0]**2+v[1]**2)/F**2
    k1=8*(v[0]*X+v[1]*Y)/F**2
    k0=4*(X**2+Y**2)/F**2
    times=np.roots([k4,k3,-k2,-k1,-k0])
    for i in range(4):                      # Selection of the root real and positive
        if times[i].imag==0:
            if times[i].real>=0:
                return times[i].real
    print('error')
    
def time_difference(mom_infos,b):
    
    tmin_1=np.inf
    for player in mom_infos['team1'].keys():
        a=mom_infos['team1'][player]['xy']
        v=mom_infos['team1'][player]['v']
        t=time_to_point(a,b,v)
        if t<tmin_1:
            tmin_1=t
                    
    tmin_2=np.inf
    for player in mom_infos['team2'].keys():
        a=mom_infos['team2'][player]['xy']
        v=mom_infos['team2'][player]['v']
        t=time_to_point(a,b,v)
        if t<tmin_2:
            tmin_2=t
    
    return(tmin_1-tmin_2)
    
def print_court_teams_occupation_inertia(events,event_id,mom_id,voronoi_cut=False,player_info=False,n=50,p=94):
    "This function return a visualization of the court for the moment mom_id of the event event_id. If voronoi_cut=True, voronoi cutting is plotted. Then, if value=True, a heat-map giving a value to space occupation is drawn."
    if voronoi_cut:
        voronoi(events,event_id,mom_id)
    event=events[event_id]
    moment=event['moments'][mom_id]
    moment1=moment
    moment2=event['moments'][mom_id+1]
    
    # separation of ball, team1 and team2 and calculation of the speed
    mom_infos=players_ball_speed_position(moment1,moment2)
    
    ind=1
    for player in mom_infos['team2'].keys():
        x=mom_infos['team2'][player]['xy'][0]
        y=mom_infos['team2'][player]['xy'][1]
        vx=mom_infos['team2'][player]['v'][0]
        vy=mom_infos['team2'][player]['v'][1]
        plt.plot(x,y,'bo',markersize=12,alpha=0.6)
        plt.arrow(x,y,vx,vy,shape='full',lw=1.5,head_width=1)
        if player_info:
            plt.annotate(str(ind),(x,y),xytext=(3,3),textcoords='offset points')
            ind+=1
    
    for player in mom_infos['team1'].keys():
        x=mom_infos['team1'][player]['xy'][0]
        y=mom_infos['team1'][player]['xy'][1]
        vx=mom_infos['team1'][player]['v'][0]
        vy=mom_infos['team1'][player]['v'][1]
        plt.plot(x,y,'ro',markersize=12,alpha=0.6)
        plt.arrow(x,y,vx,vy,shape='full',lw=1.5,head_width=1)
        if player_info:
            plt.annotate(str(ind),(x,y),xytext=(3,3),textcoords='offset points')
            ind+=1
            
    court=np.zeros((n,p))
    for i in range(n):
        for j in range(p):
            b=np.array([j,i]) # point d'arrivée
        
            tmin_1=np.inf
            for player in mom_infos['team1'].keys():
                a=mom_infos['team1'][player]['xy']
                v=mom_infos['team1'][player]['v']
                t=time_to_point(a,b,v)
                if t<tmin_1:
                    tmin_1=t
                    
            tmin_2=np.inf
            for player in mom_infos['team2'].keys():
                a=mom_infos['team2'][player]['xy']
                v=mom_infos['team2'][player]['v']
                t=time_to_point(a,b,v)
                if t<tmin_2:
                    tmin_2=t
            
            court[i,j]=tmin_1-tmin_2
    im=plt.imshow(court,origin='lower', cmap='RdBu')
    #plt.colorbar(orientation='vertical')
        
    plt.plot(mom_infos['ball']['xy'][0],mom_infos['ball']['xy'][1],'yo')
    plt.xlabel('x in feet')
    plt.ylabel('y in feet')
    field = plt.imread("Images/fullcourt.png")
    plt.imshow(field, extent=[0,94,0,50])
    plt.show()

def test_moment(moment): #looking if there is the ball and 10 players
    if len(moment[5])!=11:
        return(False)
    for i in range(len(moment[5])):
        if len(moment[5][i])!=5:
            return (False)
    return(True)

def distance_closest_opponent(moment,player_id):
    
    dmin=np.inf
    team_player=0
    players=moment[5]
    player=None
    
    for k in range(len(players)):
        if players[k][1]==player_id:
            team_player=players[k][0]
            player=players[k][2:4]
            
    for k in range(len(players)):
        if players[k][0]!=team_player and players[k][0]!=-1:
            d=distance(players[k][2:4],player)
            if d<dmin:
                dmin=d
            
    return(dmin)

def time_closest_opponent(moment1,moment2,player_id):
    
    tmin=np.inf
    team_player=0
    players=moment1[5]
    players2=moment2[5]
    player=None
    
    for k in range(len(players)):
        if players[k][1]==player_id:
            team_player=players[k][0]
            player=players[k][2:4]
    
    dt=moment1[2]-moment2[2]
    for k in range(len(players)):
        if players[k][0]!=team_player and players[k][0]!=-1:
            for l in range(len(players2)):
                if players2[l][1]==players[k][1]:
                    if dt==0:
                        v=[0,0]
                    else:
                        v=[(players2[l][2]-players[k][2])/dt,(players2[l][3]-players[k][3])/dt]
                    t=time_to_point(players[k][2:4],player,v)
                    if t<tmin:
                        tmin=t
            
    return(tmin)
    
def animation_print_court_teams_occupation_inertia(fig,ax,moment1,moment2,voronoi_cut=False,player_info=False,n=50,p=94):
    "This function return a visualization of the court for the moment mom_id of the event event_id. If voronoi_cut=True, voronoi cutting is plotted. Then, if value=True, a heat-map giving a value to space occupation is drawn."
    
    # separation of ball, team1 and team2 and calculation of the speed
    mom_infos=players_ball_speed_position(moment1,moment2)
    
    ind=1
    for player in mom_infos['team2'].keys():
        x=mom_infos['team2'][player]['xy'][0]
        y=mom_infos['team2'][player]['xy'][1] 
        vx=mom_infos['team2'][player]['v'][0]
        vy=mom_infos['team2'][player]['v'][1]
        if player=='202691':
            ax.plot(x,y,'go',markersize=60,alpha=0.5)
        ax.plot(x,y,'bo',markersize=25,alpha=1)
        ax.arrow(x,y,vx,vy,shape='full',lw=1.5,head_width=1)
        if player_info:
            ax.annotate(str(ind),(x,y),xytext=(3,3),textcoords='offset points')
            ind+=1
    
    for player in mom_infos['team1'].keys():
        x=mom_infos['team1'][player]['xy'][0]
        y=mom_infos['team1'][player]['xy'][1]
        vx=mom_infos['team1'][player]['v'][0]
        vy=mom_infos['team1'][player]['v'][1]
        if player=='202691':
            ax.plot(x,y,'go',markersize=60,alpha=0.5)
        ax.plot(x,y,'ro',markersize=25,alpha=1)
        ax.arrow(x,y,vx,vy,shape='full',lw=1.5,head_width=1)
        if player_info:
            ax.annotate(str(ind),(x,y),xytext=(3,3),textcoords='offset points')
            ind+=1
            
    court=np.zeros((n,p))
    for i in range(n):
        for j in range(p):
            b=np.array([j,i]) # point d'arrivée
        
            tmin_1=np.inf
            for player in mom_infos['team1'].keys():
                a=mom_infos['team1'][player]['xy']
                v=mom_infos['team1'][player]['v']
                t=time_to_point(a,b,v)
                if t<tmin_1:
                    tmin_1=t
                    
            tmin_2=np.inf
            for player in mom_infos['team2'].keys():
                a=mom_infos['team2'][player]['xy']
                v=mom_infos['team2'][player]['v']
                t=time_to_point(a,b,v)
                if t<tmin_2:
                    tmin_2=t
            
            court[i,j]=tmin_1-tmin_2
    im=ax.imshow(court,origin='lower', cmap='RdBu', vmin=-1.1,vmax=1.1)
    #plt.colorbar(orientation='vertical')
        
    ax.plot(mom_infos['ball']['xy'][0],mom_infos['ball']['xy'][1],'yo',markersize=20)
    field = plt.imread("../Images/fullcourt.png")
    ax.imshow(field, extent=[0,94,0,50])
    #plt.savefig('../animation_frames/frame%d.jpg' % mom_id)
    #plt.show()
    
def distance_closest_def(moments,j,who_ball):
    
    dmin=[np.inf,0]
    team_player=0
    players=moments[j][5]
    player=None
    
    for k in range(len(players)):
        if players[k][1]==who_ball:
            team_player=players[k][0]
            player=players[k][2:4]
            
    for k in range(len(players)):
        if players[k][0]!=team_player and players[k][0]!=-1:
            d=distance(players[k][2:4],player)
            if d<dmin[0]:
                dmin=[d,players[k][2:4]]
            
    return(dmin)
    
def time_closest_def(moments,j,who_ball):
    
    tmin=np.inf
    team_player=0
    players=moments[j][5]
    players2=moments[j+1][5]
    player=None
    
    for k in range(len(players)):
        if players[k][1]==who_ball:
            team_player=players[k][0]
            player=players[k][2:4]
    
    dt=moments[j][2]-moments[j+1][2]
    for k in range(len(players)):
        if players[k][0]!=team_player and players[k][0]!=-1:
            for l in range(len(players2)):
                if players2[l][1]==players[k][1]:
                    if dt==0:
                        v=[0,0]
                    else:
                        v=[(players2[l][2]-players[k][2])/dt,(players2[l][3]-players[k][3])/dt]
                    t=time_to_point(players[k][2:4],player,v)
                    if t<tmin:
                        tmin=t
            
    return(tmin)
    
def player_with_ball(moments,i):    # return the ID of the player who has the ball
    players=moments[i][5][1:]
    ball=moments[i][5][0][2:5]
    if ball[2]>2.5*3.28:
        return(0)
    else :
        dmin=[np.inf,0]
        for k in range(len(players)):
            d=m.sqrt((players[k][2]-ball[0])**2+(players[k][3]-ball[1])**2)
            if d<dmin[0] and d<1.6: #only if ball is at less than 50cm of the player
                dmin=[d,players[k][1]]
        return dmin[1]
    
    return(0)
    
def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / N