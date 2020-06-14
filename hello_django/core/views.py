from django.shortcuts import render, HttpResponse

# Create your views here.

def hello(request, nome, idade):
    return HttpResponse('<h1>Hello {} de {} anos</h1>'.format(nome, idade))

def sum(request, num1, num2):
    return HttpResponse('<h1>Sum: {} + {} = {}</h1>'.format(num1, num2, num1 + num2))

def minus(request, num1, num2):
    return HttpResponse('<h1>Minus: {} - {} = {}</h1>'.format(num1, num2, num1 - num2))

def times(request, num1, num2):
    return HttpResponse('<h1>Times: {} * {} = {}</h1>'.format(num1, num2, num1 * num2))

def division(request, num1, num2):
    if(num2 == 0):
        return HttpResponse('<h1>Division by 0 doesn\'t exist</h1>')
    return HttpResponse('<h1>Division: {} / {} = {}</h1>'.format(num1, num2, num1 / num2))