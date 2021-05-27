from dataclasses import dataclass
import datetime


@dataclass
class FileData:
    name: str
    size: float
    depth: int
    indent: str
    is_dir: bool
    time: datetime
