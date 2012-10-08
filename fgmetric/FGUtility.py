import os
import datetime

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

    @staticmethod
    def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
            return datetime.datetime.now().strftime(fmt).format(fname=fname)

    def retrieve_userinfo_ldap(ownerid):

        cmd = ['python', 'fg-user-project-info.py', '-u', ownerid, '-n']
        try:
            output = subprocess.check_output(cmd)
            res = re.split(',', output.rstrip())
            firstname = res[0]
            lastname = res[1]
            uid = res[2]
            result = { 'ownerid': ownerid, 'first_name':res[0], 'last_name' : res[1], 'uid' : res[2], 'email' : res[3] }
            return result
        except:
            return None

class dotdict(dict):
    ''' dot notation dictionary from http://parand.com/say/index.php/2008/10/24/python-dot-notation-dictionary-access/ '''
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__
