import typing as T

from jdoc.titan.imports import *
from jdoc.titan.widget_reg import *


class ReactComponent(Resource):
    name: str = ""
    props: T.List[Resource] = []
