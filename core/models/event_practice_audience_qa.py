from django.db import models

# ----------------------------------------------------------------------
# Event Practice Audience QA Model
# ----------------------------------------------------------------------

class EventPracticeAudienceQA(models.Model):

    """This model stores the data into Event Order table in db"""

    event = models.ForeignKey(
        "core.event",
        on_delete=models.CASCADE,
        related_name="evnt_qa",
        null=True,
        blank=True,
    )
    question = models.CharField(
        max_length=222, blank=True, null=True, verbose_name="Question"
    )
    answer = models.TextField(blank=True, null=True, verbose_name="Answer")

    class Meta:
        verbose_name = "Practice Audience Q.A."
        verbose_name_plural = "Practice Audience Q.A."

    def __str__(self):
        return "{0}".format(self.question)
