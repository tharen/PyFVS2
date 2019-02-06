"""
Python FVS wrappers using ctypes.
"""

import ctypes as ct

import numpy as np
import pandas as pd

from commons_ctypes import *

pd.options.display.float_format = '{:.3f}'.format

class FVSLib(object):
    def __init__(self, variant):
        self.libname = 'libFVS_{}'.format(variant.lower())
        self.fvslib = ct.CDLL(self.libname)

        self.kwdfile = None

        self._spp_codes = None
        self._init_commons()
        
    def _init_commons(self):    
        # Register the common data
        self.glblcntl = FVS_GLBLCNTL.in_dll(self.fvslib, 'glblcntl_')
        self.glblcntlc = FVS_GLBLCNTLC.in_dll(self.fvslib, 'glblcntlc_')
        self.arrays = FVS_ARRAYS.in_dll(self.fvslib, 'arrays_')
        self.pltchr = FVS_PLTCHR.in_dll(self.fvslib, 'pltchr_')
        self.plot = FVS_PLOT.in_dll(self.fvslib, 'plot_')
        self.contrl = FVS_CONTRL.in_dll(self.fvslib, 'contrl_')
        self.outchr = FVS_OUTCHR.in_dll(self.fvslib, 'outchr_')
        self.outcom  = FVS_OUTCOM.in_dll(self.fvslib, 'outcom_')
        self.workcm  = FVS_WORKCM.in_dll(self.fvslib, 'workcm_')

    def set_cmdline(self, kwdfile=None):
        """Set the FVS command line internal variable."""
        if kwdfile is None:
            kwdfile = self.kwdfile
        
        else:
            self.kwdfile = kwdfile

        self.fvslib.fvssetcmdline_.argtypes = [ct.c_char_p, ct.POINTER(ct.c_int), ct.POINTER(ct.c_int), ct.c_int]
        cmdline = '--keywordfile={} '.format(self.kwdfile)
        lencl = ct.c_int(len(cmdline))
        rtn_code = ct.c_int(0)
        self.fvslib.fvssetcmdline_(cmdline.encode(),ct.byref(lencl),ct.byref(rtn_code),len(cmdline))
        
        if not rtn_code.value==0:
            raise IOError('Failed to set the FVS command line variable: {}'.format(cmdline))

    def run_kwds(self, kwdfile=None):
        """Run FVS for keyword file."""

        self.set_cmdline(kwdfile)

        self.fvslib.fvs_.argtypes = [ct.POINTER(ct.c_int),]
        rtn_code = ct.c_int(0)
        self.fvslib.fvs_(ct.byref(rtn_code))

        if not rtn_code.value==0:
            raise IOError('Error while executing FVS for keyword file: {}'.format(self.kwdfile))
    
    @property
    def num_cycles(self):
        """Return the number of cycles in the current run."""
        return self.contrl.ncyc
        
    @property
    def cycle(self):
        """Return the current cycle number."""
        return self.contrl.icyc
        
    @property
    def num_trees(self):
        """Return the current number of tree records."""
        return self.contrl.itrn
        
    @property
    def fvs_spp(self):
        """Return a list of numeric FVS species codes."""
        return pd.Series([''.join([v.decode() for v in s]).strip() for s in self.pltchr.jsp])

    @property
    def fia_spp(self):
        """Return a list of numeric FIA species codes."""
        return pd.Series([''.join([v.decode() for v in s]) for s in self.pltchr.fiajsp])
        
    @property
    def pln_spp(self):
        """Return a list of alpha/numeric PLANTS database species codes."""
        return pd.Series([''.join([v.decode() for v in s]).strip() for s in self.pltchr.plnjsp])
        
    @property
    def spp_codes(self):
        """
        Return a Pandas dataframe of the species codes the variant
        """
        if self._spp_codes is None:
            self._spp_codes = pd.DataFrame(dict((
                    ('spp',self.fvs_spp),
                    ('fia',self.fia_spp),
                    ('pln',self.pln_spp)
                    )))
        
        return self._spp_codes
    
    @property
    def dbh(self):
        """Return a Pandas Series representing the DBH of the current treelist."""
        return pd.Series(self.arrays.dbh[0:self.contrl.itrn])

    @property
    def spp(self):
        """Return a Pandas Series representing the species codes of the current treelist."""
        return pd.Series(self.arrays.isp[0:self.contrl.itrn])
    
    @property
    def tpa(self):
        return pd.Series(self.arrays.prob[0:self.contrl.itrn])/self.plot.grospc
    
    @property
    def trees(self):
        """Return a Pandas DataFrame representing the current treelist."""
        df = pd.DataFrame(dict((
            ('treeid', self.arrays.idtree[0:self.contrl.itrn]),
            ('spp', self.arrays.isp[0:self.contrl.itrn]),
            ('tpa', self.arrays.prob[0:self.contrl.itrn]),
            ('mort', self.arrays.wk2[0:self.contrl.itrn]),
            ('dbh', self.arrays.dbh[0:self.contrl.itrn]),
            ('dg', self.arrays.dg[0:self.contrl.itrn]),
            ('ht', self.arrays.ht[0:self.contrl.itrn]),
            ('htg', self.arrays.htg[0:self.contrl.itrn]),
            ('cr', self.arrays.icr[0:self.contrl.itrn]),
            ('cw', self.arrays.crwdth[0:self.contrl.itrn]),
            ('bapctl', self.arrays.pct[0:self.contrl.itrn]),
            # ('batlg', self.varcom.ptbalt[0:self.contrl.itrn]),
            ('tcfv', self.arrays.cfv[0:self.contrl.itrn]),
            ('mcfv', self.arrays.wk1[0:self.contrl.itrn]),
            ('mbfv', self.arrays.bfv[0:self.contrl.itrn]),
            )))
        
        df['tpa'] /= self.plot.grospc
        df['mort'] /= self.plot.grospc
        
        return df.sort_values(['spp','treeid'])
    
    @property
    def summary(self):
        """Return the summary table the current run."""
        return np.ctypeslib.as_array(self.outcom.iosum)[:self.num_cycles+1]

