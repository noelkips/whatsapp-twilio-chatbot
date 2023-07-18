from django.shortcuts import redirect, render
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
from django.conf import settings
from .models import *
from django.contrib.auth.models import User
import requests
from django.views.decorators.csrf import csrf_exempt
from mpesa.views import *



@csrf_exempt
def message(request):
    user_response = request.POST.get('Body', '').lower()
    fromId = request.POST.get('From')
    phoneId = request.POST.get('WaId')
    profileName = request.POST.get('ProfileName')
    
    response = MessagingResponse()
    try:
        chat = ChatSession.objects.get(profile__phoneNumber=fromId)
    except:
        #check that user doesn't exist

        if User.objects.filter(username=phoneId).exists():
            user = User.objects.get(username=profileName)
            user_profile = user.profile
        else:
            if phoneId:
                #create user
                user =User.objects.create_user(
                    username = phoneId,
                    email = 'whitehotel@gmail.com',
                    first_name = profileName,
                    password = 'password',
                )
                #create profile
                user_profile = Profile.objects.create(
                user = user,
                phoneNumber = fromId,
                phoneId=phoneId,
                )

                #create chat session
                chat = ChatSession.objects.create(profile=user_profile)
                #send a message
                message = "Welcome to White Hotel \n To check our menu reply with Menu \n For any other enquiry relpy with More\n"
                response.message(message)
    if "menu" in user_response and "more" not in user_response:
        if chat.selected_category:
            if chat.selected_product:
                pk = chat.selected_product
                chosen_product = Product.objects.filter(pk=pk)
                for product in chosen_product:
                    message = f'''
                                <i>PRODUCT Details</i>
                                Item Name: {product.name} \n
                                Menu:  {product.category} \n
                                description:  {product.description} \n
                                price:  {product.price} \n
                    '''
                    response.message(message)
                message = 'To place order reply with order\n'
                response.message(message)
                #place order
                if Order.objects.filter(buyer=user_profile).exists():
                    #pay
                    order = Order.objects.get(buyer=user_profile)
                    amount = order.amount
                    message = f'You are to confirm the payment of {amount} in the stk push that you received to complete the payement\n'
                    response.message(message)
                    lipa_na_mpesa_online(request, phoneId, amount)
                else:
                    message = 'How many {chosen_product.name} to you want to buy ?\n Please reply with a number\n'
                    response.message(message)
                    quantity = int(user_response.replace(' ',''))
                #place order
                    order = Order.objects.create(
                        product=chosen_product,
                        buyer = user_profile,
                        quantity = quantity,
                    )
                    order.save()
            else:
                selected_category = chat.selected_category
                products = Product.objects.filter(category=selected_category)
                message = f'Below are menu items for {selected_category.name} category \nselect item number to view details'
                response.message(message)
                for index, product in enumerate(products, start=1):
                    message= f'{index}. {product.name} \n'
                    response.message(message)
                message = 'To view item detail reply with product number\n'
                response.message(message)
                try:
                    type = int(user_response.replace(' ','')) -1
                    chat.selected_product = type
                    chat.save()
                except:
                    message = 'the product you selected does not exist try again\n select  number corresponding to the product\n'
                    response.message(message)
        else:
            categories = Category.objects.all()
            message = 'Welcome to WHITE HOTEL\n ------*Our Today\'s Menu*----\n'
            response.message(message)
            if categories:
                for index, category in enumerate(categories, start=1):
                    message= f'{index}. {category.name} \n'
                    response.message(message)
            message = 'To view menu items select category number\n'
            response.message(message)
            try:
                type = int(user_response.replace(' ','')) -1
                chat.selected_category = type
                chat.save()
            except:
                message = 'the category you selected does not exist try again\n select  number corresponding to the category\n'
                response.message(message)
    elif "more" in user_response and "menu" not in user_response:
        pass
    else:
        message = "Please select correct option \n To check our menu reply with Menu \n For any other enquiry relpy with More\n"
        response.message(message)

            

   


