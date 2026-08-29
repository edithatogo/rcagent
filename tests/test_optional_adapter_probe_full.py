from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import tools.optional_adapter_probe as probe


class _Dataset:
    def __init__(self, *_args, file_meta=None, **_kwargs) -> None:
        object.__setattr__(self, "_values", {})
        if file_meta is not None:
            object.__setattr__(self, "file_meta", file_meta)

    def __getattr__(self, name: str):
        try:
            return self._values[name]
        except KeyError as error:
            raise AttributeError(name) from error

    def __setattr__(self, name: str, value) -> None:
        self._values[name] = value

    def __delattr__(self, name: str) -> None:
        del self._values[name]

    def __contains__(self, name: str) -> bool:
        return name in self._values

    def save_as(self, path: Path, *, enforce_file_format: bool) -> None:
        assert enforce_file_format is True
        path.write_bytes(b"synthetic dicom")
        _DICOM_RECORDS[str(path)] = self


class _InvalidDicomError(Exception):
    pass


_DICOM_RECORDS: dict[str, _Dataset] = {}


def _fake_pydicom_modules():
    counter = iter(range(100))

    def generate_uid(*, entropy_srcs: list[str]) -> str:
        return f"1.2.826.{'.'.join(entropy_srcs)}.{next(counter)}"

    def dcmread(path: Path):
        try:
            return _DICOM_RECORDS[str(path)]
        except KeyError as error:
            raise _InvalidDicomError from error

    return {
        "pydicom": SimpleNamespace(__version__="test", dcmread=dcmread),
        "pydicom.dataset": SimpleNamespace(FileDataset=_Dataset, FileMetaDataset=_Dataset),
        "pydicom.errors": SimpleNamespace(InvalidDicomError=_InvalidDicomError),
        "pydicom.uid": SimpleNamespace(
            ExplicitVRLittleEndian="1.2.840.10008.1.2.1", generate_uid=generate_uid
        ),
    }


class _Vector:
    def __init__(self, values) -> None:
        self.values = list(values)

    def __truediv__(self, value):
        return _Vector(item / value for item in self.values)

    def __mul__(self, value):
        return _Vector(item * value for item in self.values)

    __rmul__ = __mul__

    def __add__(self, value):
        return _Vector(item + value for item in self.values)


def _fake_wfdb_modules():
    state: dict[str, object] = {}

    numpy = SimpleNamespace(
        pi=3.141592653589793,
        int64=int,
        arange=lambda size, dtype=float: _Vector(dtype(item) for item in range(size)),
        sin=lambda values: [0.0 for _ in values.values],
        column_stack=lambda columns: list(zip(*columns, strict=True)),
        array=lambda values, dtype=None: [dtype(value) if dtype else value for value in values],
    )

    def wrsamp(name: str, **kwargs) -> None:
        root = Path(kwargs["write_dir"])
        (root / f"{name}.hea").write_text("synthetic header", encoding="utf-8")
        (root / f"{name}.dat").write_bytes(b"synthetic signal")
        state["record"] = SimpleNamespace(
            sig_name=kwargs["sig_name"], sig_len=len(kwargs["p_signal"]), fs=kwargs["fs"]
        )

    def wrann(name: str, extension: str, **kwargs) -> None:
        root = Path(kwargs["write_dir"])
        (root / f"{name}.{extension}").write_bytes(b"synthetic annotations")
        state["annotation"] = SimpleNamespace(sample=kwargs["sample"])

    def rdheader(_path: str) -> None:
        raise ValueError("invalid synthetic header")

    wfdb = SimpleNamespace(
        __version__="test",
        wrsamp=wrsamp,
        wrann=wrann,
        rdrecord=lambda _path: state["record"],
        rdann=lambda _path, _extension: state["annotation"],
        rdheader=rdheader,
    )
    return {"numpy": numpy, "wfdb": wfdb}


def test_pydicom_probe_with_fake_optional_dependency(monkeypatch) -> None:
    modules = _fake_pydicom_modules()
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)

    receipt = probe._pydicom_probe()

    assert receipt["passed"] is True
    assert receipt["framework"] == "pydicom test"
    assert receipt["observations"] == {
        "instances": 2,
        "series_integrity": True,
        "instance_numbers": [1, 2],
        "pixel_regions": [{"rows": 2, "columns": 2}, {"rows": 2, "columns": 2}],
        "burned_in_annotation_detected": True,
        "quarantine_required": True,
        "direct_identifiers_removed": True,
        "adversarial_file_rejected": True,
        "clinical_interpretation": "disabled",
    }
    assert len(receipt["probe_sha256"]) == len(receipt["receipt_sha256"]) == 64


def test_wfdb_probe_with_fake_optional_dependencies(monkeypatch) -> None:
    modules = _fake_wfdb_modules()
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)

    receipt = probe._wfdb_probe()

    assert receipt["passed"] is True
    assert receipt["framework"] == "WFDB test"
    assert receipt["observations"]["samples"] == 2500
    assert receipt["observations"]["signal_names"] == ["I", "II"]
    assert receipt["observations"]["annotation_samples"] == [250, 500]
    assert receipt["observations"]["annotation_timestamps_ms"] == [1000.0, 2000.0]
    assert receipt["observations"]["provenance_files"] == [
        "synthetic.atr",
        "synthetic.dat",
        "synthetic.hea",
    ]
    assert receipt["observations"]["adversarial_header_rejected"] is True


def test_cli_prints_successful_receipt(monkeypatch, capsys) -> None:
    monkeypatch.setattr(probe, "_pydicom_probe", lambda: {"passed": True, "profile": "fake"})
    monkeypatch.setattr(sys, "argv", ["optional_adapter_probe", "pydicom"])

    assert probe.main() == 0
    assert json.loads(capsys.readouterr().out) == {"passed": True, "profile": "fake"}


def test_cli_writes_failed_receipt_and_returns_one(monkeypatch, tmp_path: Path) -> None:
    output = tmp_path / "nested" / "receipt.json"
    monkeypatch.setattr(probe, "_wfdb_probe", lambda: {"passed": False, "profile": "fake"})
    monkeypatch.setattr(
        sys, "argv", ["optional_adapter_probe", "wfdb", "--output", str(output)]
    )

    assert probe.main() == 1
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "passed": False,
        "profile": "fake",
    }
