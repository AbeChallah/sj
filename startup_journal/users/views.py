from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .forms import UserRegistrationForm



#def register(request):
#    """Register a new user."""
#    if request.method != 'POST':
        # Display a blank registration form.
#        form = UserCreationForm()
#    else:
        # Process completed form
#        form = UserCreationForm(data=request.POST)

#        if form.is_valid():
            # The save method returns the newly created user object.
#            new_user = form.save()
            # Log the user in with the request and the new user object.
            # This creates a valid session for the new user.
#            login(request, new_user)
            # Redirect to entries list view.
#            return redirect('journal_entry:entries')

    # Display a blank or invalid form
#    return render(request, 'registration/register.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('journal_entry:entries')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})
