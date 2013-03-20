import os
import os.path
import tempfile

class graphviz:

    def do_graphviz(file):
        if platform.system() == 'Darwin':
            if os.path.isfile(file):
                os.system("open -a '\''/Applications/Graphviz.app'\'' " + file)

    def dotTo(file, format):
        base = file.replace(".dot", "")
        out = base + "." + format
        if format == "pdf":
            command = "dot -Tps %s | epstopdf --filter --ooutput %s" % (file, out)
        else:
            command = "dot -T%s %s -o %s 2>/tmp/err" % (format, file, out)
        os.system(command)
