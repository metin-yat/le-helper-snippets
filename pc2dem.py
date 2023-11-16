import os 
# Needed for loading json files
import json
# Needed for reading and executing pipelines
import pdal


# for visualization functions    
from osgeo import gdal
import matplotlib.pyplot as plt

# - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - -
# Getting needed pipeline & executing.
# That means we'll generate some DEM
# Next function - generate_dem_xxxx - will work
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

def generate_dem_from_dict(whole_pipeline:dict, dict_params:dict,
                           which_one:str="dtm"):
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
    
    """output_ = os.path.join(
        root, "dem_image.png"
    )
    """
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
    
