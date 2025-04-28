from flask import Flask

from typing import List


app = Flask(__name__)


__all__: List = ["app"]