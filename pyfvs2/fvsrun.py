"""
Run the FVS grow loop.
"""

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

# Make sure num cycles is in a workable range
if fvs.contrl.ncyc<=0:
    fvs.contrl.ncyc = 1

if fvs.contrl.ncyc>MAXCYC:
    fvs.contrl.ncyc = MAXCYC

# Increment the cycle years
for i in range(1, MAXCY1):
    if fvs.contrl.iy[i]==-1:
        fvs.contrl.iy[i] = 10
    fvs.contrl.iy[i] = fvs.contrl.iy[i-1] + fvs.contrl.iy[i]

# Add any requested cycle years (CYCLEAT)
if fvs.workcm.iwork1[0]>0:
    nyears = fvs.workcm.iwork1[0]
    for year in fvs.workcm.iwork1[1:nyears+1]:
        if (year<fvs.contrl.iy[0]
            or year>fvs.contrl.iy[fvs.contrl.ncyc+1]):
            # if the requested year not valid then skip it
            continue
        else:
            n = fvs.contrl.ncyc
            for i in range(0,n):
                # insert valid requested years
                if (year>fvs.contrl.iy[i]
                    and year<fvs.contrl.iy[i+1]):
                    # increment the number of cycles
                    fvs.contrl.ncyc = fvs.contrl.ncyc+1
                    if fvs.contrl.ncyc>MAXCYC:
                        fvs.contrl.ncyc = MAXCYC
                    # shift the years by one cycle
                    for k in reversed(range(i+2,fvs.contrl.ncyc+1)):
                        fvs.contrl.iy[k] = fvs.contrl.iy[k-1]
                    # insert the requested year
                    fvs.contrl.iy[i+1] = year
                    break

# print(fvs.contrl.iy[0:20])

# Process the activity schedule
jostnd = ct.c_long(fvs.contrl.jostnd)
ncyc = ct.c_long(fvs.contrl.ncyc)
fvs.fvslib.opexpn_(ct.byref(jostnd),ct.byref(ncyc),ct.byref(fvs.contrl.iy))
fvs.fvslib.opcycl_(ct.byref(ncyc),ct.byref(fvs.contrl.iy))

if fvs.contrl.itable[3]==0:
    t = ct.c_long(1)
    fvs.fvslib.oplist_(
            ct.byref(t),
            fvs.pltchr.nplt, 
            fvs.pltchr.mgmid, 
            fvs.outchr.ititle, 
            26, 4, 72
            )

fvs.fvslib.setup_()
fvs.fvslib.notre_()

fvs.contrl.icyc = 1

icyc = ct.c_long(fvs.contrl.icyc)
fvs.fvslib.opcset_(ct.byref(icyc))

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
    for i in range(0,itrn):
        # print(fvs.arrays.idtree[i],fvs.arrays.prob[i])
        fvs.arrays.cfv[i] = fvs.arrays.cfv[i]*fvs.arrays.prob[i]
        fvs.arrays.bfv[i] = fvs.arrays.bfv[i]*fvs.arrays.prob[i]
        fvs.arrays.wk1[i] = fvs.arrays.wk1[i]*fvs.arrays.prob[i]

itrn = ct.c_long(fvs.contrl.itrn)
ocv = ct.c_float(fvs.outcom.ocvcur[6])
obf = ct.c_float(fvs.outcom.obfcur[6])
omc = ct.c_float(fvs.outcom.omccur[6])

fvs.fvslib.pctile_(ct.byref(itrn),fvs.arrays.ind,fvs.arrays.cfv,fvs.arrays.wk3,ct.byref(ocv))
fvs.fvslib.dist_(ct.byref(itrn),fvs.outcom.ocvcur,fvs.arrays.wk3)
fvs.fvslib.pctile_(ct.byref(itrn),fvs.arrays.ind,fvs.arrays.bfv,fvs.arrays.wk3,ct.byref(obf))
fvs.fvslib.dist_(ct.byref(itrn),fvs.outcom.obfcur,fvs.arrays.wk3)
fvs.fvslib.pctile_(ct.byref(itrn),fvs.arrays.ind,fvs.arrays.wk1,fvs.arrays.wk3,ct.byref(omc))
fvs.fvslib.dist_(ct.byref(itrn),fvs.outcom.omccur,fvs.arrays.wk3)

# convert per acre volume back to per tree volume
if fvs.contrl.itrn>0:
    for i in range(0,fvs.contrl.itrn):
        fvs.arrays.cfv[i] = fvs.arrays.cfv[i]/fvs.arrays.prob[i]
        fvs.arrays.bfv[i] = fvs.arrays.bfv[i]/fvs.arrays.prob[i]
        fvs.arrays.wk1[i] = fvs.arrays.wk1[i]/fvs.arrays.prob[i]

# assign example trees
fvs.fvslib.extree_()

# COmpute initial statistical description
fvs.fvslib.stats_()

if fvs.contrl.itable[0]==0:
    fvs.fvslib.gheads_(
        fvs.pltchr.nplt,
        fvs.pltchr.mgmid,
        ct.byref(jostnd),
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

# FIXME: What does this do
sdibc = ct.c_float(fvs.plot.sdibc)
sdibc2 = ct.c_float(fvs.plot.sdibc2)
fvs.fvslib.sdicls_(ct.byref(iz),ct.byref(fz),ct.byref(f999),ct.byref(i1),
        ct.byref(sdibc),ct.byref(sdibc2),
        ct.byref(stagea),ct.byref(stageb),
        ct.byref(iz))
sdiac = sdibc
sdiac2 = sdibc2

fvs.fvslib.disply_()

fvs.fvslib.genrpt_()