"""
FVS common data structures.
"""

import ctypes as ct

import numpy as np

MAXPLT = 500
MAXTRE = 3000
MAXSP = 39
MAXSTR = 20
MAXCYC = 40
MAXCY1 = 41

F_REAL = ct.c_float
F_INTEGER = ct.c_long
F_LOGICAL = ct.c_int
F_CHAR = ct.c_char

# # Structure to represent a fortran character string
# class FCHAR(ct.Structure):
    # _fields_ = [
        # ('str', ct.c_char_p),
        # ('len', F_INTEGER)
        # ]

class FVS_GLBLCNTL(ct.Structure):
    _fields_ = [
        ('firstwrite', F_INTEGER),
        ('fvsrtncode', F_INTEGER),
        ('jdstash', F_INTEGER),
        ('jstash', F_INTEGER),
        ('majorstopptcode', F_INTEGER),
        ('majorstopptyear', F_INTEGER),
        ('maxstoppts', F_INTEGER),
        ('minorstopptcode', F_INTEGER),
        ('minorstopptyear', F_INTEGER),
        ('oldstopyr', F_INTEGER),
        ('originalrestartcode', F_INTEGER),
        ('readfilepos', F_INTEGER),
        ('restartcode', F_INTEGER),
        ('seekreadpos', F_INTEGER),
        ('stopstatcd', F_INTEGER),
        ]

class FVS_GLBLCNTLC(ct.Structure):
    _fields_ = [
        ('keywordfile', ct.c_char * 250),
        ('restartfilefile', ct.c_char * 250),
        ('stopfile', ct.c_char * 250),
        ]

class FVS_ARRAYS(ct.Structure):
    """
    ARRAYS Common block (ARRAYS.F77)
    """
    _fields_ = [
        ('abirth', F_REAL * MAXTRE),
        ('bfv', F_REAL * MAXTRE),
        ('cfv', F_REAL * MAXTRE),
        ('crwdth', F_REAL * MAXTRE),
        ('damsev', (F_INTEGER * 6)*MAXTRE),
        ('dbh', F_REAL * MAXTRE),
        ('defect', F_INTEGER * MAXTRE),
        ('dg', F_REAL * MAXTRE),
        ('ht', F_REAL * MAXTRE),
        ('ht2td', (F_REAL * MAXTRE)*2),
        ('htg', F_REAL * MAXTRE),
        ('icr', F_INTEGER * MAXTRE),
        ('idtree', F_INTEGER * MAXTRE),
        ('imc', F_INTEGER * MAXTRE),
        ('ind', F_INTEGER * MAXTRE),
        ('ind1', F_INTEGER * MAXTRE),
        ('ind2', F_INTEGER * MAXTRE),
        ('isp', F_INTEGER * MAXTRE),
        ('ispecl', F_INTEGER * MAXTRE),
        ('itre', F_INTEGER * MAXTRE),
        ('itrunc', F_INTEGER * MAXTRE),
        ('kutkod', F_INTEGER * MAXTRE),
        ('lbirth', F_LOGICAL * MAXTRE),
        ('normht', F_INTEGER * MAXTRE),
        ('oldpct', F_REAL * MAXTRE),
        ('oldrn', F_REAL * MAXTRE),
        ('pct', F_REAL * MAXTRE),
        ('pltsiz', F_REAL * MAXTRE),
        ('prob', F_REAL * MAXTRE),
        ('wk1', F_REAL * MAXTRE),
        ('wk2', F_REAL * MAXTRE),
        ('wk3', F_REAL * MAXTRE),
        ('wk4', F_REAL * MAXTRE),
        ('wk5', F_REAL * MAXTRE),
        ('wk6', F_REAL * MAXTRE),
        ('yrdlos', F_REAL * MAXTRE),
        ('zrand', F_REAL * MAXTRE),
        ]

