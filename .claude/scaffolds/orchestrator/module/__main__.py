"""python -m {{ORCHESTRATOR_PKG}} entry-point."""
import sys

from .orchestrator import main

sys.exit(main())
