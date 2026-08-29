"""Synthetic-only probes for isolated pydicom and WFDB adapter environments."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import tempfile
import time
from pathlib import Path
from typing import Any


def _hash_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    receipt["probe_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload = json.dumps(receipt, sort_keys=True, separators=(",", ":")).encode()
    return {**receipt, "receipt_sha256": hashlib.sha256(payload).hexdigest()}


def _pydicom_probe() -> dict[str, Any]:
    pydicom = importlib.import_module("pydicom")
    dataset_module = importlib.import_module("pydicom.dataset")
    errors_module = importlib.import_module("pydicom.errors")
    uid_module = importlib.import_module("pydicom.uid")
    FileDataset = dataset_module.FileDataset
    FileMetaDataset = dataset_module.FileMetaDataset
    InvalidDicomError = errors_module.InvalidDicomError
    ExplicitVRLittleEndian = uid_module.ExplicitVRLittleEndian
    generate_uid = uid_module.generate_uid

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="rcagent-pydicom-") as directory:
        root = Path(directory)
        series_uid = generate_uid(entropy_srcs=["rcagent", "synthetic", "series"])
        paths: list[Path] = []
        for instance in (1, 2):
            file_meta = FileMetaDataset()
            file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
            file_meta.MediaStorageSOPClassUID = generate_uid(
                entropy_srcs=["rcagent", "synthetic", "class"]
            )
            file_meta.MediaStorageSOPInstanceUID = generate_uid(
                entropy_srcs=["rcagent", "synthetic", str(instance)]
            )
            dataset = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
            dataset.SOPClassUID = file_meta.MediaStorageSOPClassUID
            dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
            dataset.SeriesInstanceUID = series_uid
            dataset.InstanceNumber = instance
            dataset.PatientName = "SYNTHETIC^TEST"
            dataset.PatientID = "SYNTHETIC-ONLY"
            dataset.BurnedInAnnotation = "YES"
            dataset.Rows = 2
            dataset.Columns = 2
            dataset.SamplesPerPixel = 1
            dataset.PhotometricInterpretation = "MONOCHROME2"
            dataset.BitsAllocated = 8
            dataset.BitsStored = 8
            dataset.HighBit = 7
            dataset.PixelRepresentation = 0
            dataset.PixelData = bytes([0, 1, 2, 3])
            path = root / f"synthetic-{instance}.dcm"
            dataset.save_as(path, enforce_file_format=True)
            paths.append(path)

        records = [pydicom.dcmread(path) for path in paths]
        direct_identifiers_removed = True
        for record in records:
            del record.PatientName
            del record.PatientID
            direct_identifiers_removed = direct_identifiers_removed and not any(
                key in record for key in ("PatientName", "PatientID")
            )
        invalid_path = root / "adversarial.dcm"
        invalid_path.write_bytes(b"not a dicom file")
        adversarial_rejected = False
        try:
            pydicom.dcmread(invalid_path)
        except InvalidDicomError:
            adversarial_rejected = True

        observations = {
            "instances": len(records),
            "series_integrity": len({str(item.SeriesInstanceUID) for item in records}) == 1,
            "instance_numbers": [int(item.InstanceNumber) for item in records],
            "pixel_regions": [
                {"rows": int(item.Rows), "columns": int(item.Columns)} for item in records
            ],
            "burned_in_annotation_detected": all(
                item.BurnedInAnnotation == "YES" for item in records
            ),
            "quarantine_required": True,
            "direct_identifiers_removed": direct_identifiers_removed,
            "adversarial_file_rejected": adversarial_rejected,
            "clinical_interpretation": "disabled",
        }
    return _hash_receipt(
        {
            "schema_version": "1.0",
            "profile_id": "medical-imaging-research",
            "framework": f"pydicom {pydicom.__version__}",
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
    )


def _wfdb_probe() -> dict[str, Any]:
    np = importlib.import_module("numpy")
    wfdb = importlib.import_module("wfdb")

    started = time.perf_counter()
    sampling_hz = 250
    samples = 2500
    with tempfile.TemporaryDirectory(prefix="rcagent-wfdb-") as directory:
        root = Path(directory)
        time_axis = np.arange(samples, dtype=float) / sampling_hz
        signal = np.column_stack(
            (
                np.sin(2 * np.pi * time_axis),
                np.sin(2 * np.pi * time_axis + 0.25),
            )
        )
        wfdb.wrsamp(
            "synthetic",
            fs=sampling_hz,
            units=["mV", "mV"],
            sig_name=["I", "II"],
            p_signal=signal,
            fmt=["16", "16"],
            write_dir=str(root),
        )
        wfdb.wrann(
            "synthetic",
            "atr",
            sample=np.array([250, 500], dtype=np.int64),
            symbol=["N", "N"],
            write_dir=str(root),
        )
        record = wfdb.rdrecord(str(root / "synthetic"))
        annotation = wfdb.rdann(str(root / "synthetic"), "atr")
        invalid_header = root / "adversarial.hea"
        invalid_header.write_text("invalid header\n", encoding="utf-8")
        adversarial_rejected = False
        try:
            wfdb.rdheader(str(root / "adversarial"))
        except (ValueError, IndexError):
            adversarial_rejected = True
        observed_names = list(record.sig_name or [])
        observations = {
            "samples": int(record.sig_len),
            "sampling_hz": float(record.fs),
            "signal_names": observed_names,
            "missing_standard_12_leads": len(observed_names) < 12,
            "annotation_samples": [int(value) for value in annotation.sample],
            "annotation_timestamps_ms": [
                round(int(value) * 1000 / sampling_hz, 3) for value in annotation.sample
            ],
            "provenance_files": sorted(path.name for path in root.glob("synthetic.*")),
            "adversarial_header_rejected": adversarial_rejected,
            "diagnostic_interpretation": "disabled",
        }
    return _hash_receipt(
        {
            "schema_version": "1.0",
            "profile_id": "ecg-research",
            "framework": f"WFDB {wfdb.__version__}",
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
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("profile", choices=("pydicom", "wfdb"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = _pydicom_probe() if args.profile == "pydicom" else _wfdb_probe()
    output = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0 if receipt["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