class FVS_PLTCHR(ct.Structure):
    """
    PLTCHR Common block (PLOT.F77)
    """
    _fields_ = [
        ('cpvref', ct.c_char*10),
        ('dbcn', ct.c_char*40),
        ('fiajsp', (ct.c_char*4)*MAXSP),
        ('jsp', (ct.c_char*4)*MAXSP),
        ('mgmid', ct.c_char*4),
        ('nplt', ct.c_char*26),
        ('nsp', ((ct.c_char*4)*MAXSP)*3),
        ('plnjsp', (ct.c_char*6)*MAXSP),
        ]

class FVS_PLOT(ct.Structure):
    """
    PLOT Common block (PLOT.F77)
    """
    _fields_ = [
        ('aspect', F_REAL),
        ('atavd', F_REAL),
        ('atavh', F_REAL),
        ('atba', F_REAL),
        ('atccf', F_REAL),
        ('atsdix', F_REAL),
        ('attpa', F_REAL),
        ('avh', F_REAL),
        ('ba', F_REAL),
        ('baf', F_REAL),
        ('barank', F_REAL*MAXSP),
        ('brk', F_REAL),
        ('btsdix', F_REAL),
        ('covmlt', F_REAL),
        ('covyr', F_REAL),
        ('elev', F_REAL),
        ('fint', F_REAL),
        ('fpa', F_REAL),
        ('grospc', F_REAL),
        ('iage', F_INTEGER),
        ('iaspec', F_INTEGER),
        ('icage', F_INTEGER),
        ('icnty', F_INTEGER),
        ('ifint', F_INTEGER),
        ('ifor', F_INTEGER),
        ('ifortp', F_INTEGER),
        ('igl', F_INTEGER),
        ('imodty', F_INTEGER),
        ('iphreg', F_INTEGER),
        ('iptinv', F_INTEGER),
        ('ipvec', F_INTEGER*MAXPLT),
        ('isisp', F_INTEGER),
        ('islop', F_INTEGER),
        ('ismall', F_INTEGER),
        ('istate', F_INTEGER),
        ('istcl', F_INTEGER),
        ('iszcl', F_INTEGER),
        ('iF_REAL', F_INTEGER),
        ('jspin', F_INTEGER*MAXSP),
        ('jspindef', F_INTEGER),
        ('jF_REAL', F_INTEGER*122),
        ('kodfor', F_INTEGER),
        ('kodtyp', F_INTEGER),
        ('managd', F_INTEGER),
        ('nonstk', F_INTEGER),
        ('nsitet', F_INTEGER),
        ('oldavh', F_REAL),
        ('oldba', F_REAL),
        ('oldtpa', F_REAL),
        ('ormsqd', F_REAL),
        ('pi', F_REAL),
        ('pmsdil', F_REAL),
        ('pmsdiu', F_REAL),
        ('relden', F_REAL),
        ('reldm1', F_REAL),
        ('reldsp', F_REAL*MAXSP),
        ('rmai', F_REAL),
        ('rmsqd', F_REAL),
        ('samwt', F_REAL),
        ('sdiac', F_REAL),
        ('sdiac2', F_REAL),
        ('sdibc', F_REAL),
        ('sdibc2', F_REAL),
        ('sdidef', F_REAL*MAXSP),
        ('sdimax', F_REAL),
        ('sitear', F_REAL*MAXSP),
        ('sitetr', (F_REAL*MAXSTR)*6),
        ('slope', F_REAL),
        ('stndsi', F_REAL),
        ('tfpa', F_REAL),
        ('tlat', F_REAL),
        ('tlong', F_REAL),
        ('tprob', F_REAL),
        ('vmlt', F_REAL),
        ('vmltyr', F_REAL),
        ]

