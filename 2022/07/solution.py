from __future__ import annotations
from dataclasses import dataclass
from typing import Callable


@dataclass
class Directory:
    name: str
    children: dict[str, File | Directory]
    parent: Directory | None

    @property
    def size(self) -> int:
        return sum([c.size for c in self.children.values()])


@dataclass
class File:
    name: str
    size: int
    parent: Directory


@dataclass
class FileSystem:
    root: Directory


def process_cd_command(dst: str, cwd: Directory, root: Directory) -> Directory:
    return root if dst == "/" else cwd.parent if dst == ".." else cwd.children[dst]


def consume_ls_output(lines: list[str], index: int, cwd: Directory) -> int:
    lines_processed = 0
    while index + lines_processed < len(lines):
        l = lines[index + lines_processed]
        if l.startswith("$"):
            break
        elif l.startswith("dir"):
            dir_name = l.split()[1]
            cwd.children[dir_name] = Directory(name=dir_name, children={}, parent=cwd)
        else:
            file_size, file_name = l.split()
            cwd.children[file_name] = File(name=file_name, size=int(file_size), parent=cwd)
        lines_processed += 1

    return lines_processed


def process_command(lines: list[str], index: int, cwd: Directory, root: Directory) -> tuple[Directory, int]:
    cmd = lines[index].strip().split()
    lines_processed = 1
    return (
        (process_cd_command(cmd[2], cwd, root), lines_processed)
        if cmd[1] == "cd"
        else (cwd, lines_processed + consume_ls_output(lines, index + 1, cwd))
    )


def walk_fs(root: Directory, visit: Callable):
    visit(root)
    for c in root.children.values():
        if isinstance(c, File):
            visit(c)
        else:
            walk_fs(c, visit)


def filter_fs_items(root: Directory, predicate: Callable[[Directory | File], bool]) -> list[Directory | File]:
    items = []

    def visit(item: Directory | File):
        if predicate(item):
            items.append(item)

    walk_fs(root, visit)
    return items


### Process the input
log = open("2022/07/input.txt").readlines()
root = Directory(name="/", children={}, parent=None)
cur_dir = root
cur_line = 0
while cur_line < len(log):
    cur_dir, lines_processed = process_command(log, cur_line, cur_dir, root)
    cur_line += lines_processed


## Part 1
small_dirs = filter_fs_items(root, lambda i: isinstance(i, Directory) and i.size <= 100000)
print(sum(map(lambda d: d.size, small_dirs)))

## Part 2
used_disk_space = root.size
free_disk_space = 70000000 - used_disk_space
need_to_free = 30000000 - free_disk_space
large_enough_dirs = filter_fs_items(root, lambda i: isinstance(i, Directory) and i.size >= need_to_free)
print(min(map(lambda d: d.size, large_enough_dirs)))
