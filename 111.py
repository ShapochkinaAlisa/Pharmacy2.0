from Samples.mapapi_PG import show_map
from Samples.geocoder import get_coordinates, get_ll_span
from Samples.business import find_business, find_businesses
from Samples.distance import lonlat_distance
import sys

adress = ' '.join(sys.argv[1:])
lon, lat = get_coordinates(adress)
res = get_ll_span(adress)
param1 = f'{lon},{lat}'
param2 = "&spn=3,3"
result = find_businesses(param1, res[1], 'аптека')
result_coords_apt = ''
s = -12
my = []
krug = []
eg = []
net = []
for i in result[:10]:
        rt = i["geometry"]["coordinates"]
        t = i["properties"]["CompanyMetaData"]["Hours"]["text"]
        if "круглосуточно" in t:
                a, b = rt
                w = str(a) + "," + str(b)
                krug.append(w)
        elif "-" in t:
                a, b = rt
                w = str(a) + "," + str(b)
                eg.append(w)
        else:
                a, b = rt
                w = str(a) + "," + str(b)
                net.append(w)
        st = lonlat_distance([lon, lat], rt)
        my.append(rt)
        if st > s:
                s = st
                result_coords_apt = rt
cor = ''
for i in range(len(krug)):
        cor += krug[i]
        cor += ','
        cor += 'pmgnm~'
if net:
        for i in range(len(eg)):
                cor += eg[i]
                cor += ','
                cor += 'pmblm~'
        for i in range(len(net)):
                cor += net[i]
                cor += ','
                if i + 1 == len(net):
                        cor += 'pmgrm'
                else:
                        cor += 'pmgrm~'
else:
        for i in range(len(eg)):
                cor += ','
                if i + 1 == len(net):
                        cor += 'pmblm'
                else:
                        cor += 'pmblm~'
d = round(float(s) * 0.00001, 4)
lon_apt, lat_apt = result_coords_apt
show_map(ll_spn=f"ll={res[0]}&spn={d},{d}", add_params=f"pt={cor}")

