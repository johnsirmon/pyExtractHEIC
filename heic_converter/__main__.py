"""Allow running the package with ``python -m heic_converter``."""

import sys

from .cli import main

sys.exit(main())
