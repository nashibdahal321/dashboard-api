from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User
from dashboardapi.models import Item, Category, Tag
from django.urls import path
from django.contrib.auth import authenticate, login, logout
import json

urlpatterns = []

@require_POST
def login_dashboard(request: HttpRequest):
    body = json.loads(request.body)
    if "username" not in body or "password" not in body:
        return JsonResponse({"success": False}, status=400)
    
    # Find User based on username
    user = authenticate(request, username=body["username"], password=body["password"])
    
    if user:
        login(request, user)
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"success": False}, status=400)

urlpatterns.append(path("login/", login_dashboard))

@require_POST
def register(request: HttpRequest):
    body = json.loads(request.body)
    if "username" not in body or "password" not in body or "email" not in body:
        return JsonResponse({"success": False}, status=400)
    
    if User.objects.filter(username=body["username"]).count() > 0:
        # username not unique
        return JsonResponse({"success": False, "message":"Username not unique"}, status=400)
    
    if User.objects.filter(email=body["email"]).count() > 0:
        # email not unique
        return JsonResponse({"success": False, "message":"Email not unique"}, status=400)
    
    user = User.objects.create_user(username=body["username"], password=body["password"], email=body["email"])
    if user:
        return JsonResponse({"success": True}, status=200)
    else:
        return JsonResponse({"success": False}, status=400)

urlpatterns.append(path("register/", register))

@require_GET
def get_items(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({}, status=403)
    
    item_set = Item.objects.all()
    
    if "category" in request.GET:
        item_set &= Item.objects.filter(category=request.GET["category"])

    return JsonResponse({
        "items": [
            item.to_front_end_dict() for item in item_set
        ]
    }, status=200)

urlpatterns.append(path('item/all/', get_items))

@require_GET
def get_item(request: HttpRequest, item_id):
    if not request.user.is_authenticated:
        return JsonResponse({}, status=403)

    item = Item.objects.filter(pk=item_id).first()
    return JsonResponse({
        "items": [
            item.to_front_end_dict()
        ] if item else []
        
    }, status=200)

urlpatterns.append(path('item/<item_id>/', get_item))

@require_POST
def init(request):
    # Populate the database with items (test data)
    t1 = Tag.objects.create(name="Tag 1")
    t2 = Tag.objects.create(name="Tag 2")
    
    important = Category.objects.create(name="Important")
    unimportant = Category.objects.create(name="Unimportant")

    items = [
        Item.objects.create(name="Item 1", category=important, in_stock = 20.4, available_stock=5.34),
        Item.objects.create(name="Item 2", category=important, in_stock = 200.4, available_stock=5.77),
        Item.objects.create(name="Item 3", category=unimportant, in_stock = 203.788, available_stock=50.55),
        Item.objects.create(name="Item 4", category=important, in_stock = 500, available_stock=25.34),
    ]
    items[0].tags.add(t1)
    items[0].tags.add(t2)
    return JsonResponse({})

urlpatterns.append(path('init/', init))

