"""Logger module."""


import logging


class LoggerMixin:
    """Logger Mixin class.

    Args:
        level (int): logging level.
        args (tuple): arguments.
        kwargs (dict): keyword arguments.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, level: int, *args: tuple, **kwargs: dict):
        name = f"{self.__module__}.{self.__class__.__qualname__}"

        self._log = logging.getLogger(name)
        self._log.setLevel(level)

        super().__init__(*args, **kwargs)
