# Automatic VRworks video stitching


---

# Requeriments

## Insta360 camera footage
Login into *R2* and copy the content of the **instructions footage** (*/scratch/ilopez/vr_works_instructions_footage/*) directory into your preferred location in the cluster by using the following command:

```
cp /scratch/ilopez/vr_works_instructions_footage/ {preferred_directory_path}
```

## R2 modules
There are some required modules that are already installed in *R2*:
* GCC 7.2
* CUDA 9.1
* VRworks 1.5

To load the modules to the user's current environment use the following command:

```
module load gcc/7.2.0 cuda91/toolkit/9.1.85 vrworks360/1.5
```

To load the modules to the shell init file use the following command:

```
module initadd gcc/7.2.0 cuda91/toolkit/9.1.85 vrworks360/1.5
```

## Directory structure

At this moment the automatic stitching only supports videos recorded with the
Insta360 Pro camera.
This camera generates 6 videos, one for each sensor.

Create a root directory for the **video list** and then a folder for each capture and store the generated 6 videos in it.
After finishing with all the captures, the directory structure should be like the following one:

```
./
+-- video0/
    |   +-- origin0.mp4
    |   +-- origin1.mp4
    |   +-- origin2.mp4
    |   +-- origin3.mp4
    |   +-- origin4.mp4
    |   +-- origin5.mp4
+-- video1/
    |   +-- origin0.mp4
    |   +-- origin1.mp4
    |   +-- origin2.mp4
    |   +-- origin3.mp4
    |   +-- origin4.mp4
    |   +-- origin5.mp4
+-- ...
```

In the same root directory, I will recommend to create an **xml** file in which
the video directories are listed (directory path) using the following format:

```xml
<?xml version="1.0"?>
<data>
    	<video>video0</video>
        <video>video1</video>
        <video>video2</video>
        ...
</data>
```
***Tip:*** I use to create the video directory into the *R2* **scratch** because there is
plenty of disk space to store them.


---

# Running




## Input

Before running the automatic stitching, check that you have the following files
located and copy them into the **video list** directory:

* **insta360_rig_specs.xml:** Camera rig extrinsic and intrinsic parameter estimation.
* **insta360_video_input.xml:**     List of path to videos to process.
* **insta360_stitcher_spec.xml:**   Stitcher parameters for VRworks.

After copying, the video list directory should look like this:
```
videos/
+-- video0/
    |   +-- origin0.mp4
    |    ...
+-- video1/
    |   +-- origin0.mp4
    |    ...
+-- ...
+-- insta360_calib_rig_specs.xml
+-- insta360_video_input.xml
+-- insta360_stitcher_spec.xml
```

## Camera rig modification
(*Skip this section if the Insta360 camera footage is used.*)

Camera rig specifications determines how the camera sensors are arranged in the capturing device.
*Size*, *orientation*, *location*, and intrinsic parameters are stored in the *insta360_rig_specs.xml* file.
This file is an estimation of how the camera is arranged, it is required for the calibration step where *VRworks* will create a new file, named *precalibration_specs.xml" in order to optimize the stitching.

Each sensor has the following structure for storing the parameters in the *insta360_rig_specs.xml*:
```xml
<camera height="1440" layout="equatorial" width="2560">
		<pose>
			<rotation m0="-0.01306413" m1="0.9998991" m2="-0.005569809" m3="-0.9999146" m4="-0.01306413" m5="3.638432e-05" m6="-3.638407e-05" m7="0.005569809" m8="0.9999845" pitch_deg="-0.3191282" roll_deg="-90.74855" yaw_deg="0.002084686" />
			<translation x_cm="-0" y_cm="-0" z_cm="-1" />
		</pose>
		<optics>
			<focal_length focal_pixels="813.0974" />
			<principal_point center_offset_x="2.791626" center_offset_y="18.03162" />
			<lens k1="-0.01674893" k2="-0.003644353" k3="0" k4="0" type="fisheye" />
			<fisheye_radius radius_pixels="1780" />
		</optics>
</camera>
```
**Pose** determines the extrinsic parameters and the **Optics** determines the intrinsic parameters of the sensor.
This example is for the Insta360 camera but if another device is used, the correct parameters should be modified in order to match the new camera rig configuration.

## Video input modification
(*Skip this section if the Insta360 camera footage is used.*)

It is necessary to modify the *insta360_video_input.xml* file to match the correct size, frame-rate and video name of the sensor to the camera rig specifications.
To do so, as shown in the following example, open the *insta360_video_input.xml* file and modify each **camera** element's attributes to match the camera's sensor resolution (*width* and *height*).
After that set those element's **input_media_file** children's attributes (*name*, *fps_num*, *width* and *height*) to match the sensors' specs.
There is no need to modify anything if the footage is from the Insta360 camera.

```xml
<camera width="{target_width}" height="{target_height}">
		<input_media_feed>
			<input_media_form form="file"/>
			<input_media_file name="{video_name}" fps_num="{video_fps}" fps_den="3" width="{target_width}" height="{target_height}"/>
		</input_media_feed>
	</camera>
```

The example for the Insta360 camera:
```xml
<camera width="1440" height="2560">
		<input_media_feed>
			<input_media_form form="file"/>
			<input_media_file name="origin_0.mp4" fps_num="100" fps_den="3" width="1440" height="2560"/>
		</input_media_feed>
	</camera>
```


## Calibration frames extraction
Before stitching the video, it is recommended to calibrate the camera sensors in
order to align the videos and reduce stitching errors (seams) in the final video.
This step, randomly extracts video frames and stores them as images in
a new directory (*path_to_video/calib_frames/*) next to the sensors' videos.

To generate the calibration frames use the following command:

```
python frameExtractor.py {path}/videos.xml {path_to_video_list_dir}
```

This is an example:
```
python frameExtractor.py /scratch/ilopez/vr_works_videos/videos.xml /scratch/ilopez/vr_works_videos/
```

Once the frame extractor is launched, the video list directory should look like this:

```
videos/
+-- video0/
    |   +-- calib_frames/
                |   +-- 1157_origin_0.png
                |   +-- 1157_origin_1.png
                |   +-- 1157_origin_2.png
                |   +-- ...
    |   +-- origin0.mp4
    |    ...
+-- video1/
    |   +-- calib_frames/
                    |   +-- 307_origin_0.png
                    |   +-- 307_origin_1.png
                    |   +-- 307_origin_2.png
                    |   +-- ...
    |   +-- origin0.mp4
    |    ...
+-- ...
+-- insta360_calib_rig_specs.xml
+-- insta360_video_input.xml
+-- insta360_stitcher_spec.xml
```
The generated images have its own unique name that represents the frame number (first number in the filename) and the video that it was extracted from (origin_{id} in this case).
At this moment, the frame extractor extracts 10 frames from each sensor video, therefore, there should be 10 different frame numbers per sensor (there are 6 sensors).



## Automatic stitching launch
Now that the input directory is set up (**video list**) it is possible to execute the automatic stitching.
To do so, use the following command:

```
python video_stitching.py {path}/videos.xml {path_to_video_list_dir}
```

This command makes use of the extracted calibration frames and calibrates the sensors before stitching therefore, there is no need to execute another command for calibration.

## Output
Video stitching script generates an stitched video named *{video_name}.mp4* and it is stored in each video's directory where the original sensor videos are stored.
After the stitching is done, the **video list** directory should look like this:

```
videos/
+-- video0/
    |   +-- calib_frames/
                |   +-- 1157_origin_0.png
                |   +-- 1157_origin_1.png
                |   +-- 1157_origin_2.png
                |   +-- ...
    |   +-- origin0.mp4
    |    ...
    |   +-- video0.mp4
+-- video1/
    |   +-- calib_frames/
                    |   +-- 307_origin_0.png
                    |   +-- 307_origin_1.png
                    |   +-- 307_origin_2.png
                    |   +-- ...
    |   +-- origin0.mp4
    |    ...
    |   +-- video1.mp4
+-- ...
+-- insta360_calib_rig_specs.xml
+-- insta360_video_input.xml
+-- insta360_stitcher_spec.xml
```
