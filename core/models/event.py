from django.db import models
from core.utils.image_thumbnail import make_thumbnail


# ----------------------------------------------------------------------
# Event Model
# ----------------------------------------------------------------------


class Event(models.Model):

    """This model stores the data into Event table in db"""

    EVENT_TYPE = [
        ("class_qa", "Class + Q&A (60min)"),
        ("meet_&_greet", "Meet & Greet (20 min)"),
    ]

    user = models.ForeignKey(
        "core.user",
        on_delete=models.CASCADE,
        related_name="event_user",
        null=True,
        blank=True,
    )
    event_types = models.CharField(
        max_length=222,
        blank=True,
        null=True,
        verbose_name="Event Types",
        choices=EVENT_TYPE,
    )
    about = models.TextField(blank=True, null=True, verbose_name="About")
    event_class = models.ForeignKey(
        "core.EventClass",
        on_delete=models.CASCADE,
        related_name="evnt_eventclass",
        null=True,
        blank=True,
    )
    event_date_time = models.DateTimeField(
        blank=True, null=True, verbose_name="Event date & time"
    )
    price = models.FloatField(
        default=0, blank=True, null=True, verbose_name="Event Price"
    )
    photo = models.FileField(upload_to="event", blank=True, null=True)
    number_of_participants = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Number of participants"
    )
    remianing_spots = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Remianing spots"
    )
    credit_required = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Credit required"
    )
    session_lenght = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Session length"
    )
    is_featured = models.BooleanField(default=False, verbose_name="Is featured")
    active = models.BooleanField(default=True, verbose_name="Active")
    is_popular = models.BooleanField(default=False, verbose_name="Is popular")
    time_zone = models.CharField(
        max_length=222, blank=True, null=True, verbose_name="Event timezone"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )
    is_transfer = models.BooleanField(default=False, verbose_name="Is transfered")



    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def save(self, *args, **kwargs):

        if self.photo:
            make_thumbnail(self.photo, self.photo, (753, 400), 'thumb')

        super(Event, self).save(*args, **kwargs)    

    def __str__(self):
        return "{0}".format(self.event_class.name)
