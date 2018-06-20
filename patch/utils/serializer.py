import cPickle
from patch.utils.singleton import Singleton


class Serializer(object):

    __metaclass__ = Singleton

    def __init__(self):
        self.__volatile_cache = dict()
        self.__filename = 'serializer.cache'

    def set_serialized_filename(self, filename):
        """
        Set the serialized filename path which is used to save all objects
        in the volatil cache dict.
        """
        self.__filename = filename

    def get_serialized_filename(self):
        return self.__filename

    def test_object_in_cache(self, key):
        """
        Test whether the specified key is in the volatile cache dict.
        """
        return self.__volatile_cache.has_key(key)

    def get_object_from_cache(self, object_name):
        """
        Get object from volatile cache dict by the specified object key.
        """
        return self.__volatile_cache.get(object_name, None)

    def save_object_to_cache(self, object_name, object_to_save):
        """
        Save object to the volatile cache dict.
        """
        self.__volatile_cache.setdefault(object_name, object_to_save)

    def get_all_objects_in_caches(self):
        """
        Return all objects in caches.
        """
        return self.__volatile_cache

    def save_objects_to_file(self):
        """
        Save all objects in the volatile cache to the hard disk.
        """
        try:
            with open(self.__filename, 'w') as fo:
                cPickle.dump(self.__volatile_cache, fo)
            return True
        except:
            return False

    def load_objects_from_file(self):
        """
        Load all objects in the volatile cache from the hard disk.
        """
        try:
            with open(self.__filename) as fo:
                self.__volatile_cache = cPickle.load(fo)
            return True
        except:
            self.__volatile_cache.clear()
            return False
