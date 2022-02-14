import pandas as pd
from math import sin, cos, sqrt, atan2, radians
from tqdm import tqdm


data=pd.read_csv('data.csv')

postcode_data=pd.read_csv('ukpostcodes.csv')
postcode_data=postcode_data.drop(columns=['id'])
postcode_data=postcode_data.rename(columns={"postcode": 'RegAddress.PostCode'})

R = 6373.0
#these are the coordinates of EC2R
lat2 = radians(51.5156)
lon2 = radians(0.0873)

for idx in tqdm(range(len(postcode_data))):
  aux=postcode_data.iloc[idx]
  lat1 = radians(aux['latitude'])
  lon1 = radians(aux['longitude'])
  dlon = lon2 - lon1
  dlat = lat2 - lat1
  a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  c = 2 * atan2(sqrt(a), sqrt(1 - a))
  postcode_data.at[idx, 'distance wrt EC2R']=R*c*0.621371 #in miles

idx=postcode_data[(postcode_data['distance wrt EC2R']<50)&(postcode_data['distance wrt EC2R']>0)].index
postcode_data.at[idx, 'dist']='0-50'
idx=postcode_data[(postcode_data['distance wrt EC2R']<100)&(postcode_data['distance wrt EC2R']>50)].index
postcode_data.at[idx, 'dist']='50-100'
idx=postcode_data[(postcode_data['distance wrt EC2R']<150)&(postcode_data['distance wrt EC2R']>100)].index
postcode_data.at[idx, 'dist']='100-150'
idx=postcode_data[(postcode_data['distance wrt EC2R']<200)&(postcode_data['distance wrt EC2R']>150)].index
postcode_data.at[idx, 'dist']='150-200'
idx=postcode_data[(postcode_data['distance wrt EC2R']<250)&(postcode_data['distance wrt EC2R']>200)].index
postcode_data.at[idx, 'dist']='200-250'
idx=postcode_data[(postcode_data['distance wrt EC2R']<300)&(postcode_data['distance wrt EC2R']>250)].index
postcode_data.at[idx, 'dist']='250-300'
idx=postcode_data[(postcode_data['distance wrt EC2R']<350)&(postcode_data['distance wrt EC2R']>300)].index
postcode_data.at[idx, 'dist']='300-350'
idx=postcode_data[(postcode_data['distance wrt EC2R']<400)&(postcode_data['distance wrt EC2R']>350)].index
postcode_data.at[idx, 'dist']='350-400'
idx=postcode_data[(postcode_data['distance wrt EC2R']<450)&(postcode_data['distance wrt EC2R']>400)].index
postcode_data.at[idx, 'dist']='400-450'
idx=postcode_data[(postcode_data['distance wrt EC2R']<500)&(postcode_data['distance wrt EC2R']>450)].index
postcode_data.at[idx, 'dist']='450-500'
idx=postcode_data[(postcode_data['distance wrt EC2R']>500)&(postcode_data['distance wrt EC2R']>500)].index
postcode_data.at[idx, 'dist']='>500'

data = pd.merge(data, postcode_data, on="RegAddress.PostCode")

data.to_csv('UK_postcode')