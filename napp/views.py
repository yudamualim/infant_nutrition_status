import pandas as pd
from sklearn.preprocessing import StandardScaler
from django.shortcuts import render
from django.contrib.staticfiles import finders

def data_test(request):
  csv_path = finders.find('data/testings.csv')

  df = pd.read_csv(csv_path, encoding='latin-1')
  
  # # Data Standardization
  scaler = StandardScaler()
  x = df[
    ['Berat_Badan', 'Tinggi_Badan', 'Usia_Saat_Ukur', 'Jenis_Kelamin']
  ]
  x = scaler.fit_transform(x)

  context = {
    'x': x
  }
  return render(request, 'data_test.html', context)  
