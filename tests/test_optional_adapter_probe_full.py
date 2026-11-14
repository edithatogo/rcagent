from __future__ import annotations

import json
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

import pytest

import tools.optional_adapter_probe as probe


class _Dataset:
    _values: dict[str, object]

    def __init__(self, *_args: object, file_meta: object = None, **_kwargs: object) -> None:
        object.__setattr__(self, "_values", {})
        if file_meta is not None:
            object.__setattr__(self, "file_meta", file_meta)

    def __getattr__(self, name: str) -> object:
        try:
            return self._values[name]
        except KeyError as error:
            raise AttributeError(name) from error

    def __setattr__(self, name: str, value: object) -> None:
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


def _fake_pydicom_modules(
    *, readback_changes: dict[str, object] | None = None
) -> dict[str, object]:
    counter = iter(range(100))

    def generate_uid(*, entropy_srcs: list[str]) -> str:
        return f"1.2.826.{'.'.join(entropy_srcs)}.{next(counter)}"

    def dcmread(path: Path) -> _Dataset:
        try:
            record = _DICOM_RECORDS[str(path)]
        except KeyError as error:
            raise _InvalidDicomError from error
        for name, value in (readback_changes or {}).items():
            setattr(record, name, value)
        return record

    return {
        "pydicom": SimpleNamespace(__version__="test", dcmread=dcmread),
        "pydicom.dataset": SimpleNamespace(FileDataset=_Dataset, FileMetaDataset=_Dataset),
        "pydicom.errors": SimpleNamespace(InvalidDicomError=_InvalidDicomError),
        "pydicom.uid": SimpleNamespace(
            ExplicitVRLittleEndian="1.2.840.10008.1.2.1", generate_uid=generate_uid
        ),
    }


class _Vector:
    def __init__(self, values: Iterable[float]) -> None:
        self.values = list(values)

    def __truediv__(self, value: float) -> _Vector:
        return _Vector(item / value for item in self.values)

    def __mul__(self, value: float) -> _Vector:
        return _Vector(item * value for item in self.values)

    __rmul__ = __mul__

    def __add__(self, value: float) -> _Vector:
        return _Vector(item + value for item in self.values)


@dataclass
class _Record:
    sig_name: list[str]
    sig_len: int
    fs: float


@dataclass
class _Annotation:
    sample: list[int]


def _fake_wfdb_modules(
    *,
    record_changes: dict[str, object] | None = None,
    annotation_changes: dict[str, object] | None = None,
) -> dict[str, object]:
    record: _Record | None = None
    annotation: _Annotation | None = None

    def arange(size: int, *, dtype: type[float] = float) -> _Vector:
        return _Vector(dtype(item) for item in range(size))

    def sin(values: _Vector) -> list[float]:
        return [0.0 for _ in values.values]

    def column_stack(columns: tuple[list[float], list[float]]) -> list[tuple[float, float]]:
        return list(zip(*columns, strict=True))

    def array(values: list[int], *, dtype: type[int] | None = None) -> list[int]:
        return [dtype(value) if dtype else value for value in values]

    numpy = SimpleNamespace(
        pi=3.141592653589793,
        int64=int,
        arange=arange,
        sin=sin,
        column_stack=column_stack,
        array=array,
    )

    def wrsamp(
        name: str,
        *,
        fs: int,
        units: list[str],
        sig_name: list[str],
        p_signal: list[tuple[float, float]],
        fmt: list[str],
        write_dir: str,
    ) -> None:
        nonlocal record
        assert units == ["mV", "mV"]
        assert fmt == ["16", "16"]
        root = Path(write_dir)
        (root / f"{name}.hea").write_text("synthetic header", encoding="utf-8")
        (root / f"{name}.dat").write_bytes(b"synthetic signal")
        record = _Record(sig_name=sig_name, sig_len=len(p_signal), fs=fs)

    def wrann(
        name: str, extension: str, *, sample: list[int], symbol: list[str], write_dir: str
    ) -> None:
        nonlocal annotation
        assert symbol == ["N", "N"]
        root = Path(write_dir)
        (root / f"{name}.{extension}").write_bytes(b"synthetic annotations")
        annotation = _Annotation(sample=sample)

    def rdrecord(_path: str) -> _Record:
        assert record is not None
        for name, value in (record_changes or {}).items():
            setattr(record, name, value)
        return record

    def rdann(_path: str, _extension: str) -> _Annotation:
        assert annotation is not None
        for name, value in (annotation_changes or {}).items():
            setattr(annotation, name, value)
        return annotation

    def rdheader(_path: str) -> None:
        raise ValueError("invalid synthetic header")

    wfdb = SimpleNamespace(
        __version__="test",
        wrsamp=wrsamp,
        wrann=wrann,
        rdrecord=rdrecord,
        rdann=rdann,
        rdheader=rdheader,
    )
    return {"numpy": numpy, "wfdb": wfdb}


