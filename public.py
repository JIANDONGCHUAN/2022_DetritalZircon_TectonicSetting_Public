import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas import Series,DataFrame
from numpy import nan as NaN
import statsmodels.api as sm # recommended import according to the docs


from pooch import os_cache as _os_cache
from pooch import retrieve as _retrieve
from pooch import HTTPDownloader as _HTTPDownloader
from pooch import Unzip as _Unzip
#import geopandas as _gpd
import os as _os

def fetch_Putze2019(load=True):
    '''Puetz, S. J., & Condie, K. C. (2019). Time series analysis of mantle cycles Part I: Periodicities and correlations among seven global isotopic databases. Geoscience Frontiers, 10(4), 1305–1326. https://doi.org/10.1016/j.gsf.2019.04.002'''
    fnames = _retrieve(
        url="https://github.com/JIANDONGCHUAN/Data_and_Models_Public/blob/main/puetz2019.zip?raw=true",
        known_hash="sha256:e11360a84c26d0d5f46ed84428c588470c3ced1986bc3eed45ee63c0cf78da16",  
        downloader=_HTTPDownloader(progressbar=True),
        path=_os_cache('data'),
        processor=_Unzip(extract_dir='Putze_2019'),
    )

    dirname = _os.path.split(fnames[0])[0]
    df_Ref_2019 = pd.read_excel('{:s}/1-s2.0-S1674987119300751-mmc1.xlsx'.format(dirname),sheet_name="References")
    df_Sample_2019 = pd.read_excel('{:s}/1-s2.0-S1674987119300751-mmc1.xlsx'.format(dirname),sheet_name="Samples")
    df_Data_2019 = pd.read_excel('{:s}/1-s2.0-S1674987119300751-mmc4.xlsx'.format(dirname),sheet_name="U_Pb_Detrital_Zircon")
    return df_Ref_2019, df_Sample_2019, df_Data_2019

def fetch_Putze2021_mmc1(load=True):
    '''#Puetz, S. J., Spencer, C. J., & Ganade, C. E. (2021). Analyses from a validated global UPb detrital zircon database: Enhanced methods for filtering discordant UPb zircon analyses and optimizing crystallization age estimates. Earth-Science Reviews, 103745. https://doi.org/10.1016/j.earscirev.2021.103745'''
    fnames = _retrieve(
        url="https://github.com/JIANDONGCHUAN/Data_and_Models_Public/blob/main/puetz2021_mmc1.zip?raw=true",
        known_hash="sha256:7f5c51665ddca1e04afa7095144c0d0e92248eeec40cc60b54f2c0ba92b21075",  
        downloader=_HTTPDownloader(progressbar=True),
        path=_os_cache('data'),
        processor=_Unzip(extract_dir='Putze_2021'),
    )

    dirname = _os.path.split(fnames[0])[0]
    df_Ref_2021 = pd.read_excel('{:s}/1-s2.0-S0012825221002464-mmc1.xlsx'.format(dirname),sheet_name="References")
    df_Sample_2021 = pd.read_excel('{:s}/1-s2.0-S0012825221002464-mmc1.xlsx'.format(dirname),sheet_name="Samples")
    df_Data_2021 = pd.read_excel('{:s}/1-s2.0-S0012825221002464-mmc1.xlsx'.format(dirname),sheet_name="UPb_Data")
    return df_Ref_2021, df_Sample_2021, df_Data_2021

def fetch_active_rifts(load=True):
    fnames = _retrieve(
        url="https://github.com/JIANDONGCHUAN/Data_and_Models_Public/blob/main/rifts/Sengor-Natalin-rifts.gpml?raw=true",
        known_hash="sha256:fc69f900de124e02eed794dffcca097f799405279fd72a0049a3b9f5c7344636",  
        downloader=_HTTPDownloader(progressbar=True),
        path=_os_cache('data'),
    )
    return fnames

def fetch_inactive_rifts(load=True):
    fnames = _retrieve(
        url="https://github.com/JIANDONGCHUAN/Data_and_Models_Public/blob/main/rifts/Sengor-Natalin_inactive_rifts.gpml?raw=true",
        known_hash="sha256:821b9dfbae9d2fb2eb50eac4df8510d25ad2000943257d00e80a65da6328c7e4",  
        downloader=_HTTPDownloader(progressbar=True),
        path=_os_cache('data'),
    )
    return fnames

def fetch_active_passive_margin(load=True):
    fnames = _retrieve(  
        url="https://github.com/JIANDONGCHUAN/Data_and_Models_Public/raw/main/rifts/present_day_passive_margin_active_rift_multipoints.gpmlz",
        known_hash="sha256:79820e97a053630ac1f7efb972a618d8a221df387fcdd271d7f66a6659b52239",  
        downloader=_HTTPDownloader(progressbar=True),
        path=_os_cache('data'),
    )
    return fnames

def fetch_inactive_passive_margin(load=True):
    fnames = _retrieve(
        url="https://github.com/JIANDONGCHUAN/Data_and_Models_Public/raw/main/rifts/present_day_passive_margin_inactive_rift_multipoints.gpmlz",
        known_hash="sha256:1c2f87ed9ddde518478e78a0fca4b26ef5ed47e819c5e387207f04cd2d51f64f",  
        downloader=_HTTPDownloader(progressbar=True),
        path=_os_cache('data'),
    )
    return fnames




