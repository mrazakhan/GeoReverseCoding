import sys
from geopy.geocoders import Nominatim
from pygeocoder import Geocoder
import time

geolocator=Nominatim()

def get_rev_address(lat, lng,method="geopy", district_only=False):
	string=lat+','+lng
	if 'geopy' in method:
		location = geolocator.reverse(string)
		return location.address
	else:
		lat=float(lat)
		lng=float(lng)
		print str(lat)+" , "+  str(lng)

		results=""
		try:
			rs=Geocoder.reverse_geocode(lat,lng)
		
		except:
			results=""
		try:	
			results+="city:"
			results+=rs.city
		except:
			results+=""

		try:	
			results+=",district:"
			results+=rs.county
		except:
			results+=""
		try:
			results+=",raw:"+rs.__str__()
		except:
			results+=""

		if district_only:
			return rs.county
		return results

def rev_geocode(ifname,sep='\t'):

	fin=open(ifname,'r')
	fout=open('annotated'+ifname,'w')
	lst=[]
	index=0
	for line in fin:	
		if 'id' not in line :
			ind,tid,lat,lng,land,land1,pop,pov=line.split(sep)
			pov=pov.rstrip()
			addr=get_rev_address(lat,lng, method="pygeocoder")
			if addr is None:
				addr=""
			temp='{}'.format(int(index))
			temp+=";"+tid+";"+lat+";"+lng+";"+addr
			print temp
			lst.append(temp)
			time.sleep(0.2)	
		index+=1	
	for entry in lst:
		fout.write(entry)
	fout.close()		

def rev_geocode2(ifname,sep='\t'):

	fin=open(ifname,'r')
	fout=open('annotated'+ifname,'w')
	lst=[]
	index=0
	for line in fin:	
		if 'id' not in line and 'ID' not in line :
			cellid,lng,lat=line.split(sep)
			lat=lat.rstrip()
			addr=get_rev_address(lat,lng, method="pygeocoder", district_only=True)
			print addr
			if addr is None:
				addr=""
			temp='{}'.format(cellid)
			temp+=";"+lat+";"+lng+";"+addr+'\n'
			print temp
			lst.append(temp)
			time.sleep(0.2)	
		index+=1	
	for entry in lst:
		fout.write(entry)
	fout.close()		

if __name__=='__main__':
	ifname=sys.argv[1]
	rev_geocode2(ifname,sep=',')		
