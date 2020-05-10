import netCDF4 as netcdf
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cmocean
from pylab import *

year = 1996
month= 3
text='Landfast year: %s, month: %s' % (year,month)

filedata = 'lfi_mo_ave_91-98_noNaN.nc'
#filedata = 'lfi_mo_ave_68-90_noNaN.nc'
nc = netcdf.Dataset(filedata)
lon = nc.variables['longitude'][:]
lat = nc.variables['latitude'][:]
t = nc.variables['time'][:]
t_unit = nc.variables["time"].units
t_cal = "gregorian"
time = netcdf.num2date(t, t_unit, t_cal)
lficonc = np.squeeze(nc.variables['lficonc'][:,:,:])
year0 = time[0].year
month0 = time[0].month
timeindex = (year-year0)*12 + (month-month0)

fig, ax = plt.subplots()
fig.set_size_inches(8, 8)
m = Basemap(projection='npstere',boundinglat=65,lon_0=-45,resolution='l')
m.drawcoastlines()
m.fillcontinents()
m.drawparallels(np.arange(-80.,81.,30.),labels=[False,True,True,False])
m.drawmeridians(np.arange(-180.,181.,30.),labels=[True,False,False,True])
lon, lat = np.meshgrid(lon, lat)
x, y = m(lon, lat)
lficonc = ma.masked_less_equal(lficonc, -1000.)
cmap=plt.cm.Blues
cmaplist = [cmap(i) for i in range(cmap.N)]
cmap = cmap.from_list('custom', cmaplist, cmap.N)
bounds = np.linspace(0.,1.,11)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
#cs = m.pcolormesh(x,y,np.average(lficonc[2::12,:,:],axis=0)/100.,shading='flat', \
#      cmap=cmap,norm=norm,vmin=0.,vmax=1.)
cs = m.pcolormesh(x,y,np.squeeze(lficonc[timeindex,:,:])/100.,shading='flat', \
      cmap=cmap,norm=norm,vmin=0.,vmax=1.)
ax.set_title(time[timeindex])
m.colorbar(cs,location='bottom',pad="10%")
ax.set_title(text)
plt.show()
