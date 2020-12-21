import glob
import os
from operator import itemgetter

from progress.bar import Bar


def convert_bytes(num):
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
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
                # noinspection PyBroadException
                try:
                    total_size += os.path.getsize(file_path)
                except Exception:
                    total_size += 0

    return total_size


def get_files_count(path):
    total_files = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                total_files += 1

    return total_files


# является ли строка расширением файла
def valid_ext(ext):
    for c in ext:
        if not (c.isalpha() or c.isdigit()):
            return False

    return True


# заполнить словарь ext_sizes с парами "расширение" : объем для текущей директории
def get_ext_sizes(path, ext_sizes):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                # noinspection PyBroadException
                try:
                    ext = file_path.rsplit('.', 1)[1]  # получаем расширение
                    if valid_ext(ext):
                        if ext in ext_sizes:  # если расширение уже добавлено в словарь
                            ext_sizes[ext] += os.path.getsize(file_path)  # прибавляем размер
                        else:
                            ext_sizes[ext] = os.path.getsize(file_path)  # иначе добавляем первый
                except Exception:
                    pass

    return ext_sizes


# получить список папок директории path
def get_dirs(path, max_depth):
    dirs = []

    for d in range(1, max_depth + 1):  # для всех уровней заданной глубины
        depth = "/".join("*" * d)  # список шагов по папкам /*/*/...
        search_path = os.path.join(path, depth)  # путь, по которому ищем папки - path + шаги по папкам
        for f in glob.glob(search_path):  # просматриваем текущий каталог
            if os.path.isdir(f):  # учитываем папки
                dirs.append(f)

    return dirs


# получить список директорий с их размером и количеством файлов, а также словарь {'расширение1' : размер1, 'расширение2' : размер2}
# noprogress - отсутствие прогресс бара
# ext - создаем ли словарь с размерами файлов по расширению
def get_dirs_with_size(dirs, no_progress, ext):
    data = []
    ext_sizes = {}  # пустой словарь расширений

    if not no_progress:  # с прогресс баром
        with Bar('Getting files info...') as bar:
            for d in dirs:
                data.append([d, get_size(d), get_files_count(
                    d)])  # для каждой папки вычисляем размер (здесь же заполняем словарь с расширениями) и количество файлов
                if ext:
                    get_ext_sizes(d, ext_sizes)
                bar.next()
    else:
        for d in dirs:
            data.append([d, get_size(d), get_files_count(d)])  # для каждой папки вычисляем размер и количество файлов
            if ext:
                get_ext_sizes(d, ext_sizes)

    return data, ext_sizes


def sort_dirs(dirs, sort_type, reverse):
    if sort_type == 'name':
        return sorted(dirs, key=itemgetter(0), reverse=reverse)  # сортируем по второму параметру - размеру
    elif sort_type == 'size':
        return sorted(dirs, key=itemgetter(1), reverse=reverse)  # сортируем по названию
    elif sort_type == 'fls_count':
        return sorted(dirs, key=itemgetter(2), reverse=reverse)
