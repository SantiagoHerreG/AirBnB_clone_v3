#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        obj = models.storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_by_class(self):
        """Tests that it returns the list of objects of one type of class
        """
        state = State()
        state.id = 1234553
        state.name = "California"
        models.storage.new(state)
        models.storage.save()
        key = type(state).__name__ + "." + str(state.id)
        obj = models.storage.all(State)
        self.assertTrue(key in obj.keys())
        self.assertTrue(type(obj[key]) is State)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

        user = User()
        user.id = 12345588
        user.name = "Kevin"
        user.email = "1234@yahoo.com"
        user.password = "hi"
        models.storage.new(user)
        user.save()
        obj = models.storage.all()
        key = type(user).__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        obj1 = models.storage.all()
        user = User()
        user.id = 5588
        user.name = "Kevin"
        user.email = "1234@yahoo.com"
        user.password = "hi"
        models.storage.new(user)
        user.save()
        obj2 = models.storage.all()
        self.assertTrue(len(obj1) < len(obj2))

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_reload_dbstorage(self):
        """
        tests reload
        """
        session1 = models.storage._DBStorage__session
        models.storage.reload()
        session2 = models.storage._DBStorage__session
        self.assertTrue(session1 is not session2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test the method for getting an object from its class and id
        """
        obj1 = models.storage.all()
        user = User()
        user.id = "12345"
        user.name = "Kevin"
        user.email = "1234@yahoo.com"
        user.password = "hi"
        models.storage.new(user)
        user.save()
        user_copy = models.storage.get(User, "12345")
        print(user.id, user_copy.id)
        self.assertTrue(user.id == user_copy.id)
        self.assertTrue(user.name == user_copy.name)
        self.assertTrue(user.email == user_copy.email)
        self.assertTrue(user.updated_at == user_copy.updated_at)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Tests if count method returns the count of objects of class
        """
        count1 = models.storage.count(User)
        user = User()
        user.id = "1234567"
        user.name = "Santi"
        user.email = "1234@yahoo.com"
        user.password = "hi"
        models.storage.new(user)
        user.save()
        count2 = models.storage.count(User)
        self.assertTrue(count1 < count2)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_none_cls(self):
        """Tests if count method returns the count of all objects
        """
        count1 = models.storage.count()
        user = User()
        user.id = "12345678"
        user.name = "Herre"
        user.email = "1234@yahoo.com"
        user.password = "hi"
        models.storage.new(user)
        user.save()
        count2 = models.storage.count()
        self.assertTrue(count1 < count2)
