import threading
from patterns.logger import Logger

logger = Logger(name='unit_of_work')


class UnitOfWork:
    thread = threading.local()

    def __init__(self):
        # initialize lists with 3 types of objects
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry

    # append 'new' object to new_objects list
    def register_new(self, obj):
        self.new_objects.append(obj)

    # append updated objects to dirty_objects list
    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    # append objects to be removed to removed_objects list
    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def insert_new(self):
        # if new_objects list is not cleared here, it is inserted two times
        logger.log(f'Inserting new objects: {self.new_objects}')
        try:
            for obj in self.new_objects:
                logger.log(f'Getting {self.MapperRegistry} map registry')
                self.MapperRegistry.get_mapper(obj).insert(obj)
        except Exception as e:
            raise Exception(e)
        finally:
            self.new_objects.clear()

    def update_dirty(self):
        try:
            logger.log(f'Updating objects: {self.dirty_objects}')
            for obj in self.dirty_objects:
                self.MapperRegistry.get_mapper(obj).update(obj)
        except Exception as e:
            raise Exception(e)
        finally:
            self.dirty_objects.clear()

    def delete_removed(self):
        try:
            logger.log(f'Removing objects: {self.removed_objects}')
            for obj in self.removed_objects:
                self.MapperRegistry.get_mapper(obj).delete(obj)
        except Exception as e:
            raise Exception(e)
        finally:
            self.removed_objects.clear()

    # committing all operations in db in one go
    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    @staticmethod
    def new_thread():
        __class__.set_thread(UnitOfWork())

    @classmethod
    def set_thread(cls, unit_of_work):
        cls.thread.unit_of_work = unit_of_work

    @classmethod
    def get_thread(cls):
        return cls.thread.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_thread().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_thread().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_thread().register_removed(self)


