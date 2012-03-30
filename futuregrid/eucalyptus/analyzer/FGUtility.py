class FGUtility:
    
    prefix = "[output]"

    @staticmethod
    def convertOutput(argument, name):
        return FGUtility.prefix + "[" + name + "]" + argument 

