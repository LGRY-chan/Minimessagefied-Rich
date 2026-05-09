from rich.console import Console
from .parser import parse

class MiniMessageConsole(Console):
    def print(self, *objects, **kwargs):
        new_objects = []
        for obj in objects:
            if isinstance(obj, str):
                # Check if it looks like it might contain MiniMessage tags
                if "<" in obj and ">" in obj:
                    new_objects.append(parse(obj))
                else:
                    new_objects.append(obj)
            else:
                new_objects.append(obj)
        super().print(*new_objects, **kwargs)

    def log(self, *objects, **kwargs):
        new_objects = []
        for obj in objects:
            if isinstance(obj, str) and "<" in obj and ">" in obj:
                new_objects.append(parse(obj))
            else:
                new_objects.append(obj)
        super().log(*new_objects, **kwargs)

