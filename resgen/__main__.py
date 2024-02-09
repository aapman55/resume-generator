"""
Makes it possible to call
```
python -m resgen
```
"""

import sys
from pathlib import Path

sys.path.append(str(Path(".").resolve()))


if __name__ == "__main__":
    from resgen.console.cli import run

    run()
