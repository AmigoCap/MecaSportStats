#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 11:31:40 2019

@author: gabin
"""

#########################################################################################################

# This algorithm create three dataframe from shots dictionnary : df_shots, df_plot_mean, df_stats

#########################################################################################################
#The shots are memorized in python dictionnary called Shots (too big to be on the repository). It is composed of nine keys :
#* D_CLOSEST_DEF : a list of list. Each list corresponds to a shot and has two elements. The first one is 0 or 1 : if it is 1 it means that the shot was a success and if it is 0 the shot was missed. The second element is the evolution of the shooter's *free space* ($\delta_{space}^*$ distance to the closest defender) 3 seconds before the shot. 
#* T_CLOSEST_DEF : It the same but *free space* is calculated as the time (in second) needed by the closest defender to join the position of the shooter ($\delta_{time}^*$). 
#* TIME_TO_SHOOT : a list of list. Each list has two elements : the first one for the result of the shot and the second one corresponds to the time between the reception of the ball and the shot. It is negative : -2 means that the shooter kept the ball 2 seconds before shooting.
#* TIME_ABSCISSE : a list of list. Each list corresponds to a shot and has two elements. The first one is 0 or 1 : if it is 1 it means that the shot was a success and if it is 0 the shot was missed. The second element corresponds to time values linked to pressure evolution.
#* WHO_SHOT : a list which contains shooters' ID.
#* POSITION_SHOT : a list which contains position of the player at the release.
#* BALL_TRAJECTORIES : a list of list which contains for each shots ball's trajectory.
#* TIME_SHOTS : a list of list which contains the release time in the following format : 5-quarter,time in seconds
#* MATCH_ID : a list containing matches ID

import pickle
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

## load dictionnary ##

dico=pickle.load(open('../data/Shots','rb'))

## load players description ##

def players_description(data): #data should be a string like : 'data.json', the function returns data and events
    with open(data) as json_file:  
        data = json.load(json_file)
    firstName=[]
    lastName=[]
    player_id=[]
    team_id=[]
    for d in data:
        if 'firstName' in d.keys():
            firstName.append(d['firstName'])
        else :
            firstName.append(' ')
        lastName.append(d['lastName'])
        player_id.append(d['playerId'])
        team_id.append(d['teamId'])
    
    df=pd.DataFrame({'firstName':firstName,'lastName':lastName,'player_id':player_id,'team_id':team_id},index=player_id)
    return(df)
    
players=players_description('../data/players.json')


## Structure data to make mean ##

def restructure_data(data):
    
    "This function return a dataframe. Each raw is associated with a shot via shot_id and to a time between -3.2 and 0.8 seconds before and after the release if the ball."
    
    ### getting the data ###
    D_CLOSEST_PLAYER=data['D_CLOSEST_DEF']
    T_CLOSEST_PLAYER=data['T_CLOSEST_DEF']
    TIME=data['TIME_ABSCISSE']
    TIME_TO_SHOOT=data['TIME_TO_SHOOT']
    WHO_SHOT=data['WHO_SHOT']
    POSITION_SHOT=data['POSTION_SHOT']
    BALL_TRAJECTORIES=data['BALL_TRAJECTORIES']
    TIME_SHOTS=data['TIME_SHOTS']
    MATCH_ID=data['MATCH_ID']
    
    print('number of total of shots:',len(D_CLOSEST_PLAYER))
    
    ### only the second column because the first one contains if it is a succes or a miss ###
    D_CLOSEST_PLAYER_bis=[]
    T_CLOSEST_PLAYER_bis=[]
    TIME_bis=[]
    TIME_TO_SHOOT_bis=[]
    WHO_SHOT_bis=[]
    X_SHOT=[]
    Y_SHOT=[]
    X_BALL=[]
    Y_BALL=[]
    Z_BALL=[]
    QUARTER=[]
    CLOCK=[]
    MATCH_ID_bis=[]
    SUCCESS=[]
    SHOT_ID=[]
    SHOT_TYPE=[]
    
    nb_catch_and_shoot=0
    nb_pull_up=0
    nb_success=0
    nb_missed=0
    nb_cns_success=0
    nb_cns_missed=0
    nb_pull_up_success=0
    nb_pull_up_missed=0
    for k in range(len(D_CLOSEST_PLAYER)):
        unique,count=np.unique(np.array(TIME[k][1]).round(2), return_counts=True)
        if list(count)==[1]*len(count): # we don't take shots where values of time are repeated, because in the data, sometimes the values of time doesn't change so stay on the same second but we count the evolution on this second
            if TIME_TO_SHOOT[k][1]<-0.2: # there are errors : we don't have data before the player receives the ball so we can't evaluate these shots. It sometimes corresponds to freethrows
                if D_CLOSEST_PLAYER[k][0]==0:
                    nb_missed+=1
                    if TIME_TO_SHOOT[k][1]>-2:
                        nb_catch_and_shoot+=1
                        nb_cns_missed+=1
                    else :
                        nb_pull_up+=1
                        nb_pull_up_missed+=1
                else :
                    nb_success+=1
                    if TIME_TO_SHOOT[k][1]>-2:
                        nb_catch_and_shoot+=1
                        nb_cns_success+=1
                    else :
                        nb_pull_up+=1
                        nb_pull_up_success+=1
                D_CLOSEST_PLAYER_bis.append(D_CLOSEST_PLAYER[k][1])
                T_CLOSEST_PLAYER_bis.append(T_CLOSEST_PLAYER[k][1])
                TIME_bis.append(np.array(TIME[k][1]).round(2)) # round to 0.01 second
                TIME_TO_SHOOT_bis.append([TIME_TO_SHOOT[k][1]]*len(TIME[k][1]))
                SUCCESS.append([TIME_TO_SHOOT[k][0]]*len(TIME[k][1]))
                WHO_SHOT_bis.append([WHO_SHOT[k]]*len(TIME[k][1]))
                X_SHOT.append([POSITION_SHOT[k][0]]*len(TIME[k][1]))
                Y_SHOT.append([POSITION_SHOT[k][1]]*len(TIME[k][1]))
                X_BALL.append(np.array(BALL_TRAJECTORIES[k][0]))
                Y_BALL.append(np.array(BALL_TRAJECTORIES[k][1]))
                Z_BALL.append(np.array(BALL_TRAJECTORIES[k][2]))
                QUARTER.append([5-TIME_SHOTS[k][0]]*len(TIME[k][1]))
                CLOCK.append([TIME_SHOTS[k][1]]*len(TIME[k][1]))
                MATCH_ID_bis.append([MATCH_ID[k]]*len(TIME[k][1]))
                SHOT_ID.append([k]*len(TIME[k][1]))
                if TIME_TO_SHOOT[k][1]<-2:
                    SHOT_TYPE.append(['pull-up 3P']*len(TIME[k][1]))
                else :
                    SHOT_TYPE.append(['catch-and-shoot 3P']*len(TIME[k][1]))
    
    print('number of valid shot:',len(D_CLOSEST_PLAYER_bis))
    print('number of success :',nb_success)
    print('number of miss :',nb_missed)
    print('percentage of success:',nb_success/(nb_success+nb_missed)*100)
    print('percentage of catch-and-shoot shots :',nb_catch_and_shoot/(nb_pull_up+nb_catch_and_shoot)*100)
    print('percentage of catch-and-shoot success:',nb_cns_success/(nb_cns_missed+nb_cns_success)*100)
    print('percentage of pull-up success:',nb_pull_up_success/(nb_pull_up_missed+nb_pull_up_success)*100)
    
    ### we concatenate all the data
    TIME_bis=np.concatenate(np.array(TIME_bis)) 
    D_CLOSEST_PLAYER_bis=np.concatenate(np.array(D_CLOSEST_PLAYER_bis))
    T_CLOSEST_PLAYER_bis=np.concatenate(np.array(T_CLOSEST_PLAYER_bis))
    TIME_TO_SHOOT_bis=np.concatenate(np.array(TIME_TO_SHOOT_bis))
    SUCCESS=np.concatenate(np.array(SUCCESS))
    WHO_SHOT_bis=np.concatenate(np.array(WHO_SHOT_bis))
    X_SHOT=np.concatenate(np.array(X_SHOT))
    Y_SHOT=np.concatenate(np.array(Y_SHOT))
    X_BALL=np.concatenate(np.array(X_BALL))
    Y_BALL=np.concatenate(np.array(Y_BALL))
    Z_BALL=np.concatenate(np.array(Z_BALL))
    QUARTER=np.concatenate(np.array(QUARTER))
    CLOCK=np.concatenate(np.array(CLOCK))
    MATCH_ID_bis=np.concatenate(np.array(MATCH_ID_bis))
    SHOT_ID=np.concatenate(np.array(SHOT_ID))
    SHOT_TYPE=np.concatenate(np.array(SHOT_TYPE))
    
    ### put the data into a dataframe ###
    df=pd.DataFrame({'D':D_CLOSEST_PLAYER_bis,'T':T_CLOSEST_PLAYER_bis,'Time':TIME_bis,'Time_to_shoot':TIME_TO_SHOOT_bis,'Shot result':SUCCESS,'player_id':WHO_SHOT_bis,'x_ball':X_BALL,'y_ball':Y_BALL,'z_ball':Z_BALL,'x_shooter':X_SHOT,'y_shooter':Y_SHOT,'quarter':QUARTER,'clock':CLOCK,'Match_id':MATCH_ID_bis,'shot_id':SHOT_ID,'Shot_type':SHOT_TYPE})
    
    return(df)


## Structure data by shots ##
    
def structure_data_by_shot(data):
    
    "This function return a dataframe.Each raw represents a shot."
    
    ### getting the data ###
    D_CLOSEST_PLAYER=data['D_CLOSEST_DEF']
    T_CLOSEST_PLAYER=data['T_CLOSEST_DEF']
    TIME=data['TIME_ABSCISSE']
    TIME_TO_SHOOT=data['TIME_TO_SHOOT']
    WHO_SHOT=data['WHO_SHOT']
    POSITION_SHOT=data['POSTION_SHOT']
    BALL_TRAJECTORIES=data['BALL_TRAJECTORIES']
    TIME_SHOTS=data['TIME_SHOTS']
    MATCH_ID=data['MATCH_ID']
    NB_DEF=data['NB_DEF']
    OPP_POS=data['OPP_POS']
    PLAYER_POS=data['PLAYER_POS']
    
    ### only the second column because the first one contains if it is a succes or a miss ###
    D_CLOSEST_PLAYER_bis=[]
    T_CLOSEST_PLAYER_bis=[]
    TIME_bis=[]
    TIME_TO_SHOOT_bis=[]
    WHO_SHOT_bis=[]
    X_SHOT=[]
    Y_SHOT=[]
    X_BALL=[]
    Y_BALL=[]
    Z_BALL=[]
    QUARTER=[]
    CLOCK=[]
    MATCH_ID_bis=[]
    SUCCESS=[]
    SHOT_ID=[]
    SHOT_TYPE=[]
    NB_DEF_bis=[]
    PLAYER_POS_bis=[]
    OPP_POS_bis=[]
    
    nb_catch_and_shoot=0
    nb_pull_up=0
    nb_success=0
    nb_missed=0
    nb_cns_success=0
    nb_cns_missed=0
    nb_pull_up_success=0
    nb_pull_up_missed=0
    for k in range(len(D_CLOSEST_PLAYER)):
        unique,count=np.unique(np.array(TIME[k][1]).round(2), return_counts=True)
        if list(count)==[1]*len(count): # we don't take shots where values of time are repeated, because in the data, sometimes the values of time doesn't change so stay on the same second but we count the evolution on this second
            if TIME_TO_SHOOT[k][1]<-0.2:
                if D_CLOSEST_PLAYER[k][0]==0:
                    nb_missed+=1
                    if TIME_TO_SHOOT[k][1]>-2:
                        nb_catch_and_shoot+=1
                        nb_cns_missed+=1
                    else :
                        nb_pull_up+=1
                        nb_pull_up_missed+=1
                else :
                    nb_success+=1
                    if TIME_TO_SHOOT[k][1]>-2:
                        nb_catch_and_shoot+=1
                        nb_cns_success+=1
                    else :
                        nb_pull_up+=1
                        nb_pull_up_success+=1
                D_CLOSEST_PLAYER_bis.append(D_CLOSEST_PLAYER[k][1])
                T_CLOSEST_PLAYER_bis.append(T_CLOSEST_PLAYER[k][1])
                TIME_bis.append(list(np.array(TIME[k][1]).round(2))) # round to 0.01 second
                TIME_TO_SHOOT_bis.append(TIME_TO_SHOOT[k][1])
                SUCCESS.append(TIME_TO_SHOOT[k][0])
                WHO_SHOT_bis.append(WHO_SHOT[k])
                X_SHOT.append(POSITION_SHOT[k][0])
                Y_SHOT.append(POSITION_SHOT[k][1])
                X_BALL.append(BALL_TRAJECTORIES[k][0])
                Y_BALL.append(BALL_TRAJECTORIES[k][1])
                Z_BALL.append(BALL_TRAJECTORIES[k][2])
                QUARTER.append(5-TIME_SHOTS[k][0])
                CLOCK.append(TIME_SHOTS[k][1])
                MATCH_ID_bis.append(MATCH_ID[k])
                NB_DEF_bis.append(NB_DEF[k])
                PLAYER_POS_bis.append(PLAYER_POS[k])
                OPP_POS_bis.append(OPP_POS[k])
                SHOT_ID.append(k)
                if TIME_TO_SHOOT[k][1]<-2:
                    SHOT_TYPE.append('pull-up 3P')
                else :
                    SHOT_TYPE.append('catch-and-shoot 3P')

    
    print('number of valid shot:',len(D_CLOSEST_PLAYER_bis))
    print('number of success :',nb_success)
    print('number of miss :',nb_missed)
    print('percentage of success:',nb_success/(nb_success+nb_missed)*100)
    print('percentage of catch-and-shoot shots :',nb_catch_and_shoot/(nb_pull_up+nb_catch_and_shoot)*100)
    print('percentage of catch-and-shoot success:',nb_cns_success/(nb_cns_missed+nb_cns_success)*100)
    print('percentage of pull-up success:',nb_pull_up_success/(nb_pull_up_missed+nb_pull_up_success)*100)
    
    ### put the data into a dataframe ###
    df=pd.DataFrame({'D':D_CLOSEST_PLAYER_bis,'T':T_CLOSEST_PLAYER_bis,'Time':TIME_bis,'Time_to_shoot':TIME_TO_SHOOT_bis,'Shot_result':SUCCESS,'player_id':WHO_SHOT_bis,'x_ball':X_BALL,'y_ball':Y_BALL,'z_ball':Z_BALL,'x_shooter':X_SHOT,'y_shooter':Y_SHOT,'quarter':QUARTER,'clock':CLOCK,'Match_id':MATCH_ID_bis,'shot_id':SHOT_ID,'Shot_type':SHOT_TYPE,'nb_def':NB_DEF_bis,'shooter_pos':PLAYER_POS_bis,'opp_pos':OPP_POS_bis})
    
    return(df)
    
## Calculate players stats ##
    
def players_stats(df_shots):
    
    "This function return a dataframe of players statistics."
    
    df1=df_shots[['player_id','Shot_result','D','Match_id','Shot_type']].groupby(['player_id','Match_id']).count()
    df2=df_shots[['player_id','Shot_result','D','Match_id','Shot_type']].groupby(['player_id','Shot_result']).count()
    df3=df_shots[['player_id','Shot_result','D','Match_id','Shot_type']].groupby(['player_id','Shot_type','Shot_result']).count()
    players_id=df_shots['player_id'].unique()
    
    total=[]
    success=[]
    miss=[]
    percentage=[]
    match_played=[]
    total_cas=[]
    success_cas=[]
    miss_cas=[]
    percentage_cas=[]
    
    for player in players_id:
        s=0
        m=0
        match_played.append(len(df1.loc[player]))
        if 1 in df2.loc[player,'D'].index:
            s=df2.loc[(player,1),'D']

        if 0 in df2.loc[player,'D'].index:
            m=df2.loc[(player,0),'D']
                
        
        total.append(m+s)
        success.append(s)
        miss.append(m)
        percentage.append(round(s/(m+s)*100,1))
        
        if player==1495:
            print(df3.loc[player,'D'])
        if "catch-and-shoot 3P" in df3.loc[player,'D'].index[0]:
            if 1 in df3.loc[(player,"catch-and-shoot 3P"),'D'].index: 
                s_cas=df3.loc[(player,"catch-and-shoot 3P",1),'D']
            else :
                s_cas=0
                
            if 0 in df3.loc[(player,"catch-and-shoot 3P"),'D'].index:  
                m_cas=df3.loc[(player,"catch-and-shoot 3P",0),'D']
            else:
                m_cas=0
        else :
            s_cas=0
            m_cas=0
                

        total_cas.append(m_cas+s_cas)
        success_cas.append(s_cas)
        miss_cas.append(m_cas)
        
        if s_cas+m_cas==0:
            percentage_cas.append(0)
        else:
            percentage_cas.append(round(s_cas/(m_cas+s_cas)*100,1))
            
        if player==1495:
            print(m_cas,s_cas)
    
    df_stats=pd.DataFrame({'total':total,'success':success,'miss':miss,'percentage':percentage,'match_played':match_played,'total_cas':total_cas,'success_cas':success_cas,'miss_cas':miss_cas,'percentage_cas':percentage_cas},index=players_id)
    return df_stats


df_plot_mean=restructure_data(dico)
df_shots=structure_data_by_shot(dico)

##############################################################################################################################

# Derive and clean the datasets

##############################################################################################################################

# Calculation of the distance from the ball to the hoop
def distance_to_basket(row): 
    z_ball=row['z_ball']
    x_ball=row['x_ball']
    y_ball=row['y_ball']
    
    if x_ball[-1]>94//2:
        basket_pos=[94-5.25,25]
    else :
        basket_pos=[5.25,25]
    
    d_basket=[]
    for k in range(len(x_ball)):
        d_basket.append(-np.sqrt((x_ball[k]-basket_pos[0])**2+(y_ball[k]-basket_pos[1])**2))
    
    return(d_basket)

df_shots['d_basket']=df_shots.apply(distance_to_basket,axis=1) 

def z_angle(row):
    z_ball=row['z_ball']
    d_basket=row['d_basket']
    angle=[]
    for k in range(len(d_basket)-1):
        z1=z_ball[k]
        z2=z_ball[k+1]
        d1=d_basket[k]
        d2=d_basket[k+1]
        if (d2-d1)<=0:
            angle.append(np.degrees(np.arctan((z2-z1)/(d2-d1)))+180)
        else :
            if (z2-z1)<=0:
                angle.append(np.degrees(np.arctan((z2-z1)/(d2-d1)))+360)
            else:
                angle.append(np.degrees(np.arctan((z2-z1)/(d2-d1))))
    return(angle)
 
df_shots['angle']=df_shots.apply(z_angle,axis=1)  

### A function to determine precisely the moment where the ball leaves shooter's hands ###
def release_moment(row):
    z_ball=row['z_ball']
    angle=row['angle']
    Time=row['Time']
    
    if len(z_ball)>40:
        release_time=z_ball.index(max(z_ball[40:]))
    else :
        release_time=z_ball.index(max(z_ball))
    release_time-=1
    
    while release_time>0 and z_ball[release_time]>10:
        release_time-=1
    while release_time>0 and z_ball[release_time]>6 and angle[release_time]<70:
        release_time-=1
        
    if release_time==0:
        return 0.
    
    else :
        release_time+=1
        return(Time[release_time])
        
df_shots['release_moment']=df_shots.apply(release_moment,axis=1)
        
def new_time(row):
    release_moment=row['release_moment']
    Time=row['Time']
    return(list(np.array(Time)-release_moment))

df_shots['Time']=df_shots.apply(new_time,axis=1)
        
def shot_duration(row): # to calcul shot duration we look the time between release of the ball and the minimum (higher than 2 feets toavoid rebounds) of z_ball within one second before shot
    z_ball=row['z_ball']
    Time=row['Time']
    time_start=Time.index(0.)
    zmin=[z_ball[time_start],time_start]
    z1=zmin[0]
    while time_start>0 and Time[time_start]>-1. and z_ball[time_start]>2:
        time_start-=1
        z2=z_ball[time_start]
        if z2>4:
            if z2<zmin[0]:
                zmin=[z2,time_start]
        if z2<4:
            if z2>z1:
                return(-Time[time_start+1])
        z1=z2
        
    return(-Time[zmin[1]])
    
df_shots['shot_duration']=df_shots.apply(shot_duration,axis=1)
    
def release_time(row):
    release_moment=row['release_moment']
    TTS=row['Time_to_shoot']
    shot_duration=row['shot_duration']
    if (TTS-release_moment)>-shot_duration:
        return(-shot_duration)
    return(TTS-release_moment)

df_shots['release_time']=df_shots.apply(release_time,axis=1)

def shot_type(row):
    release_time=row['release_time']
    Time=row['Time']
    if release_time<-2:
        return('pull-up 3P')
    else :
        ind1=list(abs(np.array(Time)-release_time)).index(min(abs(np.array(Time)-release_time)))
        ind2=Time.index(0.)

        z_ball=row['z_ball']
        for k in range(ind1,ind2):
            if z_ball[k]<2: #it means that there was a dribble
                return('pull-up 3P')
        return('catch-and-shoot 3P')
        
df_shots['Shot_type']=df_shots.apply(shot_type,axis=1)


def opp_position_release(row):
    Time=row['Time']
    ind=Time.index(0.)
    return(row['opp_pos'][ind])

def player_position_release(row):
    Time=row['Time']
    ind=Time.index(0.)
    return(row['shooter_pos'][ind])

df_shots['opp_position_release']=df_shots.apply(opp_position_release,axis=1)
df_shots['player_position_release']=df_shots.apply(player_position_release,axis=1)

def distance(a,b):      #a = (x,y) point de départ ; b = (i,j) point d'arrivée ; v = norme pour l'instant
    return np.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

#Looking if shots were behind the 3-point line with the new release moment
def behind_three_point_line(row):
    p=row['player_position_release']
    x_ball=row['x_ball']
    if x_ball[-1]>94/2:
        where=0
    else :
        where=1
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
            return (True)
        else :
            return (False)
    else :
        if distance(p,basket_pos)>23.5 :  #In fact 23.75 but we take a marge to have all shoots
            return (True)
        else:
            return (False)
        
df_shots['btpl']=df_shots.apply(behind_three_point_line,axis=1)

print('time df_plot_mean')

def correct_df_plot_mean(df_plot_mean,df_shots):
    Time=[]
    Shot_type=[]
    btpl=[]
    k=0
    Time_df=df_shots['Time']
    print(Time_df)
    Shot_type_df=df_shots['Shot_type']
    btpl_df=df_shots['btpl']
    for k in range(len(Time_df)):
        if k%100==0:
            print(k)
        Time=Time+Time_df[k]
        Shot_type=Shot_type+[Shot_type_df[k]]*len(Time_df[k])
        btpl=btpl+[btpl_df[k]]*len(Time_df[k])

    df_plot_mean.loc[:,'Time']=Time
    df_plot_mean.loc[:,'Shot_type']=Shot_type
    df_plot_mean.loc[:,'btpl']=btpl
    
correct_df_plot_mean(df_plot_mean,df_shots)

## only evolution between 3.2 seconds before shot and 0.8 second after. (It is because there are some errors in the data) ##
df_plot_mean=df_plot_mean.query('Time>-3. and Time<0.8')
    
df_shots=df_shots.query('btpl==True')
df_plot_mean=df_plot_mean.query('btpl==True')


df_shots.loc[10538,'Shot_result']=0
df_shots.loc[15772,'Shot_result']=0
df_shots.loc[22101,'Shot_result']=0
df_shots.loc[27446,'Shot_result']=0
df_shots.loc[20721,'Shot_result']=0
df_shots.loc[9892,'Shot_result']=0
df_shots.loc[10914,'Shot_result']=0

ind=df_shots.query('shot_id==7641').index[0]
df_shots.drop(ind,inplace=True)
ind=df_shots.query('shot_id==14919').index[0]
df_shots.drop(ind,inplace=True)

print('players_stats')

def players_stats(df_shots):
    
    "This function return a dataframe of players statistics."
    
    df1=df_shots[['player_id','Shot_result','D','Match_id','Shot_type']].groupby(['player_id','Match_id']).count()
    df2=df_shots[['player_id','Shot_result','D','Match_id','Shot_type']].groupby(['player_id','Shot_result']).count()
    df3=df_shots[['player_id','Shot_result','D','Match_id','Shot_type']].groupby(['player_id','Shot_type','Shot_result']).count()
    players_id=df_shots['player_id'].unique()
    
    total=[]
    success=[]
    miss=[]
    percentage=[]
    match_played=[]
    total_cas=[]
    success_cas=[]
    miss_cas=[]
    percentage_cas=[]
    
    for player in players_id:
        s=0
        m=0
        match_played.append(len(df1.loc[player]))
        if 1 in df2.loc[player,'D'].index:
            s=df2.loc[(player,1),'D']

        if 0 in df2.loc[player,'D'].index:
            m=df2.loc[(player,0),'D']
                
        
        total.append(m+s)
        success.append(s)
        miss.append(m)
        percentage.append(round(s/(m+s)*100,1))
        
        if player==1495:
            print(df3.loc[player,'D'])
        if "catch-and-shoot 3P" in df3.loc[player,'D'].index[0]:
            if 1 in df3.loc[(player,"catch-and-shoot 3P"),'D'].index: 
                s_cas=df3.loc[(player,"catch-and-shoot 3P",1),'D']
            else :
                s_cas=0
                
            if 0 in df3.loc[(player,"catch-and-shoot 3P"),'D'].index:  
                m_cas=df3.loc[(player,"catch-and-shoot 3P",0),'D']
            else:
                m_cas=0
        else :
            s_cas=0
            m_cas=0
                

        total_cas.append(m_cas+s_cas)
        success_cas.append(s_cas)
        miss_cas.append(m_cas)
        
        if s_cas+m_cas==0:
            percentage_cas.append(0)
        else:
            percentage_cas.append(round(s_cas/(m_cas+s_cas)*100,1))
    
    df_stats=pd.DataFrame({'total':total,'success':success,'miss':miss,'percentage':percentage,'match_played':match_played,'total_cas':total_cas,'success_cas':success_cas,'miss_cas':miss_cas,'percentage_cas':percentage_cas},index=players_id)
    return df_stats

df_stats=players_stats(df_shots)

df_plot_mean.to_csv('../data/df_plot_mean.csv', sep=',', encoding='utf-8')
df_shots.to_csv('../data/df_shots.csv', sep=',', encoding='utf-8')
df_stats.to_csv('../data/df_stats.csv', sep=',', encoding='utf-8')
#players.to_csv('../data/players.csv', sep=',', encoding='utf-8')
print('number of shots:',len(df_shots))
print(df_stats['total_cas'].sum(),df_stats['total_cas'].sum()/26295*100)
print(df_stats['success'].sum(),df_stats['miss'].sum(),df_stats['success'].sum()/26295*100)
print(df_stats['success_cas'].sum(),df_stats['miss_cas'].sum(),df_stats['success_cas'].sum()/18896*100)

print('nb CaS : ',len(df_shots.query('Shot_type=="catch-and-shoot 3P"')))
print(len(df_shots.query('Shot_type=="catch-and-shoot 3P"'))/len(df_shots)*100)

def plot_shot(df_shots,j,players):
    fig, ((ax1, ax2),(ax3,ax4)) = plt.subplots(2, 2,figsize=(10,10))
    #print(df_shots.query('shot_id==@j'))
    print(df_shots.query('shot_id==@j').index[0])
    i=df_shots.query('shot_id==@j').index[0]
    #print(df_shots.iloc[i])
    Time=df_shots.iloc[i]['Time']
    D=df_shots.iloc[i]['D']
    T=df_shots.iloc[i]['T']
    tts=df_shots.iloc[i]['release_time']
    player_id=df_shots.iloc[i]['player_id']
    c=df_shots.iloc[i]['clock']
    print(i,df_shots.iloc[i]['Match_id'],df_shots.iloc[i]['quarter'],str(c//60)+'m '+str(c%60),player_id,players.loc[player_id,'lastName'],df_shots.iloc[i]['Shot_type'],tts,df_shots.iloc[i]['Shot_result'])
    ax1.axvline(tts, color='black',linestyle="dashed",lw=1)
    ax2.axvline(tts, color='black',linestyle="dashed",lw=1)
    ax3.axvline(tts, color='black',linestyle="dashed",lw=1)
    ax1.plot(Time,D,'r-',alpha=0.8)
    ax2.plot(Time,T,'r-',alpha=0.8)
    
    ax1.set_xlim((-3.2,0.8))
    ax1.set_ylim((0,30))
    ax2.set_xlim((-3.2,0.8))
    ax2.set_ylim((0,2))
    ax3.plot(list(df_shots.iloc[i]['d_basket']),df_shots.iloc[i]['z_ball'])
    ind=Time.index(0)
    ax3.plot(df_shots.iloc[i]['d_basket'][ind],df_shots.iloc[i]['z_ball'][ind],'ro')
    print(df_shots.iloc[i]['angle'][ind-1])
    #ax4.plot(Time,df_shots.iloc[i]['angle'])
    plt.show()
    
def print_df_shot(df_shots,players):
    for i in range(len(df_shots)):
        Time=df_shots.iloc[i]['Time']
        D=df_shots.iloc[i]['D']
        T=df_shots.iloc[i]['T']
        tts=df_shots.iloc[i]['Time_to_shoot']
        player_id=df_shots.iloc[i]['player_id']
        c=df_shots.iloc[i]['clock']
        print(i,df_shots.iloc[i]['Match_id'],df_shots.iloc[i]['quarter'],str(c//60)+'m '+str(c%60),player_id,players.loc[player_id,'lastName'],df_shots.iloc[i]['Shot_type'],tts,df_shots.iloc[i]['Shot result'])
        