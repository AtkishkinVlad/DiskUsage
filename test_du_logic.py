from pyfakefs.fake_filesystem_unittest import TestCase
from diskusage import get_dirs, get_files_count, get_ext_sizes, \
    get_size, valid_ext, get_dirs_with_size, convert_bytes, \
    sort_dirs, traversal


class ExampleTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_convert_bytes_kb(self):
        self.assertEqual(convert_bytes(156023), '152.4 KB')

    def test_convert_bytes_b(self):
        self.assertEqual(convert_bytes(562), '562.0 Bytes')

    def test_convert_bytes_mb(self):
        self.assertEqual(convert_bytes(19441222), '18.5 MB')

    def test_convert_bytes_tb(self):
        self.assertEqual(convert_bytes(194412221222221), '176.8 TB')

    def test_convert_bytes_gb(self):
        self.assertEqual(convert_bytes(19441222122), '18.1 GB')

    def test_get_dirs(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path4 = '/foo/bar/another'
        path5 = '/foo/bar/another/hero'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_dir(path5)

        self.assertEqual(get_dirs('/foo/bar', 3), ['\\foo\\bar\\test', '\\foo\\bar\\another', '\\foo\\bar\\another\\hero'])

    def test_get_files_count(self):
        f = '/foo/bar/text.txt'
        s = '/foo/bar/test.txt'
        t = '/foo/bar/finder.txt'
        d = '/foo/bar/folder.txt'

        self.fs.create_file(f)
        self.fs.create_file(s)
        self.fs.create_file(t)
        self.fs.create_file(d)

        self.assertEqual(get_files_count('/foo/bar'), 4)

    def test_valid_ext_true(self):
        z = 'txt'
        self.assertEqual(valid_ext(z), True)

    def test_valid_ext_false(self):
        z = 'tx12#//12b'
        self.assertEqual(valid_ext(z), False)

    def test_get_ext_sizes(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')

        self.assertEqual(get_ext_sizes('/foo/bar', {}), {'txt': 5})

    def test_traversal(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another/man.docx'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')

        self.assertEqual(traversal(path1, 5), ([('\x1b[96m bar \x1b[0m', '5.0 Bytes'), ('\x1b[96m |--test \x1b[0m', '5.0 Bytes'), ('|  |--text.txt', '5.0 Bytes'), ('\x1b[96m |--another \x1b[0m', '0.0 Bytes'), ('\x1b[96m |  |--man.docx \x1b[0m', '0.0 Bytes')], 14))

    def test_get_ext_sizes_2(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path5 = '/foo/bar/test/flip.pdf'
        path4 = '/foo/bar/another'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')
        self.fs.create_file(path5, contents='brbr')

        self.assertEqual(get_ext_sizes('/foo/bar', {}), {'pdf': 4, 'txt': 5})

    def test_create_file(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')

        self.assertEqual(get_size(path1), 5)

    def test_get_dirs_with_size(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')

        self.assertEqual(get_dirs_with_size([path1, path2, path4], False, False),
                         ([['/foo/bar', 5, 1], ['/foo/bar/test', 5, 1], ['/foo/bar/another', 0, 0]], {}))

    def test_get_dirs_with_size_2(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')

        self.assertEqual(get_dirs_with_size([path1, path2, path4], False, True),
                         ([['/foo/bar', 5, 1], ['/foo/bar/test', 5, 1], ['/foo/bar/another', 0, 0]], {'txt': 10}))

    def test_get_dirs_with_size_3(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')

        self.assertEqual(get_dirs_with_size([path1, path2, path4], True, True),
                         ([['/foo/bar', 5, 1], ['/foo/bar/test', 5, 1], ['/foo/bar/another', 0, 0]], {'txt': 10}))

    def test_sort_dirs(self):
        path1 = '/foo/bar'
        path2 = '/foo/bar/test'
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another'
        path5 = '/foo/bar/another/t.txt'
        path6 = '/foo/bar/another/b.txt'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='tests')
        self.fs.create_file(path5, contents='tests')
        self.fs.create_file(path6, contents='tests')

        self.assertEqual(sort_dirs([path1, path2, path3, path4], 'name', True),
                         ['/foo/bar', '/foo/bar/test', '/foo/bar/test/text.txt', '/foo/bar/another'])

        self.assertEqual(sort_dirs([path1, path2, path3, path4, path5, path6], 'size', True),
                         ['/foo/bar',
                          '/foo/bar/test',
                          '/foo/bar/test/text.txt',
                          '/foo/bar/another',
                          '/foo/bar/another/t.txt',
                          '/foo/bar/another/b.txt']
                         )

        self.assertEqual(sort_dirs([path1, path2, path3, path4], 'imya', True),
                         None)

        self.assertEqual(sort_dirs([path1, path2, path3, path4, path5, path6], 'fls_count', True),
                         ['/foo/bar',
                          '/foo/bar/test',
                          '/foo/bar/test/text.txt',
                          '/foo/bar/another',
                          '/foo/bar/another/t.txt',
                          '/foo/bar/another/b.txt']
                         )
