import os
import sys
import ftplib
import fnmatch
from contextlib import closing
from subprocess import call

def processFiles(outputDir, namePattern):

    for gribFile in os.listdir(outputDir):
        if fnmatch.fnmatch(gribFile, '*' + namePattern):
            print(gribFile)
            call(["grib_to_netcdf", "-o output.nc gribFile"])
            # grib_to_netcdf -o output.nc gribFile

def downloadFiles():

    host = "data-portal.ecmwf.int"
    port = 25
    # login= 'wmo'
    # passwd= 'essential'
    orig_filename = "20170220120000/A_HTXY85ECMF201200_C_ECMF_20170220120000_216h_t_850hPa_global_0p5deg_grib2.bin"
    local_filename = 'last_fc.grib'

    with closing(ftplib.FTP()) as ftp:
        try:
            print('connect')
            ftp.connect(host, port, 30*5) #5 mins timeout
            print('login')
            ftp.login("wmo", "essential")
            ftp.set_pasv(True)

            data = []
            ftp.dir('-t',data.append)

            with open(local_filename, 'w+b') as f:
                res = ftp.retrbinary('RETR %s' % orig_filename, f.write)

                if not res.startswith('226 Transfer complete'):
                    print('Downloaded of file {0} is not compile.'.format(orig_filename))
                    os.remove(local_filename)
                    return None

            print('return')
            return local_filename

        except Exception, e:
                print('Error during download from FTP :'+ str(e))

def main():
    # downloadFiles()
    processFiles("../data", "_gh_500hPa_global_0p5deg_grib2.bin")

if __name__ == "__main__":
    sys.exit(main())
