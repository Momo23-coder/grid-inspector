# Problem statement

## Overview

The UK electricity network depends on hundreds of thousands of kilometres of overhead transmission and distribution infrastructure, whose insulators, conductors, and hardware fittings degrade over decades of exposure to weather, mechanical loading, and electrical stress. When a defect goes undetected long enough to cause failure, the consequences range from localised supply interruption to network-wide fault events with regulatory and financial penalties for the operator. Inspection is therefore both a safety obligation and an operational priority, funded through the regulated revenue framework and executed at scale using aerial and ground-based imaging. The technical bottleneck is no longer image capture but image *interpretation*: turning millions of frames into structured, actionable defect records fast enough to matter. This project publishes a reproducible reference implementation for that interpretation stage, targeted at Jetson edge hardware and calibrated to UK asset conditions.

## UK network context

The UK electricity network splits into two structural layers: a high-voltage *transmission* system that moves bulk power from generators to regional load centres, and a lower-voltage *distribution* network that delivers electricity from those centres to homes, businesses, and industrial sites.

### Transmission

Three companies own the transmission network across Great Britain:

- **National Grid Electricity Transmission (NGET)** covers England and Wales, operating at 400 kV and 275 kV.
- **SP Transmission (SPT)**, part of SP Energy Networks, covers southern Scotland.
- **SSEN Transmission**, part of SSE, covers northern Scotland. In Scotland, 132 kV is also classed as transmission.

Since 2024, real-time system operation across Great Britain is the responsibility of the **National Energy System Operator (NESO)**, a publicly owned body separate from the three transmission owners. NESO does not own physical infrastructure; it directs the flow of electricity across the network the three owners maintain.

### Distribution

Distribution in Great Britain is delivered by six operator groups across 14 licence areas:

- **UK Power Networks** covers London, the South East, and the East of England.
- **National Grid Electricity Distribution (NGED)**, previously Western Power Distribution, covers the Midlands, the South West, and South Wales.
- **Electricity North West** covers Cumbria and the North West of England.
- **Northern Powergrid** covers Yorkshire and the North East.
- **SP Energy Networks** covers central Scotland, Merseyside, Cheshire, and North Wales.
- **SSEN Distribution** covers northern Scotland and central southern England.

Distribution networks step voltage down through 132 kV, 33 kV, and 11 kV stages before delivering 230 V to end users. Northern Ireland is operated separately by NIE Networks under a different regulator, and falls outside the scope of this project.

### Why the distinction matters

Transmission and distribution networks differ in the assets they inspect, the imaging platforms used, and the operational tempo of inspection cycles. Transmission towers are large steel lattice structures inspected by helicopter and increasingly by drone under BVLOS contracts. Distribution networks include a mixture of wood pole lines, steel towers, and pole-mounted equipment inspected by ground crews and vehicle-mounted platforms. A reference implementation useful across both layers has to accommodate this diversity in asset appearance, imaging geometry, and defect taxonomy.

## Sector drivers

Inspection of overhead infrastructure is not discretionary work. It is shaped by a combination of statutory obligations, regulatory incentives, and industry standards that together define what network operators must do, what they are funded to do, and how the work is expected to be performed.

The core statutory obligation comes from the **Electricity Safety, Quality and Continuity Regulations 2002 (ESQCR)**, which places a duty on network operators to ensure their equipment is sufficient and maintained so as to prevent danger and interruption of supply. In practice, this obligation is discharged through structured inspection and maintenance programmes covering every asset class on the network.

The economic framework in which this obligation is met is the **RIIO price control**, run by Ofgem. RIIO sets each operator's allowed revenue over multi-year periods and links it to performance on reliability, safety, environmental, and customer service outputs, with separate cycles for transmission and for distribution. Under RIIO, operators are incentivised to invest in condition based asset management rather than time based replacement, which increases demand for high-quality asset condition data.

Asset management practice itself is shaped by the **ISO 55000** family of standards, which formalise how organisations should plan, deliver, and continually improve the management of physical assets over their lifecycle. UK network operators align their asset management systems to ISO 55001, which requires evidence-based decisions on inspection frequency, defect classification, and intervention priority.

