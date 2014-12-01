import os
import sys

if "CMSSW_BASE" not in os.environ:
    sys.exit("Set up the CMSSW environment.")

root_dest = "%s/src/auxiliaries/shapes/Brown" % os.environ["CMSSW_BASE"]

lumi     = 19.7   # /fb
rescaleX = False

substring_signal_example = "2B350"

#masses_spin0 = [260, 300, 350]
masses_spin0 = range(260, 360, 10) #+ [500, 700]
masses_spin2 = [500, 700]

categories = {#"MM_LM": "tauTau_2jet2tag",
              "2M": "tauTau_2jet2tag",
              "1M": "tauTau_2jet1tag",
              }

# files = {"":                             "root/take2/combined_inclusiveDY.root",
#          "_CMS_scale_t_tautau_8TeVUp":   "root/take2/combined_up.root",
#          "_CMS_scale_t_tautau_8TeVDown": "root/take2/combined_down.root",
#          }

__stem = "root/combined_relaxed_%s.root"
files = {"":                             __stem % "",
         #"_CMS_scale_t_tautau_8TeVUp":   __stem % "_tauUp",
         #"_CMS_scale_t_tautau_8TeVDown": __stem % "_tauDown",
         #"_CMS_scale_j_tautau_8TeVUp":   __stem % "_jetUp",
         #"_CMS_scale_j_tautau_8TeVDown": __stem % "_jetDown",
         }

__fakeSignals = {"ggAToZhToLLTauTau": masses_spin0,
                 "ggAToZhToLLBB": [250] + masses_spin0,
                 "ggGravitonTohhTo2Tau2B": [270, 300, 500, 700, 1000],
                 "ggRadionTohhTo2Tau2B":   [     300, 500, 700, 1000],
                 "bbH": range(90, 150, 10) + [160, 180, 200, 250, 300, 350, 400],
                 }

fakeBkgs = ["ZJ", "ZL", "ZLL"][:1]

def procs():
    out = {"TT": ["tt", "tt_semi"],
           "VV": ["ZZ", "WZJetsTo2L2Q"],
           "W": ["W2JetsToLNu", "W3JetsToLNu", "W4JetsToLNu"],  # W1 provides no events
           #"ZTT": ["DYJetsToLL"],
           "ZTT": ["DY1JetsToLL", "DY2JetsToLL", "DY3JetsToLL", "DY4JetsToLL"],
           "QCD": ["dataOSRelax"],
           }

    for m in masses_spin0:
        out["ggHTohhTo2Tau2B%3d" % m] = ["H2hh%3d" % m]

    for p in fakeBkgs + fakeSignalList():
        out[p] = [p]

    return out


def fakeSignalList():
    out = []
    for stem, masses in __fakeSignals.iteritems():
        for m in masses:
            out.append("%s%d" % (stem, m))
    return out


def isData(proc):
    return proc.startswith("data") or proc.startswith("QCD")


def isSignal(proc):
    return any([proc.startswith(p) for p in ["ggHTo", "ggATo", "ggGraviton", "ggRadion", "bbH"]])


def isAntiIsoData(proc):
    return proc == "dataOSRelax"


def cats():
    return " ".join([s[-4] for s in categories.values()])


def workDir():
    return "/".join(__file__.split("/")[:-1])



def variables():
    fm_bins = [200, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 500, 550, 600, 650, 700]
    it_sv_bins_cat1 = range(0, 200, 10) + range(200, 375, 25)
    it_sv_bins_cat2 = range(0, 210, 20) + [250, 300, 350]
    it_fm_bins_cats = range(0, 510, 20) + range(550, 1050, 50)

    preselection = {}
    fMass = {"fMassKinFit": (0.0, None)}
    #chi2 = {"chi2KinFit2": (0.0, 10.0)}
    mass_windows = {"mJJ": (70.0, 150.0), "svMass": (90.0, 150.0)}
    mass_windows.update(fMass)

    ## bins are either a tuple: (n, xMin, xMax)
    ##  or
    ## a list of bin lower edges

    out = [#{"var": "svMass",      "bins": ( 14,   0.0, 350.0), "cuts": {}},
           {"var": "svMass",      "bins": it_sv_bins_cat2, "cuts": {}},

           #{"var": "fMassKinFit", "bins": ( 4, 250.0, 410.0), "cuts": mass_windows},
           {"var": "fMassKinFit", "bins": it_fm_bins_cats, "cuts": mass_windows},
           #{"var": "fMassKinFit", "bins": fm_bins, "cuts": mass_windows},
           ]

    if False:
        for var, bins in [("BDT", (8, -0.6, 0.2)),
                          #("BDT_270", (8, -0.6, 0.2)),
                          #("BDT_280", (8, -0.6, 0.2)),
                          #("BDT_290", (8, -0.6, 0.2)),
                          #("BDT_300", (8, -0.6, 0.2)),
                          #("BDT_310", (8, -0.6, 0.2)),
                          #("BDT_320", (8, -0.6, 0.2)),
                          #("BDT_330", (8, -0.6, 0.2)),
                          #("BDT_340", (8, -0.6, 0.2)),
                          #("BDT_350", (8, -0.6, 0.2)),
                          ]:
            out.append({"var": var, "bins": bins, "cuts": preselection})
    return out


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != 17:
            raise e


def outFileName(sFactor=0, sKey="", var="", cuts={}):
    stem = root_dest + "/"
    mkdir(stem)

    if sFactor:
        print "FIXME: sFactor"
        stem += "%dx%s" % (sFactor, sKey.replace("H2hh", ""))
    stem += var
    if cutDesc(cuts):
        stem += "_%s" % cutDesc(cuts)
    return "%s.root" % stem


def cutDesc(cuts):
    descs = []
    for cutVar, (cutMin, cutMax) in sorted(cuts.iteritems()):
        cutDesc = cutVar
        if cutMin is not None:
            cutDesc = "%.1f.%s" % (cutMin, cutDesc)
        if cutMax is not None:
            cutDesc = "%s.%.1f" % (cutDesc, cutMax)
        descs.append(cutDesc)
    return "_".join(descs)


def complain():
    if len(set(files.values())) != 3:
        print "FIXME: include variations"

    if __fakeSignals:
        print "FIXME: include", sorted(__fakeSignals.keys())

    if fakeBkgs:
        print "FIXME: include", sorted(fakeBkgs)

    lst = []
    for v in procs().values():
        if type(v) != list:
            sys.exit("ERROR: type of '%s' is not list." % str(v))
        else:
            lst += v
    if len(set(lst)) != len(lst):
        sys.exit("ERROR: procs values has duplicates: %s." % str(sorted(lst)))


complain()
