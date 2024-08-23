from django.urls import path



from. import views

urlpatterns =[
    path("", views.history, name='chatbot'),
    path("translate/" , views.translate , name="transalte"),
    path('login',views.login_user,name='login'),
    path('register',views.register_user,name="register"),
path('tts/', views.text_to_speech, name='text_to_speech'),
    path('save_translation/<int:chat_id>/<int:is_correct>/', views.save_translation, name='save_translation'),
    path("stt/", views.speech_to_text, name='speech_to_text'),
    path('logout',views.logout,name='logout'),
    path("feedback" , views.feedback , name = "feedback")
]
