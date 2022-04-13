import mpu

def convertToInt(data):
    if data is None:
        return 0
    else:
        return int(data)

def distanseBeetweenTwoPoints(firstLatitude, firstLongitude, secondLatitude, secondLongitude):
    return mpu.haversine_distance((firstLatitude, firstLongitude), (secondLatitude, secondLongitude))

