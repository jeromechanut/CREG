import netCDF4 as netcdf
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

filedata='CREG12_EXT-T003_1d_icemod_19970115-19970115.nc'
filedata='CREG12_EXT-T001_1d_icemod_20011113-20011113.nc'
nc = netcdf.Dataset(filedata)
lon = nc.variables['nav_lon'][:,:]
lat = nc.variables['nav_lat'][:,:]
h = np.squeeze(nc.variables['sishea'][0,:,:]) * 86400.
conc = np.squeeze(nc.variables['siconc'][0,:,:]) 
fig, ax = plt.subplots()
fig.set_size_inches(9, 9)
m = Basemap(projection='npstere',boundinglat=70,lon_0=-45,resolution='l')
m.drawcoastlines()
m.fillcontinents()
m.drawparallels(np.arange(-80.,81.,20.),labels=[False,True,True,False])
m.drawmeridians(np.arange(-180.,181.,30.),labels=[True,False,False,True])
x, y = m(lon, lat)
conc = np.where(conc>0.9,1.,0.)
h = ma.masked_less_equal(h*conc, 0.0001)
cs=m.pcolormesh(x,y,np.log(h), cmap='viridis',vmin=-6., vmax=-2.)
ax.set_title(('Deformation [$Log(day^{-1})$]'))
m.colorbar(cs,location='bottom',pad="10%")
outfile='%s_shear.png' % (filedata)
plt.savefig(outfile,dpi=140)
plt.show()

