from api.config import INITIAL_DATA
import json
import importlib

def import_json(file_name):
    with open(INITIAL_DATA / file_name, 'r') as f:
        dict_ = json.load(f)
    
    obj_list = []
    if type(dict_) is list:
        for item in dict_:
            obj_list.append(dict_to_obj(item))
    else:
        obj_list.append(dict_)
    return obj_list


def dict_to_obj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")
        
        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")
        
        # We use the built in __import__ function since the module name is not yet known at runtime
        module = importlib.import_module(module_name)
        
        # Get the class from the module
        class_ = getattr(module,class_name)
        
        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj
