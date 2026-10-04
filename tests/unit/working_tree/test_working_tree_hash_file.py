from hashlib import sha256

from pyvcs.working_tree import hash_file


def test_hash_file_returns_sha256_for_text_file(tmp_path):
    file_path = tmp_path / "hello.txt"
    file_path.write_text("hello", encoding="utf-8")

    result = hash_file(file_path)

    expected = sha256(b"hello").hexdigest()

    assert result == expected


def test_same_content_produces_same_hash(tmp_path):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("same content", encoding="utf-8")
    second_file.write_text("same content", encoding="utf-8")

    assert hash_file(first_file) == hash_file(second_file)


def test_different_content_produces_different_hash(tmp_path):
    first_file = tmp_path / "first.txt"
    second_file = tmp_path / "second.txt"

    first_file.write_text("first content", encoding="utf-8")
    second_file.write_text("second content", encoding="utf-8")

    assert hash_file(first_file) != hash_file(second_file)


def test_hash_file_supports_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_bytes(b"")

    result = hash_file(file_path)

    expected = sha256(b"").hexdigest()

    assert result == expected


def test_hash_file_supports_binary_file(tmp_path):
    file_path = tmp_path / "image.bin"
    content = b"\x00\x01\xff\xab\x10\x20"

    file_path.write_bytes(content)

    result = hash_file(file_path)

    expected = sha256(content).hexdigest()

    assert result == expected


def test_hash_file_supports_large_file(tmp_path):
    file_path = tmp_path / "large.bin"
    content = b"a" * (64 * 1024 + 100)

    file_path.write_bytes(content)

    result = hash_file(file_path)

    expected = sha256(content).hexdigest()

    assert result == expected
