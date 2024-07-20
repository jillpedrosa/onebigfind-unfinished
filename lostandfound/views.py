from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import LostItem, FoundItem
from .forms import LostItemForm, FoundItemForm, SearchLostItemForm, VerificationForm  # Ensure you have a VerificationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm
from datetime import timedelta
from django.utils import timezone

def home(request):
    """Render the home page."""
    return render(request, 'lostandfound/home.html')

def homepage(request):
    """Render the homepage with all found items."""
    lost_items = LostItem.objects.all()  # Display all found items
    return render(request, 'lostandfound/homepage.html', {'lost_items': lost_items})


def signup(request):
    """Handle user signup."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after signup
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'lostandfound/signup.html', {'form': form})

def login_view(request):
    """Handle user login."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'lostandfound/login.html', {'form': form, 'title': 'Login'})

@login_required  # Ensure the user is logged in to report a found item
def report_found_item(request):
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)
        print("hi", form)
        if form.is_valid():
            print("Form is valid!")
            found_item = form.save(commit=False)
            found_item.user = request.user  # Associate the found item with the logged-in user
            found_item.save()
            return redirect('confirmation')  # Redirect to the confirmation page
        else:
            print("Form is not valid")
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
    else:
        form = FoundItemForm()

    return render(request, 'lostandfound/report_found_item.html', {'form': form})

@login_required  # Ensure the user is logged in to report a lost item
def search_lost_item(request):
    """Display all lost items and allow users to report a new lost item."""
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)  # Bind the form with POST data and files
        if form.is_valid():  # Check if the form is valid
            print("Form is valid!")
            lost_item = form.save(commit=False)  # Create the LostItem instance but don't save it yet
            lost_item.user = request.user  # Associate the lost item with the logged-in user
            lost_item.save()  # Save the lost item
            return redirect('verification', lost_item.id)  # Redirect to the verification page
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
            return render(request, 'lostandfound/search_lost_item.html', {'form': form})
    else:
        form = LostItemForm()  # Initialize the form for GET requests

    lost_items = LostItem.objects.all()  # Fetch all lost items
    return render(request, 'lostandfound/search_lost_item.html', {
        'form': form,
        'lost_items': lost_items,
    })

@login_required  # Ensure the user is logged in to access the confirmation page
def confirmation(request):
    """Render the confirmation page after actions."""
    return render(request, 'lostandfound/confirmation.html')

@login_required  # Ensure the user is logged in to access lost items
def lost_items(request):
    """Display all lost items."""
    lost_items = LostItem.objects.all()  # Fetch all lost items
    return render(request, 'lostandfound/lost_items.html', {'lost_items': lost_items})

@login_required  # Ensure the user is logged in to access found items
def found_items(request):
    """Display all found items."""
    found_items = FoundItem.objects.all()  # Fetch all found items
    return render(request, 'lostandfound/found_items.html', {'found_items': found_items})

@login_required  # Ensure the user is logged in to match lost items
def match_lost_items(request, lost_item_id=None):
    """Match lost items with found items based on search criteria."""
    form = SearchLostItemForm()
    matched_items = []

    # If a lost_item_id is provided, fetch specific matches
    if lost_item_id:
        lost_item = get_object_or_404(LostItem, id=lost_item_id)
        found_items = FoundItem.objects.all()  # Fetch all found items

        # Match found items with the specific lost item
        matched_items = [
            (lost_item, found_item) for found_item in found_items
            if lost_item.name == found_item.name and 
               lost_item.unique_features == found_item.unique_features
        ]

    # Handle general search based on user input
    elif request.method == 'POST':
        form = SearchLostItemForm(request.POST)
        if form.is_valid():
            # Extract search criteria from the form
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            location = form.cleaned_data.get('location')
            date_lost = form.cleaned_data.get('date_lost')

            # Build the query for lost items
            filters = {}
            if name:
                filters['name__icontains'] = name
            if description:
                filters['unique_features__icontains'] = description
            if location:
                filters['location_lost__icontains'] = location
            if date_lost:
                filters['date_lost'] = date_lost

            # Fetch lost items based on the filters
            lost_items = LostItem.objects.filter(**filters)
            found_items = FoundItem.objects.all()  # Fetch all found items

            # Match found items with the filtered lost items
            for lost_item in lost_items:
                matched_items.extend([
                    (lost_item, found_item) for found_item in found_items
                    if lost_item.name == found_item.name and 
                       lost_item.unique_features == found_item.unique_features
                ])

    return render(request, 'lostandfound/match_lost_items.html', {
        'form': form,
        'matched_items': matched_items,
    })

