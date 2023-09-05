import numpy as np
import open3d as o3d
import glob, os
from glbToPly import saveAsPly


def augment1(pcd:o3d.geometry.PointCloud):
    new_point_cloud = o3d.geometry.PointCloud()
    new_point_cloud.points = o3d.utility.Vector3dVector(
        pcd.points * np.array([2, 1, 1]))
    return new_point_cloud

def augment2(pcd:o3d.geometry.PointCloud):
    new_point_cloud = o3d.geometry.PointCloud()
    new_point_cloud.points = o3d.utility.Vector3dVector(
        pcd.points * np.array([1, 1.5, 1]))
    return new_point_cloud

def augment3(pcd:o3d.geometry.PointCloud):
    new_point_cloud = o3d.geometry.PointCloud()
    new_point_cloud.points = o3d.utility.Vector3dVector(
        pcd.points * np.array([1, 1, 2]))
    return new_point_cloud

def augment4(pcd:o3d.geometry.PointCloud):
    new_point_cloud = o3d.geometry.PointCloud()
    new_point_cloud.points = o3d.utility.Vector3dVector(
        pcd.points * np.array([2, 1.5, 1]))
    return new_point_cloud

def augment5(pcd:o3d.geometry.PointCloud):
    new_point_cloud = o3d.geometry.PointCloud()
    new_point_cloud.points = o3d.utility.Vector3dVector(
        pcd.points * np.array([2, 1, 2]))
    return new_point_cloud
    
def augment6(pcd:o3d.geometry.PointCloud):
    new_point_cloud = o3d.geometry.PointCloud()
    new_point_cloud.points = o3d.utility.Vector3dVector(
        pcd.points * np.array([1, 1.5, 2]))
    return new_point_cloud
    
def augment7(pcd:o3d.geometry.PointCloud):
    new_point_cloud = o3d.geometry.PointCloud()
    new_point_cloud.points = o3d.utility.Vector3dVector(
        pcd.points * np.array([2, 1.5, 2]))
    return new_point_cloud
    

def generate_augmentation(inRoot:str):
    """
    It takes the INROOT which is a folder path
    of your point cloud files. It will take every point cloud and
    apply the 7 augmentation step. 
    """
    
    # I do not have a chance to try on othe file formats.
    # but can be implement other file formats(e.g. .xyz) too. 
    removal_list= [".ply"]
    augment_order= [augment1, augment2,
                    augment3, augment4,
                    augment5, augment6,
                    augment7]


    for i in range(7):
        for word in removal_list:
            for pcdpath in glob.iglob(f'{inRoot}/*'):
                basename = os.path.basename(pcdpath)
                _basename = basename.replace(word, "")
                # now we have a filename without .ply
                # but also the complete name of the file

                # generate a name to save
                fn = str(_basename+f'__{i+1}.ply')

                # get the point cloud
                pcd = o3d.io.read_point_cloud(pcdpath)
                
                # augmentation part
                new_pcd = augment_order[i](pcd=pcd)

                # saving part
                # we will save it in same folder as inRoot
                saveAsPly(root=inRoot, fn=fn,
                          pcd=new_pcd)

inRoot = os.path.join(
    "/home/user/Desktop/datasets/plyTree"
)


generate_augmentation(inRoot=inRoot)