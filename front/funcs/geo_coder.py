from geopy.geocoders import Nominatim

def get_coords(name):

    name = name.lower()
    out = ['msk','мск','москва','масква','столица']
    x = []

    for word in name.split():
        if word not in out:
            x.append(word)

    search = ' '.join(x)


    geolocator = Nominatim(user_agent="Stiven")
    ret = geolocator.geocode(f'Москва, {search}', timeout = 20)
    if ret is None:
        return None
    return ret.latitude, ret.longitude

def coord_tg(place):
    return get_coords(place)