# These functions are created for 
# helping the calculations of necessary things
# for geographical works that uses LIDAR Point Clouc as input.
# GITHUB: metin-yat

import numpy as np
import os 
import laspy

import open3d as o3d
import xarray
import rioxarray

def _load_pcd_as_ndarray(PCD_NAME: str,
                         ROOT_PATH:str) -> np.ndarray :
    # PCD_NAME is your point cloud name -> PCD_NAME.laz/las
    # ROOT_PATH is where your files are inside of
    # ROOT_PATH basically can be just "." 
    # This func. uses (numpy, os, laspy) libraries.

    points = laspy.read(os.path.join(ROOT_PATH,
                                     PCD_NAME))
    
    xyz = np.vstack((points.x,
                     points.y,
                     points.z)).transpose()
    
    return xyz

def _visualize_xyz(XYZ: np.ndarray):
    # Takes xyz as np.ndarray 
    # & Visualize & returns the count of points
    # in the point cloud (PCD_NAME.las)

    try:
        import open3d as o3d

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(XYZ)
        
        o3d.visualization.draw_geometries([pcd])

        return pcd

    except ImportError:
        print("IMPORT ERROR! CHECK open3d")
def _chm_extraction(ROOT_PATH:str,
                    DSM_NAME:str,DTM_NAME:str
                    ) -> xarray.core.dataarray.DataArray:
    # ROOT_PATH is where your files are inside of
    # ROOT_PATH basically can be just "." 
    # DSM/DTM_NAME: are the existing tif files that you already
    # calculated from your existing point cloud.
    # You need to have them before calculating CHM.
    # Takes DTM & DSM and extract Canopy Height Model (CHM)
    # save it to ROOT_PATH &returns CHM as xarray.core.dataarray.DataArray

    try:
        import xarray
        import os

        dsm_path = os.path.join(ROOT_PATH, DSM_NAME)
        dtm_path = os.path.join(ROOT_PATH, DTM_NAME)

        da_dtm = xarray.open_rasterio(dtm_path).drop('band')[0]
        nodata = da_dtm.nodatavals[0]
        da_dtm = da_dtm.where(da_dtm>nodata, np.nan)

        da_dsm = xarray.open_rasterio(dsm_path).drop('band')[0]
        nodata = da_dsm.nodatavals[0]
        da_dsm = da_dsm.where(da_dsm>nodata, np.nan)

        da_chm = da_dsm- da_dtm

        chm_data_path = os.path.join(ROOT_PATH,'CHM.tif')
        da_chm.rio.to_raster(chm_data_path)

        return da_chm
    except ImportError:
        print("IMPORT ERROR! CHECK xarray")
    

def _open_tif_files(ROOT_PATH:str,
                    CHM_NAME:str):
    # Just getting back what you gave :D
    chm_data_path = os.path.join(ROOT_PATH, CHM_NAME)
    return xarray.open_rasterio(chm_data_path).squueze()

def _visualize_withgdal(ROOT_PATH:str,
                    MODEL_PATH:str):
    # Visualize your .tif file using osgeo library
    # ROOT_PATH: same
    # MODEL_PATH: Name of your .tif file that you want to
    # visualize
    try:
        from osgeo import gdal
        import matplotlib.pyplot as plt

        TIF_PATH = os.path.join(ROOT_PATH, MODEL_PATH)

        image = gdal.Open(TIF_PATH, gdal.GA_ReadOnly)
        band = image.GetRasterBand(1)

        arr = band.ReadAsArray()

        print(image.RasterXSize,
            image.RasterYSize)
        plt.imshow(arr)

    except ImportError:
        print("YOU GOT AN IMPORT ERROR FOR OSGEO (GDAL) OR MATPLOTLIB\n")
    
    


