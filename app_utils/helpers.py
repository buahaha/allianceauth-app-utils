import os
import random
import string


def chunks(lst, size):
    """Yield successive sized chunks from lst."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


# old: get_swagger_spec_path
def swagger_spec_path() -> str:
    """returns the path to the current esi swagger spec file"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "swagger.json")


def random_string(char_count: int) -> str:
    """returns a random string of given length"""
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(char_count)
    )


class AttrDict(dict):
    """Enhanced dict that allows property access to its keys.

    Example:

    .. code-block:: python

        >> my_dict = AttrDict({"color": "red", "size": "medium"})
        >> my_dict["color"]
        "red"
        >> my_dict.color
        "red"

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
