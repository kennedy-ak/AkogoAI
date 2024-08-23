# pylint: disable=unused-argument

from django.shortcuts import render,redirect

from django.http import JsonResponse ,HttpResponse


from django.contrib import auth

from django.contrib.auth.decorators import  login_required

from django.contrib.auth.models import User

from .models import Chat ,Translation

from django.utils import timezone

import urllib.request, json
import logging
import os
import uuid

from django.conf import settings

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

import requests

from django.views.decorators.csrf import csrf_exempt

import pygame

from dotenv import load_dotenv

from django.http import JsonResponse

# Create your views here.
import random


load_dotenv()


# Configure logging

logger = logging.getLogger(__name__)



my_key = os.environ.get("MY_KEY")



def translate_text(message, source_lang, target_lang):

    url = "https://translation-api.ghananlp.org/v1/translate"

    hdr = {

        'Content-Type': 'application/json',

        'Cache-Control': 'no-cache',

        'Ocp-Apim-Subscription-Key': my_key,

    }

    data = {

        "in": message,

        "lang": f"{source_lang}-{target_lang}"

    }

    data = json.dumps(data).encode('utf-8')

    req = urllib.request.Request(url, headers=hdr, data=data)


    try:

        response = urllib.request.urlopen(req)

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





# text to speech for twi endpoint

@csrf_exempt

def text_to_speech(request):

    if request.method == 'GET':

        text = request.GET.get('text', '')

        if not text:

            return JsonResponse({'error': 'No text provided'}, status=400)
        

        url = "https://translation-api.ghananlp.org/tts/v1/tts"


        headers = {

            "Content-Type": "application/json",

            "Cache-Control": "no-cache",

            "Ocp-Apim-Subscription-Key": my_key

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

    audio_file = request.FILES['audio']


    fname = f"AUDIO_{random.randint(1,1000000)}.wav"


    with open(f"{fname}", "wb+") as destination:

        for chunk in audio_file.chunks():

            destination.write(chunk)



    payload = open(fname, 'rb').read()

    req = requests.post(

    "https://translation-api.ghananlp.org/asr/v1/transcribe?language=tw", 


    headers = {

         'Cache-Control': 'no-cache',

           'Content-Type': 'audio/mpeg',

        'Ocp-Apim-Subscription-Key': my_key ,

    },


    data = payload
     )

    

    if(req.status_code != 200): raise Exception("Request failed")


    response = req.json()

    print(response)
    



    return JsonResponse({"text" : response} , status = 200 )

def feedback(request):
    try:

        isFalse = request.POST.get("isfalse")
        tid = request.POST.get("id")
        translate = Translation.objects.get(pk = tid)
        translate.iscorrect =  isFalse == "true"
        print(translate.iscorrect)
        translate.save()

        return JsonResponse({"status" : "success"})


    except Exception as e:
        print(e)
        return HttpResponse("Internal Sever Error" , status_code = 500)

def translate(request):
    try:

        if(request.method != "POST"): raise "Method not allowed"

        to = request.POST.get("to")
        text = request.POST.get("text")
        translation = Translation(user = request.user)
        translation.user = request.user
        final_translation = ""
        translation.source = text
        if to == "tw":
            print(text)
            english_translation = translate_text(text, "gaa", "en")
            english_translation = english_translation.strip('"').strip()

            print(english_translation)

            final_translation = translate_text(english_translation, "en", "tw")

            translation.source_lang = "ga"
            translation.target_lang = "twi"

        elif to == "ga":
            
            english_translation = translate_text(text, "tw", "en")

            english_translation = english_translation.strip('"').strip()

            final_translation = translate_text(english_translation, "en", "gaa")

            print(final_translation)

            translation.source_lang = "twi"
            translation.target_lang = "ga"

        else : raise "Invalid Input language"

        translation.target = final_translation.strip('"')

        translation.save()

        return JsonResponse({'text': final_translation.strip('"')  , "id": translation.id})



    except Exception as e:
        print(e)
        return HttpResponse("Internal Sever Error" , status_code = 500)
# chatbot page rendering view

@login_required(login_url='login')
def history(request):
    try:

        translations = list(Translation.objects.filter(user= request.user))

        translations.reverse()

        return render(request , "chatbot.html" , {"history" : translations} )


    except Exception as e:
        print(e)
        return HttpResponse("Internal Sever Error" , status_code = 500)




#login page view

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

   
  

#register view

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

               print(e)         

               error_message = 'Error creating the account'

               return render(request, 'register.html', {'error_message': error_message})

        else:

            error_message = 'The passwords do not match'

            return render(request, 'register.html', {'error_message': error_message})


    return render(request, 'register.html')




#logout view 

def logout(request):

    auth.logout(request)
    return redirect('login')






#feedback

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