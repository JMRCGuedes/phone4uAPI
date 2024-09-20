import pandas as pd
# importing the csv module
import csv


# data1 = pd.read_csv('./phone_final_data.csv')
# data2 = pd.read_csv('./phone_final_first_data.csv')

# newdf = data1.merge(data2, how='outer')


# newdf.to_csv("phone_merged.csv", sep=',')


phone_data = pd.read_csv('./phones_data.csv')
phone_extra_data = pd.read_csv('./phone_merged.csv')

newdf = phone_extra_data.merge(phone_data, how='outer')


newdf.to_csv("phones.csv", sep=',')