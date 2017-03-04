# encoding=utf8
import traceback
import sys
import rasterio

INPUT='latest_fc.nc'
VERBOSE=0

def create():

    print('open')
    dataset = rasterio.open(INPUT)
    # print('process')
    profile = dataset.profile
    profile.update(driver='GTiff', crs='+proj=latlong')
    stepData = dataset.read(1)
    print(stepData.shape[1], stepData.shape[0])
    print ('read done')
    with rasterio.open("test.tiff", 'w', **profile) as dst:
        dst.write(stepData, 1)

    # for index in dataset.indexes:
    #     print('Step '+ str(index))
    #     stepData = dataset.read(index)
    #     print ('read')
    #     # Write to tif, using the same profile as the source
    #     output = "file_%s.tif" % index
    #     print(output)
    #     with rasterio.open(output, 'w', **profile) as dst:
    #         dst.write(stepData)
    print ('write done')
    dataset.close()
def main():
    try:
        create()
    except Exception, err:
        print(err)
        # if VERBOSE:
        #     traceback.print_exc(file=sys.stderr)
        # else:
        #     sys.stderr.write(err)

        return 1

if __name__ == "__main__":
    sys.exit(main())
