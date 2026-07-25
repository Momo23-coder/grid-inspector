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

## Repository structure

```
grid-inspector/
├── docs/                    Problem statement, dataset strategy, results, and engineering logbook
├── datasets/                Scripts that download and prepare public datasets into a unified schema
│   └── uk_eval_set/         Hand-labelled UK evaluation frames used to measure real-world performance
├── training/                Model training code and configurations; runs on cloud GPU
│   └── configs/             Training hyperparameters, dataset splits, augmentation settings
├── conversion/              PyTorch to ONNX to TensorRT engine export scripts
│   └── calibration/         INT8 calibration data used during TensorRT engine build
├── deepstream/              Runtime inference pipeline on the Jetson Orin NX
│   └── custom_bbox_parser/  Custom bounding box parser plugin for the trained model
├── integration/             Downstream messaging, protocols, and dashboard
│   └── dashboard/           Web dashboard for reviewing detections and system health
└── benchmarks/              Reproducible latency, throughput, and power measurements
    └── results/             Committed benchmark output: CSVs, plots, and analysis notes
```

## Roadmap

The project is being built in phased blocks. Each phase produces a committed, reproducible artefact before the next phase begins.

- **Phase 0 — Repository skeleton and scoping.** `[Complete]` Repository structure, problem framing, hardware target, and engineering logbook in place.
- **Phase 1 — Dataset preparation.** `[In progress]` Unifying public transmission-inspection datasets into a common five-class schema covering intact insulators, missing insulator components, broken conductor strands, composite insulator surface degradation, and fittings and hardware defects.
- **Phase 2 — Baseline model training.** `[Planned]` Train a YOLO-family object detector on the unified dataset using a cloud GPU. Publish training configuration, checkpoints, and honest failure analysis.
- **Phase 3 — Edge conversion and deployment.** `[Planned]` Export the trained model to ONNX, build an INT8-calibrated TensorRT engine, and run inference on the Jetson Orin NX target. Publish latency, throughput, and power measurements.
- **Phase 4 — Integration.** `[Planned]` Wrap the detection pipeline behind an MQTT publisher and an OPC-UA server so results can be consumed by common industrial data platforms. Web dashboard for review.
- **Phase 5 — UK evaluation.** `[Planned]` Hand-label a small UK-specific evaluation set covering domestic asset types and conditions, and measure real-world performance against the baseline trained on international training data. Document the domain gap.

## Getting started

Installation, environment setup, and reproduction instructions will be added incrementally as each phase produces a runnable artefact. The intended structure:

- **Training environment.** A `training/environment.yml` (or `requirements.txt`) will define the Python dependencies for reproducing model training on a CUDA-capable GPU.
- **Conversion environment.** A `conversion/` script pipeline will document the ONNX export and TensorRT engine build steps for the Jetson Orin NX target.
- **Runtime environment.** A `deepstream/` configuration will document the runtime pipeline for real-time inference on the iBox-600.

At the current phase, the repository contains project scoping, hardware target documentation, and the folder structure for the phased build-out. See the [roadmap](#roadmap) for what lands when.