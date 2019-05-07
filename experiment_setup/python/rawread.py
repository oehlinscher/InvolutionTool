# MIT license: https://opensource.org/licenses/MIT
# Taken from https://gist.github.com/snmishra/27dcc624b639c2626137

from __future__ import division
import numpy as np
BSIZE_SP = 512 # Max size of a line of data; we don't want to read the
               # whole file to find a line, in case file does not have
               # expected structure.
MDATA_LIST = [b'title', b'date', b'plotname', b'flags', b'no. variables',
              b'no. points', b'dimensions', b'command', b'option']
DECODE = 'ascii' # 'ascii'
FLOATENCODEING = '>f8' # spectre
# FLOATENCODEING = '<f8' # ngspice


def rawread(fname: str):
    """Read ngspice binary raw files. Return tuple of the data, and the
    plot metadata. The dtype of the data contains field names. This is
    not very robust yet, and only supports ngspice.
    >>> darr, mdata = rawread('test.py')
    >>> darr.dtype.names
    >>> plot(np.real(darr['frequency']), np.abs(darr['v(out)']))
    """
    # Example header of raw file
    # Title: rc band pass example circuit
    # Date: Sun Feb 21 11:29:14  2016
    # Plotname: AC Analysis
    # Flags: complex
    # No. Variables: 3
    # No. Points: 41
    # Variables:
    #         0       frequency       frequency       grid=3
    #         1       v(out)  voltage
    #         2       v(in)   voltage
    # Binary:
    fp = open(fname, 'rb')
    plot = {}
    count = 0
    arrs = []
    plots = []
    while (True):
        try:
            mdata = fp.readline(BSIZE_SP).split(b':', maxsplit=1)
        except:
            raise
        if len(mdata) == 2:
            if mdata[0].lower() in MDATA_LIST:
                plot[mdata[0].lower()] = mdata[1].strip()
            if mdata[0].lower() == b'variables':
                nvars = int(plot[b'no. variables'])
                npoints = int(plot[b'no. points'])
                plot['varnames'] = []
                plot['varunits'] = []

                first = True
                for varn in range(nvars):

                    #hack for the probem that the "variables: " line contains already 0 ....
                    if first and (b'0' in mdata[1]):
                        varspec = (mdata[1].strip()
                               .decode(DECODE).split())                        

                    else:
                        varspec = (fp.readline(BSIZE_SP).strip()
                                   .decode(DECODE).split())
                        #print(str(varspec))

                    assert(varn == int(varspec[0]))
                    plot['varnames'].append(varspec[1])
                    plot['varunits'].append(varspec[2])

                    first = False

            if mdata[0].lower() == b'binary':
                #print('hu')
                #print(plot['varnames'])
                #print(plot[b'flags'])
                #print(str(nvars))

                renamed = []
                for name in plot['varnames']:
                    if name in renamed:
                        renamed += [ name + '_prime' ]
                    else:
                        renamed += [ name ]

                rowdtype = np.dtype( {'names': renamed, 'formats': [ FLOATENCODEING ] * nvars} )   #else np.float_]*nvars})
                # We should have all the metadata by now
                arrs.append(np.fromfile(fp, dtype=rowdtype, count=npoints))
                plots.append(plot)
                fp.readline() # Read to the end of line
        else:
            break
    return (arrs, plots)

if __name__ == '__main__':
    arrs, plots = rawread('test.raw')
    print(darr)

# Local Variables:
# mode: python
# End:
