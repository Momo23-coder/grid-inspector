"""
CPLID (Chinese Power Line Insulator Dataset) converter.

Reads CPLID's PASCAL VOC XML annotations and produces unified-schema
annotations in the project's COCO-style JSON format.

Class mapping (see docs/02_dataset_strategy.md):
    Normal_Insulators   → Class 1 (Intact insulator)
    Defective_Insulators defect boxes → Class 2 (Missing cap or shed)
    Defective_Insulators insulator boxes → discarded

Run:
    python datasets/prepare_cplid.py
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# All input and output locations for this converter, relative to the project
# root. Run the script from the project root so relative paths resolve.

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CPLID_ROOT = PROJECT_ROOT / "data" / "cplid"

# Source annotation folders in the CPLID release
NORMAL_LABELS_DIR = CPLID_ROOT / "Normal_Insulators" / "labels"
DEFECTIVE_DEFECT_LABELS_DIR = CPLID_ROOT / "Defective_Insulators" / "labels" / "defect"

# Source image folders (used later for verifying dimensions and filenames)
NORMAL_IMAGES_DIR = CPLID_ROOT / "Normal_Insulators" / "images"
DEFECTIVE_IMAGES_DIR = CPLID_ROOT / "Defective_Insulators" / "images"

# Output location — the unified schema JSON for this dataset
OUTPUT_DIR = PROJECT_ROOT / "datasets" / "unified"
OUTPUT_JSON = OUTPUT_DIR / "cplid.json"


def main() -> None:
    """Entry point. Prints resolved paths for verification."""
    print("prepare_cplid: starting")
    print(f"  PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"  CPLID_ROOT: {CPLID_ROOT}")
    print(f"  NORMAL_LABELS_DIR: {NORMAL_LABELS_DIR}")
    print(f"    exists: {NORMAL_LABELS_DIR.exists()}")
    print(f"  DEFECTIVE_DEFECT_LABELS_DIR: {DEFECTIVE_DEFECT_LABELS_DIR}")
    print(f"    exists: {DEFECTIVE_DEFECT_LABELS_DIR.exists()}")
    print(f"  OUTPUT_JSON: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()