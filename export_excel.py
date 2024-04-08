#This script extract the jobs information, priority and SU hours that the users had used in the cluster per month from the dat files extracted from the cluster into excel files.

#Author: Diana Marlen Castaneda Bagatella

#How to run it: python3 export_excel.py; it is necessary to have all the *.dat files in a foldes as file_month.dat. 
#   In this script the month variable needs to be specified to folder to extract the information as 'Month' or 'February January March'. 
#   The script is run outside the folder to extract the information.

import pandas as pd

months = 'March'
users = 'champagn yl24 kc623 dmc59 ab2757'

su_high, su_high_champagn, su_standard = {},{}, {}
for month in months.split():
    for user in users.split():
        dataFile = f'{month}/{user}_{month.lower()}.dat'
        df = pd.read_csv(dataFile, engine='python', delimiter='\s+',skiprows=2,
                         names=['Partition','QOS','Start','Elapsed','CPUTimeRAW','AllocTRES','State','JobName','WorkDir'])
        df['SU'] = df['CPUTimeRAW']/3600 #CPU*hour
        print(dataFile)
        print(df)

        su_high[f'{user}_{month.lower()}'] = df['SU'].loc[df['QOS'] == 'high'].sum()
        su_high_champagn[f'{user}_{month.lower()}'] = df['SU'].loc[df['QOS'] == 'high_cham+'].sum()
        su_standard[f'{user}_{month.lower()}'] = df['SU'].loc[df['QOS'] == 'standard'].sum()
        print(f'{user}_{month.lower()}')
        print(f'QoS high: {su_high[f"{user}_{month.lower()}"]}')
        print(f'QoS high_champagn: {su_high_champagn[f"{user}_{month.lower()}"]}')
        print(f'QoS standard: {su_standard[f"{user}_{month.lower()}"]}')

        df.to_csv(f'{month}/{user}_{month.lower()}.csv', index=False)

suHigh, suHigh_champagn, suStandard = 0,0,0
for month in months.split():
    su_high_per_month, su_high_champagn_per_month, su_standard_per_month = 0,0,0
    for user in users.split():
        su_high_per_month += su_high[f'{user}_{month.lower()}']
        su_high_champagn_per_month += su_high_champagn[f'{user}_{month.lower()}']
        su_standard_per_month += su_standard[f'{user}_{month.lower()}']

    print('')
    print(f'{month.lower()}')
    print(f'QoS high: {su_high_per_month}')
    print(f'QoS high_champagn: {su_high_champagn_per_month}')
    print(f'QoS standard: {su_standard_per_month}')

    suHigh += su_high_per_month
    suHigh_champagn += su_high_champagn_per_month
    suStandard += su_standard_per_month

print('')
print(f'Total SU:')
print(f'QoS high: {suHigh}')
print(f'QoS high_champagn: {suHigh_champagn}')
print(f'QoS standard: {suStandard}')

