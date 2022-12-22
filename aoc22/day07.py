import re
import sys
from typing import Generator, Optional


class File:
    def __init__(self, name: str, is_dir: bool, size: int = 0):
        self.name = name
        self.is_dir = is_dir
        self.size = size
        self.parent: Optional[File] = None
        self.children: list[File] = []

    def __str__(self):
        if self.is_dir:
            return f"- {self.name} (dir)"
        else:
            return f"- {self.name} (file, size={self.size})"

    def __iter__(self):
        return iter(self.children)

    def walk(self):
        def _recursive_filetree(
            node: File, depth: int = 0
        ) -> Generator[tuple[int, File], None, None]:
            yield depth, node
            for child in node.children:
                yield from _recursive_filetree(child, depth + 1)

        return _recursive_filetree(self)

    def append(self, other: "File"):
        if not self.is_dir:
            raise ValueError("files can only be appended to a directory")
        other.parent = self
        self.children.append(other)
        return self


def print_filetree(root: File):
    print("\n".join(d * "  " + str(f) for d, f in root.walk()))


_cd_pat = re.compile(r"^\$ cd (.+)")
_ls_pat = re.compile(r"^\$ ls")
_dir_pat = re.compile(r"^dir (.+)")
_file_pat = re.compile(r"^(\d+) (.+)")


def _explore_filesystem():
    next(sys.stdin)  # skip the first line

    root = File("/", is_dir=True)
    file = root
    for line in sys.stdin:
        if _ls_pat.match(line):
            for line in sys.stdin:
                if line.startswith("$"):
                    break
                elif mo := _dir_pat.match(line):
                    file.append(File(mo.group(1), True))
                elif mo := _file_pat.match(line):
                    file.append(File(mo.group(2), False, int(mo.group(1))))

        if mo := _cd_pat.match(line):
            dir_name = mo.group(1)
            if dir_name == "..":
                if file.parent is None:
                    raise ValueError("cannot cd above root")
                file = file.parent
            else:
                for child in file.children:
                    if dir_name == child.name:
                        if child.is_dir:
                            file = child
                            break
                        else:
                            raise ValueError("cannot cd into a non-directory")
                else:
                    raise ValueError("directory does not exist")

    return root


def _dirs_and_sizes(root: File):
    return ((d, sum(f.size for _, f in d.walk())) for _, d in root.walk() if d.is_dir)


def part_a(root: File):
    return sum(s for _, s in _dirs_and_sizes(root) if s <= 100000)


def part_b(root: File):
    total_size = sum(f.size for _, f in root.walk())
    dirs = list(_dirs_and_sizes(root))
    for _, size in sorted(dirs, key=lambda t: t[1]):
        if (70000000 - total_size) + size > 30000000:
            break
    else:
        raise ValueError("could not find a sufficient dir")
    return size


if __name__ == "__main__":
    root = _explore_filesystem()
    print_filetree(root)
    print(part_a(root))
    print(part_b(root))
