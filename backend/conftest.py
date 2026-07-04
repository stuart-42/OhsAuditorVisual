import os
import sys

# Make the sitesentry package importable when pytest runs from backend/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
