# pylint: disable=unused-argument
from django.shortcuts import render,redirect
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.models import User
from .models import Chat
from django.utils import timezone
import urllib.request, json,pygame
import logging

import requests
from django.views.decorators.csrf import csrf_exempt
import pygame
import time
from django.http import JsonResponse
# Create your views here.


import os
import uuid
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests



# Configure logging
logger = logging.getLogger(__name__)




def translate_to_twi(message):
    url = "https://translation-api.ghananlp.org/v1/translate"
    hdr = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': 'ac22989547f04e979df0b7e89beed41b',
    }
    data = {
        "in": message,
        "lang": "en-tw"
    }
    data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, headers=hdr, data=data)

    try:
        response = urllib.request.urlopen(req)
        # response_data = json.loads(response.read())
        translated_text = response.read().decode('utf-8')
        return translated_text
    except urllib.error.HTTPError as e:
        logger.error(f'HTTP error: {e.code} - {e.reason}')
        return "Error HTTP translating the message"
    except urllib.error.URLError as e:
        logger.error(f'URL error: {e.reason}')
        return "Error URL translating the message"
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return "Error UNEX translating the message"
    


    # url = "https://translation-api.ghananlp.org/v1/translate"
    # hdr = {
    #     'Content-Type': 'application/json',
    #     'Cache-Control': 'no-cache',
    #     'Ocp-Apim-Subscription-Key': 'ac22989547f04e979df0b7e89beed41b',
    # }
    # data = {
    #     "in": english_text,
    #     "lang": "en-gaa"
    # }
    # data = json.dumps(data).encode('utf-8')
    # req = urllib.request.Request(url, headers=hdr, data=data)

    # try:
    #     response = urllib.request.urlopen(req)
    #     # response_data = json.loads(response.read())
    #     translated_text = response.read().decode('utf-8')
    #     return translated_text
    # except urllib.error.HTTPError as e:
    #     logger.error(f'HTTP error: {e.code} - {e.reason}')
    #     return "Error HTTP translating the message"
    # except urllib.error.URLError as e:
    #     logger.error(f'URL error: {e.reason}')
    #     return "Error URL translating the message"
    # except Exception as e:
    #     logger.error(f'Unexpected error: {str(e)}')
    #     return "Error UNEX translating the message"

# def chatbot(request):

#     chats = Chat.objects.filter(user=request.user)
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         response = "Hi I am a chatbot"

#         chat = Chat(user=request.user,message = message,response = response,created_at=timezone.now())
#         chat.save()
#         return JsonResponse({'message':message,'response':response})
#     return render(request, 'chatbot.html',{'chats':chats})





# def text_to_speech(request):
#     if request.method == 'POST':
#         text = request.POST.get('text', '')
#         if not text:
#             return JsonResponse({'error': 'No text provided'}, status=400)
        
#         url = "https://translation-api.ghananlp.org/tts/v1/tts"
#         subscription_key = "ac22989547f04e979df0b7e89beed41b"
#         headers = {
#             "Content-Type": "application/json",
#             "Cache-Control": "no-cache",
#             "Ocp-Apim-Subscription-Key": subscription_key
#         }
#         payload = {
#             "text": text,
#             "language": "tw"
#         }

#         try:
#             response = requests.post(url, headers=headers, json=payload)

#             if response.status_code == 200:
#                 file_name = f"{uuid.uuid4()}.wav"
#                 file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#                 with open(file_path, 'wb') as audio_file:
#                     audio_file.write(response.content)

#                 audio_url = settings.MEDIA_URL + file_name
#                 return JsonResponse({'audio_url': audio_url, 'response': text})
#             else:
#                 return JsonResponse({'error': f"Error: {response.status_code}", 'details': response.text}, status=500)
        
#         except Exception as e:
            # return JsonResponse({'error': f"Exception occurred: {str(e)}"}, status=500)

@csrf_exempt
def text_to_speech(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        if not text:
            return JsonResponse({'error': 'No text provided'}, status=400)
        
        url = "https://translation-api.ghananlp.org/tts/v1/tts"
        subscription_key = "ac22989547f04e979df0b7e89beed41b"
        headers = {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": subscription_key
        }
        payload = {
            "text": text,
            "language": "tw"
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
           

            if response.status_code == 200:
                file_name = f"{uuid.uuid4()}.wav"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
               
                with open(file_path, 'wb') as audio_file:
                    audio_file.write(response.content)

                audio_url = settings.MEDIA_URL + file_name
                return JsonResponse({'audio_url': audio_url})
            else:
                return JsonResponse({'error': f"Error: {response.status_code}", 'details': response.text}, status=500)
        
        except Exception as e:
            print(e)
            return JsonResponse({'error': f"Exception occurred: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def speech_to_text(request):
    if request.method == 'POST':
        if 'audio' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        audio_file = request.FILES['audio']
        url = "https://translation-api.ghananlp.org/asr/v1/transcribe?language=tw"
        subscription_key = "ac22989547f04e979df0b7e89beed41b"
        headers = {
            "Content-Type": "audio/mpeg",
            "Cache-Control": "no-cache",
            "Ocp-Apim-Subscription-Key": subscription_key
        }

        response = requests.post(url, headers=headers, data=audio_file.read())

        if response.status_code == 200:
            transcription = response.json().get('transcription', '')
            return JsonResponse({'transcription': transcription})
        else:
            return JsonResponse({'error': f"Error: {response.status_code}", 'details': response.text}, status=500)

@login_required(login_url='login')
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = translate_to_twi(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password = password)
        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message':error_message})
    else:
        return render(request, 'login.html')

   
  

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                error_message = "Username already taken"
                return render(request, 'register.html', {'error_message': error_message})
            if User.objects.filter(email=email).exists():
                error_message = 'Email already taken'
                return render(request, 'register.html', {'error_message': error_message})
           
            try:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except Exception as e:            
               error_message = 'Error creating the account'
               return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'The passwords do not match'
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')




@login_required(login_url='login')
def save_translation(request, chat_id, is_correct):
    chat = Chat.objects.get(id=chat_id)
    if is_correct:
        file_path = os.path.join(settings.MEDIA_ROOT, 'correct_translations.txt')
        chat.is_correct = True
        chat.correct_file_path = file_path
    else:
        file_path = os.path.join(settings.MEDIA_ROOT, 'incorrect_translations.txt')
        chat.is_correct = False
        chat.incorrect_file_path = file_path

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f"Message: {chat.message}\nResponse: {chat.response}\n\n")

    chat.save()
    return redirect('chatbot')