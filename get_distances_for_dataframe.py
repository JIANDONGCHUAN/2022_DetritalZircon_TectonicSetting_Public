import pygplates



def get_distances_for_dataframe(dataframe, 
                                reconstruction_model, 
                                reconstruction_time,
                                anchor_plate_id=0,
                                remove_points_older_than_polygon=False):
    # If the option 'remove_points_older_than_polygon' is set to True, points will be excluded if the 
    # 'from_age' of the polygon they lie within is less than the reconstruction time
    
    
    # point features is an empty list to begin with
    point_features = []
    # then we go through each row in the selected data, and add this row to our
    # list of features to reconstruct using GPlates
    for index,row in dataframe.iterrows():
        point = pygplates.PointOnSphere(float(row.Latitude),float(row.Longitude))
        point_feature = pygplates.Feature()
        point_feature.set_geometry(point)
        # temporarily store the appearance and disappearance we'll want in shapefile attributes
        point_feature.set_shapefile_attribute('age_max',row.FROMAGE)
        point_feature.set_shapefile_attribute('age_min',row.TOAGE)
        # the last step in the loop is always to add the single feature to the list of features 
        point_features.append(point_feature)

    # The partition points function can then be used as before
    partitioned_point_features = pygplates.partition_into_plates(reconstruction_model.static_polygons,
                                                                 reconstruction_model.rotation_model,
                                                                 point_features,
                                                                 properties_to_copy = [
                                                                     pygplates.PartitionProperty.reconstruction_plate_id,
                                                                     pygplates.PartitionProperty.valid_time_period]) 
    
    partitioned_point_features_selection = []
    number_of_rejected_points = 0
    for partitioned_point_feature in partitioned_point_features:
        
        if remove_points_older_than_polygon:
            # only keep the point if it got its plateid from a polygon that exists for chosen reconstruction time
            if partitioned_point_feature.get_valid_time()[0] > reconstruction_time:
                partitioned_point_feature.set_valid_time(partitioned_point_feature.get_shapefile_attribute('age_max'),
                                                         partitioned_point_feature.get_shapefile_attribute('age_min'))
                partitioned_point_features_selection.append(partitioned_point_feature)
            else:
                number_of_rejected_points+=1
        else:
            partitioned_point_feature.set_valid_time(partitioned_point_feature.get_shapefile_attribute('age_max'),
                                                     partitioned_point_feature.get_shapefile_attribute('age_min'))
            partitioned_point_features_selection.append(partitioned_point_feature)
            
    #if number_of_rejected_points > 0:
        #print('Total number of points rejected due to inconsistency with polygon age = {:d}'.format(number_of_rejected_points))
    
    # Note that here, instead of saving the reconstructed points to a file, 
    # we can save them into a new object which we call 'reconstructed_point_features'
    reconstructed_point_features = []
    pygplates.reconstruct(partitioned_point_features_selection,reconstruction_model.rotation_model,
                          reconstructed_point_features,reconstruction_time,anchor_plate_id=anchor_plate_id)

    # This step gets a 'snapshot' of a reconstruction at a specific time
    snapshot = reconstruction_model.plate_snapshot(reconstruction_time,anchor_plate_id=anchor_plate_id)
    
    # Once you have a 'snapshot', you can use it to compute the distance between a set of 
    # points (reconstructed to the same time) and the plate boundaries in the snapshot
    # The type of boundary can be specified as a particular type, for example here we only
    # choose 'subduction' boundaries
    (reconstructed_lon, 
     reconstructed_lat, 
     distances) = snapshot.proximity_to_boundaries(reconstructed_point_features,
                                                   'subduction')

    return reconstructed_lon, reconstructed_lat, distances





