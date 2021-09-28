
from allauth.account.forms import SignupForm
from core.models.users import User


class MyCustomSignupForm(SignupForm):
    """Custom registration form"""

    class Meta:
        model = User
        fields = '__all__'

    
    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user