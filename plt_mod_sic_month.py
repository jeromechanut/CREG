import netCDF4 as netcdf
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from pylab import *

year = 2007
month= 9 
EXP='CREG12_EXT-T001'

text='Model SIC year: %s, month: %s' % (year,month)
if (month<10):
        filedata='%s_1d_icemod_y%sm0%s.nc' % (EXP,year,month)
        outfile='%s_sic_y%sm0%s.png' % (EXP,year,month)
else:
        filedata='%s_1d_icemod_y%sm%s.nc' % (EXP,year,month)
        outfile='%s_sic_y%sm%s.png' % (EXP,year,month)

print(filedata)
filedata='/sortref/modele/creg/creg12/CREG12-T112/CREG12-T112-MEAN/MONTHLY/CREG12-T112_y2007m09_icemod.nc'
outfile="CREG12-T112_sic_y2007m09.png"
#filedata='/homelocal-px/px-151/ggarric/Tmp/ORCA12-TRBB36s003b_1m_icemod_199809-199809.nc'
nc = netcdf.Dataset(filedata)
lon = nc.variables['nav_lon'][:,:]
lat = nc.variables['nav_lat'][:,:]
fracd = np.squeeze(nc.variables['siconc'][:,:])

fig, ax = plt.subplots()
fig.set_size_inches(8, 8)
m = Basemap(projection='npstere',boundinglat=65,lon_0=-45,resolution='l')
m.drawcoastlines()
m.fillcontinents()
m.drawparallels(np.arange(-80.,81.,30.),labels=[False,True,True,False])
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
plt.savefig(outfile,dpi=140)
