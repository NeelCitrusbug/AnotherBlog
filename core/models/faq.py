from django.db import models

# ----------------------------------------------------------------------
# Faq Model
# ----------------------------------------------------------------------


class Faq(models.Model):

    """This model stores the data into Faq table in db"""

    FAQ_TYPES = [
        ("general_faq", "General_Faq"),
        ("event_faq", "Event_Faq"),
        ("guideline_faq", "Guideline_Faq"),
    ]
    faq_types = models.CharField(
        max_length=222,
        blank=True,
        null=True,
        verbose_name="Faq Types",
        choices=FAQ_TYPES,
    )
    question = models.CharField(
        max_length=222, blank=True, null=True, verbose_name="Question"
    )
    answer = models.TextField(blank=True, null=True, verbose_name="Answer")

    class Meta:
        verbose_name = "Faq"
        verbose_name_plural = "Faq"

    def __str__(self):
        return "{0}".format(self.faq_types)
