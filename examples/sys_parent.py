# Ignore this as this is mainly used to include root directory in sys.path
import os
import sys
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.realpath(__file__),
            os.pardir,
            os.pardir
        )
    )
)