def test():
    kwdfile = 'c:/workspace/pyfvs2/data/pnt01.key'
    
    fvs = FVSLib('pn')
    fvs.run_kwds(kwdfile)

    # print(fvs.trees)
    print(fvs.summary)
    print()
    print(fvs.contrl.iy[0:25])

    # print(fvs.outcom.iosum[0:fvs.num_cycles][0:20])


    # fvs.fvssetcmdline_.argtypes = [fchar, ct.POINTER(ct.c_int), ct.POINTER(ct.c_int)]

    # cmdline = '--keywordfile={} '.format(kwdfile)
    # _cmdline = fchar()
    # _cmdline.str = cmdline.encode()
    # _cmdline.len = len(cmdline)+1

    # lencl = ct.c_int(len(cmdline))
    # rtn_code = ct.c_int(0)
    # fvs.fvssetcmdline_(_cmdline,ct.byref(lencl),ct.byref(rtn_code))


    # # Set the keyword file directly
    # glblcntlc.keywordfile = kwdfile.encode()
    # fvs.filopn_()
    # glblcntl.fvsrtncode = 0

    # print('***', glblcntlc.keywordfile.strip())


    # print('\n')
    # print('DBH', arrays.dbh[0:5])
    # print('DG', arrays.dg[0:5])
    # print('CFV TD', arrays.ht2td[0][0:5])
    # print('BFV TD', arrays.ht2td[1][0:5])
    # print('PROB', arrays.prob[0:5])
    # print('HT', arrays.ht[0:5])
    # print('ISP', arrays.isp[0:5])

    # print('FIAJSP', [''.join([v.decode() for v in s]) for s in pltchr.fiajsp])
    # print('JSP', [''.join([v.decode() for v in s]) for s in pltchr.jsp])

if __name__=='__main__':
    test()