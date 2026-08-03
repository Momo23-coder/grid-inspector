# Engineering Logbook

## 2026-07-24 — Session 1: Environment and repo setup

- Migrated development environment from Windows PowerShell to WSL2 Ubuntu.
- Confirmed WSL/VS Code integration; project relocated from `/mnt/c/...` to `/home/mj/projects/grid-inspector` to avoid filesystem interop issues.
- Created repository skeleton: 7 top-level folders (docs, datasets, training, conversion, deepstream, integration, benchmarks) with placeholder `.gitkeep` files.
- Configured global Git identity and pushed first structural commit.
- Next session: rewrite README to reflect project scope and hardware target.

## 2026-07-25 — Session 2: README written end to end

- Wrote the full README as a Tier 3 reference-implementation document: title and tagline, Overview, Status, Hardware Target, Repository Structure, Roadmap, Getting Started, Documentation index, License, Disclaimer.
- Established the sector-facing voice: DNO/TNO vocabulary, honest in-progress framing, phase-status markers.
- Decided to keep the repository public throughout the build to preserve dated commit history as visa and recruiter evidence.
- Confirmed disclaimer language separating personal-project work from employer affiliation.
- Committed each section as an atomic commit with a purposeful message.
- Next session: begin Phase 1 — problem statement document in docs/, then dataset preparation.

## 2026-07-26 — Session 3: Problem statement drafted end to end

- Wrote docs/01_problem_statement.md covering Overview, UK network context (transmission and distribution structure including the post-2024 NESO split), Sector drivers (ESQCR, RIIO, ISO 55000, ENA specs at light citation depth), State of practice and the gap, Defect taxonomy (five class schema with inspection priority), Scope and non goals, References.
- Consolidated the original eight section plan into five sections to keep the document proportionate to the project stage without losing the load bearing content.
- Removed specific RIIO cycle names and publication dates to avoid unverifiable claims; kept the framework level explanation intact.
- Updated the README documentation index to link the finished problem statement.
- Next session: begin dataset preparation. Read the STN PLAD paper properly, inventory available public datasets, and draft docs/02_dataset_strategy.md before writing any code.

## 2026-07-26 — Session 4: Dataset strategy drafted end to end

- Wrote docs/02_dataset_strategy.md covering Overview, Public dataset inventory (InsPLAD, STN PLAD, CPLID, TLDD), per-dataset class mapping to the five-class schema, coverage summary, three-tier training approach, unified output format specification, and data quality practices.
- Updated the primary backbone from STN PLAD to InsPLAD after verifying the current public dataset landscape; InsPLAD is now the strongest defect-labelled public source.
- Named the honest coverage gap: Classes 3 (broken conductor strand) and 4 (composite insulator surface degradation) are not covered by any public dataset. Deferred to a later phase with a stated collection plan rather than dropped from the schema.
- Specified the unified output format (COCO-style JSON with source_dataset and mapping_confidence fields) so the next scripts have clear conventions to build against.
- Chose the multi-file converter pattern: one prepare_*.py per source dataset plus one unify_datasets.py.
- Updated the README documentation index to link the finished dataset strategy.
- Next session: begin writing datasets/prepare_cplid.py as the first converter. This introduces Python virtual environments and the first real code commits.

## 2026-07-31 — Session 5: Python environment set up, first converter scaffolded

- Installed WSL Python venv package (python3.14-venv), created project virtual environment at .venv/, added it to .gitignore.
- Installed initial dependencies (Pillow, lxml), captured them in requirements.txt.
- Downloaded CPLID dataset into data/ (excluded from Git), inspected on-disk structure end to end: two top-level folders, images/labels split, defective/labels/ further split into defect/ and insulator/ subfolders with matching filenames across both.
- Confirmed VOC XML schema for both normal and defective annotations; recorded class strings ("insulator", "defect") and coordinate format for the converter design.
- Created datasets/prepare_cplid.py scaffold with module docstring, main function, and entry-point guard. Ran clean.
- Added path configuration constants at the top of the script, using Path(__file__).resolve().parent.parent to resolve project root regardless of run location.
- Verified all input paths exist on disk before writing any parsing code.
- Inspected sample images from both Normal_Insulators and Defective_Insulators folders before writing the converter. Confirmed visually that CPLID defective images are digital composites (real insulator crops pasted onto real backgrounds via U-Net segmentation, per the paper's methodology).
- Made an informed schema decision as a result: added a `synthetic: true` boolean flag to the unified output format spec, applied to CPLID defect annotations. Updated docs/02_dataset_strategy.md to document the new field.
- Next session: write the XML parsing function in prepare_cplid.py. Test against 0049.xml (normal) and 000.xml (defective defect). Then file walking, class mapping, and JSON output.

## 2026-08-03 — Session 6: First real Python function — parse_voc_xml

- Added VocObject and VocAnnotation dataclasses to model parsed VOC XML content. Verified via interactive shell that instances construct and print cleanly.
- Wrote parse_voc_xml function using lxml. Function reads one XML file and returns a VocAnnotation containing filename, dimensions, and a list of VocObject bounding boxes.
- Tested the parser against real sample files (data/cplid/Normal_Insulators/labels/0049.xml and data/cplid/Defective_Insulators/labels/defect/000.xml). Both parses produced output matching the source XML exactly.
- Reordered module sections to follow the constants → data → functions convention. Fixed PEP 8 blank-line spacing between top-level blocks.
- Next session: write the class mapping logic — the function that takes a parsed VocAnnotation and produces annotations in the five-class unified schema, including the synthetic flag for CPLID defect samples.