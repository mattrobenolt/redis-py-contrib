"""
redis_contrib.django.test
=====

License: BSD, see LICENSE for more details.
"""

import os
from django.test import TestCase
from django.utils import simplejson
from django.db.models import get_apps
from django.conf import settings


class RedisTestCase(TestCase):
    """
    Redis, yay!
    """
    def _fixture_setup(self):
        super(RedisTestCase, self)._fixture_setup()
        if not hasattr(self, 'redis_client'):
            return
        client = self.redis_client
        commands = self._load_fixture()
        if commands is None:
            return
        client.execute_command('MULTI')
        for command in commands:
            client.execute_command(*command)
        client.execute_command('EXEC')

    def _fixture_teardown(self):
        super(RedisTestCase, self)._fixture_teardown()
        if not hasattr(self, 'redis_client'):
            return
        client = self.redis_client
        client.flushdb()

    def _load_fixture(self):
        if not hasattr(self, 'redis_fixtures'):
            return None
        if isinstance(self.redis_fixtures, basestring):
            self.redis_fixtures = [self.redis_fixtures]
        app_module_paths = []
        for app in get_apps():
            if hasattr(app, '__path__'):
                for path in app.__path__:
                    app_module_paths.append(path)
            else:
                app_module_paths.append(app.__file__)
        app_fixtures = [os.path.join(os.path.dirname(path), 'fixtures') for path in app_module_paths]
        commands = []
        for fixture_name in self.redis_fixtures:
            fixture_found = False
            if os.path.isabs(fixture_name):
                fixture_dirs = [fixture_name]
            else:
                fixture_dirs = app_fixtures + list(settings.FIXTURE_DIRS) + ['']
            for fixture_dir in fixture_dirs:
                if fixture_found:
                    continue
                full_path = os.path.join(fixture_dir, fixture_name)
                try:
                    fixture = open(full_path, 'r')
                except IOError:
                    continue
                else:
                    try:
                        commands += simplejson.load(fixture)['commands']
                        fixture_found = True
                    except Exception:
                        # Fixture was found, but it's broken, so break out completely
                        break
                    finally:
                        fixture.close()
        if not len(commands):
            return None
        return commands
