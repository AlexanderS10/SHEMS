from re import A
from MySQLdb import IntegrityError
from django.shortcuts import render
from django.db import connection
from django.shortcuts import get_object_or_404, redirect
from .utils import *
from django.contrib import messages
from .forms import *
from accounts.models import ServiceLocations, Devices, DeviceType, DeviceModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *

@login_required
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
            city = cleaned_data.get('city')
            sstate = cleaned_data.get('sstate')
            zipcode = cleaned_data.get('zipcode')
            service_start = cleaned_data.get('serviceStart')
            square_footage = cleaned_data.get('squareFootage')
            no_bedrooms = cleaned_data.get('noBedrooms')
            no_occupants = cleaned_data.get('noOccupants')
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        '''
                        BEGIN;  -- Start a transaction
                        INSERT INTO public.accounts_servicelocations(customer_id, "unitNumber", "streetNumber", "streetName", "city", "sstate", "zipcode", "serviceStart", "squareFootage", "noBedrooms", "noOccupants")
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        COMMIT;  -- Commit the transaction
                        ''',
                        [customer_id, unit_number, street_number, street_name, city, sstate, zipcode, service_start, square_footage, no_bedrooms, no_occupants]
                    ) #Here I made the transaction atomic so that if one of the queries fails, the whole transaction will be rolled back
                messages.success(request, 'Location added successfully!')
                return redirect('service_locations')
            except IntegrityError as e:
                print(e)
                messages.error(request, 'An error occurred while adding the location.')
    else:
        form = ServiceLocationForm()
    #service_locations = ServiceLocations.objects.filter(customer=request.user.id)
    service_locations = get_service_locations(request.user.id)
    return render(request, 'customer/service_locations.html', {
        'service_locations': service_locations,
        'form': form,
    })

