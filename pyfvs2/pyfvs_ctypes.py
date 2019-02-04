"""
Python FVS wrappers using ctypes.
"""

import ctypes as ct

class fchar(ct.Structure):
	_fields_ = [
		('str', ct.c_char_p),
		('len', ct.c_int)
		]

MAXTRE = 3000
MAXSP = 39

class FVS_glblcntl(ct.Structure):
	_fields_ = [
		('firstwrite', ct.c_int),
		('fvsrtncode', ct.c_int),
		('jdstash', ct.c_int),
		('jstash', ct.c_int),
		('majorstopptcode', ct.c_int),
		('majorstopptyear', ct.c_int),
		('maxstoppts', ct.c_int),
		('minorstopptcode', ct.c_int),
		('minorstopptyear', ct.c_int),
		('oldstopyr', ct.c_int),
		('originalrestartcode', ct.c_int),
		('readfilepos', ct.c_int),
		('restartcode', ct.c_int),
		('seekreadpos', ct.c_int),
		('stopstatcd', ct.c_int),
		]

class FVS_glblcntlc(ct.Structure):
	_fields_ = [
		('keywordfile', ct.c_char * 250),
		('restartfilefile', ct.c_char * 250),
		('stopfile', ct.c_char * 250),
		]

F_REAL = ct.c_float
F_INTEGER = ct.c_int
F_LOGICAL = ct.c_int
class FVS_arrays(ct.Structure):
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

class FVS_pltchr(ct.Structure):
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
		
libname = 'libFVS_pn'
kwdfile = 'c:/workspace/pyfvs2/data/pnt01.key'

fvs = ct.CDLL(libname)

# Register the common data
glblcntl = FVS_glblcntl.in_dll(fvs, 'glblcntl_')
glblcntlc = FVS_glblcntlc.in_dll(fvs, 'glblcntlc_')
arrays = FVS_arrays.in_dll(fvs, 'arrays_')
pltchr = FVS_pltchr.in_dll(fvs, 'pltchr_')

fvs.fvssetcmdline_.argtypes = [fchar, ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]

# cmdline = '--keywordfile={} '.format(kwdfile)
# _cmdline = fchar()
# _cmdline.str = cmdline.encode()
# _cmdline.len = len(cmdline)+1

# lencl = ct.c_int(len(cmdline))
# rtn_code = ct.c_int(0)
# fvs.fvssetcmdline_(_cmdline,ct.byref(lencl),ct.byref(rtn_code))

fvs.fvssetcmdline_.argtypes = [ct.c_char_p, ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int]
fvs.fvs_.argtypes = [ct.POINTER(ct.c_int),]

cmdline = '--keywordfile={} '.format(kwdfile)
lencl = ct.c_int(len(cmdline))
rtn_code = ct.c_int(0)
fvs.fvssetcmdline_(cmdline.encode(),ct.byref(lencl),ct.byref(rtn_code),len(cmdline))

# # Set the keyword file directly
# glblcntlc.keywordfile = kwdfile.encode()
# fvs.filopn_()
# glblcntl.fvsrtncode = 0

# print('***', glblcntlc.keywordfile.strip())

rtn_code = ct.c_int(0)
fvs.fvs_(ct.byref(rtn_code))

print('\n')
print('DBH', arrays.dbh[0:5])
print('DG', arrays.dg[0:5])
print('CFV TD', arrays.ht2td[0][0:5])
print('BFV TD', arrays.ht2td[1][0:5])
print('PROB', arrays.prob[0:5])
print('HT', arrays.ht[0:5])
print('ISP', arrays.isp[0:5])

print('FIAJSP', [''.join([v.decode() for v in s]) for s in pltchr.fiajsp])
print('JSP', [''.join([v.decode() for v in s]) for s in pltchr.jsp])