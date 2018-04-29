import re
import os
import json


target_pattern = {
    re.compile(r'\S+\.k?sh'): [re.compile(r'(?P<filename>\S+\.k?sh)$')],
    re.compile(r'\S+\.bat'): [re.compile(r'(?P<filename>\S+\.k?sh)$'), re.compile(r'(?P<filename>\S+\.bat)$')],
    re.compile(r'\S+\.sp'): [],
}

target_ignore = {
    re.compile(r'\S+\.k?sh'): [re.compile(r'^\S*#.*')],
    re.compile(r'\S+\.bat'): [re.compile(r'^\S(?://|/#).*')],
    re.compile(r'\S+\.sp'): [],
}


def pattern_search(patterns, string):
    for pa in patterns:
        res = pa.search(string)
        if res:
            return res
    else:
        return None


def fileparse(filename):
    root = {}
    filename = findfile(filename)
    if filename:
        with open(filename, mode='r') as f:
            pfilename = os.path.basename(filename)
            for target in target_pattern:
                res = target.match(pfilename)
                if res:
                    for line in f:
                        line = line.rstrip('\r\n')
                        if pattern_search(target_ignore[target], line):
                            continue
                        elif pattern_search(target_pattern[target], line):
                            subfile = pattern_search(target_pattern[target], line).group('filename')
                            root.update(fileparse(subfile))
            root = {pfilename: root}
    return root


def findfile(filename, topdir='.'):
    for dirpath, dirnames, filenames in os.walk(topdir):
        if filename in filenames:
            return os.path.join(dirpath, filename)
    else:
        return ''


if __name__ == '__main__':
    ret = fileparse('test1.bat')
    with open('./result.json', mode='w') as f:
        f.write(json.dumps(ret))
