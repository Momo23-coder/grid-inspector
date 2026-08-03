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

from dataclasses import dataclass, field
from pathlib import Path

from lxml import etree


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


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
# Structured representations of a parsed VOC XML annotation. One VocObject
# per <object> block in the XML; one VocAnnotation per XML file.


@dataclass
class VocObject:
    """One <object> block from a VOC XML annotation."""

    name: str
    xmin: int
    ymin: int
    xmax: int
    ymax: int


@dataclass
class VocAnnotation:
    """One VOC XML annotation file, parsed into structured form."""

    filename: str
    width: int
    height: int
    objects: list[VocObject] = field(default_factory=list)


# ---------------------------------------------------------------------------
# XML parsing
# ---------------------------------------------------------------------------
# Reads a single PASCAL VOC XML annotation file and returns its structured
# contents. Handles both Normal_Insulators/labels/*.xml (which contain
# insulator objects) and Defective_Insulators/labels/{defect,insulator}/*.xml
# (each containing a single object type).


def parse_voc_xml(xml_path: Path) -> VocAnnotation:
    """Parse a PASCAL VOC XML annotation file.

    Reads the file at ``xml_path``, extracts the image filename, size,
    and all ``<object>`` blocks (each with class name and bounding box),
    and returns them wrapped in a ``VocAnnotation``.

    Coordinates in the XML are absolute pixel values in ``xmin, ymin,
    xmax, ymax`` form. They are returned unchanged.

    Args:
        xml_path: Path to the XML file to parse.

    Returns:
        A ``VocAnnotation`` with the file's contents.
    """
    tree = etree.parse(str(xml_path))
    root = tree.getroot()

    filename = root.find("filename").text
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    objects = [
        VocObject(
            name=obj.find("name").text,
            xmin=int(obj.find("bndbox/xmin").text),
            ymin=int(obj.find("bndbox/ymin").text),
            xmax=int(obj.find("bndbox/xmax").text),
            ymax=int(obj.find("bndbox/ymax").text),
        )
        for obj in root.findall("object")
    ]

    return VocAnnotation(
        filename=filename,
        width=width,
        height=height,
        objects=objects,
    )


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