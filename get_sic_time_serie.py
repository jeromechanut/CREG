import netCDF4 as netcdf
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd

i=0
out=np.empty([400, 5])
for year in np.arange(1993,2017,1):
	for month in np.arange(1,13,1):
		if (month<10):
			filedata='/dataref/rd/DATA/SEA_ICE/OSI_SAF/SIC/Monthly_Mean/Arctic/REPROC/ice_conc_nh_polstere-100_reproc_y%sm0%s.nc' % (year,month)
		else:
			filedata='/dataref/rd/DATA/SEA_ICE/OSI_SAF/SIC/Monthly_Mean/Arctic/REPROC/ice_conc_nh_polstere-100_reproc_y%sm%s.nc' % (year,month)

		date='year: %s, month: %s' % (year,month)
		print(date)

		nc = netcdf.Dataset(filedata)
		tmp = np.squeeze(nc.variables['ice_conc'][:,:])/100.
#		fracd = ma.masked_less_equal(fracd, 0.15)
                fracd = np.where(tmp<0.15,0.,tmp)
                area = np.where(tmp<0.15,0.,1.) 
                out[i,0] = year
                out[i,1] = month
                out[i,2] = 15.
 		out[i,3] = fracd[:,:].sum()*10.*10./1.e6
                out[i,4] = area[:,:].sum()*10.*10./1.e6
                print(out[i,3],out[i,4])
		i = i +1

colnames=('year', 'month', 'day', 'area','extent')
data = pd.DataFrame(data=out[:i-2,:],columns = colnames)
data['Date']=pd.to_datetime(data[['year', 'month', 'day']])
data.set_index('Date', inplace=True)
sic=pd.Series(data["extent"])
#
fig = plt.figure(figsize=(12,4))
ax = fig.add_subplot(111)
sic.plot(ax=ax)
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2016-01-01'))
ax.set_ylabel('[$10^6$ $km^2$]')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2016-01-01'))
ax.set_ylim(0, 20.)
ax.set_xlabel('Time')
plt.show()

#tfile = open('sic_data_arctic.txt', 'a')
#tfile.write(data.to_string())
#tfile.close()
data.to_csv("sic_data_arctic.csv")

