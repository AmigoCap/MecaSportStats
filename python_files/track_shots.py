#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:19:06 2019

@author: gabin
"""

import numpy as np
import math as m
import os
import json
import pickle


def distance(a,b):      #a = (x,y) point de départ ; b = (i,j) point d'arrivée ; v = norme pour l'instant
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def where_attack(moments,j):
    ball=moments[j][5][0][2:5]
    x_mid=94/2
    if (ball[0]-x_mid)<0:
        return(1)
    else :
        return(2)

def player_with_ball(moments,i):    # return the ID of the player who has the ball
    players=moments[i][5][1:]
    ball=moments[i][5][0][2:5]
    if ball[2]>2.5*3.28:
        return(0)
    else :
        dmin=[m.sqrt((players[0][2]-ball[0])**2+(players[0][3]-ball[1])**2),players[0][1]]
        for k in range(1,len(players)):
            d=m.sqrt((players[k][2]-ball[0])**2+(players[k][3]-ball[1])**2)
            if d<dmin[0]:
                dmin=[d,players[k][1]]
        return dmin[1]
    
def player_with_ball_bis(moments,i):    # return the position of the player who has the ball
    players=moments[i][5][1:]
    ball=moments[i][5][0][2:5]
    dmin=[m.sqrt((players[0][2]-ball[0])**2+(players[0][3]-ball[1])**2),players[0][1]]
    for k in range(1,len(players)):
        d=m.sqrt((players[k][2]-ball[0])**2+(players[k][3]-ball[1])**2)
        if d<dmin[0]:
            dmin=[d,players[k][1]]
    return dmin[1]
    
def behind_three_point_line(p,where):
    coin=False
    if where==1 :
        basket_pos=[5.25,25]
        if p[0]<15:
            coin=True
    else :
        basket_pos=[94-5.25,25]
        if p[0]>(94-15):
            coin=True
    if coin : 
        if 0<p[1]<3.5 or 50-3.5<p[1]<50 : 
            return (True,basket_pos)
        else :
            return (False,basket_pos)
    else :
        if distance(p,basket_pos)>23.5 :  #In fact 23.75 but we take a marge to have all shoots
            return (True,basket_pos)
        else:
            return (False,basket_pos)


def distance_closest_def(moments,j,who_ball):
    
    dmin=np.inf
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
            if d<dmin:
                dmin=d
            
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
    print('error',times,v,a,b)

def test_moment(moment):
    if len(moment[5])!=11:
        return(False)
    for i in range(len(moment[5])):
        if len(moment[5][i])!=5:
            return (False)
    return(True)

def position_player_with_ball(moments,i):
    players=moments[i][5][1:]
    ball=moments[i][5][0][2:5]
    if ball[2]>2.5*3.28:
        return(0)
    else :
        dmin=[m.sqrt((players[0][2]-ball[0])**2+(players[0][3]-ball[1])**2),0]
        for k in range(1,len(players)):
            d=m.sqrt((players[k][2]-ball[0])**2+(players[k][3]-ball[1])**2)
            if d<dmin[0]:
                dmin=[d,k]
        return players[dmin[1]][2:4]

def position_player_with_ball_bis(moments,i):
    players=moments[i][5][1:]
    ball=moments[i][5][0][2:5]
    dmin=[m.sqrt((players[0][2]-ball[0])**2+(players[0][3]-ball[1])**2),0]
    for k in range(1,len(players)):
        d=m.sqrt((players[k][2]-ball[0])**2+(players[k][3]-ball[1])**2)
        if d<dmin[0]:
            dmin=[d,k]
    return players[dmin[1]][2:4]
    
def track_event_shots(moments,t_end,w_ball,w_reception,TIME_SHOTS,pos,m_id):
    
    time_shots=TIME_SHOTS
    time=t_end
    
    d_closest_def=[]
    t_closest_def=[]
    time_to_shoot=[]
    time_abscisse=[]
    who_shot=[]
    position_shot=[]
    ball_trajectories=[]
    time_shots_bis=[]
    match_id=[]
    
    if len(moments)<=1:
        return([time,w_ball,time_shots,d_closest_def,t_closest_def,time_to_shoot,time_abscisse,pos,w_reception,who_shot,position_shot,ball_trajectories,time_shots_bis,match_id])
    
    ### begin at the end of the previous moment ###
    
    i=0
    while [5-moments[i][0],m.ceil(moments[i][2])]>=t_end and (i<(len(moments)-2)):    
        i+=1
        
    when_reception=w_reception
    when_shot=i
    who_ball=w_ball
    position=pos
    
    ### looking if there is a gap in data. If there is one we test if the player who had the ball is still on the court ###
    
    if abs(t_end[1]-moments[0][2])>2:
        while not test_moment(moments[i]) and i<(len(moments)-2):
            i+=1
        player_on_court=False
        for k in range(len(moments[0][5])):
            if moments[0][5][k][1]==w_ball:
                player_on_court=True
            ball0=moments[0][5][0][2:5]
            if not player_on_court and ball0[2]>2.5*3.281:
                
                who_ball=player_with_ball_bis(moments,i)
                position=position_player_with_ball_bis(moments,i)
                when_reception=moments[i][2]
                when_shot=i
    
    if i>=(len(moments)-2) : #no moment
        return([time,who_ball,time_shots,d_closest_def,t_closest_def,time_to_shoot,time_abscisse,pos,when_reception,who_shot,position_shot,ball_trajectories,time_shots_bis,match_id])
    
        
    while i<(len(moments)-2):

        ### searching who has the ball ###
        if test_moment(moments[i]):
            who_ball2=player_with_ball(moments,i)
            if who_ball2!=0 and who_ball2!=who_ball:
                who_ball=who_ball2
                when_reception=moments[i][2]
            
            position2=position_player_with_ball(moments,i-1)
            if position2!=0:
                position=position2
            
            ### looking if the ball goes over 2.5m ###
            if moments[i][5][0][0]==-1: #if the ball is in the moment
                ball0=moments[i][5][0][2:5]
                if ball0[2]>2.5*3.28:
                    
                    when_shot=i
                    
                    ### looking if the player is in three points zone ### 
                    
                    ## taking position of the player ##
                    position2=position_player_with_ball(moments,i-1)
                    if position2!=0: # if it is zero it means that no player has the ball
                        position=position2
                    
                    where=where_attack(moments,i)
                    btpl=behind_three_point_line(position,where)
                    if btpl[0]:
                        basket_pos=btpl[1]
                        
                        ball1=ball0
                        ### looking if the ball is going above basket ###
                        while i<(len(moments)-2) and ball1[2]>ball0[2] and ball1[2]<10:
                            i+=1
                            if moments[i][5][0][0]==-1:
                                ball1=moments[i][5][0][2:5]
                        
                        ### looking if the ball is going just around the basket ###
                        if ball1[2]>=10: #is the ball above 10 feet ? higher than the basket
                            ball2=ball1
                            while i<(len(moments)-2) and ball1[2]>=10 and distance(ball1[:2],basket_pos)>5: #if higher than 10feets, while higher we look if the ball enter in the zone juste above the basket 
                                ball2=ball1
                                i+=1
                                if moments[i][5][0][0]==-1:
                                    ball1=moments[i][5][0][2:5]
                            
                            if ball1[2]>=10 and distance(ball1[:2],basket_pos)<=5: #if the ball is in the zone above the basket it means that it was a shot
                                if [5-moments[i][0],moments[i][2]+5]<time_shots[-1]:

                                    d=[0,[]]
                                    t_clos=[0,[]]
                                    t_abs=[0,[]]
                                    time_to_shoot.append([0,moments[when_shot][2]-when_reception])
                                    who_shot.append(who_ball)
                                    position_shot.append(position)
                                    match_id.append(m_id)
                                    ball_traj=[[],[],[]]
                                
                                    time_shots.append([5-moments[i][0],moments[i][2]])
                                    time_shots_bis.append([5-moments[when_shot][0],moments[when_shot][2]])
                                    
                                    ### calculating pressure evolution 3seconds before and 1 second after the shot with both models ###
                                    
                                    maxi=min(len(moments)-1,when_shot+20)
                                    mini=max(when_shot-80,0) # 3 last seconds + 2 moments for initial conditions
                                    
                
                                    for j in range(mini,maxi):
                                        if test_moment(moments[j]) and test_moment(moments[j+1]):

                                            t_abs[1].append(moments[when_shot][2]-moments[j][2])
                                            d[1].append(distance_closest_def(moments,j,who_ball))
                                            t_clos[1].append(time_closest_def(moments,j,who_ball))  
                                            ball_traj[0].append(moments[j][5][0][2])
                                            ball_traj[1].append(moments[j][5][0][3])
                                            ball_traj[2].append(moments[j][5][0][4])
                                    
                                
                                    ### waiting for the ball descending under basket ###
                                    while i<(len(moments)-2) and ball1[2]>=10:
                                        i+=1
                                        ball2=ball1
                                        if moments[i][5][0][0]==-1:
                                            ball1=moments[i][5][0][2:5]
        
                                    ### looking if the ball passed through the basket ###
                                    if ball1[2]<10:
                                        a=ball1[0]-ball2[0]
                                        b=ball1[1]-ball2[1]
                                        c=ball1[2]-ball2[2]
                                        t=(10-ball2[2])/c
                                        x=ball2[0]+t*a
                                        y=ball2[1]+t*b
                                        if distance(np.array([x,y]),basket_pos)<0.75:
                                            d[0]=1
                                            t_clos[0]=1
                                            time_to_shoot[-1][0]=1
                                            t_abs[0]=1
                                    
                                    d_closest_def.append(d)
                                    t_closest_def.append(t_clos)
                                    time_abscisse.append(t_abs)
                                    ball_trajectories.append(ball_traj)
                            
                                else:
                                    while ball1[2]>=2.5*3.28 and i<(len(moments)-2):
                                        i+=1
                                        if moments[i][5][0][0]==-1:
                                            ball1=moments[i][5][0][2:5]
    
                            
        i+=1
    
    time=[5-moments[i][0],moments[i][2]]        
    return([time,who_ball,time_shots,d_closest_def,t_closest_def,time_to_shoot,time_abscisse,position,when_reception,who_shot,position_shot,ball_trajectories,time_shots_bis])
                                
                            
    
def track_shots(file_name):
    with open(file_name) as json_file:  
        data = json.load(json_file)
        events=data['events']
        
    m_id=file_name[7:10]
    event=events[2]
    time_end=[np.inf,np.inf]
    TIME_SHOTS=[[10,100]]
    who_ball=1950#events[0]['moments'][0][5][5][1]
    when_reception=720
    position=[50,50]
    
    D_closest_def=[]
    T_closest_def=[]
    Time_to_shoot=[]
    Time_abscisse=[]
    WHO_SHOT=[]
    POSITION_SHOT=[]
    BALL_TRAJECTORIES=[]
    MATCH_ID=[]
    TIME_SHOTS_bis=[]
    
    for q in range(len(events)):
        event=events[q]
        moments=event['moments']
        res=track_event_shots(moments,time_end,who_ball,when_reception,TIME_SHOTS,position,m_id)
        time_end=res[0]
        who_ball=res[1]
        TIME_SHOTS=res[2]
        D_closest_def=D_closest_def+res[3]
        T_closest_def=T_closest_def+res[4]
        Time_to_shoot=Time_to_shoot+res[5]
        Time_abscisse=Time_abscisse+res[6]
        position=res[7]
        when_reception=res[8]
        WHO_SHOT=WHO_SHOT+res[9]
        POSITION_SHOT=POSITION_SHOT+res[10]
        BALL_TRAJECTORIES=BALL_TRAJECTORIES+res[11]
        MATCH_ID=MATCH_ID+res[13]
        TIME_SHOTS_bis=TIME_SHOTS_bis+res[12]
    
    return(D_closest_def,T_closest_def,Time_to_shoot,Time_abscisse,WHO_SHOT,POSITION_SHOT,BALL_TRAJECTORIES,MATCH_ID,TIME_SHOTS_bis)


#import matplotlib.pyplot as plt
#plt.figure(1)   
#for k in range(len(D_CLOSEST_DEF)):
#    plt.plot(TIME_ABSCISSE[k][1],D_CLOSEST_DEF[k][1])
#    
#plt.figure(2)   
#for k in range(len(T_CLOSEST_DEF)):
#    plt.plot(TIME_ABSCISSE[k][1],T_CLOSEST_DEF[k][1])

#D_CLOSEST_DEF=[]
#T_CLOSEST_DEF=[]
#TIME_TO_SHOOT=[]
#TIME_ABSCISSE=[]
#WHO_SHOT=[]
#POSTION_SHOT=[]
#BALL_TRAJECTORIES=[]
#MATCH_ID=[]
#TIME_SHOTS=[]
#
#match_number=0
#for k in range(638):
#    os.chdir('/Volumes/My Passport/GABIN/Documents/CENTRALE_LYON_1A/PaR/Basket/')
#    if k<10:
#        if ('002150000'+str(k)+'.json') in os.listdir():
#            print(k)
#            match_number+=1
#            result=track_shots('002150000'+str(k)+'.json')
#            D_CLOSEST_DEF=D_CLOSEST_DEF+result[0]
#            T_CLOSEST_DEF=T_CLOSEST_DEF+result[1]
#            TIME_TO_SHOOT=TIME_TO_SHOOT+result[2]
#            TIME_ABSCISSE=TIME_ABSCISSE+result[3]
#            WHO_SHOT=WHO_SHOT+result[4]
#            POSTION_SHOT=POSTION_SHOT+result[5]
#            BALL_TRAJECTORIES=BALL_TRAJECTORIES+result[6]
#            MATCH_ID=MATCH_ID+result[7]
#            TIME_SHOTS=TIME_SHOTS+result[8]
#            
#    if 9<k<100:
#        if ('00215000'+str(k)+'.json') in os.listdir():
#            print(k)
#            match_number+=1
#            result=track_shots('00215000'+str(k)+'.json')
#            D_CLOSEST_DEF=D_CLOSEST_DEF+result[0]
#            T_CLOSEST_DEF=T_CLOSEST_DEF+result[1]
#            TIME_TO_SHOOT=TIME_TO_SHOOT+result[2]
#            TIME_ABSCISSE=TIME_ABSCISSE+result[3]
#            WHO_SHOT=WHO_SHOT+result[4]
#            POSTION_SHOT=POSTION_SHOT+result[5]
#            BALL_TRAJECTORIES=BALL_TRAJECTORIES+result[6]
#            MATCH_ID=MATCH_ID+result[7]
#            TIME_SHOTS=TIME_SHOTS+result[8]
#            
#    if 99<k:
#        if ('0021500'+str(k)+'.json') in os.listdir():
#            print(k)
#            match_number+=1
#            result=track_shots('0021500'+str(k)+'.json')
#            D_CLOSEST_DEF=D_CLOSEST_DEF+result[0]
#            T_CLOSEST_DEF=T_CLOSEST_DEF+result[1]
#            TIME_TO_SHOOT=TIME_TO_SHOOT+result[2]
#            TIME_ABSCISSE=TIME_ABSCISSE+result[3]
#            WHO_SHOT=WHO_SHOT+result[4]
#            POSTION_SHOT=POSTION_SHOT+result[5]
#            BALL_TRAJECTORIES=BALL_TRAJECTORIES+result[6]
#            MATCH_ID=MATCH_ID+result[7]
#            TIME_SHOTS=TIME_SHOTS+result[8]
#    
#    if k%100==0:
#        os.chdir('/Users/gabin/Ordinateur/Documents/CENTRALE_LYON_1A/PaR/MecaFootCo/Notebooks')
#        save={'D_CLOSEST_DEF':D_CLOSEST_DEF,'T_CLOSEST_DEF':T_CLOSEST_DEF,'TIME_TO_SHOOT':TIME_TO_SHOOT,'TIME_ABSCISSE':TIME_ABSCISSE,'WHO_SHOT':WHO_SHOT,'POSTION_SHOT':POSTION_SHOT,'BALL_TRAJECTORIES':BALL_TRAJECTORIES,
#            'TIME_SHOTS':TIME_SHOTS,'MATCH_ID':MATCH_ID}
#        pickle.dump(save, open('Shots_25_11_k', 'wb'))
    
####################################################################################
####################################################################################
####################################################################################

############## Steph Curry ###################
def teams(data):
    return(data['events'][1]['visitor']['name'],data['events'][1]['home']['name'])

def Stephen_curry(data):  #playerid=201939
    team1,team2=teams(data)
    players=data['events'][1]['visitor']['players']
    for player in players:
        if player['playerid']==201939:
            return True
    players=data['events'][1]['home']['players']
    for player in players:
        if player['playerid']==201939:
            return True
    return False

def track_event_shots_Curry(moments,t_end,w_ball,w_reception,TIME_SHOTS,pos):
    
    time_shots=TIME_SHOTS
    time=t_end
    
    d_closest_def=[]
    t_closest_def=[]
    time_to_shoot=[]
    time_abscisse=[]
    
    if len(moments)<=1:
        return([time,w_ball,time_shots,d_closest_def,t_closest_def,time_to_shoot,time_abscisse,pos,w_reception])
    
    ### begin at the end of the previous moment ###
    
    i=0
    while [5-moments[i][0],m.ceil(moments[i][2])]>=t_end and (i<(len(moments)-2)):    
        i+=1
        
    when_reception=w_reception
    when_shot=i
    who_ball=w_ball
    position=pos
    
    ### looking if there is a gap in data. If there is one we test if the player who had the ball is still on the court ###
    
    if abs(t_end[1]-moments[0][2])>2:
        while not test_moment(moments[i]) and i<(len(moments)-2):
            i+=1
        player_on_court=False
        for k in range(len(moments[0][5])):
            if moments[0][5][k][1]==w_ball:
                player_on_court=True
            ball0=moments[0][5][0][2:5]
            if not player_on_court and ball0[2]>2.5*3.281:
                
                who_ball=player_with_ball_bis(moments,i)
                position=position_player_with_ball_bis(moments,i)
                when_reception=moments[i][2]
                when_shot=i
    
    if i>=(len(moments)-2) : #no moment
        return([time,w_ball,time_shots,d_closest_def,t_closest_def,time_to_shoot,time_abscisse,pos,when_reception])
    
        
    while i<(len(moments)-2):

        ### searching who has the ball ###
        if test_moment(moments[i]):
            who_ball2=player_with_ball(moments,i)
            if who_ball2!=0 and who_ball2!=who_ball:
                who_ball=who_ball2
                when_reception=moments[i][2]
            
            ### looking if Curry's has the ball ###
            if who_ball==201939:
            
                ### looking if the ball goes over 2.5m ###
                if moments[i][5][0][0]==-1: #if the ball is in the moment
                    ball0=moments[i][5][0][2:5]
                    if ball0[2]>2.5*3.28:
                        
                        when_shot=i
                        
                        ### looking if the player is in three points zone ### 
                        
                        ## taking position of the player ##
                        position2=position_player_with_ball(moments,i-1)
                        if position2!=0:
                            position=position2
                        
                        where=where_attack(moments,i)
                        btpl=behind_three_point_line(position,where)
                        if btpl[0]:
                            basket_pos=btpl[1]
                            
                            ball1=ball0
                            ### looking if the ball is going above basket ###
                            while i<(len(moments)-2) and ball1[2]>ball0[2] and ball1[2]<10:
                                i+=1
                                if moments[i][5][0][0]==-1:
                                    ball1=moments[i][5][0][2:5]
                            
                            ### looking if the ball is going just around the basket ###
                            if ball1[2]>=10: #is the ball above 10 feet ? higher than the basket
                                ball2=ball1
                                while i<(len(moments)-2) and ball1[2]>=10 and distance(ball1[:2],basket_pos)>5: #if higher than 10feets, while higher we look if the ball enter in the zone juste above the basket 
                                    ball2=ball1
                                    i+=1
                                    if moments[i][5][0][0]==-1:
                                        ball1=moments[i][5][0][2:5]
                                
                                if ball1[2]>=10 and distance(ball1[:2],basket_pos)<=5: #if the ball is in the zone above the basket it means that it was a shot
                                    if [5-moments[i][0],moments[i][2]+5]<time_shots[-1]:
    
                                        d=[0,[]]
                                        t_clos=[0,[]]
                                        t_abs=[0,[]]
                                        time_to_shoot.append([0,moments[when_shot][2]-when_reception])
                                    
                                        time_shots.append([5-moments[i][0],moments[i][2]])
                                        
                                        ### calculating pressure evolution 3seconds before and 1 second after the shot with both models ###
                                        
                                        maxi=min(len(moments)-1,when_shot+20)
                                        mini=max(when_shot-80,0) # 3 last seconds + 2 moments for initial conditions
                                        
                    
                                        for j in range(mini,maxi):
                                            if test_moment(moments[j]) and test_moment(moments[j+1]):
    #                                            print('who:',who_ball)
    #                                            for k in range(len(moments[j][5])):
    #                                                print(moments[j][5][k][1])
                                                t_abs[1].append(moments[when_shot][2]-moments[j][2])
                                                d[1].append(distance_closest_def(moments,j,who_ball))
                                                t_clos[1].append(time_closest_def(moments,j,who_ball))   
                                        
                                    
                                        ### waiting for the ball descending under basket ###
                                        while i<(len(moments)-2) and ball1[2]>=10:
                                            i+=1
                                            ball2=ball1
                                            if moments[i][5][0][0]==-1:
                                                ball1=moments[i][5][0][2:5]
            
                                        ### looking if the ball passed through the basket ###
                                        if ball1[2]<10:
                                            a=ball1[0]-ball2[0]
                                            b=ball1[1]-ball2[1]
                                            c=ball1[2]-ball2[2]
                                            t=(10-ball2[2])/c
                                            x=ball2[0]+t*a
                                            y=ball2[1]+t*b
                                            if distance(np.array([x,y]),basket_pos)<0.75:
                                                d[0]=1
                                                t_clos[0]=1
                                                time_to_shoot[-1][0]=1
                                                t_abs[0]=1
                                        
                                        d_closest_def.append(d)
                                        t_closest_def.append(t_clos)
                                        time_abscisse.append(t_abs)
                                
                                    else:
                                        while ball1[2]>=2.5*3.28 and i<(len(moments)-2):
                                            i+=1
                                            if moments[i][5][0][0]==-1:
                                                ball1=moments[i][5][0][2:5]
        
                            
        i+=1
    
    time=[5-moments[i][0],moments[i][2]]        
    return([time,who_ball,time_shots,d_closest_def,t_closest_def,time_to_shoot,time_abscisse,position,when_reception])
                

def track_shots_Curry(data):
    with open(data) as json_file:  
        data = json.load(json_file)
        events=data['events']
    
    D_closest_def=[]
    T_closest_def=[]
    Time_to_shoot=[]
    Time_abscisse=[]
        
    if Stephen_curry(data):
        
        event=events[2]
        time_end=[np.inf,np.inf]
        TIME_SHOTS=[[10,100]]
        who_ball=1950#events[0]['moments'][0][5][5][1]
        when_reception=720
        position=[50,50]
        
    
        for q in range(len(events)):
            event=events[q]
            moments=event['moments']
            res=track_event_shots_Curry(moments,time_end,who_ball,when_reception,TIME_SHOTS,position)
            time_end=res[0]
            who_ball=res[1]
            TIME_SHOTS=res[2]
            D_closest_def=D_closest_def+res[3]
            T_closest_def=T_closest_def+res[4]
            Time_to_shoot=Time_to_shoot+res[5]
            Time_abscisse=Time_abscisse+res[6]
            position=res[7]
            when_reception=res[8]
        
        print(len(Time_to_shoot))
        
    return(D_closest_def,T_closest_def,Time_to_shoot,Time_abscisse)

#D_CLOSEST_DEF=[]
#T_CLOSEST_DEF=[]
#TIME_TO_SHOOT=[]
#TIME_ABSCISSE=[]
#
#for k in range(638):
#    os.chdir('/Volumes/My Passport/GABIN/Documents/CENTRALE_LYON_1A/PaR/Basket/')
#    if k<10:
#        if ('002150000'+str(k)+'.json') in os.listdir():
#            print(k)
#            result=track_shots_Curry('002150000'+str(k)+'.json')
#            D_CLOSEST_DEF=D_CLOSEST_DEF+result[0]
#            T_CLOSEST_DEF=T_CLOSEST_DEF+result[1]
#            TIME_TO_SHOOT=TIME_TO_SHOOT+result[2]
#            TIME_ABSCISSE=TIME_ABSCISSE+result[3]
#            
#    if 9<k<100:
#        if ('00215000'+str(k)+'.json') in os.listdir():
#            print(k)
#            result=track_shots_Curry('00215000'+str(k)+'.json')
#            D_CLOSEST_DEF=D_CLOSEST_DEF+result[0]
#            T_CLOSEST_DEF=T_CLOSEST_DEF+result[1]
#            TIME_TO_SHOOT=TIME_TO_SHOOT+result[2]
#            TIME_ABSCISSE=TIME_ABSCISSE+result[3]
#            
#    if 99<k:
#        if ('0021500'+str(k)+'.json') in os.listdir():
#            print(k)
#            result=track_shots_Curry('0021500'+str(k)+'.json')
#            D_CLOSEST_DEF=D_CLOSEST_DEF+result[0]
#            T_CLOSEST_DEF=T_CLOSEST_DEF+result[1]
#            TIME_TO_SHOOT=TIME_TO_SHOOT+result[2]
#            TIME_ABSCISSE=TIME_ABSCISSE+result[3]
#            
#
#