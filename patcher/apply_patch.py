from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import os
import shutil
import struct
import sys
from pathlib import Path


OVERWRITE_HEADER = struct.Struct("<4sQ")
OVERWRITE_RECORD = struct.Struct("<QQ")
OVERWRITE_MAGIC = b"YWO1"
CHUNK_SIZE = 16 * 1024 * 1024


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def copy_exact(source_handle, output_handle, length: int) -> None:
    remaining = length
    while remaining:
        block = source_handle.read(min(CHUNK_SIZE, remaining))
        if not block:
            raise IOError("원본 아카이브를 읽는 중 파일이 예상보다 일찍 끝났습니다.")
        output_handle.write(block)
        remaining -= len(block)


def decompress_to_output(path: Path, output_handle) -> None:
    with lzma.open(path, "rb") as input_handle:
        shutil.copyfileobj(input_handle, output_handle, length=CHUNK_SIZE)


def verify_payload(package: Path, manifest: dict) -> None:
    for name, expected in manifest["payload"].items():
        path = package / "payload" / name
        if not path.is_file():
            raise FileNotFoundError(f"패치 데이터가 없습니다: {path}")
        if path.stat().st_size != expected["size"] or sha256(path) != expected["sha256"]:
            raise ValueError(f"패치 데이터가 손상됐습니다: {name}")


def apply_patch(package: Path, source: Path, output: Path) -> None:
    manifest = json.loads((package / "patch_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("format") != "YW3S_ARC0_ALIGNED_PATCH" or manifest.get("format_version") != 1:
        raise ValueError("지원하지 않는 패치 형식입니다.")
    source_expected = manifest["source"]
    output_expected = manifest["output"]
    if source.resolve() == output.resolve():
        raise ValueError("원본과 출력 경로는 달라야 합니다. 원본 파일은 덮어쓰지 않습니다.")
    if not source.is_file():
        raise FileNotFoundError(f"원본 yw_a.fa가 없습니다: {source}")
    if source.stat().st_size != source_expected["size"]:
        raise ValueError("원본 크기가 지원 버전과 다릅니다.")
    print("원본 SHA-256 확인 중...", flush=True)
    source_hash = sha256(source)
    if source_hash != source_expected["sha256"]:
        raise ValueError(f"지원하지 않는 원본입니다: {source_hash}")
    verify_payload(package, manifest)

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".building")
    temporary.unlink(missing_ok=True)
    source_data_offset = int(source_expected["data_offset"])
    target_data_offset = int(output_expected["data_offset"])
    reused = int(manifest["layout"]["reused_source_data_bytes"])
    try:
        with source.open("rb") as source_handle, temporary.open("w+b") as output_handle:
            print("패치 헤더 적용 중...", flush=True)
            decompress_to_output(package / "payload" / "prefix.bin.xz", output_handle)
            if output_handle.tell() != target_data_offset:
                raise ValueError("패치 헤더 크기가 매니페스트와 다릅니다.")
            print("원본 데이터 복사 중...", flush=True)
            source_handle.seek(source_data_offset)
            copy_exact(source_handle, output_handle, reused)
            print("변경 바이트 적용 중...", flush=True)
            with lzma.open(package / "payload" / "overwrites.bin.xz", "rb") as overwrite_handle:
                header = overwrite_handle.read(OVERWRITE_HEADER.size)
                magic, record_count = OVERWRITE_HEADER.unpack(header)
                if magic != OVERWRITE_MAGIC:
                    raise ValueError("변경 데이터 헤더가 손상됐습니다.")
                for _ in range(record_count):
                    record = overwrite_handle.read(OVERWRITE_RECORD.size)
                    if len(record) != OVERWRITE_RECORD.size:
                        raise ValueError("변경 데이터 레코드가 잘렸습니다.")
                    relative_offset, length = OVERWRITE_RECORD.unpack(record)
                    data = overwrite_handle.read(length)
                    if len(data) != length:
                        raise ValueError("변경 데이터 본문이 잘렸습니다.")
                    output_handle.seek(target_data_offset + relative_offset)
                    output_handle.write(data)
            output_handle.seek(target_data_offset + reused)
            print("추가 패치 데이터 적용 중...", flush=True)
            decompress_to_output(package / "payload" / "tail.bin.xz", output_handle)
            output_handle.truncate()
        if temporary.stat().st_size != output_expected["size"]:
            raise ValueError("패치 결과 크기가 예상과 다릅니다.")
        print("결과 SHA-256 확인 중...", flush=True)
        output_hash = sha256(temporary)
        if output_hash != output_expected["sha256"]:
            raise ValueError(f"패치 결과 검증 실패: {output_hash}")
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise
    print(f"완료: {output}")
    print(f"SHA-256: {output_expected['sha256']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="요괴워치 3 스키야키 한국어 패치 적용기")
    parser.add_argument("source", nargs="?", type=Path, help="지원 원본에서 추출한 yw_a.fa")
    parser.add_argument("output", nargs="?", type=Path, help="생성할 한국어 패치 yw_a.fa")
    parser.add_argument("--no-pause", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        source = args.source
        if source is None:
            source = Path(input("원본 yw_a.fa 경로를 입력하세요: ").strip().strip('"'))
        output = args.output or source.with_name("yw_a.ko.fa")
        apply_patch(Path(__file__).resolve().parent, source.expanduser().resolve(), output.expanduser().resolve())
        return 0
    except Exception as exc:
        print(f"오류: {exc}", file=sys.stderr)
        return 1
    finally:
        if not args.no_pause and sys.stdin.isatty():
            input("Enter 키를 누르면 종료합니다...")


if __name__ == "__main__":
    raise SystemExit(main())
