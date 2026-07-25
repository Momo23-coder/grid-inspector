# grid-inspector

Reference implementation of a real-time defect detection system for UK transmission networks, running on Jetson-class edge AI hardware.

## Overview

The system detects and classifies defects on overhead transmission and distribution infrastructure: insulators, conductors, and hardware fittings, from imagery captured by drones, helicopters, and vehicle-mounted cameras. Existing inspection workflows in the UK generate large volumes of imagery that is reviewed largely by hand or by proprietary vendor tooling, with no open, reproducible reference for how the machine-learning stage should be built. This project fills that gap: an end-to-end pipeline from dataset preparation through model training to real-time inference on Jetson edge hardware, calibrated to UK asset types and network operating conditions. It is intended as a reference for engineers, drone operators, DNOs, and TNOs building or specifying inspection systems.

**Status:** Early-phase development. Repository skeleton and documentation in place; dataset preparation and baseline model training are the current focus. See the [roadmap](#roadmap) below for phase status.

## Hardware target

The reference deployment platform for this project is the Sintrones iBox-600, a fanless in-vehicle rugged computer built around the NVIDIA Jetson Orin NX module. The system is designed to be portable to other Jetson-family carriers with equivalent I/O.

| Component        | Specification                                     |
| ---------------- | ------------------------------------------------- |
| Carrier          | Sintrones iBox-600                                |
| Compute module   | NVIDIA Jetson Orin NX 16GB                        |
| AI performance   | Up to 100 TOPS (INT8, sparse)                     |
| GPU              | 1024-core NVIDIA Ampere, 32 Tensor Cores          |
| CPU              | 8-core Arm Cortex-A78AE                           |
| Memory           | 16 GB LPDDR5                                      |
| Power envelope   | 10–25 W configurable                              |
| Operating system | NVIDIA JetPack 6.x (Ubuntu 22.04)                 |
| Runtime stack    | TensorRT, DeepStream SDK, GStreamer               |