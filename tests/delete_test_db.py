import os
from tests.create_test_db import DIR_PATH
if os.path.exists(os.path.join(DIR_PATH, 'test.db')):
    os.remove(os.path.join(DIR_PATH, 'test.db'))