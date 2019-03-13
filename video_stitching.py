import xml.etree.ElementTree as ET
import os
import sys


input_xml = sys.argv[1]
video_dir = sys.argv[2]

tree = ET.parse(input_xml)
root = tree.getroot()

"""
os.system("cp /home/ilopez/tests/VRWorksStitching/insta360_calib_rig_specs.xml {}".format(video_dir))
os.system("cp /home/ilopez/tests/VRWorksStitching/insta360_video_input.xml {}".format(video_dir))
os.system("cp /home/ilopez/tests/VRWorksStitching/insta360_stitcher_spec.xml {}".format(video_dir))
"""

for child in root:
	video_path = video_dir + child.text

	#%%---- GENERATE PRECALIBRATION FILE ----
	os.system("python generate_precalib.py {}insta360_calib_rig_specs.xml {} ".format(video_dir, video_path))
	print("Precalibration file finshed.")

	#%%---- GENERATE CALIBRATION FILE ----
	#os.system("/cm/shared/apps/vrworks360/1.5/samples/nvcalib_sample/nvcalib_sample --wd {} --in_xml precalibration_specs.xml --out_xml calibration_specs.xml".format(video_path))
	#print("Calibration finished.")

	#%%---- AUTOMATIC STITCHING ----
	os.system("nvstitch_sample --input_dir_base {} --calib --rig_spec precalibration_specs.xml --video_input ../insta360_video_input.xml --stitcher_spec ../insta360_stitcher_spec.xml".format(video_path))
	os.system("mv out_stitched.mp4 {}.mp4".format(child.text))
	os.system("mv {}.mp4 {}".format(child.text, video_path))

	print("Finished:	{}".format(child.text))
