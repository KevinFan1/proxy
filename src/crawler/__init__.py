import inspect
import pkgutil

from src.crawler.base import BaseCrawler

classes = []
for file, name, is_pkg in pkgutil.walk_packages(__path__):
    module = file.find_module(name).load_module(name)
    for n, value in inspect.getmembers(module):
        if inspect.isclass(value) and issubclass(value, BaseCrawler):
            if value is not BaseCrawler and not getattr(value, 'ignore', False):
                classes.append(value)

__all__ = __ALL__ = classes
