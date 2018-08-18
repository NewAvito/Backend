from django.shortcuts import HttpResponse
from articles.models import Articles, User_likes
from django.db import connection
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class ArticlesView(APIView):
    permission_classes = [permissions.AllowAny, ]


    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT art.title, art.description, art.cost, art.location, " +
                       "us.username, cat.title, lk.like, art.date, art.id " +
                       "FROM avito.articles AS art " +
                       "INNER JOIN avito.auth_user AS us ON art.user_id = us.id " +
                       "INNER JOIN avito.category AS cat ON cat.id = art.category_id " +
                       "INNER JOIN avito.user_likes AS lk ON lk.id = art.likes_id " +
                       "AND art.id = lk.id_article ")

        a = cursor.fetchall()
        str = []
        for i in a:
            str.append({"title": i[0], "descrition": i[1], "cost": i[2],
                        "location": i[3], "username": i[4], "category": i[5],
                        "like": i[6], "date": i[7], "id_article": i[8]})
        return Response(str)


    def post(self, request):
        data = request.data

        username = data["username"]
        title = data["title"]
        cost = data["cost"]
        category = data["category"]
        description = data["description"]
        location = data["location"]
        date = data["date"]
        numphone = data["numphone"]
        likes = 9999

        Articles.objects.create(user=username, title=title, description=description,
                               category=category, cost=cost, location=location,
                                date=date, numphone=numphone, likes=likes)
        return Response({"answer": "Your message added!"})

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
            a.likes_id = u.id
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
        return HttpResponse(str)