from django.core.management.base import BaseCommand


from blog.models import Post
from mysite.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.contrib.auth.models import User

from django.template.loader import render_to_string
from django.utils import timezone

class Command(BaseCommand):

    help = "Send Email"

    def handle(self, *args, **options):
        latest_post = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[0]
        print(latest_post)
        try:
            subject = "Latest Post is Here!!"
            # message = "abcd"
            message = render_to_string('core/latest_post.html', {'post':latest_post})
            recepient = ['shahneel169@gmail.com']

            send_mail(subject, message, EMAIL_HOST_USER,recepient,fail_silently=False,)
            print(".........................................success")
            self.stdout.write(self.style.SUCCESS("Successfully sent email"))
        except:
            self.stdout.write(self.style.ERROR("Error in sending email"))
