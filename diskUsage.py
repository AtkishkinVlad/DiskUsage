from glob import glob
from os import walk, path, sep, stat, listdir
from tqdm import tqdm
from fileData import FileData
from datetime import datetime, timezone, timedelta


def convert_bytes(num: float):
    units = ('B', 'KB', 'MB', 'GB', 'TB')

    for unit in units:
        if num < 1024.0:
            return f'{num:3.1f} {unit}'

        num /= 1024.0


def get_size(file_path) -> int:
    total_size: int = 0

    for root, dirs, files in walk(file_path):
        for file in files:
            file_path = path.join(root, file)

            if not path.islink(file_path):
                try:
                    total_size += path.getsize(file_path)
                except FileNotFoundError:
                    total_size += 0

    return total_size


def get_all_directories(file_path, max_depth):
    dirs = []

    for i in range(1, max_depth + 1):
        search_path = path.join(file_path, "/".join("*" * i))

        for f in glob(search_path):
            if path.isdir(f):
                dirs.append(f)

    return dirs


def traversal(file_path, depth=-1):
    result = []
    max_len = 0
    prefix = 0

    if file_path != '/':
        if file_path.endswith('/'):
            file_path = file_path[:-1]

        prefix = len(file_path)

    for root, dirs, files in walk(file_path):
        level = root[prefix:].count(sep)

        if -1 < depth < level:
            continue

        indent = ''

        if level > 0:
            indent = ' |   ' * (level - 1) + ' |---'

        sub_indent = ' |   ' * level + ' |---'
        time = datetime.fromtimestamp(stat(root).st_mtime,
                                      tz=timezone(offset=timedelta(hours=5)))

        file_data = FileData(path.basename(root), get_size(root),
                             level, indent, True, time)

        if len(file_data.name) + len(file_data.indent) + 1 > max_len:
            max_len = len(file_data.name) + len(file_data.indent) + 1

        result.append(file_data)
        for_sort = []

        for f in listdir(root):
            f_path = path.join(root, f)

            if path.isfile(f_path):
                for_sort.append(((path.basename(f)),
                                 path.getsize(f_path)))

        for_sort.sort(key=lambda a: a[1])

        for file in tqdm(for_sort, colour='green'):
            time = datetime.fromtimestamp(stat(root).st_mtime,
                                          tz=timezone(offset=timedelta(hours=5)))

            file_data = FileData(file[0], file[1], level, sub_indent, False, time)

            if len(file_data.name) + len(file_data.indent) + 1 > max_len:
                max_len = len(file_data.name) + len(file_data.indent) + 1

            result.append(file_data)

    return result, max_len


def sort_dirs(file_list, sort_type, reverse):
    if sort_type == 'name':
        return sorted(file_list, key=lambda i: i.name.lower(), reverse=reverse)

    elif sort_type == 'size':
        return sorted(file_list, key=lambda i: i.size, reverse=not reverse)

    elif sort_type == 'depth':
        return sorted(file_list, key=lambda i: i.depth, reverse=reverse)

    elif sort_type == 'modify':
        return sorted(file_list, key=lambda i: i.time, reverse=reverse)
