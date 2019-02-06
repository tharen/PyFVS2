"""
Run the FVS grow loop.
"""

import numpy as np

import ctypes as ct
from pyfvs_ctypes import FVSLib

MAXPLT = 500
MAXTRE = 3000
MAXSP = 39
MAXSTR = 20
MAXCYC = 40
MAXCY1 = 41

fvs = FVSLib('pn')

kwdfile = 'c:/workspace/pyfvs2/data/pnt01.key'
fvs.set_cmdline(kwdfile)

stagea = ct.c_float(0)
stageb = ct.c_float(0)

fvs.contrl.icl1 = 0
fvs.contrl.lstart = True
fvs.contrl.lflag = True
fvs.contrl.icyc = 0

fvs.fvslib.initre_()
fvs.set_seed()

# Make sure num cycles is in a workable range
if fvs.contrl.ncyc<=0:
    fvs.contrl.ncyc = 1

if fvs.contrl.ncyc>MAXCYC:
    fvs.contrl.ncyc = MAXCYC

# Increment the cycle years by 10 if not set by keyword timeint
fvs.iy[fvs.iy==-1] = 10
# Accumulate the increment
fvs.iy[:] = fvs.iy.cumsum()

# Add any requested cycle years (CYCLEAT)
fvs.iy[:] = np.insert(fvs.iy,0,fvs.workcm.iwork1[1:fvs.workcm.iwork1[0]+1])[:MAXCY1]
fvs.iy.sort()
fvs.contrl.ncyc += fvs.workcm.iwork1[0]

# Process the activity schedule
jostnd = ct.byref(ct.c_long(fvs.contrl.jostnd))
ncyc = ct.byref(ct.c_long(fvs.contrl.ncyc))
iy = ct.byref(fvs.contrl.iy)
fvs.fvslib.opexpn_(jostnd,ncyc,iy)
fvs.fvslib.opcycl_(ncyc,iy)

if fvs.contrl.itable[3]==0:
    t = ct.c_long(1)
    fvs.fvslib.oplist_(
            ct.byref(ct.c_bool(1)),
            fvs.pltchr.nplt, 
            fvs.pltchr.mgmid, 
            fvs.outchr.ititle, 
            26, 4, 72
            )

fvs.fvslib.setup_()
fvs.fvslib.notre_()

fvs.cycle = 1

fvs.fvslib.opcset_(ct.byref(ct.c_long(fvs.cycle)))

# Calibrate growth functions and fill gaps
iz = ct.c_long(0)
i1 = ct.c_long(1)
fz = ct.c_float(0.0)
f999 = ct.c_float(999.0)
sdiac = ct.c_float(fvs.plot.sdiac)
sdiac2 = ct.c_float(fvs.plot.sdiac2)

fvs.fvslib.sdicls_(ct.byref(iz),ct.byref(fz),ct.byref(f999),ct.byref(i1),
        ct.byref(sdiac),ct.byref(sdiac2),
        ct.byref(stagea),ct.byref(stageb),
        ct.byref(iz))
fvs.fvslib.cratet_()

# Set calibration and flag best tree records for estab model
fvs.fvslib.esfltr_()

# Initialize the simulation
fvs.contrl.icyc = 0

# Initialize crown width
fvs.fvslib.cwidth_()
# Initialize tree volume
fvs.fvslib.vols_()

# Initialize volume distribution
# convert tree volume to per acre volume
itrn = fvs.contrl.itrn
if itrn>0:
    fvs.cfv[:itrn] = fvs.cfv[:itrn]*fvs.prob[:itrn]
    fvs.bfv[:itrn] = fvs.bfv[:itrn]*fvs.prob[:itrn]
    fvs.wk1[:itrn] = fvs.wk1[:itrn]*fvs.prob[:itrn]

_itrn = ct.byref(ct.c_long(fvs.contrl.itrn))
ocv = ct.byref(ct.c_float(fvs.outcom.ocvcur[6]))
obf = ct.byref(ct.c_float(fvs.outcom.obfcur[6]))
omc = ct.byref(ct.c_float(fvs.outcom.omccur[6]))

