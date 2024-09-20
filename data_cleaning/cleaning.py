import pandas as pd
import functools 
import re

phones = pd.read_csv('./crawler/data_preparation/phones.csv')


phones.describe()

def dimension_cleaner(dimension):
    try:
        dimensions = dimension.replace(' mm', '').split('x')
        return int(functools.reduce(lambda a, b: float(a)*float(b), dimensions))
    except:
        return None
    
def cpu_cleaner(cpu):
    try:
        total = 1
        for value in re.split(' GHz|, ', row['cpu']):
            if bool(re.search("[1-9]x .", value)):
                total*= functools.reduce(lambda a, b: float(a)*float(b), value.split('x '))
        return int(total if total != 1 else None)
    except:
        return None
    
def gpu_cleaner(gpu):
    try:
        if not bool(re.search("MHz", gpu)):
            return None
        return int(gpu.replace('MHz,', '').replace('MHz', '').split(', ')[-1])
    except:
        return None

def weigth_cleaner(weigth):
    try:
        return int(weigth.replace(' g', ''))
    except:
        return None
    
def storage_cleaner(storage):
    try:
        return int(storage.replace(' GB', ''))
    except:
        return None
    

#review this for ram
#a = "4 GB, 2133 MHz"

#import re
#import functools 


#print(functools.reduce(lambda a, b: int(a.strip()) * int(b.strip()) if not bool(re.search("MHz", a)) and bool(re.search("MHz", b)) else 0, re.split('GB,', a)))



volume = []
cpu = []
gpu = []
weigth = []
storage = []
popularity = []


for index, row in phones.iterrows():
    volume.append(dimension_cleaner(row['dimensions']))
    cpu.append(cpu_cleaner(row['cpu']))
    gpu.append(gpu_cleaner(row['gpu']))
    weigth.append(weigth_cleaner(row['weight']))
    #ram
    storage.append(storage_cleaner(row['storage']))


data = {
    'volume': volume,
    'cpu': cpu,
    'gpu': gpu,
    'weigth': weigth,
    'storage': storage,
    'popularity':  phones['popularity'],
    'sellers_amount': phones['sellers_amount'],
    'screen_size': phones['screen_size'],
    'memory_size': phones['memory_size'],
    'battery_size': phones['battery_size'],
    'blue': phones['blue'],
    'price': phones['best_price'],
    'model_name': phones['model_name'],

}
cleaned_data = pd.DataFrame(data)

cleaned_data = cleaned_data.dropna()
cleaned_data = cleaned_data.drop_duplicates()

#cleaned_data.round(0).astype(int)
cleaned_data.to_csv("./crawler/data_cleaning/cleaned_data_dropna.csv", sep=',')




#cleaned_data = pd.read_csv('./crawler/data_cleaning/cleaned_data.csv', sep=',')

