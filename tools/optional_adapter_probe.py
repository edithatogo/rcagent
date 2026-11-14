"""Synthetic-only probes for isolated pydicom and WFDB adapter environments."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import tempfile
import time
from collections.abc import Iterable, Mapping
from numbers import Integral, Real
from pathlib import Path
from typing import Literal, Protocol, TypedDict, TypeGuard, runtime_checkable


class ReceiptHashes(TypedDict):
    probe_sha256: str
    receipt_sha256: str


class ProbeBody(TypedDict):
    schema_version: Literal["1.0"]
    framework: str
    data_class: Literal["generated_synthetic_only"]
    network: str
    telemetry: Literal["none"]
    remote_code: Literal["prohibited"]
    elapsed_ms: float
    passed: bool
    limitations: list[str]


class PixelRegion(TypedDict):
    rows: int
    columns: int


class PydicomObservations(TypedDict):
    instances: int
    series_integrity: bool
    instance_numbers: list[int]
    pixel_regions: list[PixelRegion]
    burned_in_annotation_detected: bool
    quarantine_required: Literal[True]
    direct_identifiers_removed: bool
    adversarial_file_rejected: bool
    clinical_interpretation: Literal["disabled"]


class PydicomBody(ProbeBody):
    profile_id: Literal["medical-imaging-research"]
    observations: PydicomObservations


class PydicomReceipt(PydicomBody, ReceiptHashes):
    pass


class WfdbObservations(TypedDict):
    samples: int
    sampling_hz: float
    signal_names: list[str]
    missing_standard_12_leads: bool
    annotation_samples: list[int]
    annotation_timestamps_ms: list[float]
    provenance_files: list[str]
    adversarial_header_rejected: bool
    diagnostic_interpretation: Literal["disabled"]


class WfdbBody(ProbeBody):
    profile_id: Literal["ecg-research"]
    observations: WfdbObservations


class WfdbReceipt(WfdbBody, ReceiptHashes):
    pass


@runtime_checkable
class _CallablePort(Protocol):
    """Only callable presence is established; every returned payload stays raw."""

    def __call__(self, *args: object, **kwargs: object) -> object: ...


@runtime_checkable
class _VectorPort(Protocol):
    """Arithmetic member presence without asserting a native array's result type."""

    def __truediv__(self, value: float) -> object: ...

    def __rmul__(self, value: float) -> object: ...

    def __add__(self, value: float) -> object: ...


def _member(owner: object, name: str) -> object:
    try:
        return getattr(owner, name)
    except AttributeError as exc:
        raise ValueError(f"optional adapter is missing {name}") from exc


def _callable_member(owner: object, name: str) -> _CallablePort:
    member = _member(owner, name)
    if not isinstance(member, _CallablePort) or not callable(member):
        raise ValueError(f"optional adapter {name} must be callable")
    return member


def _call_member(owner: object, name: str, *args: object, **kwargs: object) -> object:
    return _callable_member(owner, name)(*args, **kwargs)


def _vector(value: object) -> _VectorPort:
    if not isinstance(value, _VectorPort):
        raise ValueError("optional adapter numeric vector has invalid arithmetic members")
    for name in ("__truediv__", "__rmul__", "__add__"):
        if not callable(_member(value, name)):
            raise ValueError("optional adapter numeric vector has invalid arithmetic members")
    return value


