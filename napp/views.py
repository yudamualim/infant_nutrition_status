import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from .models import Person

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.staticfiles import finders
from .forms import PersonForm  # Use relative import for forms
from django.shortcuts import redirect


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
    # Baca file CSV
    df = pd.read_csv(finders.find('data/trains.csv'), encoding='latin1')

    x = df[['Berat_Badan', 'Tinggi_Badan', 'Usia_Saat_Ukur', 'Jenis_Kelamin']]

    # Standardize the data
    scaler = StandardScaler()
    x_standardized = scaler.fit_transform(x)

    # Create a list of standardized data formatted to two decimal places
    standardized_data = []
    for row in x_standardized:
        standardized_data.append([f'{value:.2f}' for value in row])

    # Prepare context for rendering
    context = {
        'standardized_data': standardized_data,
        'columns': ['Berat Badan', 'Tinggi Badan', 'Usia Saat Ukur', 'Jenis Kelamin'],  # Column headers
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

def graph(request):
  # Prediction data
  tp = 18
  tn = 5
  fp = 3
  fn = 4

  accuracy = (tp + tn) / (tp + tn + fp + fn)
  precision = tp / (tp + fp)
  recall = tp / (tp + fn)
  f1 = 2 * (precision * recall) / (precision + recall)
  
  context = {
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1': f1,
  }
  
  return render(request, 'graph.html', context)

def person_form(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index_person')  # Replace 'success' with your desired redirect
    else:
        form = PersonForm()
    
    return render(request, 'person_form.html', {'form': form})

def success_view(request):
    # Retrieve all records from the Person model
    people = Person.objects.all()
    return render(request, 'success.html', {'people': people})
  
def index_person(request):
    people = Person.objects.all()
    return render(request, 'index_person.html', {'people': people})
  
def edit_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('index_person')  # Redirect to index_person after saving
    else:
        form = PersonForm(instance=person)

    return render(request, 'edit_person.html', {'form': form, 'person': person})
  
def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return redirect('index_person')  # Redirect to index_person after deletion


