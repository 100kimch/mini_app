# Setting up a backend server

- Author: Kim Jihyeong(KJHRicky@gmail.com)
- Written in Nov 2, 2019

## Overview

This document describes how to set up a backend server to service web. This backend server will enable us to control the ros-based robots such as Turtlebot3 Burger and will be able to monitor every status value of it.

## Specification

- Backend Server

  - Model: NVIDIA Jetson Nano
  - CPU: Quadcore ARM Cortex-A56 MPCore Processor
  - GPU: NVIDIA Maxwell Architecture with 128 NVIDIA CUDA Core
  - OS: Ubuntu 18.04 with NVIDIA Developer Kit

- Router
  - NETGEAR R6700v3

## Configuration

Although I get used to code with javascript, I picked up Django as a framework of a backend server due to the connectivity to roscore; every ROS Packages I made are python-based. After setting up the turtlebot, a ROS-based robot, what I have to do is make a web service which controls and monitors the turtlebot. I chose frameworks below:

- Front-end framework
  - Vue.js
- Back-end frameworks
  - NGINX
  - Django
  - roscore

### Setting up the router

There are some steps to access the backend server anywhere:

1. Static IP Address

The server's IP Address is set as static because there are four routers in a room and needed to keep it in the same address.

1. Port Forwarding

SSH ports should be opened for developing and HTTP ports should be opened for providing web services.

### Docker Installation

> See: [Official Document: Quickstart: Compose and Django](https://docs.docker.com/compose/django/)
> See: [docker로 django 개발하고 배포하기(+ nginx, gunicorn)](<https://teamlab.github.io/jekyllDecent/blog/tutorials/docker%EB%A1%9C-django-%EA%B0%9C%EB%B0%9C%ED%95%98%EA%B3%A0-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0(+-nginx,-gunicorn)>)

- After following the official document, type:

```bash
sudo docker-compose up
```

### Django Installation

> See: [Official Document: Quickstart: Compose and Django](https://docs.docker.com/compose/django/)

- change codes in `settings.py`:

```python
ALLOWED_HOSTS = ['*']
```

### PostgreSQL Installation

> See: [우분투 PostgreSQL 설치](https://zetawiki.com/wiki/%EC%9A%B0%EB%B6%84%ED%88%AC_PostgreSQL_%EC%84%A4%EC%B9%98)

### Create a docker image for a jetson device

> See: [How to create / update a docker image for a jetson device](https://opendatacam.github.io/opendatacam/documentation/jetson/CREATE_DOCKER_IMAGE.html)

#### Install OpenCV 3.4.3 with Gstreamer

```bash
# Remove all old opencv stuffs installed by JetPack
sudo apt-get purge libopencv*

# Download .deb files

# For Jetson Nano:
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-nano-3.4.3/OpenCV-3.4.3-aarch64-libs.deb
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-nano-3.4.3/OpenCV-3.4.3-aarch64-dev.deb
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-nano-3.4.3/OpenCV-3.4.3-aarch64-python.deb

# For Jetson TX2
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-tx2-3.4.3/OpenCV-3.4.3-aarch64-libs.deb
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-tx2-3.4.3/OpenCV-3.4.3-aarch64-dev.deb
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-tx2-3.4.3/OpenCV-3.4.3-aarch64-python.deb

# Install .deb files
sudo dpkg -i OpenCV-3.4.3-aarch64-libs.deb
sudo apt-get install -f
sudo dpkg -i OpenCV-3.4.3-aarch64-dev.deb
sudo dpkg -i OpenCV-3.4.3-aarch64-python.deb

# Verify opencv version
pkg-config --modversion opencv

pip
```

##### Install Darknet (Neural network framework running YOLO)

- Get the source files

```bash
#NB: the only change from https://github.com/alexeyab/darknet is : https://github.com/opendatacam/darknet/pull/1/files

git clone --depth 1 -b opendatacam https://github.com/opendatacam/darknet
```

- Modify the Makefile before compiling

```bash
# Set these variable to 1:
GPU=1
CUDNN=1
OPENCV=1

# Uncomment the following line
# For Jetson TX1, Tegra X1, DRIVE CX, DRIVE PX - uncomment:
ARCH= -gencode arch=compute_53,code=[sm_53,compute_53]
```

- For Generic Ubuntu machine with CUDA GPU
- Make sure you have CUDA installed:

```bash
# Type this command
nvcc --version

# If it returns Command 'nvcc' not found , you need to install cuda properly: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#package-manager-installation and also add cuda to your PATH with the post install instructions: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#post-installation-actions
```

- Make change to Makefile:

```bash
# Set these variable to 1:
GPU=1
OPENCV=1
```

##### Compile Darknet

```bash
# Go to darknet folder
cd darknet
# Optional: put jetson in performance mode to speed up things
sudo nvpmodel -m 0
sudo jetson_clocks
# Compile
make
```

- If you have an error “nvcc not found” on Jetson update path to NVCC in Makefile

```bash
NVCC=/usr/local/cuda/bin/nvcc
```

##### Download weight file

- The .weights files that need to be in the root of the `/darknet` folder

```bash
cd darknet #if you are not already in the darknet folder

# YOLOv2-VOC
wget https://pjreddie.com/media/files/yolo-voc.weights --no-check-certificate
# YOLOv3-tiny
wget https://pjreddie.com/media/files/yolov3-tiny.weights --no-check-certificate
# YOLOv3
wget https://pjreddie.com/media/files/yolov3.weights --no-check-certificate
```

##### (Optional) Test darknet

```bash
# Go to darknet folder
cd darknet
# Run darknet (yolo) on webcam
./darknet detector demo cfg/voc.data cfg/yolo-voc.cfg yolo-voc.weights "v4l2src ! video/x-raw, framerate=30/1, width=640, height=360 ! videoconvert ! appsink" -ext_output -dont_show

# Run darknet on file
./darknet detector demo cfg/voc.data cfg/yolo-voc.cfg yolo-voc.weights opendatacam_videos/demo.mp4 -ext_output -dont_show
```

#### Create the docker image

```bash
# Create a docker folder to gather all dependencies
mkdir docker
cd docker

# Copy previously compiled darknet in docker folder
cp -R <pathtodarknet> .

# Download opencv-3.4.3.tar.gz
# This is the pre-installed version of opencv to include in the docker container
# If you compiled Opencv yourself, you'll find how to create the tar file in the section explaning how to compile opencv

# For Jetson Nano:
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-nano-3.4.3/opencv-3.4.3.tar.gz

# For Jetson TX2:
wget https://github.com/opendatacam/opencv-builds/raw/master/opencv-tx2-3.4.3/opencv-3.4.3.tar.gz

# Download the Dockerfile
wget https://raw.githubusercontent.com/opendatacam/opendatacam/master/docker/run-jetson/Dockerfile

# Download a script to include in the docker container
wget https://raw.githubusercontent.com/opendatacam/opendatacam/master/docker/run-jetson/docker-start-mongo-and-opendatacam.sh

# Build image
sudo docker build -t opendatacam .

# If you are building a second time, use this to pull the latest opendatacam code
# TODO change this by adding the tag of the version in the Dockerfile
# Technique to rebuild the docker file from here : https://stackoverflow.com/a/49831094/1228937
# Build using date > marker && docker build .
date > marker && sudo docker build -t opendatacam .
```
