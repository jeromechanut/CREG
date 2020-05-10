import netCDF4 as netcdf
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


year = 1996
month= 3 
date='year: %s, month: %s' % (year,month)
if (month<10):
	filedata='CREG12_EXT-T002_1d_icemod_y%sm0%s.nc' % (year,month)
else:
	filedata='CREG12_EXT-T002_1d_icemod_y%sm%s.nc' % (year,month)
print(filedata)
#filedata="/sortref/modele/creg/creg12/CREG12-T111/CREG12-T111-MEAN/MONTHLY/CREG12-T111_y2014m03_icemod.nc"
filedata='CREG12_EXT-T001_1d_icemod_20011113-20011113.nc'
nc = netcdf.Dataset(filedata)
lon = nc.variables['nav_lon'][:,:]
lat = nc.variables['nav_lat'][:,:]
h = np.squeeze(nc.variables['sivolu'][0,:,:])
fig, ax = plt.subplots()
fig.set_size_inches(9, 9)
m = Basemap(projection='npstere',boundinglat=65,lon_0=-45,resolution='l')
m.drawcoastlines()
m.drawparallels(np.arange(-80.,81.,20.),labels=[False,True,True,False])
m.drawmeridians(np.arange(-180.,181.,30.),labels=[True,False,False,True])
x, y = m(lon, lat)
h = ma.masked_less_equal(h, 0.1)
#m.pcolormesh(x,y,h, cmap='gist_ncar',vmin=0.,vmax=5.)
m.pcolormesh(x,y,h, cmap='plasma',vmin=0.,vmax=4.)
ax.set_title(date)
cbar = plt.colorbar()
cbar.set_label('THICKNESS')
h[1077,798]=0.
res=np.where(h==np.amax(h))
listOfCordinates = list(zip(res[0], res[1]))
for cord in listOfCordinates:
    print(cord)
print(h[1077,796])
plt.show()