class FVS_CONTRL(ct.Structure):
    _fields_ = [
        ('auteff', F_REAL),
        ('autmax', F_REAL),
        ('autmin', F_REAL),
        ('bamax', F_REAL),
        ('bamin', F_REAL),
        ('bfmin', F_REAL),
        ('cccoef', F_REAL),
        ('cccoef2', F_REAL),
        ('cfmin', F_REAL),
        ('dbhmin', F_REAL*MAXSP),
        ('dbhsdi', F_REAL),
        ('dbhstage', F_REAL),
        ('dbhzeide', F_REAL),
        ('dgsd', F_REAL),
        ('dr016', F_REAL),
        ('eff', F_REAL),
        ('fintm', F_REAL),
        ('frmcls', F_REAL*MAXSP),
        ('ibegin', F_INTEGER*MAXSP),
        ('iccode', F_INTEGER),
        ('icflag', F_INTEGER),
        ('icl1', F_INTEGER),
        ('icl2', F_INTEGER),
        ('icl3', F_INTEGER),
        ('icl4', F_INTEGER),
        ('icl5', F_INTEGER),
        ('icl6', F_INTEGER),
        ('icyc', F_INTEGER),
        ('idg', F_INTEGER),
        ('ifst', F_INTEGER),
        ('ins', F_INTEGER*6),
        ('iptgrp', (F_INTEGER*30)*52),
        ('iread', F_INTEGER),
        ('irec1', F_INTEGER),
        ('irec2', F_INTEGER),
        ('irecnt', F_INTEGER),
        ('irecrd', F_INTEGER),
        ('iref', F_INTEGER*MAXSP),
        ('isct', (F_INTEGER*MAXSP)*2),
        ('ispgrp', (F_INTEGER*30)*52),
        ('istdat', F_INTEGER),
        ('itable', F_INTEGER*7),
        ('ithnpa', F_INTEGER),
        ('ithnpi', F_INTEGER),
        ('ithnpn', F_INTEGER),
        ('itrn', F_INTEGER),
        ('iy', F_INTEGER*MAXCY1),
        ('jocalb', F_INTEGER),
        ('jolist', F_INTEGER),
        ('jostnd', F_INTEGER),
        ('josum', F_INTEGER),
        ('jotree', F_INTEGER),
        ('kount', F_INTEGER*MAXSP),
        ('kptr', F_INTEGER*MAXSP),
        ('lauton', F_LOGICAL),
        ('lbkden', F_LOGICAL),
        ('lbvols', F_LOGICAL),
        ('lcvols', F_LOGICAL),
        ('ldcor2', F_LOGICAL),
        ('ldgcal', F_LOGICAL*MAXSP),
        ('ldubdg', F_LOGICAL),
        ('leavesp', F_LOGICAL*MAXSP),
        ('lfia', F_LOGICAL),
        ('lfire', F_LOGICAL),
        ('lflag', F_LOGICAL),
        ('lhtdrg', F_LOGICAL*MAXSP),
        ('lmort', F_LOGICAL),
        ('lrcor2', F_LOGICAL),
        ('lsite', F_LOGICAL),
        ('lstart', F_LOGICAL),
        ('lstknt', F_INTEGER),
        ('lsumry', F_LOGICAL),
        ('ltrip', F_LOGICAL),
        ('lzeide', F_LOGICAL),
        ('methb', F_INTEGER*MAXSP),
        ('methc', F_INTEGER*MAXSP),
        ('mordat', F_LOGICAL),
        ('ncyc', F_INTEGER),
        ('notrip', F_LOGICAL),
        ('nptgrp', F_INTEGER),
        ('nspgrp', F_INTEGER),
        ('nstknt', F_INTEGER),
        ('numsp', F_INTEGER),
        ('pbawt', F_REAL),
        ('pccfwt', F_REAL),
        ('ptpawt', F_REAL),
        ('rcor2', F_REAL*MAXSP),
        ('sizcap', (F_REAL*MAXSP)*4),
        ('spclwt', F_REAL),
        ('stmp', F_REAL*MAXSP),
        ('tcfmin', F_REAL),
        ('tcwt', F_REAL),
        ('topd', F_REAL*MAXSP),
        ('trm', F_REAL),
        ('yr', F_REAL),
        ]
        
class FVS_OUTCHR(ct.Structure):
    _fields_ = [
        ('ionsp', (F_CHAR*3)*6),
        ('iospac', (F_CHAR*3)*4),
        ('iospbr', (F_CHAR*3)*4),
        ('iospbv', (F_CHAR*3)*4),
        ('iospct', (F_CHAR*3)*4),
        ('iospcv', (F_CHAR*3)*4),
        ('iospmc', (F_CHAR*3)*4),
        ('iospmo', (F_CHAR*3)*4),
        ('iospmr', (F_CHAR*3)*4),
        ('iosprt', (F_CHAR*3)*4),
        ('iosptt', (F_CHAR*3)*4),
        ('iosptv', (F_CHAR*3)*4),
        ('ititle', F_CHAR*72),
        ]
        
        
