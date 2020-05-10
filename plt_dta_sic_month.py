import netCDF4 as netcdf
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pylab import *

year=2006
month=9
EXP='OSISAF'

if (month<10):
	filedata='/dataref/rd/DATA/SEA_ICE/OSI_SAF/SIC/Monthly_Mean/Arctic/REPROC/ice_conc_nh_polstere-100_reproc_y%sm0%s.nc' % (year,month)
        outfile='%s_sic_y%sm0%s.png' % (EXP,year,month)
else:
	filedata='/dataref/rd/DATA/SEA_ICE/OSI_SAF/SIC/Monthly_Mean/Arctic/REPROC/ice_conc_nh_polstere-100_reproc_y%sm%s.nc' % (year,month)
        outfile='%s_sic_y%sm%s.png' % (EXP,year,month)

date='OSISAF year: %s, month: %s' % (year,month)
nc = netcdf.Dataset(filedata)
lon = nc.variables['lon'][:,:]
lat = nc.variables['lat'][:,:]
fracd = np.squeeze(nc.variables['ice_conc'][:,:])/100.

fig, ax = plt.subplots()
fig.set_size_inches(9, 9)
m = Basemap(projection='npstere',boundinglat=65,lon_0=-45,resolution='l')
m.drawcoastlines()
m.fillcontinents()
m.drawparallels(np.arange(-80.,81.,20.),labels=[False,True,True,False])
m.drawmeridians(np.arange(-180.,181.,30.),labels=[True,False,False,True])
x, y = m(lon, lat)
fracd = ma.masked_less_equal(fracd, 0.15)
cmap=plt.cm.gist_ncar_r
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = cmap.from_list('custom', cmaplist, cmap.N)
bounds = np.linspace(0.15,0.95,17)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cs = m.pcolormesh(x,y,fracd,shading='flat', \
      cmap=cmap,norm=norm,vmin=0.,vmax=1.)
ax.set_title(text)
m.colorbar(cs,location='bottom',pad="10%",extend='max')
ax.set_title(date)
plt.savefig(outfile,dpi=140)

