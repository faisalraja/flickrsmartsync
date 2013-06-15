import os
import sys

__author__ = 'faisal'


if __name__ == "__main__":
    # Access from source
    sys.path.insert(0, os.sep.join(os.path.dirname(__file__).split(os.sep)[:-1]))

    import flickrsmartsync
    flickrsmartsync.main()