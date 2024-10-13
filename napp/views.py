import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

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

def data_train(request):
  data_train = pd.read_csv(finders.find('data/trains.csv'))
  data_testing = pd.read_csv(finders.find('data/testings.csv'))

  x_train, y_train = data_train.iloc[:, :-1], data_train.iloc[:, -1]
  x_test, y_test = data_testing.iloc[:, :-1], data_testing.iloc[:, -1]

  context = {
    'x_train': x_train,
    'y_train': y_train,
    'x_test': x_test,
    'y_test': y_test
  }

  return render(request, 'data_train.html', context)

def correlation(request):
  df = pd.read_csv(finders.find('data/trains.csv'))
  
  columns_to_correlate = ['Berat_Badan', 'Tinggi_Badan', 'Usia_Saat_Ukur', 'Jenis_Kelamin']
  
  # Change object data type into binary
  df = pd.get_dummies(df, columns=['Jenis_Kelamin'])
  # Update the list of columns to correlate to include the new one-hot encoded columns
  columns_to_correlate = ['Berat_Badan', 'Tinggi_Badan', 'Usia_Saat_Ukur',] + [col for col in df.columns if 'Jenis_Kelamin' in col]
  
  correlations = []
  for col1 in columns_to_correlate:
    for col2 in columns_to_correlate:
      if col1 != col2:
        try:
          r, p = pearsonr(df[col1].dropna(), df[col2].dropna())
          correlations.append((col1, col2, r))
        except ValueError:
          print(f"Error: {col1} and {col2} have NaN values.")
          
  correlation_df = pd.DataFrame(correlations, columns=['column_1', 'column_2', 'correlation'])
  correlation_df = correlation_df.to_dict(orient='records')
  
  context = {
    'correlation': correlation_df
  }
  
  return render(request, 'correlation.html', context)

def predict(request):
  df = pd.read_csv(finders.find('data/test.csv'))
  
  # Features and target
  x = df[
    ['Berat_Badan', 'Tinggi_Badan', 'Usia_Saat_Ukur', 'Jenis_Kelamin'] # Fitur
  ]
  y = df['Status_Gizi_Balita'] # Target
  
  feature_weight = np.array([
    0.35,
    0.39,
    -1.41,
    0.16,
  ]) # Weights given manually
  bias = 0.61
  
  y_pred_manual = np.dot(x, feature_weight) + bias
  y_pred_classified = np.where(y_pred_manual < 0, -1, 1)

  label_mapping = {
    1: 'Normal',
    -1: 'Stunting'
  }
  
  predictions = []
  for i, (berat, tinggi, usia, jk, pred, actual) in enumerate(zip(
    x['Berat_Badan'], x['Tinggi_Badan'], x['Usia_Saat_Ukur'], x['Jenis_Kelamin'], y_pred_classified, y), 1):
    
    pred_label = label_mapping[pred]
    actual_label = label_mapping.get(actual, 'Tidak Terklasifikasi')
    
    predictions.append({
        'index': i,
        'berat': berat,
        'tinggi': tinggi,
        'usia': usia,
        'jenis_kelamin': jk,
        'predicted': pred_label,
        'actual': actual_label
    })

  context = {
    'predictions': predictions,
    'accuracy': accuracy_score(y, y_pred_classified),
    'confusion_matrix': confusion_matrix(y, y_pred_classified),
    'classification_report': classification_report(y, y_pred_classified),
  }
  
  return render(request, 'predict.html', context)
