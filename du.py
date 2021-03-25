import argparse
from diskusage import sort_dirs, convert_bytes, traversal

def arguments_parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('base_path', type=str, help='Starting directory path')
    parser.add_argument('-s', '--sort', type=str, choices=['name', 'size', 'depth', 'none', 'modify'], default='none',
                        help='Type of sorting: name - lexical, size - by size')
    parser.add_argument('-d', '--depth', type=int, default=2, help='Max depth of subdirectories')
    parser.add_argument('--reverse', default=False, action='store_true', help='Reverse sorting')
    parser.add_argument('--ext', default=False, action='store_true', help='Show total file size by extensions')
    parser.add_argument('--noprogress', default=False, action='store_true', help='Not to show processing progress')
    parser.add_argument('--top', default=-1, type=int, help='Select [VALUE] files from top of list')
    parser.add_argument('--block', default=100, type=int, help='Get files that consume [VALUE] percents of used space')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = arguments_parsing()
    result, maxlen = traversal(args.base_path, args.depth)
    if args.top == -1:
        border = len(result)
    else:
        border = min(len(result), args.top)

    if args.block != 100:
        result = sort_dirs(result, 'size', False)
        totalSize = 0
        for i in result:
            if i.isDir:
                continue
            totalSize += i.size
        remainingAmount = (totalSize * args.block) // 100
        qwe = remainingAmount
        output = []
        for i in result:
            if i.isDir:
                continue
            output.append(i)
            remainingAmount -= i.size
            if remainingAmount <= 0:
                break
        for i in output:
            print(i.name, ' ' * (maxlen - len(i.name)), '\t', convert_bytes(i.size), '\t', str(i.time).split('.')[0])
        print('remaining files:', ' ' * (maxlen - len('remaining files:')), '\t', convert_bytes(totalSize - qwe + remainingAmount))
    elif args.sort != 'none':
        result = sort_dirs(result, args.sort, args.reverse)
        for i in result[:border]:
            name = i.name
            if i.isDir:
                name = f'\033[96m{name}\033[0m'
            print(name, ' ' * (maxlen - len(i.name + i.indent)), '\t', convert_bytes(i.size), '\t', str(i.time).split('.')[0])
    else:
        for i in result:
            name = i.name
            if i.isDir:
                name = f'\033[96m{name}\033[0m'
            print(i.indent, name, ' ' * (maxlen - len(i.name + i.indent)), convert_bytes(i.size), '\t', str(i.time).split('.')[0])