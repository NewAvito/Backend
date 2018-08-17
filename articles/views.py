from django.shortcuts import HttpResponse
from articles.models import Articles, User_likes
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class ArticlesView(APIView):
    permission_classes = [permissions.AllowAny, ]


    def get(self, request):
        cursor = connection.cursor()
        cursor.execute("SELECT art.title, art.description, art.cost, art.location, " +
                       "us.username, cat.title, lk.like " +
                       "FROM avito.articles AS art " +
                       "INNER JOIN avito.auth_user AS us ON art.user_id = us.id " +
                       "INNER JOIN avito.category AS cat ON cat.id = art.category_id " +
                       "LEFT JOIN avito.user_likes AS lk ON lk.id = art.likes_id " +
                       "AND art.id = lk.id_article ")

        a = cursor.fetchall()
        str = []
        for i in a:
            if i[6]:
                num = i[6]
            else:
                num = 0
            str.append({"title": i[0], "descrition": i[1], "cost": i[2],
                        "location": i[3], "username": i[4], "category": i[5],
                        "like": num})
        return Response(str)


    def post(self, request):
        data = request.data

        username = data["username"]
        title = data["title"]
        cost = data["cost"]
        category = data["category"]
        description = data["description"]
        location = data["location"]

        Articles.objects.create(user=username, title=title, description=description,
                               category=category, cost=cost, location=location)
        return Response({"answer": "Your message added!"})


def user_add_like(request):
    user = request.data["username"]
    id_article = request.data["id_article"]

    try:
        i = User_likes.objects.get(user=user, id_article=id_article)
        if not i.like:
            i.like = True
        else:
            i.like = False
        i.save()
    except:
        User_likes.objects.create(user=user, id_article=id_article, like=True)
    return Response({"answer": "Done!"})


def get_category(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * " +
                   "FROM avito.category")
    a = cursor.fetchall()
    str = []
    for i in a:
        str.append({"category": i[1]})
    return HttpResponse(str)
