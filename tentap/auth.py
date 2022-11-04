from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from tentap.models import Users
from tentap.serializers import UsersSerializer
from tentap.security import encode_password


# https://www.django-rest-framework.org/tutorial/1-serialization/
# TODO there is an important not on the website about @crsf_exempt check it out.
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['password'] = encode_password(data['password'])
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"RESPONSE": "CREATED"}, status=201)
        return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({"ERROR": "WRONG REQUEST METHOD"})



@csrf_exempt
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if list(data.keys()) == ['user_name', 'password']:
            try:
                user = Users.objects.get(user_name=data['user_name'])
                response_data = UsersSerializer(user).data
                if response_data['password'] == encode_password(data['password']):
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({"ERROR": "WRONG PASSWORD"}, status=404)

            except:
                return JsonResponse({"ERROR": "USERNAME DOSE NOT EXIST"}, status=404)

        elif list(data.keys()) == ['e_mail', 'password']:
            try:
                user = Users.objects.get(e_mail=data['e_mail'])
                response_data = UsersSerializer(user).data
                if response_data['password'] == encode_password(data['password']):
                    return JsonResponse(response_data)
                else:
                    return JsonResponse({"ERROR": "WRONG PASSWORD"}, status=404)
            except:
                return JsonResponse({"ERROR": "EMAIL DOSE NOT EXIST"}, status=404)
        else:
            return JsonResponse({"ERROR": "WRONG INPUT"})
    else:
        return JsonResponse({"ERROR": "WRONG REQUEST METHOD"})


@csrf_exempt
def users_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        data['password'] = encode_password(data['password'])
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"TEST": "DDF"}, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def user_details(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        user = Users.objects.get(pk=pk)
    except Users.objects.get(pk=pk).DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UsersSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UsersSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)
