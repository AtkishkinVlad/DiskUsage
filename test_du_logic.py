from pyfakefs.fake_filesystem_unittest import TestCase
from du_logic import get_dirs, get_files_count, get_ext_sizes, get_size, valid_ext, sort_dirs, convert_bytes, \
    get_dirs_with_size
from du import arguments_parsing


class ExampleTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.parser = arguments_parsing()

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
        path3 = '/foo/bar/test/text.txt'
        path4 = '/foo/bar/another'

        self.fs.create_dir(path1)
        self.fs.create_dir(path2)
        self.fs.create_dir(path4)
        self.fs.create_file(path3, contents='test')

        self.assertEqual(get_dirs('/foo/bar', 3), ['\\foo\\bar\\test', '\\foo\\bar\\another'])

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
        _dir = '/foo/bar'
        f = '/foo/bar/text.txt'
        s = '/foo/bar/test.md'
        t = '/foo/bar/finder.cs'
        d = '/foo/bar/folder.dll'

        self.fs.create_dir(_dir)
        self.fs.create_file(f)
        self.fs.create_file(s)
        self.fs.create_file(t)
        self.fs.create_file(d)

        self.assertEqual(get_ext_sizes('/foo/bar', {}), {'md': 0, 'txt': 0, 'cs': 0, 'dll': 0})

    def test_get_size(self):
        f = 'text.txt'

        self.fs.create_file(f)

        self.assertEqual(get_size(f), 0)

    def test_sort_dirs_name(self):
        f = '/foo/bar'
        d = '/foo/bar/arc'
        r = '/foo/bar/bay'
        w = '/foo/bar/tray'

        self.fs.create_dir(f)
        self.fs.create_dir(d)
        self.fs.create_dir(r)
        self.fs.create_dir(w)

        self.assertEqual(sort_dirs(get_dirs_with_size(f, False, False), 'name', True), ['\\foo\\bar\\arc', '\\foo\\bar\\bay', '\\foo\\bar\\tray'])
        self.assertEqual(sort_dirs(get_dirs_with_size(f, False, False), 'name', False), ['\\foo\\bar\\arc', '\\foo\\bar\\bay', '\\foo\\bar\\tray'])

    def test_something(self):
        d = '/foo/bar/t.txt'

        self.fs.create_dir(d)

        parsed = self.parser.parse_args([d, '--ext'])
        self.assertEqual(parsed.ext, 'test')


