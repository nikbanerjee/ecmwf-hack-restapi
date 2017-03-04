
# era5_test_2016-01-01_12Z_waveAN.grib

# grib_dump -j era5_test_2016-01-01_12Z_waveAN.grib

import traceback
import sys

from gribapi import *
# from eccodes import *

# INPUT='era5_test_2016-01-01_12Z_waveAN.grib'
INPUT = 'data/mars0.grib'
VERBOSE=1 # verbose error reporting


def example(lat, lon):

        # Get the total number of args passed to the demo.py
    # total = len(sys.argv)

    # Get the arguments list
    # cmdargs = str(sys.argv)

    # Print it
    # print ("The total numbers of args passed to the script: %d " % total)
    # print ("Args list: %s " % cmdargs)

    # points = ((56.,24.), (53.,21.))
    # points = (float(cmdargs[1]),floacmdargs[2]),(13,234))

    f = open(INPUT)
    gid = grib_new_from_file(f)
    nearest = grib_find_nearest(gid,lat,lon)
    for n in nearest:
    # print lat,lon
        print n.index
        # print nearest.lat,nearest.lon,nearest.value,nearest.distance,nearest.index

    # "Snow_depth_surface"
    # v = grib_index_get(gid, "Snow_depth_surface")
    # v = grib_get_size(gid, "2590")
    # print v
    # get nearest index data


    # for lat,lon in points:
    #     nearest = grib_find_nearest(gid,lat,lon)[0]
    #     print lat,lon
    #     print nearest.lat,nearest.lon,nearest.value,nearest.distance,nearest.index

        # four = grib_find_nearest(gid,lat,lon,is_lsm = False,npoints = 4)
        # for i in range(len(four)):
        #     print "- %d -" % i
        #     print four[i]
        #
        # print "-"*100

    grib_release(gid)
    f.close()

# next !!!
def example1():
    f = open(INPUT)

    mcount = grib_count_in_file(f)
    gid_list = [grib_new_from_file(f) for i in range(mcount)]
    print mcount

    f.close()

    keys = [
        'Ni',
        'Nj',
        'latitudeOfFirstGridPointInDegrees',
        'longitudeOfFirstGridPointInDegrees',
        'latitudeOfLastGridPointInDegrees',
        'longitudeOfLastGridPointInDegrees',
        'jDirectionIncrementInDegrees',
        'iDirectionIncrementInDegrees',
        'values'
        ]

    for i in range(mcount):
        gid = gid_list[i]

        print "processing message number",i+1

        for key in keys:
            print '%s=%g' % (key,grib_get(gid,key))

        print 'There are %d, average is %g, min is %g, max is %g' % (
                  grib_get_size(gid,'values'),
                  grib_get(gid,'average'),
                  grib_get(gid,'min'),
                  grib_get(gid,'max')
               )

        print '-'*100

        grib_release(gid)



def example2():
    f = open(INPUT)

    while 1:
        gid = grib_new_from_file(f)
        if gid is None: break

        iterid = grib_keys_iterator_new(gid,'ls')

        # Different types of keys can be skipped
        # grib_skip_computed(iterid)
        # grib_skip_coded(iterid)
        # grib_skip_edition_specific(iterid)
        # grib_skip_duplicates(iterid)
        # grib_skip_read_only(iterid)
        # grib_skip_function(iterid)

        while grib_keys_iterator_next(iterid):
            keyname = grib_keys_iterator_get_name(iterid)
            keyval = grib_get_string(iterid,keyname)
            # if keyval is "2t"
            print "%s = %s" % (keyname,keyval)

        grib_keys_iterator_delete(iterid)
        grib_release(gid)

    f.close()

# ----------------------------------------------


def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def example3():
    index_keys = ["shortName","dataDate","step"]
    index_file = "my.idx"

    iid = None

    if (os.path.exists(index_file)):
        iid = grib_index_read(index_file)
    else:
        iid = grib_index_new_from_file(INPUT,index_keys)

        # multiple files can be added to an index:
        # grib_index_add_file(iid,"grib file to add")

        grib_index_write(iid,index_file)

    index_vals = []

    # ---------------------------------------------
    for key in index_keys:
        print "%sSize=%d" % (
            key,
            grib_index_get_size(iid,key)
        )

        key_vals = grib_index_get(iid,key)
        # print " ".join(key_vals)
        index_vals.append(key_vals)

    searchKey = "sd"
    for prod in product(*index_vals):
        print prod
        # prod_list = filter(lambda a: a[1]=='sd', prod)
        # if prod[0] == searchKey:
        #     print prod[1]

        # for i in range(len(index_keys)):
        #     grib_index_select(iid,index_keys[i],prod[i])
            # print index_keys[i],prod[i]

    #     while 1:
    #         gid = grib_new_from_index(iid)
    #         if gid is None: break
    #         # print " ".join(["%s=%s" % (key,grib_get(gid,key)) for key in index_keys])
    #         grib_release(gid)

    grib_index_release(iid)



def main():
    try:
        # Get the arguments list
        # cmdargs = str(sys.argv)
        # print cmdargs[1], cmdargs[2]
        # lat = float(cmdargs[1])
        # lon = float(cmdargs[2])
        lat = 54.
        lon = 24.
        # example(lat, lon)
        example2()
        # example3()
    except GribInternalError,err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr,err.msg

        return 1

if __name__ == "__main__":
    sys.exit(main())
