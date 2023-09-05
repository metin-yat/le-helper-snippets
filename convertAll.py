from glbToPly import convertAll
import os 
import glob

INROOT = os.path.join(
    "/home/metin/Desktop/datasets/glbTree")

OUTROOT = os.path.join(
    "/home/metin/Desktop/datasets/plyTree")

convertAll(inRoot=INROOT,
           outRoot=OUTROOT)