@login_required
def delete_location(request, location_id):
    location = get_object_or_404(ServiceLocations, id=location_id)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM accounts_servicelocations WHERE id = %s FOR UPDATE 
                ''',
                [location_id]#Here the row will be locked with an exclusive lock
            )
            location_to_delete = cursor.fetchone()
            if location_to_delete and request.user.id == location_to_delete[11]:  # Assuming user ID is at index 5
                cursor.execute(
                    '''
                    DELETE FROM accounts_servicelocations
                    WHERE id = %s
                    ''',
                    [location_id]
                )
                messages.success(request, 'Location deleted successfully!')
            else:
                messages.error(request, 'You are not authorized to delete this location.')

    except IntegrityError as e:
        print(e)
        messages.error(request, 'An error occurred while deleting the location.')
    return redirect('service_locations')

@login_required
def manage_devices(request):#This is where we fetch the list of service locations
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM accounts_servicelocations WHERE customer_id = %s", [request.user.id])
        service_locations = cursor.fetchall()  
    return render(request, 'customer/devices_manager/locations_list.html', {'service_locations': service_locations})

def devices_list(request, location_id):
    query = """
    SELECT d."device_id", d.device_name, dt.name, dm."modelNumber", d.is_active
    FROM accounts_devices AS d
    JOIN accounts_devicetype AS dt ON d.device_type_id = dt.id
    JOIN accounts_devicemodel AS dm ON d."modelNumber_id"=dm.id
    WHERE d.location_id = %s
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [location_id])
        devices = cursor.fetchall()  
    return render(request, 'customer/devices_manager/devices_list.html', {'devices': devices, 'location_id': location_id})

def delete_device(request, device_id):#Instead of delete what is needed is to set it to inactive
    global_location = None
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts_devices WHERE device_id = %s FOR UPDATE', [device_id])#Here the row will be locked an exclusive lock
            device_to_delete = cursor.fetchone()
            if device_to_delete:
                print(device_to_delete)
                location_id = device_to_delete[3]
                global_location = location_id
                cursor.execute('SELECT customer_id FROM accounts_servicelocations WHERE id = %s', [location_id]) #Slect the user to check if the user owns the device
                user = cursor.fetchone()[0] if cursor.rowcount > 0 else None
                print(user)
                if request.user.id != user:
                    messages.error(request, 'You are not authorized to delete this device.')
                    return redirect('devices_list', location_id=location_id)
                cursor.execute('UPDATE accounts_devices SET is_active = FALSE WHERE device_id = %s', [device_id])
                messages.success(request, 'Device deleted successfully!')
                return redirect('devices_list', location_id=location_id)
            else:
                messages.error(request, 'Device not found.')
                return redirect('manage_devices')

    except IntegrityError:
        messages.error(request, 'Another user modified this device. Please refresh and try again.')
        return redirect('devices_list', location_id=location_id)
    except Exception as e:
        if global_location:
            messages.error(request, f'There was an error deleting the device: {e}')
            return redirect('devices_list', location_id=global_location)
        else:
            return redirect('manage_devices')

def activate_device(request, device_id):
    global_location = None
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM accounts_devices WHERE device_id = %s FOR UPDATE', [device_id])#Here the row will be locked an exclusive lock
            device_to_delete = cursor.fetchone()
            if device_to_delete:
                location_id = device_to_delete[3]
                global_location = location_id
                cursor.execute('SELECT customer_id FROM accounts_servicelocations WHERE id = %s', [location_id]) #Slect the user to check if the user owns the device
                user = cursor.fetchone()[0] if cursor.rowcount > 0 else None
                print(user)
                if request.user.id != user:
                    messages.error(request, 'You are not authorized to activate this device.')
                    return redirect('devices_list', location_id=location_id)
                cursor.execute('UPDATE accounts_devices SET is_active = TRUE WHERE device_id = %s', [device_id])
                messages.success(request, 'Device activated successfully!')
                return redirect('devices_list', location_id=location_id)
            else:
                messages.error(request, 'Device not found.')
                return redirect('manage_devices')

    except IntegrityError:
        messages.error(request, 'Another user modified this device. Please refresh and try again.')
        return redirect('devices_list', location_id=location_id)
    except Exception as e:
        if global_location:
            messages.error(request, f'There was an error activating the device: {e}')
            return redirect('devices_list', location_id=global_location)
        else:
            return redirect('manage_devices')


def pair_device(request, location_id):
    device_types = DeviceType.objects.all()
    device_models = DeviceModel.objects.all()
    try:
        if request.method == 'POST':
            form_data = request.POST.copy()
            form = DeviceCreationForm(form_data)
            if form.is_valid():
                device_name = form.cleaned_data['device_name']
                device_type_id = form.cleaned_data['device_type'].id
                model_number_id = form.cleaned_data['modelNumber'].id
                with connection.cursor() as cursor:
                    cursor.execute(
                        '''
                        BEGIN;
                        INSERT INTO accounts_devices ("location_id", "device_name", "device_type_id", "modelNumber_id", "is_active")
                        VALUES (%s, %s, %s, %s, TRUE);
                        COMMIT;
                        ''',
                        [location_id, device_name, device_type_id, model_number_id]
                    )
                messages.success(request, 'Device paired successfully!')
                return redirect('pair_device', location_id=location_id)
            else:
                error_message = "Please correct the form data."
                messages.error(request, error_message)
            
        else:
            print ("This doesn't work")
            form = DeviceCreationForm()
    except IntegrityError as e:
        print(e)
        messages.error(request, 'An error occurred while pairing the device.')
    context = {
        'device_types': device_types,
        'device_models': device_models,
    }
    return render(request, 'customer/devices_manager/pair_device.html', context)

class EnergyUsageDataDevice24(APIView):
    def get(self, request):
        customer_id = request.user.id
        data = get_energy_usage_device_24(customer_id)
        return Response(data)
    
class EnergyUsageDataLocation24(APIView):
    def get(self, request):
        customer_id = request.user.id  # Or retrieve the customer ID from the request
        data = get_energy_usage_location_24(customer_id)
        return Response(data)

class HistoryEnergyUsageAPIView(APIView):#The API view for the history energy usage on daily basis per device for a location
    def get(self, request, location_id):
        customer_id = request.user.id  
        energy_usage_data = get_energy_usage_data(customer_id, location_id)
        return Response(energy_usage_data)
    def post(self, request, location_id):
        customer_id = request.user.id  
        days = request.data.get('days')
        if days is not None and int(days) >= 3 and int(days) <= 20:  # Ensure location_id is provided in the POST request
            energy_usage_data = get_energy_usage_data_custom(customer_id, location_id, days)
            return Response(energy_usage_data)
        else:
            return Response({"error": "Location ID is missing or range too large"}, status=status.HTTP_400_BAD_REQUEST)
    
@login_required
def history_energy_usage(request):
    #service_locations = ServiceLocations.objects.filter(customer=request.user.id)
    service_locations = get_service_locations(request.user.id)
    return render(request, 'customer/chart_templates/usage_history.html',{'service_locations':service_locations})

@login_required
def location_energy_usage(request):
    form = DateSelectorForm()
    yesterday_date = (timezone.now() - timezone.timedelta(days=2)).strftime("%Y-%m-%d")
    print(yesterday_date)
    service_locations = get_service_locations(request.user.id)
    #service_locations = ServiceLocations.objects.filter(customer=request.user.id)
    return render(request, 'customer/chart_templates/location_energy_usage.html',{'service_locations':service_locations, 'form':form, 'yesterday_date':yesterday_date})

class DeviceEnergyUsageAPIView(APIView):
    def post(self, request):
        serializer = EnergyUsageSerializer(data=request.data)
        if serializer.is_valid():
            customer_id = request.user.id
            validated_data = serializer.validated_data
            location_id = validated_data.get('location_id') # type: ignore
            date = validated_data.get('date') # type: ignore
            print(location_id, date)
            if location_id is not None and date is not None:
                energy_usage_data = device_energy_usage_per_date(customer_id, location_id, date)
                return Response(energy_usage_data)
            else:
                # Handle the case where 'location_id' or 'date' is missing
                return Response({'error': 'Location ID or Date missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@login_required
def location_usage_history_comparison(request):
    form = MonthYearForm()
    service_locations = get_service_locations(request.user.id)
    #service_locations = ServiceLocations.objects.filter(customer=request.user.id)
    return render(request, 'customer/chart_templates/location_usage_comparison.html',{'service_locations':service_locations, 'form':form})

class LocationEnergyComparisonAPIView(APIView):
    def post(self, request):
        serializer = LocationDateSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            location_id = validated_data.get('location_id') # type: ignore
            date = validated_data.get('date') # type: ignore
            print(location_id, date)
            if location_id is not None and date is not None:
                energy_usage_data = get_location_history_comparison(location_id, date)
                return Response(energy_usage_data)
            else:
                # Handle the case where 'location_id' or 'date' is missing
                return Response({'error': 'Location ID or Date missing'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required
def peak_power_view(request):
   customer_id = request.user.id
   peak_power_data = get_peak_power_data(customer_id)
   print(peak_power_data)
   return render(request, 'customer/chart_templates/peak_power_template.html', {'peak_power_data': peak_power_data})

class PeakPowerAPIView(APIView):
   def get(self, request):
       customer_id = request.user.id 
       peak_power_data = get_peak_power_data(customer_id)
       print(peak_power_data)
       return Response(peak_power_data)