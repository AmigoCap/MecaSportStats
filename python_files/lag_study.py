#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 10:07:38 2019

@author: gabin
"""

import json
import space as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing as mp

import sys

def progress(count, total, status=''):
    bar_len=60
    filled_len=int(round(bar_len*count/float(total)))
    
    percents=round(100.0*count/float(total),1)
    bar= '=' * filled_len+'-'*(bar_len-filled_len)
    sys.stdout.write('\r%s |%s| %s%% %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def json_extracter(data): #data should be a string like : 'data.json', the function returns data and events
    with open(data) as json_file:  
        data = json.load(json_file)
        events=data['events']
    return(data,events)

match_data,events=json_extracter('0021500001.json')
save_DELTA_X=0
save_DELTA_T=0

def intercorrel(DELTA_X,DELTA_T,T,N=int(round(5/0.04))):
    
    RHO=np.zeros(N)
    
    mean_DELTA_X=np.mean(DELTA_X, axis=0)
    mean_DELTA_T=np.mean(DELTA_T, axis=0)
    
    delta_x_RMS=0
    delta_t_RMS=0

    for n in range(50):
        for p in range(94):
            for i in range(len(DELTA_X)):
                delta_x_RMS+=(DELTA_X[i][n][p]-mean_DELTA_X[n][p])**2
                delta_t_RMS+=(DELTA_T[i][n][p]-mean_DELTA_T[n][p])**2
    
    #print(mean_DELTA_X[0][0],DELTA_X[0][0])

    delta_x_RMS=np.sqrt(delta_x_RMS/(50*94*T))
    delta_t_RMS=np.sqrt(delta_t_RMS/(50*94*T))
    
    for k in range(N):
        for n in range(50):
            for p in range(94):
                rho=0
                for i in range(len(DELTA_X)-k):
                    deltax=DELTA_X[i+k][n][p]
                    mean_deltax=mean_DELTA_X[n][p]
                    deltat=DELTA_T[i][n][p]
                    mean_deltat=mean_DELTA_T[n][p]
                    rho+=(deltat-mean_deltat)*(deltax-mean_deltax)
                    
                rho=rho/(T-0.04*k)
                RHO[k]+=rho
        RHO[k]=RHO[k]/(delta_x_RMS*delta_t_RMS)
    
    return(RHO/(94*50))            

def time_diff_matrix(mom_infos):
    global f
    D_T=np.zeros([50,94])
    for i in range(50):
        for j in range(94):
            b=np.array([j,i])
            D_T[i][j]=sp.time_difference(mom_infos,b,f)
    return D_T

def distance_diff_matrix(mom_infos):
    D_X=np.zeros([50,94])
    for i in range(50):
        for j in range(94):
            b=np.array([j,i])
            D_X[i][j]=sp.distance_difference(mom_infos,b)
    return D_X

def event_correlation(event,F):
    deb=time.time()
    moments=event['moments']
    T=moments[0][2]-moments[-1][2]
    
    #DELTA_X = np.zeros([50, 94, len(moments)-1])
    #DELTA_T = np.zeros([50, 94, len(moments)-1])
    MOM_INFOS=[]
    for k in range(len(moments)-1):
        moment1=moments[k]
        moment2=moments[k+1]
        MOM_INFOS.append(sp.players_ball_speed_position(moment1,moment2))
    
    pool=mp.Pool()
    DELTA_X=pool.map(distance_diff_matrix, MOM_INFOS)
    DELTA_T=pool.map(time_diff_matrix, MOM_INFOS)
    pool.close()
    pool.join()        

    R=intercorrel(DELTA_X,DELTA_T,T)
    
    #plt.plot(R)
    #plt.show()
    
    maxi=0
    t=0
    for k in range(len(R)):
        if R[k]>maxi:
            maxi=R[k]
            t=k
    return(R,maxi,t)
    

def match_correlation(events):
    correlations=[]
    times=[]
    tau=[]
    rho=[]
    for event in events:
        print(event['eventId'])
        moments=event['moments']
        T=moments[0][2]-moments[-1][2]
        if T>6:
            times.append(T)
            R,maxi,t=event_correlation(event)
            correlations.append(R)
            tau.append(t)
            rho.append(maxi)
    
    df=pd.DataFrame({'tau':tau,'maxi':rho,'time':times})
    plt.plot(correlations)
    df.to_csv('match_correl.csv')
    df2=pd.DataFrame({'correl':correlations})
    df2.to_csv('match_correl2.csv')
        

        
        
def dt_event(i):
    event=events[i]
    moments=event['moments'] 
    T=[] 
    for i in range(len(moments)-1) :
        T.append(moments[i][2]-moments[i+1][2])
    
    T=pd.DataFrame({'time':T})
    print(T['time'].value_counts())
    

frames=[]
forces=[i for i in range(1,20)]+[30,50,100,1000]
keys=[]
moments_before=[]
if __name__=='__main__':
    for event in events :
        moments=event['moments']
        if len(moments_before)!=len(moments):
            moments_before=moments
            T=moments[0][2]-moments[-1][2]
            if T>6:
                print(event['eventId'])
                keys.append(event['eventId'])
                progress(0, len(forces), status=str(0))
                frames_forces=[]
                for i in range(len(forces)) :
                    f=forces[i]
                    R,maxi,t=event_correlation(event,f)
                    df=pd.DataFrame({'R':R,'tau':t,'rho':maxi,'time':T})
                    frames_forces.append(df)
                    progress(i, len(forces), status=str(f))
                event_df=pd.concat(frames_forces,keys=forces)
                frames.append(event_df)
                event_df.to_csv('event_'+str(event['eventId'])+'.csv', sep=',', encoding='utf-8')
            
total_df=pd.concat(frames,keys=keys)
total_df.to_csv('total_df.csv', sep=',', encoding='utf-8')


    

