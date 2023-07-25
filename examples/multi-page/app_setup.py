import os
import sys
from dotenv import load_dotenv

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
        )
    )
)

load_dotenv()
