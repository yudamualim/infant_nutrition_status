import pandas as pd
from sklearn.preprocessing import StandardScaler
from django.shortcuts import render
from django.contrib.staticfiles import finders

def data_test(request):
  csv_path = finders.find('data/testings.csv')

  df = pd.read_csv(csv_path, encoding='latin-1')
  
  # Data Standardization
  scaler = StandardScaler()
  x = df[
    ['Berat_Badan', 'Tinggi_Badan', 'Usia_Saat_Ukur', 'Jenis_Kelamin']
  ]
  x = scaler.fit_transform(x)
  
  # Format data with two decimal places
  formatted_data = [
    [f'{value:.2f}' for value in row] for row in x
  ]

  context = {
    'x': x,
    'formatted_data': formatted_data
  }
  return render(request, 'data_test.html', context)  
