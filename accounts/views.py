from django.shortcuts import render
from django.db import connection
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ServiceLocationForm
from accounts.models import ServiceLocations
from django.contrib.auth.decorators import login_required


def customer_home_view(request):
    user_info = request.session.get('user_info')
    return render(request, "customer/customer_home.html", {'user_info':user_info})

@login_required
def service_locations(request):
    if request.method == 'POST':
        form = ServiceLocationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            customer_id = request.user.id  
            unit_number = cleaned_data.get('unitNumber')
            street_number = cleaned_data.get('streetNumber')
            street_name = cleaned_data.get('streetName')
            sstate = cleaned_data.get('sstate')
            zipcode = cleaned_data.get('zipcode')
            service_start = cleaned_data.get('serviceStart')
            square_footage = cleaned_data.get('squareFootage')
            no_bedrooms = cleaned_data.get('noBedrooms')
            no_occupants = cleaned_data.get('noOccupants')
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    INSERT INTO public.accounts_servicelocations(customer_id, "unitNumber", "streetNumber", "streetName", "sstate", "zipcode", "serviceStart", "squareFootage", "noBedrooms", "noOccupants")
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                    ''',
                    [customer_id, unit_number, street_number, street_name, sstate, zipcode, service_start, square_footage, no_bedrooms, no_occupants]
                )
            messages.success(request, 'Location added successfully!')
            return redirect('service_locations')
    else:
        form = ServiceLocationForm()
    service_locations = ServiceLocations.objects.all()
    
    return render(request, 'customer/service_locations.html', {
        'service_locations': service_locations,
        'form': form,
    })

@login_required
def delete_location(request, location_id):
    # Perform deletion using raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            DELETE FROM accounts_servicelocations
            WHERE id = %s
            ''',
            [location_id]
        )
    messages.success(request, 'Location added successfully!')
    return redirect('service_locations')