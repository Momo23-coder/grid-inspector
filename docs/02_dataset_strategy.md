# Dataset strategy

## Overview

This document specifies the training data strategy for the defect detection model. It inventories the public datasets used, maps each source dataset's labels to the project's five-class schema (defined in [`01_problem_statement.md`](01_problem_statement.md)), and states the three-tier training approach that combines foreign public data with a UK-focused evaluation set.

The strategy is deliberately honest about coverage gaps. Public transmission-inspection data is dominated by non-UK networks and by a narrow subset of defect types. Where the project's schema is not well served by public data, this document names the gap rather than obscuring it, and defers the fix to a later phase.

## Available public datasets

The dataset inventory below covers the public releases used or evaluated for this project.

| Dataset | Source | Size | Coverage | Notes |
| ------- | ------ | ---- | -------- | ----- |
| InsPLAD | Silva et al., 2023 | 10,607 images, 28,933 instances | 17 component classes, 6 defect types (4 corrosion variants, 1 broken component, 1 bird's nest) | Primary backbone. Real-world Brazilian UAV imagery. Distinguishes InsPLAD-fault (defect detection) from InsPLAD-anomaly (anomaly detection). |
| STN PLAD | Vieira-e-Silva et al., 2021 | 2,409 annotated objects | 5 asset classes: transmission tower, insulator, spacer, tower plate, Stockbridge damper | Complementary asset-detection source. High-resolution UAV. No defect annotations at the instance level. |
| CPLID | Tao et al., 2018 | 848 images (600 normal, 248 defective) | Ceramic cap-and-pin insulators only | Insulator-specific baseline. Defective examples are synthetic (data augmentation over real defect crops), which limits real-world generalisation. |
| TLDD | Zhang et al., 2024 | 1,830 images | 7 defect categories including insulator bunch-drop, insulator damage, grading ring damage, corrosion, hardware defects | Newer defect-focused dataset with useful hardware coverage. |

All four datasets originate from non-UK networks (Brazil for InsPLAD and STN PLAD, China for CPLID and TLDD). The domain gap between these networks and UK infrastructure is addressed in the three-tier approach below.

Licence terms vary and should be verified before redistributing any derived artefacts. This project does not redistribute source imagery; only preprocessing scripts, class mappings, and derived model checkpoints are committed.