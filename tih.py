import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def get_1_data():
    gen_1 = pd.read_csv('Plant_1_Generation_Data.csv')
    return gen_1

def sens_2_data():
    sens_1 = pd.read_csv('Plant_1_Weather_Sensor_Data.csv')
    return sens_1

def drop_and_convert(gen_1, sens_1):
    gen_1.drop('PLANT_ID',1,inplace=True)
    sens_1.drop('PLANT_ID',1,inplace=True)
    gen_1['DATE_TIME']= pd.to_datetime(gen_1['DATE_TIME'],format='%d-%m-%Y %H:%M')
    sens_1['DATE_TIME']= pd.to_datetime(sens_1['DATE_TIME'],format='%Y-%m-%d %H:%M:%S')

    return gen_1, sens_1

def dc_power_converted(losses=None, sens_1=None):
    losses = get_1_data()
    sens_1 = sens_2_data()
    losses, sens_1 = drop_and_convert(losses, sens_1)
    losses['day']=losses['DATE_TIME'].dt.date
    losses=losses.groupby('day').sum()
    losses['losses']=losses['AC_POWER']/losses['DC_POWER']*100

    losses['losses'].plot(style='o--',figsize=(17,5),label='Real Power')

    plt.title('% of DC power converted in AC power',size=17)
    plt.ylabel('DC power converted (%)',fontsize=14,color='red')
    plt.axhline(losses['losses'].mean(),linestyle='--',color='gray',label='mean')
    plt.legend()
    #return the plot as an image
    plt.savefig('values/losses.png')

def dc_power_generated():
    sources = get_1_data()
    sources['DATE_TIME']= pd.to_datetime(sources['DATE_TIME'],format='%d-%m-%Y %H:%M')
    sources['time']=sources['DATE_TIME'].dt.time
    sources.set_index('time').groupby('SOURCE_KEY')['DC_POWER'].plot(style='o',legend=True,figsize=(20,10))
    plt.title('DC Power during day for all sources',size=17)
    plt.ylabel('DC POWER ( kW )',color='navy',fontsize=17)
    plt.savefig('values/dc_generated.png')

def underperforming_modules():
    dc_gen = get_1_data()
    dc_gen['DATE_TIME']= pd.to_datetime(dc_gen['DATE_TIME'],format='%d-%m-%Y %H:%M')
    dc_gen['time']=dc_gen['DATE_TIME'].dt.time
    dc_gen=dc_gen.groupby(['time','SOURCE_KEY'])['DC_POWER'].mean().unstack()

    cmap = sns.color_palette("Spectral", n_colors=12)

    fig,ax=plt.subplots(ncols=2,nrows=1,dpi=100,figsize=(15,5))
    dc_gen.iloc[:,0:11].plot(ax=ax[0],color=cmap)
    dc_gen.iloc[:,11:22].plot(ax=ax[1],color=cmap)

    ax[0].set_title('First 11 sources')
    ax[0].set_ylabel('DC POWER ( kW )',fontsize=17,color='navy')
    ax[1].set_title('Last 11 sources')
    plt.savefig("values/underperforming_modules.png")

def dc_power_daily_yield():
    temp1_gen=get_1_data()
    temp1_gen['DATE_TIME']= pd.to_datetime(temp1_gen['DATE_TIME'],format='%d-%m-%Y %H:%M')

    temp1_gen['time']=temp1_gen['DATE_TIME'].dt.time
    temp1_gen['day']=temp1_gen['DATE_TIME'].dt.date


    temp1_sens=sens_2_data()
    temp1_sens['DATE_TIME']= pd.to_datetime(temp1_sens['DATE_TIME'],format='%Y-%m-%d %H:%M:%S')

    temp1_sens['time']=temp1_sens['DATE_TIME'].dt.time
    temp1_sens['day']=temp1_sens['DATE_TIME'].dt.date

    # just for columns
    cols=temp1_gen.groupby(['time','day'])['DC_POWER'].mean().unstack()
    ax =temp1_gen.groupby(['time','day'])['DC_POWER'].mean().unstack().plot(sharex=True,subplots=True,layout=(17,2),figsize=(20,30))
    temp1_gen.groupby(['time','day'])['DAILY_YIELD'].mean().unstack().plot(sharex=True,subplots=True,layout=(17,2),figsize=(20,20),style='-.',ax=ax)

    i=0
    for a in range(len(ax)):
        for b in range(len(ax[a])):
            ax[a,b].set_title(cols.columns[i],size=15)
            ax[a,b].legend(['DC_POWER','DAILY_YIELD'])
            i=i+1

    plt.tight_layout()
    plt.savefig("values/dc_power_daily_yield.png")
    ax= temp1_sens.groupby(['time','day'])['MODULE_TEMPERATURE'].mean().unstack().plot(subplots=True,layout=(17,2),figsize=(20,30))
    temp1_sens.groupby(['time','day'])['AMBIENT_TEMPERATURE'].mean().unstack().plot(subplots=True,layout=(17,2),figsize=(20,40),style='-.',ax=ax)

    i=0
    for a in range(len(ax)):
        for b in range(len(ax[a])):
            ax[a,b].axhline(50)
            ax[a,b].set_title(cols.columns[i],size=15)
            ax[a,b].legend(['Module Temperature','Ambient Temperature'])
            i=i+1

    plt.tight_layout()
    plt.savefig("values/module_ambient_temperature.png")

def forecasting():
    pred_gen=get_1_data()
    pred_gen['DATE_TIME']= pd.to_datetime(pred_gen['DATE_TIME'],format='%d-%m-%Y %H:%M')
    pred_gen=pred_gen.groupby('DATE_TIME').sum()
    pred_gen=pred_gen['DAILY_YIELD'][-288:].reset_index()
    pred_gen.set_index('DATE_TIME',inplace=True)

    train=pred_gen[:192]
    test=pred_gen[-96:]
    plt.figure(figsize=(15,5))
    plt.plot(train,label='Real',color='navy')
    plt.plot(test,label='Forecasted',color='darkorange')
    plt.title('Last 4 days of daily yield',fontsize=17)
    plt.legend()
    plt.savefig('values/forecasting.png')