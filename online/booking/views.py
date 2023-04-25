import os
from django.shortcuts import render, redirect
from datetime import datetime, timedelta, time
from .models import *
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from dotenv import load_dotenv
from .tasks import notifacation_record

load_dotenv()


def booking(request):
    services = Service.objects.all()
    if request.method == 'POST':
        service = request.POST.get('service')
        if service is None:
            messages.success(request, "Please Select A Service!")
            return redirect(reverse('booking:booking'))
        request.session['service'] = service  # присвоение значения service в сессию
        return redirect(reverse('booking:booking_day'))

    return render(request, 'booking/booking.html', {

        'services': services
    })


def booking_day(request, service_id=None):
    weekdays = validWeekday(31)
    validate_weekdays = isWeekdayValid(weekdays)
    if service_id is not None:
        service = Service.objects.get(id=service_id)
        request.session['service'] = service.name
    if request.method == 'POST':
        day = request.POST.get('day')
        request.session['day'] = day  # присвоение значения day в сессию
        return redirect(reverse('booking:bookingSubmit'))

    return render(request, 'booking/booking_day.html', {
        'weekdays': weekdays,
        'validateWeekdays': validate_weekdays,
    })


def bookingSubmit(request):
    times = [
        "10.00 PM", "10:30 PM",
        "11.00 PM", "11:30 PM",
        "12.00 PM", "12:30 PM",
        "13.00 PM", "13:30 PM",
        "14.00 PM", "14:30 PM",
        "15.00 PM", "15:30 PM",
        "16.00 PM", "16:30 PM",
        "17.00 PM", "17:30 PM",
        "18.00 PM",
    ]
    today = datetime.now()
    mindate = today.strftime('%Y-%m-%d')  # выбор даты с которой можно записаться
    deltatime = today + timedelta(days=31)  # кол-во дней на которые можно записываться
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxdate = strdeltatime  # самая дальняя запись
    day = request.session.get('day')
    service_name = request.session.get('service')
    service = Service.objects.get(name=service_name) if service_name else None
    hour = checkTime(times, day)  # проверка забронировано ли время другим пользователем в этот день
    if request.method == 'POST':
        time = request.POST.get("time")  # получение времени
        if service != None:
            if day <= maxdate and day >= mindate:
                if Appointment.objects.filter(day=day).count() < 11:
                    if Appointment.objects.filter(day=day, time=time).count() < 1:
                        record = Appointment.objects.get_or_create(
                            user=request.user,
                            service=service,
                            day=day,
                            time=time,
                        )
                        appoint_id = record[0].id
                        notifacation_record.delay(appoint_id)
                        messages.success(request, "Appointment already exists!")
                        return redirect('booking:user_record')
    return render(request, 'booking/bookingSubmit.html', {
        'times': hour,
    })


def userUpdate(request, id):
    services = Service.objects.all()
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    # Copy  booking:
    today = datetime.today()
    minDate = today.strftime('%Y-%m-%d')

    # 24h if statement in template:
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    # Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validWeekday(31)

    # Only show the days that are not full:
    validateWeekdays = isWeekdayValid(weekdays)

    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')

        # Store day and service in django session:
        request.session['day'] = day
        request.session['service'] = service

        return redirect(reverse('booking:userUpdateSubmit', args=[id]))

    return render(request, 'booking/userUpdate.html', {
        'weekdays': weekdays,
        'validateWeekdays': validateWeekdays,
        'delta24': delta24,
        'id': id,
        'services': services
    })


