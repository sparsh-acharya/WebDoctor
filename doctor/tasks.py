from celery import shared_task
from datetime import datetime

from hms import disable_room


@shared_task
def appointment_completed_task(roomId,pk):
    result = disable_room(roomId)
    from doctor.models import Appointment
    appointment = Appointment.objects.get(pk=pk)
    appointment.completed()
    status = appointment.status
    print(f"{roomId} has been set {result} \n appointment has been {status}")

@shared_task
def appointment_cancelled_task(roomId):
    disable_room(roomId)
    print(f"{roomId} has been cancelled")
