from django.shortcuts import HttpResponse
from articles.models import Articles, User_likes, Category
from django.db import connection
from django.contrib.auth.models import User
from django.db.models import Max
import requests, os, sys

from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class ArticlesView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        keyword = request.GET.get("keyword", '')
        keyword_str ="\x22" + keyword + "\x22"
        page = int(request.GET.get("page", 0))
        user = request.GET.get("username", '')
        category = request.GET.get("category", '')

        if category != "":
            try:
                c = Category.objects.get(title=category).id
                add_str_4 = " art.category_id = " + c.__str__()
            except:
                add_str_4 = " art.category_id = 999 "
        else:
            add_str_4 = " "

        if user != "":
            try:
                u = User.objects.get(username=user)
                id = u.id
            except:
                id = 0

            add_str_3 = "AND " + id.__str__() + " = lk.user "
        else:
            add_str_3 = " "

        if page != "" and page > 0:
            num1 = page * 10 - 1
            num2 = num1 - 9
            num = num2.__str__() + ", " + num1.__str__()
            add_str_2 = "LIMIT " + num
        else:
            add_str_2 = " "

        if keyword_str != "":
            add_str = "(INSTR(art.title, " + keyword_str + ") > 0 OR INSTR(art.description, " + keyword_str + ") > 0) "
        else:
            add_str = " "

        if add_str_4 != "" or add_str != "":
            if len(add_str_4) > 1 and len(add_str) > 1:
                add_str_5 = "WHERE " + add_str_4 + " AND " + add_str + " "
            else:
                add_str_5 = "WHERE " + add_str_4 + add_str + " "
        else:
            add_str_5 = " "

        cursor = connection.cursor()
        cursor.execute("SELECT art.title, art.description, art.cost, art.location, " +
                       "us.username, cat.title, lk.like, art.date, art.id " +
                       "FROM avito.articles AS art " +
                       "INNER JOIN avito.auth_user AS us ON art.user_id = us.id " +
                       "INNER JOIN avito.category AS cat ON cat.id = art.category_id " +
                       "LEFT JOIN avito.user_likes AS lk ON lk.id = art.likes_id " +
                       add_str_3 + add_str_5 +
                       "ORDER BY art.id DESC " + add_str_2)

        a = cursor.fetchall()
        str = []
        for i in a:
            str.append({"title": i[0], "description": i[1], "cost": i[2],
                        "location": i[3], "username": i[4], "category": i[5],
                        "like": i[6], "date": i[7], "id_article": i[8]})
        return Response(str)

    def post(self, request):
        data = request.data

        user = data["username"]
        u = User.objects.get(username=user)
        title = data["title"]
        cost = data["cost"]
        category = data["category"]
        c = Category.objects.get(title=category)
        description = data["description"]
        location = data["location"]
        numphone = data["numphone"]
        likes = 9999
        l = User_likes.objects.get(id=likes)

        Articles.objects.create(user=u, title=title, description=description,
                                category=c, cost=cost, location=location,
                                numphone=numphone, likes=l)

        id = Articles.objects.all().aggregate(Max('id'))["id__max"]

        return Response({"answer": "Your message added!", "id_article": id})


class LikeView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        user = request.data["username"]
        id_user = User.objects.get(username=user).id
        id_article = request.data["id_article"]

        try:
            i = User_likes.objects.get(user=id_user, id_article=id_article)
            if not i.like:
                i.like = True
            else:
                i.like = False
            i.save()
        except:
            User_likes.objects.create(user=id_user, id_article=id_article, like=True)
            u = User_likes.objects.get(user=id_user, id_article=id_article)
            a = Articles.objects.get(id=id_article)
            us = User.objects.get(username=user)
            a.likes_id = u.id
            a.user = us
            a.save()
        return Response({"answer": "Done!"})


class CategoryView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT * " +
                       "FROM avito.category")
        a = cursor.fetchall()
        str = []
        for i in a:
            str.append({"category": i[1]})
        return Response(str)


class ImageView(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        data = request.data
        return Response({"answer": data})


class FileUploadView(APIView):
    permission_classes = [permissions.AllowAny, ]
    parser_classes = (MultiPartParser,)
    # FileUploadParser,
    def post(self, request, format=None):
        # up_file = request.files
        up_data = request.data["title"]
        return Response({"answer": up_data})
        # destination = open('/home/django/Backend/media/' + up_file.name, 'wb+')
        # for chunk in up_file.chunks():
        #     destination.write(chunk)
        #     destination.close()
        #
        # # ...
        # # do some stuff with uploaded file
        # # ...
        #
        # return Response(up_file.name, status.HTTP_201_CREATED)

#
# def post_file(request):
#
#     r = requests.post('http://78.140.221.46/api/image/', data={"gg":"wp"})
#
#     # print(r.raw)
#     # with open('/home/eugene/Изображения/1.jpeg', 'rb') as f:
#     #     r = requests.post('http://127.0.0.1:8000/go/test/', data={"omg":"winter"})
#         # files = {'file': f}
#     return HttpResponse("gg")
#
#
# class test(APIView):
#     permission_classes = [permissions.AllowAny, ]
#     # parser_classes = (FileUploadParser,)
#
#     def post(self,request):
#         print(request)
#         request
#         return HttpResponse("gg")