def _string(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("optional adapter text field must be a string")
    return value


def _integer(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError("optional adapter integer field must be an integer")
    return int(value)


def _number(value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("optional adapter numeric field must be finite")
    try:
        number = float(value)
    except OverflowError as exc:
        raise ValueError("optional adapter numeric field must be finite") from exc
    if not math.isfinite(number):
        raise ValueError("optional adapter numeric field must be finite")
    return number


def _boolean(value: object) -> bool:
    if not isinstance(value, bool):
        raise ValueError("optional adapter predicate must return a boolean")
    return value


def _is_iterable(value: object) -> TypeGuard[Iterable[object]]:
    return isinstance(value, Iterable)


def _items(value: object) -> Iterable[object]:
    if isinstance(value, (str, bytes)) or not _is_iterable(value):
        raise ValueError("optional adapter collection must be an iterable")
    return value


def _is_exception_class(value: object) -> TypeGuard[type[Exception]]:
    return isinstance(value, type) and issubclass(value, Exception)


def _receipt_hashes(receipt: Mapping[str, object]) -> ReceiptHashes:
    probe_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload = json.dumps(
        {**receipt, "probe_sha256": probe_hash}, sort_keys=True, separators=(",", ":")
    ).encode()
    return {"probe_sha256": probe_hash, "receipt_sha256": hashlib.sha256(payload).hexdigest()}


def hash_receipt(receipt: dict[str, object]) -> dict[str, object]:
    hashes = _receipt_hashes(receipt)
    receipt["probe_sha256"] = hashes["probe_sha256"]
    return {**receipt, "receipt_sha256": hashes["receipt_sha256"]}


def probe_pydicom() -> PydicomReceipt:
    pydicom: object = importlib.import_module("pydicom")
    dataset_module: object = importlib.import_module("pydicom.dataset")
    errors_module: object = importlib.import_module("pydicom.errors")
    uid_module: object = importlib.import_module("pydicom.uid")
    invalid_dicom_error = _member(errors_module, "InvalidDicomError")
    if not _is_exception_class(invalid_dicom_error):
        raise ValueError("optional adapter InvalidDicomError must be an exception class")
    explicit_vr_little_endian = _string(_member(uid_module, "ExplicitVRLittleEndian"))

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="rcagent-pydicom-") as directory:
        root = Path(directory)
        series_uid = _string(
            _call_member(
                uid_module, "generate_uid", entropy_srcs=["rcagent", "synthetic", "series"]
            )
        )
        paths: list[Path] = []
        for instance in (1, 2):
            file_meta = _call_member(dataset_module, "FileMetaDataset")
            metadata_fields = {
                "TransferSyntaxUID": explicit_vr_little_endian,
                "MediaStorageSOPClassUID": _string(
                    _call_member(
                        uid_module, "generate_uid", entropy_srcs=["rcagent", "synthetic", "class"]
                    )
                ),
                "MediaStorageSOPInstanceUID": _string(
                    _call_member(
                        uid_module,
                        "generate_uid",
                        entropy_srcs=["rcagent", "synthetic", str(instance)],
                    )
                ),
            }
            for name, value in metadata_fields.items():
                setattr(file_meta, name, value)
            dataset = _call_member(
                dataset_module, "FileDataset", None, {}, file_meta=file_meta, preamble=b"\0" * 128
            )
            fields: dict[str, object] = {
                "SOPClassUID": _string(_member(file_meta, "MediaStorageSOPClassUID")),
                "SOPInstanceUID": _string(_member(file_meta, "MediaStorageSOPInstanceUID")),
                "SeriesInstanceUID": series_uid,
                "InstanceNumber": instance,
                "PatientName": "SYNTHETIC^TEST",
                "PatientID": "SYNTHETIC-ONLY",
                "BurnedInAnnotation": "YES",
                "Rows": 2,
                "Columns": 2,
                "SamplesPerPixel": 1,
                "PhotometricInterpretation": "MONOCHROME2",
                "BitsAllocated": 8,
                "BitsStored": 8,
                "HighBit": 7,
                "PixelRepresentation": 0,
                "PixelData": bytes([0, 1, 2, 3]),
            }
            for name, value in fields.items():
                setattr(dataset, name, value)
            path = root / f"synthetic-{instance}.dcm"
            _call_member(dataset, "save_as", path, enforce_file_format=True)
            paths.append(path)

        records = [_call_member(pydicom, "dcmread", path) for path in paths]
        direct_identifiers_removed = True
        for record in records:
            delattr(record, "PatientName")
            delattr(record, "PatientID")
            direct_identifiers_removed = direct_identifiers_removed and not any(
                _boolean(_call_member(record, "__contains__", key))
                for key in ("PatientName", "PatientID")
            )
        invalid_path = root / "adversarial.dcm"
        invalid_path.write_bytes(b"not a dicom file")
        adversarial_rejected = False
        try:
            _call_member(pydicom, "dcmread", invalid_path)
        except invalid_dicom_error:
            adversarial_rejected = True

        observations: PydicomObservations = {
            "instances": len(records),
            "series_integrity": len(
                {_string(_member(item, "SeriesInstanceUID")) for item in records}
            )
            == 1,
            "instance_numbers": [_integer(_member(item, "InstanceNumber")) for item in records],
            "pixel_regions": [
                {
                    "rows": _integer(_member(item, "Rows")),
                    "columns": _integer(_member(item, "Columns")),
                }
                for item in records
            ],
            "burned_in_annotation_detected": all(
                _string(_member(item, "BurnedInAnnotation")) == "YES" for item in records
            ),
            "quarantine_required": True,
            "direct_identifiers_removed": direct_identifiers_removed,
            "adversarial_file_rejected": adversarial_rejected,
            "clinical_interpretation": "disabled",
        }
    receipt: PydicomBody = {
        "schema_version": "1.0",
        "profile_id": "medical-imaging-research",
        "framework": f"pydicom {_string(_member(pydicom, '__version__'))}",
        "data_class": "generated_synthetic_only",
        "network": "disabled_no_network_api_used",
        "telemetry": "none",
        "remote_code": "prohibited",
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "observations": observations,
        "passed": all(
            (
                observations["series_integrity"],
                observations["burned_in_annotation_detected"],
                observations["quarantine_required"],
                observations["direct_identifiers_removed"],
                observations["adversarial_file_rejected"],
            )
        ),
        "limitations": [
            "metadata and uncompressed synthetic pixels only",
            "burned-in annotation is detected but not removed",
            "no clinical interpretation, validation, or operational support claim",
        ],
    }
    return {**receipt, **_receipt_hashes(receipt)}


def probe_wfdb() -> WfdbReceipt:
    np: object = importlib.import_module("numpy")
    wfdb: object = importlib.import_module("wfdb")

    started = time.perf_counter()
    sampling_hz = 250
    samples = 2500
    with tempfile.TemporaryDirectory(prefix="rcagent-wfdb-") as directory:
        root = Path(directory)
        time_axis = _vector(_vector(_call_member(np, "arange", samples, dtype=float)) / sampling_hz)
        phase = _vector(2 * _number(_member(np, "pi")) * time_axis)
        signal = _call_member(
            np,
            "column_stack",
            (
                _call_member(np, "sin", phase),
                _call_member(np, "sin", phase + 0.25),
            ),
        )
        _call_member(
            wfdb,
            "wrsamp",
            "synthetic",
            fs=sampling_hz,
            units=["mV", "mV"],
            sig_name=["I", "II"],
            p_signal=signal,
            fmt=["16", "16"],
            write_dir=str(root),
        )
        _call_member(
            wfdb,
            "wrann",
            "synthetic",
            "atr",
            sample=_call_member(np, "array", [250, 500], dtype=_member(np, "int64")),
            symbol=["N", "N"],
            write_dir=str(root),
        )
        record = _call_member(wfdb, "rdrecord", str(root / "synthetic"))
        annotation = _call_member(wfdb, "rdann", str(root / "synthetic"), "atr")
        invalid_header = root / "adversarial.hea"
        invalid_header.write_text("invalid header\n", encoding="utf-8")
        read_header = _callable_member(wfdb, "rdheader")
        adversarial_rejected = False
        try:
            read_header(str(root / "adversarial"))
        except (ValueError, IndexError):
            adversarial_rejected = True
        names = _member(record, "sig_name")
        observed_names = [] if names is None else [_string(value) for value in _items(names)]
        annotation_samples = [_integer(value) for value in _items(_member(annotation, "sample"))]
        observations: WfdbObservations = {
            "samples": _integer(_member(record, "sig_len")),
            "sampling_hz": _number(_member(record, "fs")),
            "signal_names": observed_names,
            "missing_standard_12_leads": len(observed_names) < 12,
            "annotation_samples": annotation_samples,
            "annotation_timestamps_ms": [
                round(value * 1000 / sampling_hz, 3) for value in annotation_samples
            ],
            "provenance_files": sorted(path.name for path in root.glob("synthetic.*")),
            "adversarial_header_rejected": adversarial_rejected,
            "diagnostic_interpretation": "disabled",
        }
    receipt: WfdbBody = {
        "schema_version": "1.0",
        "profile_id": "ecg-research",
        "framework": f"WFDB {_string(_member(wfdb, '__version__'))}",
        "data_class": "generated_synthetic_only",
        "network": "disabled_local_file_api_only",
        "telemetry": "none",
        "remote_code": "prohibited",
        "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        "observations": observations,
        "passed": all(
            (
                observations["samples"] == samples,
                observations["sampling_hz"] == sampling_hz,
                observations["signal_names"] == ["I", "II"],
                observations["missing_standard_12_leads"],
                observations["annotation_samples"] == [250, 500],
                observations["adversarial_header_rejected"],
            )
        ),
        "limitations": [
            "generated two-channel waveform only",
            "no diagnostic or clinical interpretation",
            "no model inference, clinical validation, or operational support claim",
        ],
    }
    return {**receipt, **_receipt_hashes(receipt)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", choices=("pydicom", "wfdb"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = probe_pydicom() if args.profile == "pydicom" else probe_wfdb()
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