def userUpdateSubmit(request, id):
    times = [
        "10.00 PM", "10:30 PM",
        "11.00 PM", "11:30 PM",
        "12.00 PM", "12:30 PM",
        "13.00 PM", "13:30 PM",
        "14.00 PM", "14:30 PM",
        "15.00 PM", "15:30 PM",
        "16.00 PM", "16:30 PM",
        "17.00 PM", "17:30 PM",
        "18.00 PM",
    ]
    today = datetime.now()
    minDate = today.strftime('%Y-%m-%d')
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime('%Y-%m-%d')
    maxDate = strdeltatime

    day = request.session.get('day')
    service_name = request.session.get('service')
    service = Service.objects.get(name=service_name) if service_name else None

    # Only show the time of the day that has not been selected before and the time he is editing:
    hour = checkEditTime(times, day, id)
    appointment = Appointment.objects.get(pk=id)
    userselectedtime = appointment.time
    if request.method == 'POST':
        time = request.POST.get("time")
        if service != None:
            if day <= maxDate and day >= minDate:
                if Appointment.objects.filter(day=day).count() < 11:
                    if Appointment.objects.filter(day=day, time=time).count() < 1 or userselectedtime == time:
                        record = Appointment.objects.filter(pk=id).update(
                            user=request.user,
                            service=service,
                            day=day,
                            time=time,
                        )
                        appoint_id = record[0].id
                        notifacation_record.delay(appoint_id)
                        messages.success(request, "Appointment Edited!")
                        return redirect('booking:user_record')
    return render(request, 'booking/userUpdateSubmit.html', {
        'times': hour,
        'id': id,
    })


def dayToWeekday(x):
    z = datetime.strptime(x, "%Y-%m-%d")
    y = z.strftime('%A')
    return y


def validWeekday(days):
    today = datetime.now()  # получение текущей даты
    weekdays = []  # пустой список для хранения для недели
    booking_settings = BookingSettings.objects.all()
    for i in range(0, days):
        x = today + timedelta(days=i)
        for setting in booking_settings:
            x = today + timedelta(days=i)
            start_time = datetime.combine(setting.start_time, time.min)
            end_time = datetime.combine(setting.end_time, time.max)
            if start_time <= x <= end_time:
                weekdays.append(x.strftime('%Y-%m-%d'))  # если удовлетворяет условие добавляем этот день в список
    return weekdays


def isWeekdayValid(x):
    validateWeekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:  # кол-во записей на день
            validateWeekdays.append(j)
    return validateWeekdays


def checkTime(times, day):
    # Only show the time of the day that has not been selected before:
    x = []
    now = datetime.now()
    time = now.time()
    formatted_time = time.strftime('%H:%M')
    for k in times:
        if k[0:5] > formatted_time and day == str(now.date()):
            if Appointment.objects.filter(day=day, time=k).count() < 1:
                x.append(k)
        elif day != str(now.date()):
            if Appointment.objects.filter(day=day, time=k).count() < 1:
                x.append(k)
    return x


def checkEditTime(times, day, id):
    # Only show the time of the day that has not been selected before:
    x = []
    now = datetime.now()
    time = now.time()
    formatted_time = time.strftime('%H:%M')
    appointment = Appointment.objects.get(pk=id)
    time = appointment.time
    for k in times:
        if k[0:5] > formatted_time and day == str(now.date()):
            if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
                x.append(k)
        elif day != str(now.date()):
            if Appointment.objects.filter(day=day, time=k).count() < 1 or time == k:
                x.append(k)
    return x


def remove(request, id):
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    today = datetime.today()
    delta24 = (userdatepicked).strftime('%Y-%m-%d') >= (today + timedelta(days=1)).strftime('%Y-%m-%d')
    if delta24 is True:
        appointment.delete()
        return redirect(reverse('booking:user_record'))
    else:
        return render(request, 'booking/Falsedelete.html')


def record_view(request):
    service = Service.objects.all()
    now = datetime.now()
    appointments = Appointment.objects.filter(user=request.user)
    appointments_expired = Appointment.objects.filter(Q(day__lt=now.date()) | Q(day=now.date(), time__lt=now.time()))

    if appointments_expired:
        for appointment in appointments_expired:
            history = HistoryBooking(user=appointment.user, service=appointment.service, day=appointment.day,
                                     time=appointment.time, time_ordered=appointment.time_ordered)
            history.save()
        appointments_expired.delete()
    return render(request, "booking/user_record.html",
                  context={'appointments': appointments, 'service': service})
