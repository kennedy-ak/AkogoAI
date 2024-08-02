from django.urls import path



from. import views

urlpatterns =[
    path("",views.chatbot, name='chatbot'),
    path('login',views.login_user,name='login'),
    path('register',views.register_user,name="register"),
path('tts/', views.text_to_speech, name='text_to_speech'),

    path('logout',views.logout,name='logout')
]
