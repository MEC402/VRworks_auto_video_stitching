# Automatic VRworks video stitching
[Testing](#Testing)

---

# Requeriments

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

* **insta360_calib_rig_specs.xml:** Camera rig extrinsic and intrinsic parameters.
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



## Calibration frames extraction
Before stitching the video, it is recommended to calibrate the camera sensors in
order to align the videos and reduce stitching errors (seams) in the final video.
This step, randomly extracts video frames and stores them as images in
a new directory (*path_to_video/calib_frames/*) next to the sensor's videos for.

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
The generated images have its own unique name that represents the frame number (first number in the filename) and the video that it was extracted from (origin_{id} in this case). At this moment, the frame extractor extracts 10 frames from each sensor video, therefore, there should be 10 different frame numbers per sensor (there are 6 sensors).



## Automatic stitching launch
Now that the input directory is set up (**video list**) it is possible to execute the automatic stitching. To do so, use the following command:

```
python video_stitching.py {path}/videos.xml {path_to_video_list_dir}
```

This command makes use of the extracted calibration frames and calibrates the sensors before stitching therefore, there is no need to execute another command for calibration.

## Output
Video stitching script generates an stitched video named *{video_name}.mp4* and it is stored in each video's directory where the original sensor videos are stored. After the stitching is done, the **video list** directory should look like this:

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


---

# Testing
