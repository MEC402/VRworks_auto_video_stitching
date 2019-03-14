import cv2
import os
import sys
from os.path import isfile, isdir, join

import xml.etree.ElementTree as ET
import random

""" EXAMPLE CALL: python frameExtractor.py /scratch/ilopez/vr_works_videos/videos.xml /scratch/ilopez/vr_works_videos/ """

n_frames = 10


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
	print(video_path)

	output_dir = "{}/calib_frames/".format(video_path)
	if isdir(output_dir):
		os.system("rm {}*".format(output_dir))
	else:
		os.system("mkdir {}".format(output_dir))

	# Enter the input directory.
	os.system("cd {}".format(video_path))

	# Read and generate the video capture objects based on rig cameras.
	tree = ET.parse("{}/../insta360_video_input.xml".format(video_path))
	cameras = [c.get('name') for c in tree.findall('./camera/input_media_feed/input_media_file')]
	caps = [(cv2.VideoCapture("{}/{}".format(video_path,cam)), cam) for cam in cameras]

	# Get random frame numbers.
	length = int(caps[0][0].get(cv2.CAP_PROP_FRAME_COUNT))
	r_frames = random.sample(list(range(0,length-70)), n_frames)
	r_frames.sort()

	# Extract random frames and store them as images.
	for rf in r_frames:
		for cap, camname in caps:
			cap.set(cv2.CAP_PROP_POS_FRAMES, rf)
			ret, frame = cap.read()
			if ret == True:
				camname = camname[:-4]
				cv2.imwrite("{}{}_{}.png".format(output_dir, rf, camname), frame)
			else:
				print("Something went wrong at reading frame {}!".format(rf))
	for cap, _ in caps:
		cap.release()
