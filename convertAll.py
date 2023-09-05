from glbToPly import convertAll
import os 
import glob


"""
saveAsPly(root=rootP2,
          fn="tree_20.ply",
          pcd=glbToPcd(root=rootP,
                       fn="tree_20.glb",
                       number_of_points=50000))
#*-----"""
"""inRoot = "/home/metin/Desktop/datasets"

removal_list = [".glb"]

for word in removal_list:
    for meshpath in glob.iglob(f'{inRoot}/*'):
            # Take mesh object file names
            if word in os.path.basename(meshpath):
                print(os.path.basename(meshpath).replace(word, ""))"""


INROOT = os.path.join(
    "/home/metin/Desktop/datasets/glbTree")

OUTROOT = os.path.join(
    "/home/metin/Desktop/datasets/plyTree")

convertAll(inRoot=INROOT,
           outRoot=OUTROOT)