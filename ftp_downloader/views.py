from django.shortcuts import render
from django.http import HttpResponse
from ftplib import FTP
from django.views.decorators.csrf import csrf_exempt

response = None


def store(data):
    global response
    response = data


@csrf_exempt
def my_view(request):
    if request.method == "GET":
        return render(request, 'ftp_downloader.html')

    elif request.method == "POST":
        address = request.POST.get('address')
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        cwd = request.POST.get('cwd')
        file_name = request.POST.get('filename')

        ftp = FTP(address)
        ftp.login(user=user_name, passwd=password)
        if cwd is not None and cwd != '':
            ftp.cwd(cwd)

        ftp.retrbinary('RETR ' + file_name, store)
        ftp.quit()

        return HttpResponse(response)
