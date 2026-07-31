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


def main() -> None:
    """Entry point. Prints a startup line and exits."""
    print("prepare_cplid: starting")


if __name__ == "__main__":
    main()