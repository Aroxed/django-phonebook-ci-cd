from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
import json
from .models import Contact

def index(request):
    contacts = Contact.objects.order_by('name')
    return render(request, 'contacts/index.html', {'contacts': contacts})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def get_contacts(request):
    if request.method == "POST":
        try:
            # Handle both JSON and form data
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            if not all(k in data for k in ('name', 'phone')):
                return JsonResponse({'error': 'Name and phone are required'}, status=400)
            
            contact = Contact(
                name=data['name'],
                phone=data['phone']
            )
            contact.save()
            
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'message': 'Contact added successfully'}, status=201)
            return redirect('index')
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    if request.headers.get('Accept') == 'application/json':
        contacts = [{
            'name': contact.name,
            'phone': contact.phone,
            'created_at': contact.created_at,
            'updated_at': contact.updated_at
        } for contact in Contact.objects.order_by('name')]
        return JsonResponse(contacts, safe=False)
    
    contacts = Contact.objects.order_by('name')
    return render(request, 'contacts/contacts.html', {'contacts': contacts})

@csrf_exempt
@require_http_methods(["GET", "POST", "PUT", "DELETE"])
def contact_detail(request, name):
    try:
        contact = Contact.objects.get(name=name)
        
        # Handle _method parameter for PUT and DELETE
        if request.method == "POST":
            method = request.POST.get('_method', '').upper()
            if method == 'PUT':
                request.method = 'PUT'
            elif method == 'DELETE':
                request.method = 'DELETE'
        
        if request.method == "GET":
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({
                    'name': contact.name,
                    'phone': contact.phone,
                    'created_at': contact.created_at,
                    'updated_at': contact.updated_at
                })
            return render(request, 'contacts/contact_detail.html', {'contact': contact})
        
        elif request.method == "PUT":
            # Handle both JSON and form data
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            if 'phone' in data:
                contact.phone = data['phone']
                contact.save()
            
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'message': 'Contact updated successfully'})
            return redirect('contact_detail', name=contact.name)
        
        elif request.method == "DELETE":
            contact.delete()
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'message': 'Contact deleted successfully'})
            return redirect('index')
            
    except Contact.DoesNotExist:
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'error': 'Contact not found'}, status=404)
        return render(request, 'contacts/error.html', {'error': 'Contact not found'}, status=404) 