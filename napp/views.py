from django.shortcuts import render

def data_test(request):
  context = {
    'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quaerat velit illum odit inventore magnam nihil iure fuga mollitia cumque eum.',
  }
  return render(request, 'data_test.html', context)  
