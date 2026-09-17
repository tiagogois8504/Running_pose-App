# Running Gait Analysis

Python prototype developed during my Biomedical Engineering and Biophysics curricular internship at the High Performance Centre of Jamor (CAR Jamor / IPDJ).

## Overview

The project explores automatic video-based analysis of treadmill running using pose estimation.

The main objective was to track lower-limb anatomical landmarks and investigate the automatic detection of gait events such as initial contact and toe-off.

The prototype was developed as part of a broader project comparing video-based running analysis with measurements obtained using systems such as Kinovea and OptoJump.

## Features

* Video loading and playback
* Lower-limb pose estimation
* Tracking of hip, knee, ankle and foot landmarks
* Estimation of hip and knee joint angles
* Experimental detection of foot-ground contact events
* Basic graphical interface for video analysis

## How to Run

1. Install the required dependencies:

    pip install -r requirements.txt

2. Run the application:

    python main.py

## Context

This project was developed during a curricular internship focused on running biomechanics, spatiotemporal gait parameters and validation of measurement methods.

The work combined programming, computer vision, biomechanics and data analysis in an applied sports-performance environment.