class FVS_OUTCOM(ct.Structure):
    _fields_ = [
        ('dbhio', F_REAL*6),
        ('dgio', F_REAL*6),
        ('htio', F_REAL*6),
        ('ioicr', F_INTEGER*6),
        ('iosum', (F_INTEGER*20)*MAXCY1),
        # ('c_iosum', ct.POINTER(F_INTEGER)),
        ('oacc', F_REAL*7),
        ('obfcur', F_REAL*7),
        ('obfrem', F_REAL*7),
        ('ocvcur', F_REAL*7),
        ('ocvrem', F_REAL*7),
        ('omccur', F_REAL*7),
        ('omcrem', F_REAL*7),
        ('omort', F_REAL*7),
        ('ontcur', F_REAL*7),
        ('ontrem', F_REAL*7),
        ('ontres', F_REAL*7),
        ('ospac', F_REAL*4),
        ('ospbr', F_REAL*4),
        ('ospbv', F_REAL*4),
        ('ospct', F_REAL*4),
        ('ospcv', F_REAL*4),
        ('ospmc', F_REAL*4),
        ('ospmo', F_REAL*4),
        ('ospmr', F_REAL*4),
        ('osprt', F_REAL*4),
        ('osptt', F_REAL*4),
        ('osptv', F_REAL*4),
        ('pctio', F_REAL*6),
        ('prbio', F_REAL*6),
    ]
    
    # def __init__(self,*args,**kwargs):
    #     super(FVS_OUTCOM,self).__init__(*args,**kwargs)
    #     self.iosum = np.zeros((20, MAXCY1), dtype="int16")
    #     self.c_iosum = np.ctypeslib.as_ctypes(self.iosum)

class FVS_WORKCM(ct.Structure):
    _fields_ = [
        ('iwork1', F_INTEGER*MAXTRE),
        ('work1', F_INTEGER*MAXTRE),
        ('work2', F_INTEGER*MAXSP),
        ('work3', F_INTEGER*MAXTRE),
    ]

class FVS_VARCHR(ct.Structure):
    _fields_ = [
        ('pcom', F_CHAR*8),
        ('pcomx', F_CHAR*8)
    ]

class FVS_VARCOM(ct.Structure):
    _fields_ = [
        ('aa', F_REAL*MAXSP),
        ('b0accf', F_REAL*MAXSP),
        ('b0astd', F_REAL*MAXSP),
        ('b0bccf', F_REAL*MAXSP),
        ('b1accf', F_REAL*MAXSP),
        ('b1bccf', F_REAL*MAXSP),
        ('b1bstd', F_REAL*MAXSP),
        ('bb', F_REAL*MAXSP),
        ('cepmrt', F_REAL),
        ('cepmsb', F_REAL),
        ('dhimsb', F_REAL),
        ('dlomsb', F_REAL),
        ('effmsb', F_REAL),
        ('htt1', (F_REAL*MAXSP)*9),
        ('htt2', (F_REAL*MAXSP)*9),
        ('iabflg', F_INTEGER*MAXSP),
        ('ibasp', F_INTEGER),
        ('isilft', F_INTEGER),
        ('istagf', F_INTEGER*MAXSP),
        ('lbamax', F_LOGICAL),
        ('lfixsd', F_LOGICAL),
        ('lflagv', F_LOGICAL),
        ('maxsdi', F_INTEGER*MAXSP),
        ('mflmsb', F_INTEGER),
        ('ptbaa', F_REAL*MAXPLT),
        ('ptbalt', F_REAL*MAXTRE),
        ('qmdmsb', F_REAL),
        ('slpmrt', F_REAL),
        ('slpmsb', F_REAL),
        ('tpamrt', F_REAL),
    ]