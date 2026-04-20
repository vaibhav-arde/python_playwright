# conftest.py
# =====================
# ROOT CONFTEST — REGISTRY ONLY
# =====================
# This file acts as the fixture registry.
# All fixture logic lives in the fixtures/ package.
# Only imports and lightweight hooks belong here.

from fixtures.api import *  # noqa: F401, F403
from fixtures.auth import *  # noqa: F401, F403
from fixtures.browser import *  # noqa: F401, F403
from fixtures.user import *  # noqa: F401, F403
from setup.setuptest import *  # noqa: F401, F403
