# Setting up backend server

- Author: Kim Jihyeong(KJHRicky@gmail.com)
- Written in Nov 2, 2019

## Overview

This document describes how to set up the backend server to service web. This backend server will enable us to control the ros-based robots such as Turtlebot3 Burger and will be able to monitor every status value of it.

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
