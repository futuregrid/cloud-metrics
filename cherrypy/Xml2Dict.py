import xml.etree.ElementTree as ET
import pprint

class Xml2Dict:

    def __init__(self, msg, is_file=False):

        if is_file:
            tree = ET.parse(msg)
            root = tree.getroot()
        else:
            root = ET.fromstring(msg)
        self.root = root

    def parse(self):
        return self._parse(self.root, 0, 0)

    def _parse(self, msg, depth, count):
        if len(msg) == 0:
            return msg.text
        res = {}
        item_cnt = 0
        for a in msg:
            key = self.remove_xmlns(a.tag)
            if key == "item":
                if depth == 1:
                    key = count
                    count = count + 1

            if key in res:
                key = key + str(item_cnt)
                item_cnt += 1
                    
            res[key] = self._parse(a, depth + 1, count)
        return res

    def remove_xmlns(self, msg):
        return msg.split("{http://ec2.amazonaws.com/doc/2010-08-31/}")[1]

    def test(self, msg):
        for a in msg:
            print "A",a.tag, a.text
            for b in a:
                print "B", b.tag, b.text
                for c in b:
                    print "C", c.tag, c.text
                    for d in c:
                        print "D", d.tag, d.text
                        for e in d:
                            print "E", e.tag, e.text

#pp = pprint.PrettyPrinter(indent=4)
#tup = test2(root, 0, 0)
#pp.pprint(tup)
