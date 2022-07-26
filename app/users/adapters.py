from allauth.account.adapter import DefaultAccountAdapter

class UserAdapter(DefaultAccountAdapter):

  def save_user(self, request, user, form, commit=True):
    data = form.cleaned_data
    user = super().save_user(request, user, form, False)

    name = data.get("name")
    if name:
      user.name = name

    user.save()
    return user