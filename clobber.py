#!/usr/bin/env python

import cfg
import os
import ROOT as r


br = cfg.outFileName(**cfg.variable())
it = "%s/src/auxiliaries/shapes/Italians/htt_tt.inputs-Hhh-8TeV_m_ttbb_kinfit_KinFitConvergedWithMassWindow.root" % os.environ["CMSSW_BASE"]

print br
print it

histos = ["data_obs"]

for cat in cfg.categories.values():
    print cat
    for hName in histos:
        fIn = r.TFile(br)
        hIn = fIn.Get("%s/%s" % (cat, hName)).Clone()
        hIn.SetDirectory(0)
        fIn.Close()

        fOut = r.TFile(it, "UPDATE")
        fOut.cd(cat)
        hIn.Write()
        fOut.Close()

