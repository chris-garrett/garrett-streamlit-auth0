import os
import sys
from dotenv import load_dotenv
from pprint import pprint

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
        )
    )
)
pprint(sys.path)
load_dotenv()
