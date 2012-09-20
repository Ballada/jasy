#!/usr/bin/env python3

import sys, os, unittest, logging, pkg_resources, tempfile

import jasy.core.Config as Config

# Extend PYTHONPATH with local 'lib' folder
jasyroot = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir, os.pardir, os.pardir))
sys.path.insert(0, jasyroot)


class Tests(unittest.TestCase):

    def test_write_json(self):

        tempDirectory = tempfile.TemporaryDirectory().name
        os.makedirs(tempDirectory)

        Config.writeConfig([{"one": 1,"two": 2},{"three": 3,"four": 4}], os.path.join(tempDirectory, "test.json"))
        
        self.assertEqual(Config.findConfig(os.path.join(tempDirectory, "test.json")), os.path.join(tempDirectory, "test.json"))        
       
       
    def test_write_and_read_json(self):

        tempDirectory = tempfile.TemporaryDirectory().name
        os.makedirs(tempDirectory)

        Config.writeConfig([{"one": 10-9,"two": 5-3},{"three": 1+1+1,"four": 2*2}], os.path.join(tempDirectory, "test.json"))
        data = Config.loadConfig(os.path.join(tempDirectory, "test.json"))

        self.assertEqual(data, [{'two': 2, 'one': 1}, {'four': 4, 'three': 3}])        
       

    def test_write_yaml(self):

        tempDirectory = tempfile.TemporaryDirectory().name
        os.makedirs(tempDirectory)

        Config.writeConfig([{"one": 1,"two": 2},{"three": 3,"four": 4}], os.path.join(tempDirectory, "test.yaml"))
        
        self.assertEqual(Config.findConfig(os.path.join(tempDirectory, "test.yaml")), os.path.join(tempDirectory, "test.yaml"))        
    

    def test_write_and_read_json(self):

        tempDirectory = tempfile.TemporaryDirectory().name
        os.makedirs(tempDirectory)

        Config.writeConfig([{"one": 10-9,"two": 5-3},{"three": 1+1+1,"four": 2*2}], os.path.join(tempDirectory, "test.yaml"))
        data = Config.loadConfig(os.path.join(tempDirectory, "test.yaml"))

        self.assertEqual(data, [{'two': 2, 'one': 1}, {'four': 4, 'three': 3}]) 


    def test_matching_types(self):

        self.assertTrue(Config.matchesType(42, "int"))
        self.assertTrue(Config.matchesType(11.0, "float"))
        self.assertTrue(Config.matchesType(11.1, "float"))
        self.assertTrue(Config.matchesType("hello", "string"))
        self.assertTrue(Config.matchesType(False, "bool"))
        self.assertTrue(Config.matchesType([{"one": 10-9,"two": 5-3},{"three": 1+1+1,"four": 2*2}], "list"))
        self.assertTrue(Config.matchesType({"one": 10-9,"two": 5-3}, "dict"))
    

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.ERROR)
    suite = unittest.TestLoader().loadTestsFromTestCase(Tests)
    unittest.TextTestRunner(verbosity=2).run(suite)