def plot_figure9(df_test, savefig = False, show_equation = False):
    df_threshold = pd.read_csv('data/better_threshold.csv',sep=',')
    fig, ax = plt.subplots(1, 3, figsize = (12,4))
    value1 = np.arange(0,1,0.01)
    value2 = np.arange(0,3010,10)
    vmaxs = [1,1,0.8]
    titles = ('(a) Precision','(b) Recall','(c) F$-$score')
    for i, key in enumerate(['precision','sensitivity','F1']):
        #cm = ax[i].contour(value2, value1, np.reshape(np.array(df_threshold[key]), (len(value1), len(value2))), levels=20, cmap= plt.cm.magma_r)
        cm = ax[i].pcolormesh(value2, value1,
                     np.reshape(np.array(df_threshold[key]), (len(value1), len(value2))),vmin=0.2, vmax=vmaxs[i], cmap= plt.cm.magma_r)
        ax[i].set_xlim(0,3000)
        ax[i].set_ylim(0,1)
        ax[i].set_title(titles[i])
        #ax[i].scatter(x=270,y=0.37, zorder=2, color='SpringGreen')
        ax[i].scatter(x=100,y=0.30, zorder=2, color='yellow')
        ax[i].set_xlabel('CA$-$DA (Ma)')
        if i == 0:
            ax[i].set_ylabel('Cumulative proportion')
            #ax[i].set_ylabel('Cumulative Frequency')
        plt.colorbar(cm, ax=ax[i])

        CA_DA = df_test['206Pb/238U age (Ma)'] - df_test['Depos. Age (Ma)']
        #CA_DA.dropna(inplace=True)
        if CA_DA.shape[0]>0:
            ecdf = sm.distributions.ECDF(CA_DA)
            x = np.linspace(0, 3000, 100)
            y = ecdf(x)
            ax[i].step(x, y, color = 'grey', alpha=0.8)

            z1 = np.polyfit(x, y, 20) # 用20次多项式拟合
            p1 = np.poly1d(z1)
            yvals=p1(x) # 也可以使用yvals=np.polyval(z1,x)
            ax[i].plot(x, yvals, color='SpringGreen', alpha = 0.5)
    if show_equation == True:
        print(p1)
    if savefig == True:
        plt.savefig('fig9.png', dpi=600) 

    left_data = pd.DataFrame()
    position=[]
    for i in np.arange(len(df_threshold)):
        df_each = df_threshold.iloc[i,:]
        x = df_each['x']
        y = np.round(p1(x),2)
        if df_each['y'] == y:
            position.append('on_line')
        elif df_each['y'] < y:
            position.append('left')
        else:
            position.append('right')
    df_threshold['position']=position

    df_on_line = df_threshold[df_threshold['position']=='on_line']
    #print(len(df_threshold))
    #print(len(df_left))
    precision_mean = df_on_line['precision'].mean()
    recall_mean = df_on_line['recall'].mean()
    #F = df_left['F1'].min()

    print('precision_mean:')
    print(precision_mean)
    print('recall_mean:')
    print(recall_mean)

def fetch_Clennett(load=True, model_case='S2013'):
    if model_case=='S2013':
        fnames = _retrieve(
            url="https://www.earthbyte.org/webdav/ftp/Data_Collections/Clennett_etal_2020_G3/Clennett_etal_2020_S2013.zip",
            known_hash="sha256:7749aac19c2d07c80a2cd77ba6a9038c8911fa8804c1d4adb3c9da7cb635b691",  
            downloader=_HTTPDownloader(progressbar=True),
            path=_os_cache('gprm'),
            processor=_Unzip(extract_dir='Clennett2020_S2013'),
        )

        #dirname = '{:s}/Clennett_etal_2020_S2013/'.format(_os.path.split(fnames[0])[0])
        dirname = '{:s}/Clennett2020_S2013/Clennett_etal_2020_S2013/'.format(fnames[0].split('Clennett2020_S2013')[0])


        from gprm import ReconstructionModel as _ReconstructionModel
        reconstruction_model = _ReconstructionModel('Clennett++S2013')
        
        reconstruction_model.add_rotation_model('{:s}/Clennett_etal_2020_Rotations.rot'.format(dirname))
        
        reconstruction_model.add_static_polygons('{:s}/Clennett_etal_2020_Terranes.gpml'.format(dirname))

        reconstruction_model.add_continent_polygons('{:s}/Clennett_etal_2020_Terranes.gpml'.format(dirname))
        reconstruction_model.add_coastlines('{:s}/Clennett_etal_2020_Coastlines.gpml'.format(dirname))
        
        reconstruction_model.add_dynamic_polygons('{:s}/Clennett_etal_2020_NAm_boundaries.gpml'.format(dirname))
        reconstruction_model.add_dynamic_polygons('{:s}/Clennett_etal_2020_Plates.gpml'.format(dirname))

        return reconstruction_model 

