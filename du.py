import argparse
import glob
import os
from operator import itemgetter


def convert_bytes(num):
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    for unit in units:
        if num < 1024.0:
            return f'{num:3.1f} {unit}'
        num /= 1024.0


# получить размер папки path
def get_dir_size(path):
    total_size = os.path.getsize(path)  # начальный размер папки
    for f in os.listdir(path):  # просмотр всех элементов папки
        f_path = os.path.join(path, f)
        if os.path.isfile(f_path):  # если это файл
            total_size += os.path.getsize(f_path)  # суммируем размер
        elif os.path.isdir(f_path):  # если это папка
            total_size += get_dir_size(f_path)  # вызываем подсчет объема подпапки
    return total_size


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


# получить список директорий с их размером
def get_dirs_with_size(dirs):
    data = []
    for d in dirs:
        data.append([d, get_dir_size(d)])  # для каждой папки вычисляем размер
    return data


def sort_by_size(dirs):
    return sorted(dirs, key=itemgetter(1), reverse=True)  # сортируем по второму параметру - размеру


def sort_lexical(dirs):
    return sorted(dirs, key=itemgetter(0))  # сортируем по названию


# настройка аргрументов командной строки
parser = argparse.ArgumentParser()
parser.add_argument('base_path', action='store', type=str, help='Starting directory path')
parser.add_argument('-sort', type=str, default='s', help='Type of sorting: l - lexical, s - by size')
parser.add_argument('-depth', type=int, default=2, help='Max depth of subdirectories')
args = parser.parse_args()  # cчитываем аргументы

path = args.base_path  # получаем из аргументов путь
sort_type = args.sort  # тип сортировки
d = args.depth  # уровень вложенноести

dirs = get_dirs(path, d)

if (sort_type == 's'):
    dirs_list = sort_by_size(get_dirs_with_size(dirs))
else:
    dirs_list = sort_lexical(get_dirs_with_size(dirs))

for d in dirs_list:
    print(d[0], convert_bytes(d[1]))
