import hashlib
import os
import pathlib
import typing as tp
import zlib


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    root = ".git"

    header = f"{fmt} {len(data)}\0".encode()
    data = header + data
    # data = (fmt + " " + str(len(data))).encode() + data
    hash = hashlib.sha1(data).hexdigest()

    if not write:
        return hash

    path = root + "/objects/" + hash[:2]
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + os.sep + hash[2:], "wb") as f:
        f.write(zlib.compress(data))

    return hash


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    objects = []
    if len(obj_name) > 40 or len(obj_name) < 4:
        raise Exception(f"Not a valid object name {obj_name}")

    path = gitdir / "objects" / obj_name[:2]

    paths = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        paths.extend(filenames)
        break

    for p in paths:
        if p.find(obj_name[2:]) == 0:
            objects.append(obj_name[:2] + p)

    if not objects:
        raise Exception(f"Not a valid object name {obj_name}")

    return objects


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    if obj_name[2:] in gitdir.parts[-1]:
        return str(gitdir.parts[-2] + str(gitdir.parts[-1]))
    else:
        return None


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    path = gitdir / "objects" / sha[:2] / sha[2:]
    with open(path, mode="rb") as f:
        obj_data = zlib.decompress(f.read())
    header = obj_data[:obj_data.find(b"\x00")]
    fmt = header[:header.find(b" ")]
    fmt = fmt.decode("ascii")
    content = obj_data[len(header) + 1:]
    return (fmt, content)


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    while len(data) != 0:
        mi = data.find(b" ")
        mode = int(data[: mi].decode())
        data = data[mi + 1:]
        zi = data.find(b"\x00")
        name = data[: zi].decode()
        data = data[zi + 1:]
        sha = bytes.hex(data[:20])
        data = data[20:]
        res = (mode, name, sha)
        result.append(res)
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    gitdir = pathlib.Path(".git")

    for obj in resolve_object(obj_name, gitdir):
        header, content = read_object(obj, gitdir)
        if header == "tree":
            result = ""
            tree_files = read_tree(content)
            for f in tree_files:
                object_type = read_object(f[2], pathlib.Path(".git"))[0]
                result += str(f[0]).zfill(6) + " "
                result += object_type + " "
                result += f[2] + "\t"
                result += f[1] + "\n"
            print(result, flush=True)
        else:
            print(content.decode(), flush=True)


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    result = []
    header, data = read_object(tree_sha, gitdir)
    for f in read_tree(data):
        if read_object(f[2], gitdir)[0] == "tree":
            tree = find_tree_files(f[2], gitdir)
            for blob in tree:
                name = f[1] + "/" + blob[0]
                result.append((name, blob[1]))
        else:
            result.append((f[1], f[2]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = zlib.decompress(raw)
    i = data.find(b"tree")
    return data[i + 5: i + 45]