def get_lon_lat_for_dataframe(dataframe, 
                                reconstruction_model, 
                                reconstruction_time,
                                anchor_plate_id=0,
                                remove_points_older_than_polygon=False):
    # If the option 'remove_points_older_than_polygon' is set to True, points will be excluded if the 
    # 'from_age' of the polygon they lie within is less than the reconstruction time
    
    
    # point features is an empty list to begin with
    point_features = []
    # then we go through each row in the selected data, and add this row to our
    # list of features to reconstruct using GPlates
    for index,row in dataframe.iterrows():
        point = pygplates.PointOnSphere(float(row.Latitude),float(row.Longitude))
        point_feature = pygplates.Feature()
        point_feature.set_geometry(point)
        # temporarily store the appearance and disappearance we'll want in shapefile attributes
        point_feature.set_shapefile_attribute('age_max',row.FROMAGE)
        point_feature.set_shapefile_attribute('age_min',row.TOAGE)
        # the last step in the loop is always to add the single feature to the list of features 
        point_features.append(point_feature)

    # The partition points function can then be used as before
    partitioned_point_features = pygplates.partition_into_plates(reconstruction_model.static_polygons,
                                                                 reconstruction_model.rotation_model,
                                                                 point_features,
                                                                 properties_to_copy = [
                                                                     pygplates.PartitionProperty.reconstruction_plate_id,
                                                                     pygplates.PartitionProperty.valid_time_period]) 
    
    partitioned_point_features_selection = []
    number_of_rejected_points = 0
    for partitioned_point_feature in partitioned_point_features:
        
        if remove_points_older_than_polygon:
            # only keep the point if it got its plateid from a polygon that exists for chosen reconstruction time
            if partitioned_point_feature.get_valid_time()[0] > reconstruction_time:
                partitioned_point_feature.set_valid_time(partitioned_point_feature.get_shapefile_attribute('age_max'),
                                                         partitioned_point_feature.get_shapefile_attribute('age_min'))
                partitioned_point_features_selection.append(partitioned_point_feature)
            else:
                number_of_rejected_points+=1
        else:
            partitioned_point_feature.set_valid_time(partitioned_point_feature.get_shapefile_attribute('age_max'),
                                                     partitioned_point_feature.get_shapefile_attribute('age_min'))
            partitioned_point_features_selection.append(partitioned_point_feature)
            
    #if number_of_rejected_points > 0:
        #print('Total number of points rejected due to inconsistency with polygon age = {:d}'.format(number_of_rejected_points))
    
    # Note that here, saving the reconstructed points to a file, 

    reconstructed_point_features = []
    pygplates.reconstruct(partitioned_point_features_selection,reconstruction_model.rotation_model,
                          reconstructed_point_features,reconstruction_time,anchor_plate_id=anchor_plate_id)
                          
    reconstructed_lat = []
    reconstructed_lon = []
    for point in reconstructed_point_features:
            reconstructed_lat.append(point.get_reconstructed_geometry().to_lat_lon()[0])
            reconstructed_lon.append(point.get_reconstructed_geometry().to_lat_lon()[1])


    return reconstructed_lon, reconstructed_lat


def get_distances_for_dataframe_rifts(dataframe, reconstruction_model, rifts, reconstruction_time):
   
    # point features is an empty list to begin with
    point_features = []
    # then we go through each row in the selected data, and add this row to our
    # list of features to reconstruct using GPlates
    for index,row in dataframe.iterrows():
        point = pygplates.PointOnSphere(float(row.Latitude),float(row.Longitude))
        point_feature = pygplates.Feature()
        point_feature.set_geometry(point)
        point_feature.set_valid_time(row.FROMAGE,row.TOAGE)
        # the last step in the loop is always to add the single feature to the list of features 
        point_features.append(point_feature)

    # The partition points function can then be used as before
    partitioned_point_features = pygplates.partition_into_plates(reconstruction_model.static_polygons,
                                                                 reconstruction_model.rotation_model,
                                                                 point_features) 

    # Note that here, instead of saving the reconstructed points to a file, 
    # we can save them into a new object which we call 'reconstructed_point_features'
    reconstructed_point_features = []
    pygplates.reconstruct(partitioned_point_features,reconstruction_model.rotation_model,
                          reconstructed_point_features,reconstruction_time)

    # This step gets a 'reconstructed_rifts' of a reconstruction at a specific time
    reconstructed_rifts = []
    pygplates.reconstruct(rifts, reconstruction_model.rotation_model, reconstructed_rifts, reconstruction_time)
    
    # Then, you can use it to compute the distance between a set of 
    # points (reconstructed to the same time) and the reconstructed_rifts
    (reconstructed_lon, 
     reconstructed_lat, 
     distances) = proximity_to_rifts(reconstructed_point_features,reconstructed_rifts)

    return reconstructed_lon, reconstructed_lat, distances


from gprm.utils.geometry import distance_between_reconstructed_points_and_features
def proximity_to_rifts(reconstructed_point_features, reconstructed_rifts):
        
        #Given a set of reconstructed point features, returns the distance of each
        #point to the nearest reconstructed_rifts
        rift_features = []
        for reconstructed_rift in reconstructed_rifts:
            geom = reconstructed_rift.get_reconstructed_geometry()
            if geom is not None:
                feature = pygplates.Feature()
                feature.set_geometry(geom)
                rift_features.append(feature)
                #plt.plot(geom.to_lat_lon_array()[:,1],geom.to_lat_lon_array()[:,0])
        
        (reconstructed_lon,
         reconstructed_lat,
         distances) = distance_between_reconstructed_points_and_features(reconstructed_point_features,
                                                                         rift_features)
        return reconstructed_lon, reconstructed_lat, distances

from gprm import ReconstructionModel, PointDistributionOnSphere
from gprm.utils.spatial import rasterise_polygons

def get_random_points_within_continents(reconstruction_model, reconstruction_time, number_of_points=10000):

    random_points = PointDistributionOnSphere(distribution_type='random', N=number_of_points)

    res = rasterise_polygons(reconstruction_model.continent_polygons, 
                             reconstruction_model.rotation_model, 
                             reconstruction_time, 
                             random_points.meshnode_feature, 
                             masking='outside')

    points = []
    for feature in res:
        points.extend(feature.get_geometry().to_lat_lon_list())

    masked_longitudes = list(zip(*points))[1]
    masked_latitudes = list(zip(*points))[0]
    
    return masked_longitudes, masked_latitudes