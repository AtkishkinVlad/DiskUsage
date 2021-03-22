class FileData:
    def __init__(self, name, size, depth, indent, isDir, datetime):
        self.name = name
        self.size = size
        self.depth = depth
        self.indent = indent
        self.isDir = isDir
        self.time = datetime
