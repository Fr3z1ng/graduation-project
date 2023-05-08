from datetime import time, timedelta

from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from dotenv import load_dotenv

from .constant import TIMES
from .models import Service
from .tasks import notifacation_record

load_dotenv()


def booking(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу выбора услуги и делается запрос в БД  service для отображения услуг
    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со страницей выбора услуги
    """
    services = Service.objects.all()
    if request.method == "POST":
        service = request.POST.get("service")
        if service is None:
            messages.success(request, "Выберите услугу")
            return redirect(reverse("booking:booking"))
        request.session["service"] = service  # присвоение значения service в сессию
        return redirect(reverse("booking:booking_day"))

    return render(request, "booking/booking.html", {"services": services})


def booking_day(request: HttpRequest, service_id: int = None) -> HttpResponse:
    """
    Отображает страницу выбора дня для бронирования услуги.

    Args:
    - request: объект HttpRequest, содержащий информацию о запросе, который вызывает функцию.
    - service_id: необязательный целочисленный параметр, содержащий идентификатор услуги, выбранной пользователем.

    Return: объект HttpResponse с отображением шаблона booking/booking_day.html с контекстом,
    содержащим список дней и информацию о том, являются ли эти дни доступными для бронирования.
    """
    weekdays = validweekday(31)
    services = Service.objects.all()
    validate_weekdays = isweekdayvalid(weekdays)
    if service_id is not None:
        service = Service.objects.get(id=service_id)
        request.session["service"] = service.name
    if request.method == "POST":
        day = request.POST.get("day")
        request.session["day"] = day
        return redirect(reverse("booking:bookingSubmit"))

    return render(
        request,
        "booking/booking_day.html",
        {
            "weekdays": weekdays,
            "validateWeekdays": validate_weekdays,
            "services": services,
        },
    )


def bookingsubmit(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу выбора времени записи для клиента
    Args:
        request (HttpRequest): объект запроса HTTP

    Returns:
        HttpResponse: объект ответа HTTP со временем записи для клиента
    """
    services = Service.objects.all()
    today = datetime.now()
    mindate = today.strftime("%Y-%m-%d")  # выбор даты с которой можно записаться
    deltatime = today + timedelta(days=31)  # кол-во дней на которые можно записываться
    strdeltatime = deltatime.strftime("%Y-%m-%d")
    maxdate = strdeltatime  # самая дальняя запись
    day = request.session.get("day")
    service_name = request.session.get("service")
    service = Service.objects.get(name=service_name) if service_name else None
    hour = checktime(
        TIMES, day
    )  # проверка забронировано ли время другим пользователем в этот день
    time = request.POST.get("time")  # получение времени
    if request.method == "POST":
        if maxdate >= day >= mindate:
            if (
                Appointment.objects.filter(day=day, time=time).count() < 1
                and Appointment.objects.filter(day=day).count() < 11
            ):
                record = Appointment.objects.get_or_create(
                    user=request.user,
                    service=service,
                    day=day,
                    time=time,
                )
                appoint_id = record[0].id
                notifacation_record.delay(appoint_id)
                messages.success(request, "Appointment already exists!")
                return redirect("booking:user_record")
    return render(
        request,
        "booking/bookingSubmit.html",
        {"times": hour, "services": services},
    )


def userupdate(request: HttpRequest, id: int) -> HttpResponse:
    """
    Обрабатывает запрос на обновление записи клиента,клиент заново выбирает день и услугу и передает id дальше.

    Args:
    - request: объект запроса Django HttpRequest
    - id: идентификатор записи, которую нужно обновить

    Returns: HttpResponse объект, который содержит HTML-страницу с формой обновления времени и услуги.
    """
    services = Service.objects.all()
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    # Copy  booking:
    today = datetime.today()

    # 24h if statement in template:
    delta24 = userdatepicked.strftime("%Y-%m-%d") >= (
        today + timedelta(days=1)
    ).strftime("%Y-%m-%d")
    # Calling 'validWeekday' Function to Loop days you want in the next 21 days:
    weekdays = validweekday(31)

    # Only show the days that are not full:
    validateweekdays = isweekdayvalid(weekdays)
    if delta24 is True:
        if request.method == "POST":
            service = request.POST.get("service")
            day = request.POST.get("day")

            # Store day and service in django session:
            request.session["day"] = day
            request.session["service"] = service

            return redirect(reverse("booking:userUpdateSubmit", args=[id]))
        return render(
            request,
            "booking/userUpdate.html",
            {
                "weekdays": weekdays,
                "validateWeekdays": validateweekdays,
                "delta24": delta24,
                "id": id,
                "services": services,
            },
        )
    else:
        return render(request, "booking/falsedelete.html")


def userupdatesubmit(request: HttpRequest, id: int) -> HttpResponse:
    """
    Обрабатывает запрос на обновление записи клиента, клиент выбирает новое время записи.

    Args:
    - request: объект запроса Django HttpRequest
    - id: идентификатор записи, которую нужно обновить

    Returns: HttpResponse объект, который содержит HTML-страницу с формой обновления времени записи.
    """
    services = Service.objects.all()
    today = datetime.now()
    mindate = today.strftime("%Y-%m-%d")
    deltatime = today + timedelta(days=21)
    strdeltatime = deltatime.strftime("%Y-%m-%d")
    maxdate = strdeltatime
    day = request.session.get("day")
    service_name = request.session.get("service")
    service = Service.objects.get(name=service_name) if service_name else None
    hour = checktime(TIMES, day)
    appointment = Appointment.objects.get(pk=id)
    userselectedtime = appointment.time
    if request.method == "POST":
        time = request.POST.get("time")
        if (
            maxdate >= day >= mindate
            or Appointment.objects.filter(day=day).count() < 11
        ):
            if (
                Appointment.objects.filter(day=day, time=time).count() < 1
                or userselectedtime == time
            ):
                Appointment.objects.filter(pk=id).update(
                    user=request.user,
                    service=service,
                    day=day,
                    time=time,
                )
                messages.success(request, "Appointment Edited!")
                return redirect("booking:user_record")
    return render(
        request,
        "booking/userUpdateSubmit.html",
        {
            "times": hour,
            "id": id,
            "services": services,
        },
    )


def validweekday(days: int) -> list:
    """
    Возвращает список дат, на которые можно записаться на прием в течение следующих дней.

    Args:
    - days (int): количество дней, на которые нужно вернуть список дат.

    Returns:
    - weekdays : список дат в формате 'YYYY-MM-DD'.
    """
    today = datetime.now()  # получение текущей даты
    weekdays = []  # пустой список для хранения для недели
    booking_settings = BookingSettings.objects.all()
    for i in range(0, days):
        for setting in booking_settings:
            x = today + timedelta(days=i)
            start_time = datetime.combine(setting.start_time, time.min)
            end_time = datetime.combine(setting.end_time, time.max)
            if start_time <= x <= end_time:
                weekdays.append(x.strftime("%Y-%m-%d"))
    return weekdays


def isweekdayvalid(x: list) -> list:
    """
    Возвращает список дат из списка x, на которые количество записей не превышает 10.

    Args:
    x (list): Список дат в формате YYYY-MM-DD.

    Returns:
    list: Список дат в формате YYYY-MM-DD, на которые количество записей не превышает 10.
    """
    validateweekdays = []
    for j in x:
        if Appointment.objects.filter(day=j).count() < 10:  # кол-во записей на день
            validateweekdays.append(j)
    return validateweekdays


def checktime(times: list, day: str) -> list:
    """
    Возвращает список доступный диапазон времени записи на сегодняшний день

    Args:
        times (list): Список всех возможных временных рамок.
        day (str): Строка с датой в формате 'YYYY-MM-DD'.

    Returns:
        list: Возвращает список доступный диапазон времени записи на сегодняшний день
    """
    x = []
    now = datetime.now()
    time = now.time()
    formatted_time = time.strftime("%H:%M")
    for k in times:
        if k > formatted_time and day == str(now.date()):
            if Appointment.objects.filter(day=day, time=k).count() < 1:
                x.append(k)
        elif day != str(now.date()):
            if Appointment.objects.filter(day=day, time=k).count() < 1:
                x.append(k)
    return x


def remove(request: HttpRequest, id: int) -> HttpResponse:
    """
    Удаляет запись на приём по переданному id.

    Args:
        request: объект запроса.
        id (int): id удаляемой записи.

    Returns:
        Если удаление прошло успешно, то происходит перенаправление на страницу
        со списком записей пользователя, иначе отображается страница с сообщением
        об ошибке удаления.
    """
    appointment = Appointment.objects.get(pk=id)
    userdatepicked = appointment.day
    today = datetime.today()
    delta24 = userdatepicked.strftime("%Y-%m-%d") >= (
        today + timedelta(days=1)
    ).strftime("%Y-%m-%d")
    if delta24 is True:
        appointment.delete()
        return redirect(reverse("booking:user_record"))
    else:
        return render(request, "booking/falsedelete.html")


def record_view(request: HttpRequest) -> HttpResponse:
    """
    Функция обработки запроса на отображение страницы со списком записей пользователя.

    Args:
        request: объект запроса HttpRequest.

    Returns:
        Объект ответа HttpResponse с отображением страницы со списком записей пользователя.
    """
    service = Service.objects.all()
    now = datetime.now()
    appointments = Appointment.objects.filter(user=request.user).order_by("day", "time")
    appointments_expired = Appointment.objects.filter(
        Q(day__lt=now.date()) | Q(day=now.date(), time__lt=now.time())
    )

    if appointments_expired:
        for appointment in appointments_expired:
            history = HistoryBooking(
                user=appointment.user,
                service=appointment.service,
                day=appointment.day,
                time=appointment.time,
                time_ordered=appointment.time_ordered,
            )
            history.save()
        appointments_expired.delete()
    return render(
        request,
        "booking/user_record.html",
        context={"appointments": appointments, "service": service},
    )


def history_user(request: HttpRequest) -> HttpResponse:
    """
    Возвращает страницу с историей бронирования для пользователя.

    Args:
        request: объект запроса HttpRequest.

    Returns:
        Объект ответа HttpResponse с отображением страницы с историей бронирования пользователя
    """
    service = Service.objects.all()
    history_booking = HistoryBooking.objects.filter(user=request.user).order_by(
        "day", "time"
    )

    return render(
        request,
        "booking/history_user.html",
        context={"history_user": history_booking, "service": service},
    )
