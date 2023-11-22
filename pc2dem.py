import os 
# Needed for loading json files
import json
# Needed for reading and executing pipelines
import pdal


# for visualization functions    
from osgeo import gdal
import matplotlib.pyplot as plt

# for CHM generation
import numpy as np
import rasterio as rio
from rasterio.plot import show
from rasterio.plot import show_hist
from shapely.geometry import Polygon, mapping
from rasterio.mask import mask
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep

from matplotlib.colors import ListedColormap
import matplotlib.colors as colors

from glob import glob

######
import numpy.ma as ma

# for detecting best combination
import itertools

# - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - -
# Getting needed pipeline & executing.
# That means we'll generate some DEM
# Next functions - generate_dem_xxxx - will work
# no matter what the purpose is 
# as long as it is pipeline and pdal needed.
# Which means you can generate any model (dtm or dsm).
# - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def generate_dem_from_path(json_path):
    # This func. will take any executable
    # json file and make it work. 
    # But you should always adapt the things 
    # like params paths and so on.

    with open(json_path) as pipeline:
        json_dict = json.load(pipeline)
        _json= json.dumps(json_dict)
    
    pipeline = pdal.Pipeline(_json)
    count = pipeline.execute()
    # arrays = pipeline.arrays
    metadata = pipeline.metadata
    # log = pipeline.log
    
# - - - - - - - - - - - - -
"""
param_dict = {
    "input_path": "3333313132413.laz",
    "filters.smrf":{
        "type":"filters.33333",
        "ignore":"33333[33333:33333]",
        "slope":33333,
        "window":33333,
        "threshold":33333,
        "scalar":33333,
        "returns":"33333, 33333"
        },
    "writers.gdal":{
        "type":"writers.gdal",
        "filename":"33333.tif",
        "gdaldriver":"33333",
        "output_type":"33333",
        "window_size":"33333",
        "resolution":"33333"
    }
}
"""
def generate_dem_from_dict_v1(whole_pipeline:dict,
                           dict_params:dict):
    # Difference between these two generation func
    # is that the names suggest one takes a path
    # other one takes a dictionary that you'll take from
    # json path.
    
    # You need to know that this pipeline has its own params for
    # labeling-classifying points. e.g. morphological filter
    """
    dict_pipeline: dictionary form of pipeline.
    dict_params: params of the algorithms
    """
    # Getting the pipeline 
    # it is a list of funcs.and more
    pipeline = whole_pipeline["pipeline"]
    
    # set input point cloud.
    input_path = dict_params["input_path"]
    pipeline[0] = input_path

    # filename is the output name
    for (index,i) in enumerate(pipeline[1::]):
        if (i["type"] in dict_params.keys()): 
            needed_params = dict_params[i["type"]]
            for j in i.keys():
                if j in needed_params.keys():
                    pipeline[index+1][j] = needed_params[j]
                else:
                    print(index, ":D :D :D :D :D :D :D :D :D :D")
    
    whole_pipeline["pipeline"]= pipeline
    _json = json.dumps(whole_pipeline)
    
    pipeline = pdal.Pipeline(_json)
    count = pipeline.execute()
    # arrays = pipeline.arrays
    metadata = pipeline.metadata
    # log = pipeline.log
    
    return pipeline
    
def generate_dem_from_dict_v2(pipeline_dict:dict):
    _json= json.dumps(pipeline_dict)
    pipeline = pdal.Pipeline(_json)
    count = pipeline.execute()
    # arrays = pipeline.arrays
    metadata = pipeline.metadata
    # log = pipeline.log
    
# - - - - - - - - - - - - - - - - - - - - - - - - - -

def single_rband_visualizer(root ,dem_path,
                            visualize:bool= False):
    # root for saving 
    #  dem_path for getting tiff
    # visualize= True if youre using jupyter 

    data = gdal.Open(dem_path)
    # data.RasterCount
    # Note that this is just for Single band
    # so its just one stat
    # you can basically make it for other bands too
    # but its just experimental
    # this funcs are aimed to examine the dem.tiff
    
    band1 = data.GetRasterBand(1)
    b1 = band1.ReadAsArray()

    plt.imsave(root, b1)
    
    if visualize == True:
        plt.imshow(b1)
        
# - - - - - - - - - - - - -
def change_tiff_name(old, new):
    os.rename(old, new)
    
# - - - - - - - - - - - - -
# import rasterio 
# from rasterio.plot import show
def get_info(dem_path)-> list:
    
    data= rasterio.open(dem_path)
    # count is band count
    # height and width is resolution
    # crs is EPSG
    return [data.count,
            (data.height, data.width),
            data.crs]
    

# - - - - - - - - - - - - -
def generate_chm(DTM_PATH:str,
                 DSM_PATH:str,
                 OUTPUT_PATH:str,
                 save_png:bool=False):
    # Notice that there is no second output path for
    # saving png files. So there must be folder like under this comment
    
    # Returns masked array that contains Canopyt Height Model.
    
    PNG_SAVE_PATH = os.path.join(
        OUTPUT_PATH, "png"
    )
    
    DTM_LIST = glob(DTM_PATH)
    DSM_LIST = glob(DSM_PATH)
    
    for i in DTM_LIST:
        for j in DSM_LIST:
            print(". . . ExtractinG Model Files . . .")
            
            # Extractin DTM Model file 
            with rio.open(i) as src:
                lidar_dem_im = src.read(1, masked =True)
                sjer_ext = rio.plot.plotting_extent(src)
                print(" Extracted DTM: ", os.path.basename(i))

            # Extracting DSM Model File
            with rio.open(j) as src:
                lidar_dsm_im = src.read(1, masked= True)
                dsm_meta = src.profile
                print(" Extracted DSM: ", os.path.basename(j))

            lidar_chm = lidar_dsm_im - lidar_dem_im
            lidar_chm_asarray = ma.compress_rowcols(lidar_chm, 1)
            
            CHM_NAME =  str(os.path.basename(i),
                            "-", os.path.basename(j))
            
            PNG_SAVE_NAME = str(CHM_NAME,".png") 
            NP_SAVE_NAME = str(CHM_NAME, ".np")
            
            PNG_WHOLE_PATH= os.path.join(
                PNG_SAVE_PATH, PNG_SAVE_NAME
            )
            
            NP_WHOLE_PATH = os.path.join(
                OUTPUT_PATH, NP_SAVE_NAME
            )
            # Saving the masked array as numpy array in the 
            # specified path.
            np.save(NP_WHOLE_PATH, lidar_chm_asarray)
            
            
            if (save_png==True):
                # Plotting every CHM 
                plt.imsave(PNG_WHOLE_PATH)

    return lidar_chm

# - -- -- - -- - -- - - - -- 
def detect_best_by_number(dict_with_param_lists:dict,
                          best_combination_number:int) -> dict:
    # gets param lists that will where combinations were created
    # and also gets best combination number which for this,
    # manuel confirmation needed. Since this is an experimental work,
    # you have to examine all the results (dtm,dsm & chm) and then
    # decide which has the best params.
    # i.e. best chm name: dtm-25:dsm-10.tif/.png ; you'll send
    # dict_with_param_list which is you used to optimize & also
    # 25t as best_combination_number if you want to see params of 
    # best resulting DTM.
    all_combinations = []
    
    for combination in itertools.product(*dict_with_param_lists.values()):
        all_combinations.append(combination)
    return all_combinations[best_combination_number]