def test_pydicom_probe_with_fake_optional_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    modules = _fake_pydicom_modules()
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)

    receipt = probe.probe_pydicom()

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


def test_wfdb_probe_with_fake_optional_dependencies(monkeypatch: pytest.MonkeyPatch) -> None:
    modules = _fake_wfdb_modules()
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)

    receipt = probe.probe_wfdb()

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


@pytest.mark.parametrize(
    ("field", "value"),
    [("SeriesInstanceUID", None), ("InstanceNumber", True), ("Rows", 2.5)],
)
def test_malformed_native_dicom_fields_are_not_coerced_into_evidence(
    monkeypatch: pytest.MonkeyPatch, field: str, value: object
) -> None:
    modules = _fake_pydicom_modules(readback_changes={field: value})
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)
    with pytest.raises(ValueError, match="optional adapter"):
        probe.probe_pydicom()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("sig_len", True),
        ("fs", True),
        ("fs", float("nan")),
        ("fs", float("inf")),
        ("sig_name", [None, "II"]),
    ],
)
def test_malformed_native_signal_fields_are_not_coerced_into_evidence(
    monkeypatch: pytest.MonkeyPatch, field: str, value: object
) -> None:
    modules = _fake_wfdb_modules(record_changes={field: value})
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)
    with pytest.raises(ValueError, match="optional adapter"):
        probe.probe_wfdb()


@pytest.mark.parametrize("sample", [True, "500"])
def test_every_native_annotation_sample_is_checked(
    monkeypatch: pytest.MonkeyPatch, sample: object
) -> None:
    modules = _fake_wfdb_modules(annotation_changes={"sample": [250, sample]})
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)
    with pytest.raises(ValueError, match="integer field"):
        probe.probe_wfdb()


def test_integer_scalar_subclasses_retain_native_compatibility(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class NativeInteger(int):
        pass

    modules = _fake_wfdb_modules(
        record_changes={"sig_len": NativeInteger(2500), "fs": NativeInteger(250)},
        annotation_changes={"sample": [NativeInteger(250), NativeInteger(500)]},
    )
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)
    assert probe.probe_wfdb()["passed"] is True


@pytest.mark.parametrize("damage", ["missing", "noncallable"])
def test_unavailable_header_reader_cannot_count_as_adversarial_rejection(
    monkeypatch: pytest.MonkeyPatch, damage: str
) -> None:
    modules = _fake_wfdb_modules()
    wfdb = modules["wfdb"]
    if damage == "missing":
        monkeypatch.delattr(wfdb, "rdheader")
    else:
        monkeypatch.setattr(wfdb, "rdheader", None)
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)
    with pytest.raises(ValueError, match="optional adapter"):
        probe.probe_wfdb()


def test_native_index_error_remains_adversarial_header_rejection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def reject_header(_path: str) -> None:
        raise IndexError("invalid synthetic header")

    modules = _fake_wfdb_modules()
    monkeypatch.setattr(modules["wfdb"], "rdheader", reject_header)
    monkeypatch.setattr(probe.importlib, "import_module", modules.__getitem__)
    receipt = probe.probe_wfdb()
    assert receipt["observations"]["adversarial_header_rejected"] is True
    assert receipt["passed"] is True


def test_cli_prints_successful_receipt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(probe, "probe_pydicom", lambda: {"passed": True, "profile": "fake"})
    monkeypatch.setattr(sys, "argv", ["optional_adapter_probe", "pydicom"])

    assert probe.main() == 0
    assert json.loads(capsys.readouterr().out) == {"passed": True, "profile": "fake"}


def test_cli_writes_failed_receipt_and_returns_one(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output = tmp_path / "nested" / "receipt.json"
    monkeypatch.setattr(probe, "probe_wfdb", lambda: {"passed": False, "profile": "fake"})
    monkeypatch.setattr(sys, "argv", ["optional_adapter_probe", "wfdb", "--output", str(output)])

    assert probe.main() == 1
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "passed": False,
        "profile": "fake",
    }
