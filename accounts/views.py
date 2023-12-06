from django.shortcuts import render
from django.db import connection
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ServiceLocationForm, DeviceCreationForm
from accounts.models import ServiceLocations, Devices
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def customer_home_view(request):
    user_info = request.session.get('user_info')
    return render(request, "customer/customer_home.html", {'user_info':user_info})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')  # Redirect to the same page after successful password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'customer/change_password.html', {'form': form})

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
    messages.success(request, 'Location deleted successfully!')
    return redirect('service_locations')

@login_required
def manage_devices(request):#This is where we fetch the list of service locations
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM accounts_servicelocations")
        service_locations = cursor.fetchall()  
    return render(request, 'customer/devices_manager/locations_list.html', {'service_locations': service_locations})

def devices_list(request, location_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM accounts_devices WHERE location_id = %s", [location_id])
        devices = cursor.fetchall()  # Fetch all devices associated with the location
    form = DeviceCreationForm()
    if request.method == 'POST':
        form = DeviceCreationForm(request.POST)
        if form.is_valid():
            # Save form data into variables
            location_id = location_id
            device_name = form.cleaned_data['device_name']
            device_type_id = form.cleaned_data['device_type'].id
            model_number_id = form.cleaned_data['modelNumber'].id
            
            # Insert data using raw SQL
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    INSERT INTO accounts_devices ("location_id", "device_name", "device_type_id", "modelNumber_id")
                    VALUES (%s, %s, %s, %s);
                    ''',
                    [location_id, device_name, device_type_id, model_number_id]
                )
            return redirect('devices_list')
    return render(request, 'customer/devices_manager/devices_list.html', {'devices': devices, 'form': form})

def delete_device(request, device_id):
    device = Devices.objects.get(deviceID=device_id)    
    location_id = device.location_id # type: ignore
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM accounts_devices WHERE deviceID = %s", [device_id])
    messages.success(request, 'Device deleted successfully!')
    return redirect('devices_list', location_id=location_id)