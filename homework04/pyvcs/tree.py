import pathlib
import time
import typing as tp

from pyvcs.index import GitIndexEntry
from pyvcs.objects import hash_object


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    tree = dict()
    current = bytes()

    for i in index:
        if i.name.find(dirname) == 0 and dirname != "":
            n = i.name[len(dirname) + 1 :].split("/")
        else:
            n = i.name.split("/")
        if n[0] == dirname:
            n = n[1:]
        if len(n) == 1:
            current += ("100644 " + "/".join(n)).encode() + b"\x00" + i.sha1
        else:
            if n[0] not in tree.keys():
                tree[n[0]] = []
            tree[n[0]].append(i)
    for i in list(tree.keys())[::-1]:
        l = tree[i]
        res = write_tree(gitdir, l, dirname + "/" + i if dirname != "" else i)
        current = ("40000 " + i).encode() + b"\x00" + bytes.fromhex(res) + current

    return hash_object(current, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    timestamp = int(time.mktime(time.localtime()))
    offset = -time.timezone
    hours = abs(offset) // 3600
    author_time = str(timestamp) + " {}{:02}{:02}".format(
        "+" if offset > 0 else "-",
        hours,
        (hours * 60) % 60,
    )
    content = f"tree {tree}\n"
    if parent:
        content += f"parent {parent}\n"
    content += f"author {author} {author_time}\n"
    content += f"committer {author} {author_time}\n\n{message}\n"
    sha = hash_object(content.encode(), "commit", True)
    return sha
