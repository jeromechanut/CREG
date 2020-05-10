import netCDF4 as netcdf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import datetime

EXP='CREG12_EXT-T001'
filedata='%s_1d_scalar.nc' % (EXP)
outfile='%s_ice_stats.png' % (EXP)

#piomas data:
colnames=('year', 'month', 'day', 'h1', 'h2', 'h3', 'h4', 'h5', 'v1', 'v2', 'v3', 'v4', 'v5')
data = pd.read_fwf("/home/jchanut/PIOMAS/PIOMAS_2NC/heff_mon_Data", header=None, names=colnames)
data['Date']=pd.to_datetime(data[['year', 'month', 'day']])
data.set_index('Date', inplace=True)
piomas=pd.Series(data["v4"])

#OSISAF data:
datas = pd.read_csv("sic_data_arctic.csv")
datas['Date']=pd.to_datetime(datas[['year', 'month', 'day']])
datas.set_index('Date', inplace=True)
sicda=pd.Series(datas["extent"])
sicd=pd.Series(datas["area"])

nc = netcdf.Dataset(filedata)
times = nc.variables['time_counter']
jd = netcdf.num2date(times[:],times.units)

vol = nc.variables['ibgvol_tot']
vv = pd.Series(vol[:],index=jd)/1000.
vvm=vv.resample('M', how='mean')

area = nc.variables['ibgarea_tot']
ar = pd.Series(area[:],index=jd)/1000000.
arm=ar.resample('M', how='mean')
# Shift at the middle of the month:
#arm = ar.resample('MS', loffset=pd.Timedelta(14, 'd'),how='mean')

vols = nc.variables['sbgvol_tot']
vvs = pd.Series(vols[:],index=jd)/1000.
vvms = vvs.resample('M', how='mean')
vvms_warren = sicd*0.

# snow volume (X1000 km3):
vvms_warren[0::12] = 2.4
vvms_warren[1::12] = 2.8 
vvms_warren[2::12] = 3.4
vvms_warren[3::12] = 3.1
vvms_warren[4::12] = 2.8
vvms_warren[5::12] = 2.5
vvms_warren[6::12] = 0.4
vvms_warren[7::12] = 0.3
vvms_warren[8::12] = 0.7 
vvms_warren[9::12] = 1.4 
vvms_warren[10::12] = 1.8 
vvms_warren[11::12] = 2.0

# averaged snow depths from warren (cm):
vvms_warren[0::12] = 27. 
vvms_warren[1::12] = 28. 
vvms_warren[2::12] = 32. 
vvms_warren[3::12] = 34. 
vvms_warren[4::12] = 35. 
vvms_warren[5::12] = 30. 
vvms_warren[6::12] =  6. 
vvms_warren[7::12] =  2. 
vvms_warren[8::12] = 10. 
vvms_warren[9::12] = 18. 
vvms_warren[10::12] = 23. 
vvms_warren[11::12] = 25. 

fig = plt.figure(figsize=(14,6))
ax = fig.add_subplot(331)
vvm.plot(ax=ax,label='model - CREG12_SAS-T002')
piomas.plot(ax=ax,title='Sea ice volume [$10^3$ $km^3$]',label='piomas',color='red')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_ylim(3., 35.)
ax.set_xlabel('')
ax.set_xticks([])
ax.set_ylabel('')

ax = fig.add_subplot(332)
arm.plot(ax=ax, title='Sea ice area [$10^6$ $km^2$]', label='model - CREG12_SAS-T002')
sicd.plot(ax=ax, label='OSISAF',color='red')
ax.set_ylabel('')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_xlabel('')
ax.set_xticks([])
ax.set_ylim(0., 18.)

ax = fig.add_subplot(333)
sdms=vvms/arm*100.
#vvms.plot(ax=ax,title='Snow volume', label='model')
sdms.plot(ax=ax,title='Snow depth [$cm$]', label='model')
vvms_warren.plot(ax=ax, label='warren',color='red')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
#ax.set_ylim(0, 4.)
ax.set_ylim(0, 40.)
ax.set_xlabel('')
ax.set_xticks([])
ax.set_ylabel('')

ax = fig.add_subplot(334)
vvm[2::12].plot(ax=ax,label='model')
piomas[2::12].plot(ax=ax,title='March',label='piomas',color='red')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_ylim(20, 35.)
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_xticks([])

ax = fig.add_subplot(335)
arm[2::12].plot(ax=ax, title='March', label='model')
sicd[2::12].plot(ax=ax, label='OSISAF',color='red')
ax.set_ylabel('')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_ylim(12., 18.)
ax.set_xlabel('')
ax.set_xticks([])

ax = fig.add_subplot(336)
sdms[4::12].plot(ax=ax, title='May', label='model')
vvms_warren[4::12].plot(ax=ax, label='Warren',color='red')
ax.set_ylabel('')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_ylim(0, 40.)
ax.set_xlabel('')
ax.set_xticks([])

ax = fig.add_subplot(337)
vvm[8::12].plot(ax=ax,label='model', legend=True)
piomas[8::12].plot(ax=ax,title='September',label='piomas', legend=True,color='red')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_ylim(0, 15.)
ax.set_ylabel('')
ax.set_xlabel('Year')

ax = fig.add_subplot(338)
arm[8::12].plot(ax=ax, title='September', label='model', legend=True)
sicd[8::12].plot(ax=ax, label='OSISAF', legend=True,color='red')
#sicd[8::12].plot(ax=ax, label='OSISAF',color='red',linestyle='dashed')
ax.set_ylabel('')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_ylim(0, 8.)
ax.set_xlabel('Year')

ax = fig.add_subplot(339)
sdms[7::12].plot(ax=ax, title='August', label='model', legend=True)
vvms_warren[7::12].plot(ax=ax, label='Warren', legend=True, color='red')
ax.set_ylabel('')
ax.set_xlim(pd.Timestamp('1993-01-01'), pd.Timestamp('2013-01-01'))
ax.set_ylim(0, 5.)
ax.set_xlabel('Year')
plt.savefig(outfile,dpi=140)
plt.show()
