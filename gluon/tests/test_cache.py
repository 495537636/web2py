#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unit tests for gluon.cache
"""

import sys
import os
import unittest


def fix_sys_path():
    """
    logic to have always the correct sys.path
     '', web2py/gluon, web2py/site-packages, web2py/ ...
    """

    def add_path_first(path):
        sys.path = [path] + [p for p in sys.path if (
            not p == path and not p == (path + '/'))]

    path = os.path.dirname(os.path.abspath(__file__))

    if not os.path.isfile(os.path.join(path,'web2py.py')):
        i = 0
        while i<10:
            i += 1
            if os.path.exists(os.path.join(path,'web2py.py')):
                break
            path = os.path.abspath(os.path.join(path, '..'))

    paths = [path,
             os.path.abspath(os.path.join(path, 'site-packages')),
             os.path.abspath(os.path.join(path, 'gluon')),
             '']
    [add_path_first(path) for path in paths]

fix_sys_path()


from storage import Storage
from cache import CacheInRam, CacheOnDisk, Cache

oldcwd = None


def setUpModule():
    global oldcwd
    if oldcwd is None:
        oldcwd = os.getcwd()
        if not os.path.isdir('gluon'):
            os.chdir(os.path.realpath('../../'))


def tearDownModule():
    global oldcwd
    if oldcwd:
        os.chdir(oldcwd)
        oldcwd = None


class TestCache(unittest.TestCase):

    def testCacheInRam(self):

        # defaults to mode='http'

        cache = CacheInRam()
        self.assertEqual(cache('a', lambda: 1, 0), 1)
        self.assertEqual(cache('a', lambda: 2, 100), 1)
        cache.clear('b')
        self.assertEqual(cache('a', lambda: 2, 100), 1)
        cache.clear('a')
        self.assertEqual(cache('a', lambda: 2, 100), 2)
        cache.clear()
        self.assertEqual(cache('a', lambda: 3, 100), 3)
        self.assertEqual(cache('a', lambda: 4, 0), 4)
        #test singleton behaviour
        cache = CacheInRam()
        cache.clear()
        self.assertEqual(cache('a', lambda: 3, 100), 3)
        self.assertEqual(cache('a', lambda: 4, 0), 4)
        #test key deletion
        cache('a', None)
        self.assertEqual(cache('a', lambda: 5, 100), 5)
        #test increment
        self.assertEqual(cache.increment('a'), 6)
        self.assertEqual(cache('a', lambda: 1, 100), 6)
        cache.increment('b')
        self.assertEqual(cache('b', lambda: 'x', 100), 1)


    def testCacheOnDisk(self):

        # defaults to mode='http'

        s = Storage({'application': 'admin',
                     'folder': 'applications/admin'})
        cache = CacheOnDisk(s)
        self.assertEqual(cache('a', lambda: 1, 0), 1)
        self.assertEqual(cache('a', lambda: 2, 100), 1)
        cache.clear('b')
        self.assertEqual(cache('a', lambda: 2, 100), 1)
        cache.clear('a')
        self.assertEqual(cache('a', lambda: 2, 100), 2)
        cache.clear()
        self.assertEqual(cache('a', lambda: 3, 100), 3)
        self.assertEqual(cache('a', lambda: 4, 0), 4)
        #test singleton behaviour
        cache = CacheOnDisk(s)
        cache.clear()
        self.assertEqual(cache('a', lambda: 3, 100), 3)
        self.assertEqual(cache('a', lambda: 4, 0), 4)
        #test key deletion
        cache('a', None)
        self.assertEqual(cache('a', lambda: 5, 100), 5)
        #test increment
        self.assertEqual(cache.increment('a'), 6)
        self.assertEqual(cache('a', lambda: 1, 100), 6)
        cache.increment('b')
        self.assertEqual(cache('b', lambda: 'x', 100), 1)

    def testCacheWithPrefix(self):
        s = Storage({'application': 'admin',
                     'folder': 'applications/admin'})
        cache = Cache(s)
        prefix = cache.with_prefix(cache.ram,'prefix')
        self.assertEqual(prefix('a', lambda: 1, 0), 1)
        self.assertEqual(prefix('a', lambda: 2, 100), 1)
        self.assertEqual(cache.ram('prefixa', lambda: 2, 100), 1)




if __name__ == '__main__':
    setUpModule()       # pre-python-2.7
    unittest.main()
    tearDownModule()
