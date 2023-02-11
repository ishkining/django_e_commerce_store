from django.shortcuts import render


def payment_success(request):
    return render(request, 'payment/payment-success')


def payment_failed(request):
    return render(request, 'payment/payment-failed')
