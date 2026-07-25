# grid-inspector

Reference implementation of a real-time defect detection system for UK transmission networks, running on Jetson-class edge AI hardware.

## Overview

The system detects and classifies defects on overhead transmission and distribution infrastructure: insulators, conductors, and hardware fittings, from imagery captured by drones, helicopters, and vehicle-mounted cameras. Existing inspection workflows in the UK generate large volumes of imagery that is reviewed largely by hand or by proprietary vendor tooling, with no open, reproducible reference for how the machine-learning stage should be built. This project fills that gap: an end-to-end pipeline from dataset preparation through model training to real-time inference on Jetson edge hardware, calibrated to UK asset types and network operating conditions. It is intended as a reference for engineers, drone operators, DNOs, and TNOs building or specifying inspection systems.