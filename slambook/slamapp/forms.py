from django import forms




# from .models import Comment
#
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ('author', 'email', 'body')



from .models import UserProfile


class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['user', 'first_name', 'last_name', 'profile_pic', 'day', 'month', 'year', 'gender', 'city', 'country']