Finally, the technical detail of what inspection looks like on the ground is codified in the **Energy Networks Association (ENA) Engineering Recommendations**, a suite of industry-agreed standards covering overhead line design, condition assessment, and safety. The ENA specs are what a field crew or a contracted drone operator actually works to.

Taken together, these four pillars; statutory duty, regulated revenue, asset-management standard, and industry-agreed technical practice  create sustained, funded demand for better inspection data. The gap this project addresses sits inside that demand.

## State of practice and the gap

Inspection of overhead assets is today carried out through a mix of helicopter patrols, ground-based crews with cameras and binoculars, and increasingly Beyond Visual Line of Sight (BVLOS) drone contracts. All three approaches produce large volumes of imagery, which is then reviewed to identify defects and generate structured work orders for maintenance crews.

The dominant bottleneck is no longer image capture. Drone and helicopter platforms can now generate more imagery in a single inspection campaign than a team of engineers can review manually within reasonable timescales. Vendor-supplied machine-learning tooling exists to accelerate this review, but it is fragmented across proprietary platforms, closed to independent evaluation, and often trained on datasets whose geographic and asset-type coverage is not disclosed.

Three specific gaps result from this. First, there is no open, reproducible reference showing how a modern defect-detection pipeline should be constructed on edge AI hardware suitable for in-vehicle or on-drone deployment. Second, the public academic datasets that do exist are drawn largely from non-UK networks, with asset types, hardware fittings, and weathering patterns that differ from UK conditions in ways that are known to degrade model performance. Third, the industry lacks a common defect taxonomy and evaluation protocol against which vendor claims can be independently compared.

This project addresses the first gap directly, contributes toward closing the second through a UK focused evaluation set, and provides a starting point for the third through a documented five class defect schema.

## Defect taxonomy

The project trains and evaluates against a five class schema covering the most safety-relevant and inspection-actionable defect categories on overhead transmission and distribution assets.

| Class | Description | Inspection priority |
| ----- | ----------- | ------------------- |
| Intact insulator | Ceramic, glass, or composite insulator in serviceable condition. Baseline reference class. | Low (baseline) |
| Missing cap or shed | Physical loss of one or more sheds on a ceramic or glass cap-and-pin insulator string. Reduces electrical creepage distance and increases flashover risk. | High |
| Broken conductor strand | Mechanical damage to individual strands of the conductor wire, typically from arcing, corrosion, or clashing. Reduces mechanical strength and current-carrying capacity. | High |
| Composite insulator surface degradation | Tracking, erosion, or loss of hydrophobicity on silicone rubber composite insulators. Precursor to internal failure and flashover. | Medium to high |
| Fittings and hardware defects | Corroded, deformed, or missing hardware including clamps, spacers, vibration dampers, arcing horns, and suspension assemblies. Range of severities and consequences. | Variable |

Three deliberate scope choices are worth stating. The taxonomy focuses on visually inspectable defects; internal or thermal defects requiring infrared or ultrasonic sensing are out of scope. It applies to overhead assets only; underground cable defects are excluded. And the "Intact insulator" class exists to provide a proper negative reference for training and evaluation, not because intact assets need reporting.

## Scope and non-goals

This project is a reference implementation of the machine-learning stage of an inspection pipeline. It deliberately does not attempt to be a full inspection product. Specifically, out of scope:

- Data capture platforms, drones, or camera hardware
- Flight planning, BVLOS operations, or CAA regulatory compliance
- Asset registry integration or work order management
- Any claim of production-readiness or fitness for use on a live UK network

What is in scope: an end-to-end, reproducible, documented pipeline from public dataset ingestion through model training and edge deployment to real-time inference on Jetson hardware, evaluated against a UK focused test set.

## References

- Electricity Safety, Quality and Continuity Regulations 2002 (SI 2002/2665), UK Statutory Instrument.
- Ofgem, RIIO price control documents (transmission and distribution).
- ISO 55000:2014, *Asset management — Overview, principles and terminology*, and ISO 55001:2014, *Asset management — Management systems — Requirements*.
- Energy Networks Association, *Engineering Recommendations* (various), published by ENA.
- Vieira-e-Silva, A. L. B. et al., *STN PLAD: A Dataset for Multi-Size Power Line Assets Detection in High-Resolution UAV Images*, 2021 (source for baseline public dataset).