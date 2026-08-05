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

import warnings
from dataclasses import dataclass, field
from enum import Enum
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


# Category IDs from the unified five-class schema. Kept as module-level
# constants so mapping code reads as CATEGORY_INTACT_INSULATOR rather than
# a bare integer literal.

CATEGORY_INTACT_INSULATOR = 1
CATEGORY_MISSING_CAP_OR_SHED = 2
CATEGORY_BROKEN_CONDUCTOR_STRAND = 3
CATEGORY_COMPOSITE_SURFACE_DEGRADATION = 4
CATEGORY_FITTINGS_AND_HARDWARE = 5


@dataclass
class UnifiedAnnotation:
    """One annotation in the project's unified five-class schema.

    Corresponds to one bounding box in one image. Multiple annotations
    per image are allowed; each carries its own category and provenance.
    """

    image_id: str
    source_dataset: str
    category_id: int
    bbox_xyxy: tuple[int, int, int, int]
    mapping_confidence: str
    synthetic: bool = False

class CplidSourceKind(Enum):
    """Which subset of CPLID an annotation was loaded from.

    The same class string (``insulator``) means different things depending
    on which folder the XML came from. This enum makes the source explicit
    at the mapping-function boundary rather than inferring it from paths.
    """

    NORMAL_INSULATORS = "normal_insulators"
    DEFECTIVE_DEFECTS = "defective_defects"    


@dataclass
class WalkResult:
    """Aggregated output from walking one CPLID subfolder.

    Bundles the produced annotations with counts that let ``main`` print
    a per-folder summary without recomputing statistics from the list.
    """

    annotations: list[UnifiedAnnotation] = field(default_factory=list)
    files_processed: int = 0
    files_failed: int = 0
    files_skipped_no_objects: int = 0
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


# ---------------------------------------------------------------------------
# Class mapping
# ---------------------------------------------------------------------------
# Translates parsed VOC annotations into the project's five-class unified
# schema. Class mapping decisions and their rationale live in
# docs/02_dataset_strategy.md; this code is the executable form of that
# document's per-dataset mapping table.


def voc_to_unified(
    voc_ann: VocAnnotation,
    source_kind: CplidSourceKind,
    image_id: str,
) -> list[UnifiedAnnotation]:
    """Map a parsed VOC annotation to unified-schema annotations.

    Applies the CPLID class mapping from docs/02_dataset_strategy.md.
    Objects with an unexpected class name for their source folder are
    skipped and a warning is emitted; parsing continues on the rest.

    Args:
        voc_ann: The parsed VOC annotation.
        source_kind: Which CPLID subfolder the annotation came from.
        image_id: Unique identifier for the source image, used in the
            output annotation's ``image_id`` field.

    Returns:
        A list of ``UnifiedAnnotation`` instances. May be empty if all
        objects were unexpected for the source.
    """
    match source_kind:
        case CplidSourceKind.NORMAL_INSULATORS:
            expected_name = "insulator"
            category_id = CATEGORY_INTACT_INSULATOR
            mapping_confidence = "clean"
            synthetic = False
        case CplidSourceKind.DEFECTIVE_DEFECTS:
            expected_name = "defect"
            category_id = CATEGORY_MISSING_CAP_OR_SHED
            mapping_confidence = "with_caveats"
            synthetic = True

    unified: list[UnifiedAnnotation] = []
    for obj in voc_ann.objects:
        if obj.name != expected_name:
            warnings.warn(
                f"Unexpected object name {obj.name!r} in {image_id} "
                f"from source {source_kind.value}; expected {expected_name!r}. "
                f"Skipping.",
                stacklevel=2,
            )
            continue

        unified.append(
            UnifiedAnnotation(
                image_id=image_id,
                source_dataset="CPLID",
                category_id=category_id,
                bbox_xyxy=(obj.xmin, obj.ymin, obj.xmax, obj.ymax),
                mapping_confidence=mapping_confidence,
                synthetic=synthetic,
            )
        )

    return unified


