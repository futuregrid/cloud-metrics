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


    def retrieve_userinfo_ldap(ownerid):

        cmd = ['python', 'fg-user-project-info.py', '-u', ownerid, '-n']
        try:
            output = subprocess.check_output(cmd)
            res = re.split(',', output.rstrip())
            firstname = res[0]
            lastname = res[1]
            uid = res[2]
            result = { 'ownerid': ownerid, 'first_name':res[0], 'last_name' : res[1], 'uid' : res[2] }
            return result
        except:
            return None

