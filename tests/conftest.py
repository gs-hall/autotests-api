import sys
from pathlib import Path

# Add the parent directory (project root) to sys.path so that imports like
# 'from clients.users...' work correctly when running tests
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
