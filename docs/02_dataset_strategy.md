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

## Class mapping

Each source dataset uses its own label vocabulary. This section documents the mapping from source labels to the project's five-class schema. Mappings are marked as *clean* (direct semantic match), *with caveats* (usable but with a stated limitation), or *discarded* (out of scope for this project).

### CPLID

| Source label | Target class | Confidence | Note |
| ------------ | ------------ | ---------- | ---- |
| Normal insulator | Class 1 — Intact insulator | Clean | Direct match |
| Defective insulator | Class 2 — Missing cap or shed | With caveats | Defects are synthetic, cropped and pasted; limits real-world generalisation |

### STN PLAD

| Source label | Target class | Confidence | Note |
| ------------ | ------------ | ---------- | ---- |
| Insulator | Class 1 — Intact insulator | Clean | Real-world intact insulator examples |
| Spacer | Class 5 — Fittings and hardware (intact reference) | With caveats | Intact-only; used to teach the model what serviceable hardware looks like |
| Stockbridge damper | Class 5 — Fittings and hardware (intact reference) | With caveats | Same reasoning as spacer |
| Transmission tower | Discarded | — | Tower detection is a separate task |
| Tower plate | Discarded | — | Not defect-relevant in this schema |

### InsPLAD

The InsPLAD-fault variant (object detection with explicit class labels) is used, not InsPLAD-anomaly (unlabelled anomaly detection). InsPLAD's 17 component classes provide intact-reference material for Class 1 (insulator components) and Class 5 (hardware components). The six defect types map as follows.

| Source label | Target class | Confidence | Note |
| ------------ | ------------ | ---------- | ---- |
| Corrosion — Yoke suspension | Class 5 — Fittings and hardware defects | Clean | Hardware corrosion |
| Corrosion — Vari-grip | Class 5 — Fittings and hardware defects | Clean | Conductor termination fitting corrosion |
| Corrosion — Damper Stockbridge | Class 5 — Fittings and hardware defects | Clean | Damper corrosion |
| Corrosion — Lightning rod suspension | Class 5 — Fittings and hardware defects | Clean | Hardware corrosion |
| Broken component — Polymer insulator lower shackle | Class 5 — Fittings and hardware defects | With caveats | Fractured hardware component; treated as a hardware defect rather than insulator defect |
| Bird's nest | Discarded | — | Foreign object; separate task class |

### TLDD

| Source label | Target class | Confidence | Note |
| ------------ | ------------ | ---------- | ---- |
| Insulator bunch-drop | Class 2 — Missing cap or shed | Clean | Physical drop of insulator components |
| Insulator damage | Class 2 — Missing cap or shed | With caveats | Label is ambiguous; requires visual inspection of samples to confirm mapping before use in training |
| Grading ring damage | Class 5 — Fittings and hardware defects | Clean | Grading ring hardware |
| Shielded ring corrosion | Class 5 — Fittings and hardware defects | Clean | Shielded ring hardware |
| Shockproof hammer intersection | Class 5 — Fittings and hardware defects | Clean | Damper hardware |
| Bird nest | Discarded | — | Foreign object |
| Foreign body | Discarded | — | Not an asset defect |

### Coverage summary and the honest gap

Aggregating the mappings above against the five-class schema:

| Class | Public data coverage | Sources |
| ----- | -------------------- | ------- |
| Class 1 — Intact insulator | Well covered | CPLID, STN PLAD, InsPLAD components |
| Class 2 — Missing cap or shed | Moderately covered | CPLID (synthetic), TLDD (real, some ambiguity) |
| Class 3 — Broken conductor strand | Not covered by any public dataset | None |
| Class 4 — Composite insulator surface degradation | Not covered by any public dataset | None |
| Class 5 — Fittings and hardware defects | Heavily covered | InsPLAD, TLDD |

Classes 3 and 4 are the coverage gap. Conductor-strand damage requires close-range imagery of the conductor wire itself, which the public UAV datasets do not provide at meaningful volume. Composite insulator surface degradation requires specific ceramic-versus-composite disambiguation and high-resolution capture of surface texture, which no public dataset labels systematically.

This project trains and evaluates Classes 1, 2, and 5 in Phase 2. Classes 3 and 4 are deferred to a later phase, contingent on targeted data collection either from UK inspection contract imagery under appropriate agreements, or from purpose-collected close-range captures. The five-class schema is retained in the pipeline so that the deferred classes can be added without schema changes.