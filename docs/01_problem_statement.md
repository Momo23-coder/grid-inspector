# Problem statement

## Overview

The UK electricity network depends on hundreds of thousands of kilometres of overhead transmission and distribution infrastructure, whose insulators, conductors, and hardware fittings degrade over decades of exposure to weather, mechanical loading, and electrical stress. When a defect goes undetected long enough to cause failure, the consequences range from localised supply interruption to network-wide fault events with regulatory and financial penalties for the operator. Inspection is therefore both a safety obligation and an operational priority, funded through the regulated revenue framework and executed at scale using aerial and ground-based imaging. The technical bottleneck is no longer image capture but image *interpretation*: turning millions of frames into structured, actionable defect records fast enough to matter. This project publishes a reproducible reference implementation for that interpretation stage, targeted at Jetson edge hardware and calibrated to UK asset conditions.

