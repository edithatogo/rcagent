#!/usr/bin/env python3
"""Download publisher-original Sax/Schultz reviews with provenance and integrity checks.

Run outside source control; third-party source files are NOT covered by this repo's
Apache-2.0 licence. Failed downloads are not reported as completed.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

MAX_BYTES = 25 * 1024 * 1024
DOCX_MIME = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
SOURCES = (
    (
        "Sax_Institute_Evidence_Check_2022.pdf",
        "https://www.saxinstitute.org.au/wp-content/uploads/Patient-characteristics-and-interventions-associated-with-complaints-and-medico-legal-claims.pdf",
        "Sax Institute / Avant Insurance Limited; preserve original publisher rights notice",
    ),
    (
        "Schultz_et_al_Systematic_Reviews_2024.pdf",
        "https://link.springer.com/content/pdf/10.1186/s13643-024-02501-8.pdf",
        "Schultz et al. (2024), CC BY 4.0, subject to third-party credits",
    ),
    (
        "Schultz_et_al_2024_Additional_file_1_Tables_S1-S7.docx",
        "https://static-content.springer.com/esm/art%3A10.1186%2Fs13643-024-02501-8/MediaObjects/13643_2024_2501_MOESM1_ESM.docx",
        "Schultz et al. (2024) supplement, CC BY 4.0, subject to third-party credits",
    ),
)


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_file(name: str, content: bytes) -> str:
    if name.endswith(".pdf"):
        if not content.startswith(b"%PDF-") or b"%%EOF" not in content[-2048:]:
            raise ValueError("Not a complete PDF (possibly an HTML error page)")
        return "application/pdf"
    if name.endswith(".docx"):
        if not zipfile.is_zipfile(io.BytesIO(content)):
            raise ValueError("Not a valid DOCX ZIP package")
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            if not {"[Content_Types].xml", "word/document.xml"}.issubset(archive.namelist()):
                raise ValueError("DOCX missing required OOXML components")
        return DOCX_MIME
    raise ValueError(f"Unexpected source file extension: {name}")


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; scientific-research-source-archive/1.0)",
            "Accept": "application/pdf,application/octet-stream,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"Source exceeds {MAX_BYTES} byte limit")
    return data


def acquire(destination: Path) -> list[dict[str, object]]:
    destination.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, object]] = []
    for name, url, rights in SOURCES:
        record: dict[str, object] = {"filename": name, "source_url": url, "rights": rights}
        error: Exception | None = None
        for attempt in range(3):
            try:
                data = fetch_bytes(url)
                mime = validate_file(name, data)
                (destination / name).write_bytes(data)
                record.update({
                    "status": "downloaded",
                    "mime_type": mime,
                    "size_bytes": len(data),
                    "sha256": sha256_hex(data),
                    "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                })
                error = None
                break
            except (OSError, ValueError, urllib.error.URLError, zipfile.BadZipFile) as err:
                error = err
                if attempt < 2:
                    time.sleep(2 * (attempt + 1))
        if error is not None:
            record.update({"status": "failed", "error": str(error)})
        records.append(record)
    (destination / "source_manifest.json").write_text(
        json.dumps({"sources": records}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (destination / "RIGHTS.txt").write_text(
        "Original third-party publisher documents, unchanged.\n"
        "Sax Evidence Check © Avant Insurance Limited: respect the rights notice "
        "in the publisher PDF; NOT under the repository Apache-2.0 licence.\n"
        "Schultz et al., Systematic Reviews 2024, DOI:10.1186/s13643-024-02501-8: "
        "CC BY 4.0 https://creativecommons.org/licenses/by/4.0/ "
        "(subject to third-party credits).\n"
        "Source URLs, retrieval timestamps, byte lengths and SHA-256 in source_manifest.json.\n",
        encoding="utf-8",
    )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    records = acquire(args.output_dir)
    for record in records:
        print(f"{record['status']}: {record['filename']}: "
              f"{record.get('sha256', record.get('error', ''))}")
    return 1 if any(r["status"] != "downloaded" for r in records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
