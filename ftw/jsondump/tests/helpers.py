from path import Path
from StringIO import StringIO


def asset(filename):
    path = Path(__file__).dirname().realpath().joinpath('assets', filename)
    return path


def asset_as_StringIO(filename):
    result = StringIO(asset(filename).bytes())
    result.filename = filename
    return result
