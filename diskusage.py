import glob
import os
from my_progress_bar import ProgressBar
from fileData import FileData
from datetime import datetime, timezone, timedelta


def convert_bytes(num):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if num < 1024.0:
            return f'{num:3.1f} {unit}'
        num /= 1024.0


def get_size(path):
    total_size = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.islink(file_path):
                try:
                    total_size += os.path.getsize(file_path)
                except Exception:
                    total_size += 0
    return total_size


def get_all_directories(path, max_depth):
    dirs = []
    for d in range(1, max_depth + 1):
        search_path = os.path.join(path, "/".join("*" * d))
        for f in glob.glob(search_path):
            if os.path.isdir(f):
                dirs.append(f)
    return dirs


def traversal(path, depth = -1):
    bar = ProgressBar(len(get_all_directories(path, depth)))
    result = []
    maxlen = 0
    prefix = 0
    if path != '/':
        if path.endswith('/'):
            path = path[:-1]
        prefix = len(path)

    for root, dirs, files in os.walk(path):
        level = root[prefix:].count(os.sep)
        if -1 < depth < level:
            continue
        indent = ''
        if level > 0:
            indent = ' |   ' * (level - 1) + ' |---'
        sub_indent = ' |   ' * level + ' |---'
        taem = datetime.fromtimestamp(os.stat(root).st_mtime, tz=timezone(offset=timedelta(hours=5)))
        fileData = FileData(os.path.basename(root), get_size(root), level, indent, True, taem)
        if len(fileData.name) + len(fileData.indent) + 1 > maxlen:
            maxlen = len(fileData.name) + len(fileData.indent) + 1
        result.append(fileData)
        for_sort = []
        for f in os.listdir(root):
            f_path = os.path.join(root, f)
            if os.path.isfile(f_path):
                for_sort.append(((os.path.basename(f)), os.path.getsize(f_path)))
        for_sort.sort(key=lambda a: a[1])
        for file in for_sort:
            taem = datetime.fromtimestamp(os.stat(root).st_mtime, tz=timezone(offset=timedelta(hours=5)))

            fileData = FileData(file[0], file[1], level, sub_indent, False, taem)
            if len(fileData.name) + len(fileData.indent) + 1 > maxlen:
                maxlen = len(fileData.name) + len(fileData.indent) + 1
            result.append(fileData)
        bar.nextState()
    bar.finish()
    return result, maxlen


def sort_dirs(fileList, sort_type, reverse):
    if (sort_type == 'name'):
        return sorted(fileList, key=lambda i: i.name.lower(), reverse=reverse)
    elif (sort_type == 'size'):
        return sorted(fileList, key=lambda i: i.size, reverse=not reverse)
    elif (sort_type == 'depth'):
        return sorted(fileList, key=lambda i: i.depth, reverse=reverse)
    elif (sort_type == 'modify'):
        return sorted(fileList, key=lambda i: i.time, reverse=reverse)
