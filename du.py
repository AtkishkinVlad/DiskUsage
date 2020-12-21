import argparse
import sys

from du_logic import get_dirs, sort_dirs, get_dirs_with_size, convert_bytes

def arguments_parsing():
    # настройка аргрументов командной строки
    parser = argparse.ArgumentParser()

    parser.add_argument('base_path', help='Starting directory path')
    parser.add_argument('-s', '--sort', type=str, choices=['name', 'size', 'fls_count'],
                        default='size',
                        help='Type of sorting: name - lexical, size - by size, '
                             'fls_count - by count of files dirs contain')
    parser.add_argument('-d', '--depth', type=int, default=2,
                        help='Max depth of subdirectories')
    parser.add_argument('--reverse', default=True, action='store_true',
                        help='Reverse sorting')
    parser.add_argument('--ext', default=False, action='store_true',
                        help='Show total file size by extensions')
    parser.add_argument('--noprogress', default=False, action='store_true',
                        help='Not to show processing progress')

    args = parser.parse_args(sys.argv[1:])  # cчитываем аргументы

    return args


if __name__ == '__main__':
    args = arguments_parsing()

    dirs, ext_sizes = get_dirs_with_size(get_dirs(args.base_path, args.depth),
                                         args.noprogress, args.ext)

    dirs_list = sort_dirs(dirs, args.sort, args.reverse)

    for d in dirs_list:
        print(f'{d[0]} ({d[2]} files) {convert_bytes(d[1])}')

    if args.ext:
        print('\nTotal file size by extensions:\n')

        for k, v in ext_sizes.items():
            print(k, ':', convert_bytes(v))
