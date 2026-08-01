from django.conf import settings


class SyncRouter:
    """
    A router to route database operations based on USE_POSTGRES setting.
    """
    def _get_primary_db(self):
        return 'default'

    def _get_secondary_db(self):
        return 'sqlite' if settings.USE_POSTGRES else 'postgres'

    def db_for_read(self, model, **hints):
        return self._get_primary_db()

    def db_for_write(self, model, **hints):
        return self._get_primary_db()

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Only migrate the primary database
        return db == self._get_primary_db()
