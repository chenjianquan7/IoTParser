
import copy
import time
import types

class AttribDict(dict):
    """
    This class defines the dictionary with added capability to access members as attributes
    """
    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}
        
        
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True
        
        
    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError("unable to access item '%s'" % item)
    def __setattr__(self, item, value):
        """
        Maps attributes to values
        Only if we are initialised
        """
        
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)
        
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)
    def __getstate__(self):
        return self.__dict__
    def __setstate__(self, dict):
        self.__dict__ = dict
    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal
        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))
        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))
        return retVal
