import os
import sys


if "CMSSW_BASE" not in os.environ:
    sys.exit("Set up the CMSSW environment.")

root_dest = "%s/src/auxiliaries/shapes/Brown" % os.environ["CMSSW_BASE"]

bdt_tmp = "%s/src/LIMITS-tmp/tt" % os.environ["CMSSW_BASE"]

def copy(src="", channel="tt", era="8TeV", tag="Hhh", link=False):
    dest = "%s/%s" % (root_dest, "htt_%s.inputs-%s-%s.root" % (channel, tag, era))

    try:
        os.remove(dest)
    except OSError as e:
        if e.errno != 2:
            print e
            sys.exit(1)
    if link:
        src = os.path.abspath(src).replace(root_dest + "/", "")
        os.system("ln -s %s %s" % (src, dest))
    else:
        os.system("cp -p %s %s" % (src, dest))
