import os

import open3d as o3d
import numpy as np


# Func List 
# glbToPcd: basically helps you to convert glb to
#               point cloud and returns o3d.geometry.PointCloud

# saveAsPly: takes your point cloud and save it as FILENAME.ply
                # it will work nested-like with glbToPcd

# visualize_mesh: names say it all. But takes pointclouds too.


def glbToPcd(root:str, fn:str,
              sampling_mode:str="u",
              number_of_points:int=50000,
              init_factor:int = 1) -> o3d.geometry.PointCloud:
    """
        takes:
        root:       Folder path of your workshop/dataset
        
        fn:       Filename of the .glb file
                       that you want to convert.
        
        sampling_mode:   u means uniformly 
                        p means poisson
                You can basically go to the link to see the modes from there.
                http://www.open3d.org/docs/release/tutorial/geometry/mesh.html#Sampling
        
        number_of_points: How many points you want to extract 
                            from your mesh object? default is 50.000

        init_factor: This is for poisson method. init_factor * number_of_points
                           default is 1

        returns:
        xyz: your glb file but point cloud version of it.
                as-> > > o3d.geometry.PointCloud

    """

    glb_path =  os.path.join(root, fn)

    mesh = o3d.io.read_triangle_mesh(glb_path)

    if sampling_mode=="u" or sampling_mode=="U":
        pcd = mesh.sample_points_uniformly(
            number_of_points=number_of_points)
    
    else:
        # it is poisson
        pcd = mesh.sample_points_poisson_disk(
            number_of_points=number_of_points,
            init_factor=init_factor)
        
    return pcd

def saveAsPly(root:str, fn:str,
              pcd:o3d.geometry.PointCloud):
    """
        takes:
            root: Output of this function which it will
                save the .ply file to that root path
            fn: file name that you want to save as

            pcd: you can basically write the function above 
                for this parameter ---
                e.g. saveAsPly(... pcd=glbToPcd(...))
    """

    ply_path = os.path.join(root, fn)
    o3d.io.write_point_cloud(ply_path, pcd)


def convertAll(inRoot:str,
                     outRoot:str=""):
    """
    takes:
        inRoot: Folder path that contains input files that 
        you want to convert to point cloud and save as .ply

        outRoot: Output path that you want to save the 
        .ply files
    returns:
        --
    """

    import glob

    removal_list = [".glb"]

    for word in removal_list:
        for meshpath in glob.iglob(f'{inRoot}/*'):
            # Take mesh object file names
            basename= os.path.basename(meshpath)
            _basename= basename.replace(word, "")

            # Getting the mesh file 
            mesh = o3d.io.read_triangle_mesh(meshpath)
            # Generating name for point cloud file
            fn = str(_basename+".ply")

            saveAsPly(
                root=outRoot, fn= fn,
                pcd=glbToPcd(
                    root=inRoot, fn=basename,
                    number_of_points=100000
                )
            )



def visualize_mesh(mesh):
    # visualize_mesh: names say it all. But takes pointclouds too.
    vis  = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    vis.run()
    vis.destroy_window()



def get_quartiles(root:str) -> list:
    import glob

    """
    It takes all of your glb file which is in 'root' path.
    Then gets all of the mesh's surface area and list 'em
    After listing, it calculates 3th() quartile of the list.

    Idea behind of this function is, optimizing number_of_points.
    You can basically say when its greater than 3th quartile do this 
    else not and so on so forth.

    takes:
        root: folder that contains all the mesh file

    returns:
        quartiles: (Q1, Q2, Q3) -> Q2 means median 
    """

    # empty list for listing all the surface 
    # areas of the mesh objects.
    surface_areas = []

    for meshname in glob.iglob(f'{root}/*'):
        # print(os.path.basename(mesh))
        mesh = o3d.io.read_triangle_mesh(meshname)
        # gets surface area
        surface_area = int(mesh.get_surface_area())
        # adding to our list 
        surface_areas.append(surface_area)

    # calculates the quartiles as integer
    q1 = int(np.percentile(
        surface_areas,25))

    q2 = int(np.percentile(
        surface_areas,50))
    
    q3 = int(np.percentile(
        surface_areas,75))
    

    quartiles = [q1, q2, q3]

    return quartiles