fvs.fvslib.pctile_(_itrn, fvs.ind.ctypes, fvs.cfv.ctypes, fvs.wk3.ctypes, ocv)
fvs.fvslib.dist_(_itrn, fvs.outcom.ocvcur, fvs.wk3.ctypes)
fvs.fvslib.pctile_(_itrn, fvs.ind.ctypes, fvs.bfv.ctypes, fvs.wk3.ctypes, obf)
fvs.fvslib.dist_(_itrn, fvs.outcom.obfcur, fvs.wk3.ctypes)
fvs.fvslib.pctile_(_itrn, fvs.ind.ctypes, fvs.wk1.ctypes, fvs.wk3.ctypes, omc)
fvs.fvslib.dist_(_itrn, fvs.outcom.omccur, fvs.wk3.ctypes)

# convert per acre volume back to per tree volume
itrn = fvs.contrl.itrn
if itrn>0:
    fvs.cfv[:itrn] = fvs.cfv[:itrn]/fvs.prob[:itrn]
    fvs.bfv[:itrn] = fvs.bfv[:itrn]/fvs.prob[:itrn]
    fvs.wk1[:itrn] = fvs.wk1[:itrn]/fvs.prob[:itrn]

# assign example trees
fvs.fvslib.extree_()

# COmpute initial statistical description
fvs.fvslib.stats_()

if fvs.contrl.itable[0]==0:
    fvs.fvslib.gheads_(
        fvs.pltchr.nplt,
        fvs.pltchr.mgmid,
        jostnd,
        ct.byref(iz),
        fvs.outchr.ititle
    )

# Write initial statistics
fvs.contrl.icl6 = 1
fvs.fvslib.disply_()

fvs.fvslib.prtrls_(ct.byref(i1))

#FIXME: fvs.f line 294, what is MAXTP1
# fvs.contrl.irec2 = MAXTP1

fvs.contrl.lstart = False
fvs.contrl.lflag = False

# initialize the event monitor variables
neg1 = ct.c_long(-1)
fvs.fvslib.evtstv_(ct.byref(neg1))

# Run the growth routines in a loop
for cycle in range(1,fvs.contrl.ncyc+1):
    fvs.contrl.icyc = fvs.contrl.icyc+1

    fvs.fvslib.tregro_()

    fvs.fvslib.extree_()

    fvs.fvslib.disply_()

    fvs.fvslib.resage_()

    fvs.fvslib.prtrls_(ct.byref(i1))

# Finalize the run
fvs.contrl.icyc = fvs.contrl.icyc+1

# FIXME: Is this necessary
fvs.contrl.icl6 = -99
fvs.outcom.ontrem[6] = 0.0
fvs.plot.oldtpa = fvs.plot.tprob
fvs.plot.oldba = fvs.plot.ba
fvs.plot.oldavh = fvs.plot.avh
fvs.plot.ormsqd = fvs.plot.rmsqd
fvs.plot.reldm1 = fvs.plot.relden

# Compute SDI - entry sdicls in sdical.f
sdibc = ct.c_float(fvs.plot.sdibc)
sdibc2 = ct.c_float(fvs.plot.sdibc2)
fvs.fvslib.sdicls_(ct.byref(iz),ct.byref(fz),ct.byref(f999),ct.byref(i1),
        ct.byref(sdibc),ct.byref(sdibc2),
        ct.byref(stagea),ct.byref(stageb),
        ct.byref(iz))
fvs.plot.sdiac = sdibc
fvs.plot.sdiac2 = sdibc2

# print(sdibc, sdibc2)
# print(fvs.plot.sdibc,fvs.plot.sdibc2)

fvs.fvslib.disply_()

fvs.fvslib.genrpt_()
fvs.fvslib.filclose_()
# fvs = None

# print(fvs.trees)
