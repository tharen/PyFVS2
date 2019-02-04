"""
PyFVS wrappers using the cffi foreign function interface library.
"""

import os

from cffi import FFI

root = os.path.dirname(__file__)
print(root)

kwdfile = 'c:/workspace/pyfvs2/data/pnt01.key'

variant = 'pn'
#libname = '{root}/bin/libFVS_{variant}.dll'.format(**locals())'
libname = 'libFVS_pn'

ffi = FFI()
fvs = ffi.dlopen(libname)

ffi.cdef(
	"""
	void fvs_(int* rtn);
	""")

ffi.cdef(
	"""
	void fvsSetCmdLine_(char *cmdline, int lencl, int* rtn);
	""")

s = '--keywordfile={}'.format(kwdfile)
cmdline = bytes(s.encode())

_cmdline = ffi.new('char[]', cmdline)
_lencl = ffi.new('int',len(cmdline))
_rtn = ffi.new('int* rtn',0)

fvs.fvsSetCmdLine_(_cmdline, _lencl, _rtn)
fvs.fvs_(rtn)

