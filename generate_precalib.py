import os
import sys
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET

output_filename = 'precalibration_specs.xml'

input_rig_specs_xml = sys.argv[1]
input_video_path = sys.argv[2]
input_calib_frames_dir = "{}/calib_frames/".format(input_video_path)

output_filename = "{}/{}".format(input_video_path, output_filename)
print(output_filename)

tree = ET.parse(input_rig_specs_xml)

# Read all filenames in calib frames folder.
calib_frames = ["calib_frames/{}".format(f) for f in listdir(input_calib_frames_dir) if isfile(join(input_calib_frames_dir, f))]

# Find cameras in the rig spec xml file.
cameras = tree.findall('./camera')

# Add calibration frame paths to the xml tree.
cam = 0
for f in range(0,len(calib_frames)):
    if cam >= len(cameras):
        cam = 0
    new_calib_img = ET.Element('input_calib_file')
    new_calib_img.set('name', calib_frames[f])
    cameras[cam].insert(0, new_calib_img)
    cam = cam + 1

# Write tree as xml file.
tree.write(output_filename)
