import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import cartopy.crs as ccrs
#import scipy.stats as stats
import matplotlib.gridspec as gridspec
#import seaborn as sns
import pygplates
import xarray as xr
from gprm import ReconstructionModel

def dataframe_to_partitioned_point_features(dataframe, 
                                            reconstruction_model,
                                            longitude_field='longitude',
                                            latitude_field='latitude',
                                            fromage_field='FROMAGE',
                                            toage_field='TOAGE'):
    
    dataframe.dropna(subset=[longitude_field,latitude_field,fromage_field,toage_field])
    dataframe = dataframe[dataframe[fromage_field]>=dataframe[toage_field]]

    
    # point features is an empty list to begin with
    point_features = []
    # then we go through each row in the selected data, and add this row to our
    # list of features to reconstruct using GPlates
    for index,row in dataframe.iterrows():
        point = pygplates.PointOnSphere(float(row[latitude_field]),float(row[longitude_field]))
        point_feature = pygplates.Feature()
        point_feature.set_geometry(point)
        point_feature.set_valid_time(row[fromage_field],row[toage_field])
        # the last step in the loop is always to add the single feature to the list of features 
        point_features.append(point_feature)

    # The partition points function can then be used as before
    partitioned_point_features = pygplates.partition_into_plates(reconstruction_model.static_polygons,
                                                                 reconstruction_model.rotation_model,
                                                                 point_features) 
    
    return partitioned_point_features


def distance_to_point_features(partitioned_point_features, 
                               reconstruction_model, 
                               reconstruction_time,
                               anchor_plate_id=0):
    
    # Note that here, instead of saving the reconstructed points to a file, 
    # we can save them into a new object which we call 'reconstructed_point_features'
    reconstructed_point_features = []
    pygplates.reconstruct(partitioned_point_features, reconstruction_model.rotation_model,
                          reconstructed_point_features,reconstruction_time, anchor_plate_id=anchor_plate_id)

    
    snapshot = reconstruction_model.plate_snapshot(reconstruction_time, anchor_plate_id=anchor_plate_id)
    
    (reconstructed_lon, 
     reconstructed_lat, 
     distances) = snapshot.proximity_to_boundaries(reconstructed_point_features,
                                                   'subduction')

    return reconstructed_lon, reconstructed_lat, distances


def create_partitioned_feature_selection(df, selection_string, reconstruction_model):    
    subset_df = df.iloc[np.where(df.environment.str.contains(selection_string, na=False))]
    #subset_df.dropna(subset=['age','longitude','latitude'], inplace=True)
    return dataframe_to_partitioned_point_features(subset_df, reconstruction_model)


def write_netcdf_grid(filename,x,y,z):
    ds = xr.DataArray(z, coords=[('y',y), ('x',x)], name='z')
    ds.to_netcdf(filename, format='NETCDF4')
    