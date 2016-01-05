import os
import sys
from root_dest import root_dest

#lumi     = 1.264e3
lumiUnit = "/pb"

rescaleX = False

# masses = [160]
# masses = [260,270,280]#range(260, 360, 10) #+ [500, 700]
masses = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
# masses = masses[:2]

substring_signal_example = "ggH%d" % masses[0]

_suffix = "inclusive"
categories = {# "tt": "tauTau_%s" % _suffix,
              "et": "eleTau_%s" % _suffix,
              # "mt": "muTau_%s" % _suffix,
              "em": "emu_%s" % _suffix,
              }

#bdtDir = "/nfs_scratch/zmao/samples_Iso/datacard_new/bdt_new/"
bdtDir = "root/bdt/11/"
# WARNING: this variable gets modified by multi-bdt.py
# _stem = "13TeV_datacards_Spring15_eletronID2/combined%s.root"
# _stem = "13TeV_zp_inclusive/combined%s.root"
#lumi     = 1546.91; _stem = "13TeV_zp/combined%s.root"
#lumi     = 1546.91; _stem = "13TeV_zp2/combined%s.root"
#lumi     = 2093.3; _stem = "13TeV_zp3/combined%s.root"
#lumi     = 2093.3; _stem = "13TeV_zp3l/combined%s.root"
lumi     = 2093.3; _stem = "13TeV_zp_jan4/combined%s.root"


def files(variable=""):
    assert variable
    s = ""
    # s = "_withPUWeight"
    return {"":                             _stem % s,
            # "_CMS_scale_t_tautau_8TeVUp":   _stem % "tauUp",
            # "_CMS_scale_t_tautau_8TeVDown": _stem % "tauDown",
            # "_CMS_scale_j_8TeVUp":   _stem % "jetUp",
            # "_CMS_scale_j_8TeVDown": _stem % "jetDown",
            # "_CMS_scale_btag_8TeVUp": _stem % "bSysUp",
            # "_CMS_scale_btag_8TeVDown": _stem % "bSysDown",
            # "_CMS_scale_btagEff_8TeVUp": _stem % "bSysUp",     # duplicate of btag
            # "_CMS_scale_btagEff_8TeVDown": _stem % "bSysDown", # duplicate of btag
            # "_CMS_scale_btagFake_8TeVUp": _stem % "bMisUp",
            # "_CMS_scale_btagFake_8TeVDown": _stem % "bMisDown",
            }


def qcd_sf_name(category):
    # return "L_to_T_SF_%s" % category
    # return "SS_to_OS_%s" % category
    return "Loose_to_Tight_%s" % category  # NOTE! incorporate prong req


def procs(variable="", category=""):
    assert variable
    assert category

    # first character '-' means subtract rather than add
    # first character '*' (see procs2)
    out = {"TT": ["TTJets", 'ST_antiTop_tW', 'ST_top_tW', 'ST_t-channel_antiTop_tW', 'ST_t-channel_top_tW'],
           "VV": ['VVTo2L2Nu', 'WWTo1L1Nu2Q', 'WZJets', 'WZTo1L1Nu2Q', 'WZTo1L3Nu', 'WZTo2L2Q', 'ZZTo2L2Q', 'ZZTo4L'],
           "W": ['WJets_HT-0to100', 'WJets_HT-100to200', 'WJets_HT-200to400', 'WJets_HT-400to600', 'WJets_HT-600toInf'],
           "ZTT": ['DY_M-50-H-0to100', 'DY_M-50-H-100to200', 'DY_M-50-H-200to400', 'DY_M-50-H-400to600', 'DY_M-50-H-600toInf'] +\
               ['DY_M-5to50-H-0to100', 'DY_M-5to50-H-200to400', 'DY_M-5to50-H-400to600', 'DY_M-5to50-H-600toInf'],

           # "VV": ["WZ", "WW", "ZZ"],
           # "W": ["WJets"],
           # "ZTT": ["ZTT"],
           # "ZLL": ["ZL", "ZJ"],
           # "ZL": ["ZL"],
           # "ZJ": ["ZJ"],

           # "QCD": ["dataSS", "-MCSS"],
           # "data_obs": ["dataOS"],

           "QCD": ["dataLoose", "-MCLoose"],
           "data_obs": ["dataTight"],
           }
    for m in masses:
        out["ggH%d" % m] = ["Zprime_%d" % m]

    checkProcs(out)
    return out


def procs2(variable="", category=""):
    """first character '*' means unit normalize and then use factor"""
    assert variable
    assert category
    # out = {"VV": ["*VV", "*singleT"],
    #        "ZLL": ["*ZLL"],
    #        }
    return {}


def isData(proc):
    return proc.startswith("data")

def isDataEmbedded(proc):
    return proc.startswith("DY_embed")  # fixme: dimuon


def isMcEmbedded(proc):
    return proc.endswith("tt_embed")  # first character may be minus sign


def isSignal(proc):
    return any([proc.startswith(p) for p in ["ggH", "ggA", "ggGraviton", "ggRadion", "bbH"]])


def reportExtra(proc):
    # don't report about MC DY and W, which are typically not used
    if proc.startswith("DY") and proc.endswith("JetsToLL"):
        return False
    if proc.startswith("W") and proc.endswith("JetsToLNu"):
        return False
    return True


def cats():
    print "FIXME: cfg.cats()"
    return " ".join([s[-4] for s in sorted(categories.values())])


def workDir():
    return "/".join(__file__.split("/")[:-1])



def variable():
    fm_bins_old= (4, 250.0, 410.0)
    fm_bins_lt = [200, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 500, 550, 600, 650, 700]
    fm_bins_tt = [200, 250, 280, 310, 340, 370, 400, 500, 600, 700]

    preselection = {}
    fMass = {"fMassKinFit": (0.0, None)}
    #chi2 = {"chi2KinFit2": (0.0, 10.0)}
    mass_windows = {"mJJ": (70.0, 150.0), "svMass": (90.0, 150.0)}
    mass_windows.update(fMass)

    ## bins are either a tuple: (n, xMin, xMax)
    ##  or
    ## a list of bin lower edges
    # out = {"var": "m_vis", "bins": range(0, 200, 10) + range(200, 325, 25), "cuts": {}}
    out = {"var": "m_vis", "bins": range(0, 300, 50) + [300, 400, 600, 800, 1200], "cuts": {}}
    return out


def mkdir(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno != 17:
            raise e


def outFileName(sFactor=0, sKey="", var="", cuts={}, tag="", **_):
    stem = root_dest + "/"
    mkdir(stem)

    if sFactor:
        print "FIXME: sFactor"
        stem += "%dx%s" % (sFactor, sKey.replace("H2hh", ""))
    stem += var
    if cutDesc(cuts):
        stem += "_%s" % cutDesc(cuts)

    return "%s%s.root" % (stem, tag)


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


def checkProcs(d):
    fakeBkgs = []
    lst = []
    for k, v in d.iteritems():
        if type(v) != list:
            sys.exit("ERROR: type of '%s' is not list." % str(v))
        else:
            lst += v

        if len(v) == 1 and v[0] == k:  # FIXME: condition is imperfect
            fakeBkgs.append(k)

    if len(set(lst)) != len(lst):
        sys.exit("ERROR: procs values has duplicates: %s." % str(sorted(lst)))

    fakeBkgs = list(set(fakeBkgs))
    if fakeBkgs:
        print "FIXME: include", sorted(fakeBkgs)