@login_required  # Ensure the user is logged in to verify ownership
def verification(request, lost_item_id):
    """Render the verification form for the selected lost item."""
    lost_item = get_object_or_404(LostItem, id=lost_item_id)

    if request.method == 'POST':
        form = VerificationForm(request.POST, request.FILES)  # Ensure you have a VerificationForm
        if form.is_valid():
            messages.success(request, 'Your verification has been submitted successfully!')  # Success message
            
            # Redirect to the match lost items page, passing the lost_item_id
            return redirect('match_lost_items', lost_item_id=lost_item.id)  # Redirect to match lost items
    else:
        form = VerificationForm()

    return render(request, 'lostandfound/verification.html', {
        'form': form,
        'lost_item': lost_item,
    })

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('home')

def display_images(request):
    """Retrieve and display images of lost and found items."""
    lost_items = LostItem.objects.all()  # Query all lost items

    return render(request, 'lostandfound/display_images.html', {
        'lost_items': lost_items,
    })

def submit_lost_item(request):
    """Handle submission of a lost item."""
    if request.method == 'POST':
        form = LostItemForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            form.save()  # Save the new lost item to the database
            return redirect('success_page')  # Redirect to a success page or another view
    else:
        form = LostItemForm()  # Create a blank form

    return render(request, 'lostandfound/submit_lost_item.html', {
        'form': form,
    })

def submit_found_item(request):
    """Handle submission of a found item."""
    if request.method == 'POST':
        form = FoundItemForm(request.POST, request.FILES)  # Include request.FILES for image upload
        if form.is_valid():
            found_item = form.save(commit=False)  # Create a FoundItem instance but don't save yet
            found_item.lost_item.is_matched = True  # Mark the corresponding lost item as matched
            found_item.lost_item.save()  # Save the lost item
            found_item.save()  # Now save the found item
            return redirect('success_page')  # Redirect to a success page or another view
    else:
        form = FoundItemForm()  # Create a blank form

    return render(request, 'lostandfound/submit_found_item.html', {
        'form': form,
    })

@login_required
def claim(request, lost_item_id):
    lost_item = get_object_or_404(LostItem, id=lost_item_id)

    if request.method == 'POST':
        # Find the corresponding found item
        found_item = FoundItem.objects.filter(
            name=lost_item.name,
            unique_features=lost_item.unique_features
        ).first()
        
        if found_item:
            found_item.delete()  # Delete the found item from the database
        
        # Handle the claim logic here
        claim_deadline = timezone.now() + timedelta(days=3)
        lost_item.claimed_by = request.user
        lost_item.claim_deadline = claim_deadline
        lost_item.save()

        messages.success(request, 'You have claimed the item. Please collect it from OADSA, Xavier Hall in ADMU within 2-3 days.')
        return redirect('homepage')

    return render(request, 'lostandfound/claim.html', {'lost_item': lost_item})


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import LostItem, FoundItem
from .forms import SearchLostItemForm

@login_required
def match_lost_items(request, lost_item_id=None):
    form = SearchLostItemForm()
    matched_items = []

    if lost_item_id:
        lost_item = get_object_or_404(LostItem, id=lost_item_id)
        found_items = FoundItem.objects.all()

        matched_items = [
            (lost_item, found_item) for found_item in found_items
            if (lost_item.name.lower() in found_item.name.lower() and
                lost_item.brand.lower() in found_item.brand.lower() and
                lost_item.color.lower() in found_item.color.lower())
        ]

    elif request.method == 'POST':
        form = SearchLostItemForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            location = form.cleaned_data.get('location')
            date_lost = form.cleaned_data.get('date_lost')

            filters = {}
            if name:
                filters['name__icontains'] = name
            if location:
                filters['location_lost__icontains'] = location
            if date_lost:
                filters['date_lost'] = date_lost

            lost_items = LostItem.objects.filter(**filters)
            found_items = FoundItem.objects.all()

            for lost_item in lost_items:
                matched_items.extend([
                    (lost_item, found_item) for found_item in found_items
                    if (lost_item.name.lower() in found_item.name.lower() and
                        lost_item.brand.lower() in found_item.brand.lower() and
                        lost_item.color.lower() in found_item.color.lower())
                ])

    return render(request, 'lostandfound/match_lost_items.html', {
        'form': form,
        'matched_items': matched_items,
    })
