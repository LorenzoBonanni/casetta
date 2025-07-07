import numpy as np
from gymnasium.spaces import Box


from dataclasses import dataclass, field, fields, make_dataclass, MISSING, is_dataclass
from typing import Any

def merge_dataclasses(name: str, instances: list[Any]) -> Any:
    """
    Merges multiple dataclass instances into a new dataclass instance
    with all combined fields and their values.

    Args:
        name (str): Name of the new merged dataclass.
        instances (list): List of dataclass instances to merge.

    Returns:
        Any: A new dataclass instance with combined fields and values.
    """
    new_fields = []
    new_values = {}

    for obj in instances:
        if not is_dataclass(obj):
            raise TypeError(f"{obj} is not a dataclass instance")

        for f in fields(obj):
            new_name = f"{str(obj).split('Output(')[0].lower()}_{f.name}"  # Prefix with the class name

            # Handle default values
            if f.default is not MISSING:
                new_fields.append((new_name, f.type, f.default))
            elif f.default_factory is not MISSING:  # type: ignore
                new_fields.append((new_name, f.type, field(default_factory=f.default_factory)))  # type: ignore
            else:
                new_fields.append((new_name, f.type))

            new_values[new_name] = getattr(obj, f.name)

    # Create the new dataclass type
    Combined = make_dataclass(name, new_fields)

    # Instantiate it with merged values
    return Combined(**new_values)


def merge_box_spaces(spaces: list[Box]) -> Box:
    """
    Merge a list of gym.spaces.Box into a single Box space.

    Args:
        spaces (list[Box]): List of Box spaces to merge.

    Returns:
        Box: A new Box space with concatenated bounds and shape.
    """
    low = np.concatenate([space.low.flatten() for space in spaces])
    high = np.concatenate([space.high.flatten() for space in spaces])

    return Box(low=low, high=high)