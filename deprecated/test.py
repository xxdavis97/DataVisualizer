import pandas as pd
import matplotlib.pyplot as plt

#Reading the csv file given
data = pd.read_csv('weather_data.csv')
data.set_index("City", inplace=True)
#Displaying the data from csv read
print(data.head())
#Getting data from the csv file read
c1 = data[data.index == 'Battle Creek']
c2 = data[data.index == 'Houghton']
c3 = data[data.index == 'Chicago']
c4 = data[data.index == 'Dallas']
c5 = data[data.index == 'San Francisco']
c6 = data[data.index == 'Columbus']

plt.plot(c1.columns.values, c1.values[0], label='Battle Creek')
plt.plot(c2.columns.values, c2.values[0], label='Houghton')
plt.plot(c3.columns.values, c3.values[0], label='Chicago')
plt.plot(c4.columns.values, c4.values[0], label='Dallas')
plt.plot(c5.columns.values, c5.values[0], label='San Francisco')
plt.plot(c6.columns.values, c6.values[0], label='Columbus')
plt.xticks(rotation=45)
plt.legend()
plt.show()