def _visualize_withpyplot(ROOT_PATH:str,
                          MODEL_PATH:str,
                          _cmap="Greens"):
    # Visualize your .tif file using matplotlib library
    # ROOT_PATH: same
    # MODEL_PATH: Name of your .tif file that you want to
    # visualize

    try:
        import os
        import matplotlib.pyplot as plt
        import rioxarray

        chm_data_path = os.path.join(ROOT_PATH, MODEL_PATH)
        chm_data = rioxarray.open_rasterio(chm_data_path).squeeze()

        fig, ax = plt.subplots(figsize=(15, 7))
        chm_data.plot(cmap= _cmap)

        ax.set_axis_off()
        _ = ax.set_title("Canopy Height Model (CHM)", fontsize= 10)


    except ImportError:
        print("YOU ARE HAVING IMPORT ERROR\n Check matplotlib, rioxarray")
    
def _advanced_visualization():
    #treedetection3.py
    pass

def _normalize_points(points: np.ndarray) -> np.ndarray: 
    # points: as np.ndarray 

    centroid = np.mean(points, axis=0)
    points -= centroid
    furthest_distance = np.max(np.sqrt(np.sum(abs(points)**2,axis=-1)))
    points /= furthest_distance

    return points

def _calculate_model_with_pipeline(_PIPELINE:str):
    # This function takes JSON Pipeline and make it work.
    # returns dictionary that contains arrays, metadata, log of your pipeline

    try:
        import pdal

        pipeline = pdal.Pipeline(_PIPELINE)
        count = pdal.execute()

        arrays = pipeline.arrays
        metadata = pipeline.metadata
        log = pipeline.log

        infos = {
            "arrays" : arrays,
            "metadata" : metadata,
            "log" : log,
        }

        return infos


    except ImportError:
        print("YOU ARE HAVING IMPORT ERROR\n CHECK pdal")

def _observe_laplacian_sobelXY(ROOT_PATH:str,
                            MODEL_NAME:str,
                            _make_it_gray=False):
    # It takes your model (e.g. CHM) 
    # apply some filters on it for some use cases
    # e.g. finding local maxima on it.

    try:
        import rioxarray
        import cv2
        import os 
        import matplotlib.pyplot as plt 

        model_path = os.path.join(ROOT_PATH, 
                                  MODEL_NAME)
        model = rioxarray.open_rasterio(model_path).squeeze().values

        if _make_it_gray == True:
            model = cv2.cvtColor(model, cv2.COLOR_BGR2GRAY)
        else:
            laplacian = cv2.Laplacian(model, cv2.CV_64F)
            sobelx = cv2.Sobel(model, cv2.CV_64F, 1, 0, ksize=5)
            sobely = cv2.Sobel(model, cv2.CV_64F, 1, 0, ksize=5)

            plt.subplot(2, 2, 1), plt.imshow(model)
            plt.title('Original'), plt.xticks([]), plt.yticks([])

            plt.subplot(2, 2, 2), plt.imshow(laplacian)
            plt.title('laplacian'), plt.xticks([]), plt.yticks([])

            plt.subplot(2, 2, 3), plt.imshow(sobelx)
            plt.title('Sobel X'), plt.xticks([]), plt.yticks([])

            plt.subplot(2, 2, 4), plt.imshow(sobely)
            plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

            save_figure_as_png_path = os.path.join(ROOT_PATH,
                                                   'laplacian_sobelXY_graphs.png')

            plt.savefig(save_figure_as_png_path,
                        dpi=300, orientation='landscape',
                        bbox_inches='tight', pad_inches=0.1)

    except ImportError:
        print("YOU ARE HAVING IMPORT ERROR\n CHECK pdal")

def _save_ndarray_as_las(xyz: np.ndarray,
                         _point_format_id:int,
                         ROOT_PATH, file_name:str):
    try:
        import numpy as np
        import pylas

        pcd = pylas.create(point_format_id= _point_format_id)
        pcd.xyz = xyz

        pcd.write(ROOT_PATH, file_name)

        
    except ImportError:
        print("This process using pylas & numpy libraries. Check them.")



# save the all models above as .tif and so
# then calculate find_maxima 