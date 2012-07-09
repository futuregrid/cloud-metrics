import os

class FGUtility:

    prefix = "[output]"

    @staticmethod
    def convertOutput(argument, name):
        return FGUtility.prefix + "[" + name + "]" + argument 

    @staticmethod
    def ensure_dir(f):
        d = os.path.dirname(f)
        if d:
            if not os.path.exists(d):
                os.makedirs(d)