# ---------------------------------------------------------------------------
# File walking
# ---------------------------------------------------------------------------
# Iterates over every XML file in a CPLID subfolder, parsing each and mapping
# its objects to unified schema. Individual file failures are logged but do
# not abort the walk; overall counters are returned alongside the annotations.


def walk_normal_insulators() -> WalkResult:
    """Walk Normal_Insulators/labels/ and produce Class 1 annotations.

    Every XML file in the folder is parsed, mapped through
    ``voc_to_unified`` with source kind ``NORMAL_INSULATORS``, and its
    resulting annotations added to the returned ``WalkResult``. Files
    that raise an exception during parsing are logged as failures.

    Returns:
        A ``WalkResult`` bundling the produced annotations with counts
        for processed, failed, and empty files.
    """
    print(f"Walking Normal_Insulators from {NORMAL_LABELS_DIR}")
    result = WalkResult()

    xml_files = sorted(NORMAL_LABELS_DIR.glob("*.xml"))
    total = len(xml_files)
    print(f"  Found {total} XML files")

    for i, xml_path in enumerate(xml_files, start=1):
        image_id = f"cplid_normal_{xml_path.stem}"

        try:
            voc_ann = parse_voc_xml(xml_path)
            unified = voc_to_unified(voc_ann, CplidSourceKind.NORMAL_INSULATORS, image_id)
        except Exception as e:
            warnings.warn(f"Failed to process {xml_path.name}: {e}", stacklevel=2)
            result.files_failed += 1
            continue

        result.files_processed += 1
        if not unified:
            result.files_skipped_no_objects += 1
        else:
            result.annotations.extend(unified)

        if i % 100 == 0:
            print(f"  Processed {i}/{total} files, {len(result.annotations)} annotations so far")

    print(
        f"  Done. {result.files_processed} processed, "
        f"{result.files_failed} failed, "
        f"{result.files_skipped_no_objects} yielded no annotations. "
        f"{len(result.annotations)} annotations total."
    )
    return result


def walk_defective_defects() -> WalkResult:
    """Walk Defective_Insulators/labels/defect/ and produce Class 2 annotations.

    Every XML file in the folder is parsed, mapped through
    ``voc_to_unified`` with source kind ``DEFECTIVE_DEFECTS``, and its
    resulting annotations added to the returned ``WalkResult``. Files
    that raise an exception during parsing are logged as failures.

    Note that the insulator-level XMLs in
    ``Defective_Insulators/labels/insulator/`` are not walked here; per
    the class mapping in docs/02_dataset_strategy.md, those are discarded
    because the insulator objects on defective images do not represent
    intact reference material.

    Returns:
        A ``WalkResult`` bundling the produced annotations with counts
        for processed, failed, and empty files.
    """
    print(f"Walking Defective_Insulators/defect from {DEFECTIVE_DEFECT_LABELS_DIR}")
    result = WalkResult()

    xml_files = sorted(DEFECTIVE_DEFECT_LABELS_DIR.glob("*.xml"))
    total = len(xml_files)
    print(f"  Found {total} XML files")

    for i, xml_path in enumerate(xml_files, start=1):
        image_id = f"cplid_defective_{xml_path.stem}"

        try:
            voc_ann = parse_voc_xml(xml_path)
            unified = voc_to_unified(voc_ann, CplidSourceKind.DEFECTIVE_DEFECTS, image_id)
        except Exception as e:
            warnings.warn(f"Failed to process {xml_path.name}: {e}", stacklevel=2)
            result.files_failed += 1
            continue

        result.files_processed += 1
        if not unified:
            result.files_skipped_no_objects += 1
        else:
            result.annotations.extend(unified)

        if i % 100 == 0:
            print(f"  Processed {i}/{total} files, {len(result.annotations)} annotations so far")

    print(
        f"  Done. {result.files_processed} processed, "
        f"{result.files_failed} failed, "
        f"{result.files_skipped_no_objects} yielded no annotations. "
        f"{len(result.annotations)} annotations total."
    )
    return result

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