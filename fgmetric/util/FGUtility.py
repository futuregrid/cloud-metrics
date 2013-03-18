import os
import sys
import re
import subprocess
import datetime
from fgmetric.shell.FGInstances import FGInstances  # for insert_userinfo
import errno


class FGUtility:

    prefix = "[output]"

    @staticmethod
    def convertOutput(argument, name):
        return FGUtility.prefix + "[" + name + "]" + argument

    @staticmethod
    def ensure_dir(f):
        d = os.path.dirname(f)
        if not d:
            return False
        if not os.path.exists(d):
            try:
                os.makedirs(d)
                return True
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print e
                    print "path '" + d + "' is not accessible"
                    return False
        return True

    @staticmethod
    def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
            return datetime.datetime.now().strftime(fmt).format(fname=fname)

    @staticmethod
    def retrieve_userinfo_ldap(ownerid):

        # cmd = ['python', 'fg-user-project-info.py', '-u', ownerid, '-n']
        cmd = ['fg-user-project-info.py', '-u', ownerid, '-n']
        try:
            output = subprocess.check_output(cmd)
            res = re.split(',', output.rstrip())
            result = {'ownerid': ownerid, 'first_name': res[
                0], 'last_name': res[1], 'uid': res[2], 'email': res[3]}
            return result
        except:
            return None

    @staticmethod
    def debug(output=False):
        timestamp = datetime.datetime.now().strftime('%s.%f')
        f1 = sys._getframe(1)
        msg = f1.f_code.co_filename, f1.f_code.co_name, f1.f_lineno, timestamp
        if isinstance(output, (str)) and len(output) != 0:
            print str(msg) + output
        elif output:
            print msg
        return msg

    @staticmethod
    def insert_userinfo():
        '''Store userinfo into database by reading a userid(s) from a
        text file or a standard input This command will read a
        userid(s) and do ldapsearch to find userinfo. And then it will
        store the userinfo into mysql database.

        Usage: $ fg-metrics-utility insert_userinfo -i filename [hostname]
               or
               $ fg-metrics-utility insert_userinfo userid [hostname]
        '''

        i = FGInstances()
        filename = ""
        userid = ""
        ownerid = ""
        username = ""
        project = ""

        if len(sys.argv) < 3 or sys.argv[1] != "insert_userinfo":
            print "usage: ./$ fg-metrics-utility insert_userinfo -i filename [hostname] \n\
                   or \n\
                   $ fg-metrics-utility insert_userinfo userid [hostname]"
            return

        if sys.argv[2] == "-i":
            filename = sys.argv[3]
            hostname = sys.argv[4]
        else:
            userid = sys.argv[2]
            hostname = sys.argv[3]

        if os.path.exists(filename):
            f = open(filename, "r")
            while 1:
                line = f.readline()
                if not line:
                    break

                ownerid = line.rstrip()
                # For comma seperated lines
                # E.g. 5TQVNLFFHPWOH22QHXERX,hyunjoo,fg45
                # Ownerid, username, projectid
                m = re.search(r'(.*),(.*),(.*)', line.rstrip())

                if m:
                    try:
                        userid = m.group(1)
                        username = m.group(2)
                        project = m.group(3)
                    except:
                        m = None
                        pass

                    # In euca3.0+, username is an ownerid of past version of
                    # euca
                    if username:
                        ownerid = username
                res = self.retrieve_userinfo_ldap(ownerid)
                if res:
                    if m:
                        # if m exists, res (dict) should be merged with the
                        # comma separated values in order to store the info
                        # into db
                        res["ownerid"] = userid
                        res["username"] = username
                        res["project"] = project
                        if hostname:
                            res["hostname"] = hostname
                    print res
                    i.userinfo_data.append(res)
        else:
            res = self.retrieve_userinfo_ldap(userid)
            if res:
                i.userinfo_data.append(res)

        i.write_userinfo_to_db()


class dotdict(dict):
    ''' dot notation dictionary from
    http://pearand.com/say/index.php/2008/10/24/python-dot-notation-dictionary-access/
    '''
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
