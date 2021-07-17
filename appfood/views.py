from django.shortcuts import render, redirect
from django.contrib import messages

from .models import FoodCategory,Food


def home(request):
    # из базы получаем данные для сайта
    foodCategories = FoodCategory.objects.all()
    foods = Food.objects.all()

    return render(request, 'home.html',{
        'foodCategories' : foodCategories,
        'foods': foods
    })

def get_foods_by_category(request, category_id):
    foods = Food.objects.all().filter(food_category_id = category_id)
    category = FoodCategory.objects.get(id = category_id)
    foodCategories = FoodCategory.objects.all()
    return render(request, 'foods_by_category.html',{
        'foods': foods,
        'category': category,
        'foodCategories': foodCategories
    })

def food_detail_view(request, food_id):
    # получаем еду по id
    food = Food.objects.get(id = food_id)
    # Из базы получаем все категории еды (нужен для header)
    foodCategories = FoodCategory.objects.all()
    # Рендерим на шаблон food_detail.html
    return render(request,
        'food_detail.html',
        {
            'food': food,
            'foodCategories': foodCategories
        }
    )


def add_to_card(request,food_id):
    cards = request.session.get('food_cards',[])

    cards.append(food_id)

    request.session['food_cards'] = cards
    prev = request.GET.get('prev')
    return redirect(prev)

def del_to_card(request,food_id):
    cards = request.session.get('food_cards',[])

    cards.remove(food_id)

    request.session['food_cards'] = cards
    prev = request.GET.get('prev')
    return redirect(prev)

def remove_to_card(request,food_id):
    cards = request.session.get('food_cards',[])
    new_cards = []
    for card in cards:
        if card != food_id:
            new_cards.append(card)
    request.session['food_cards'] = new_cards
    prev = request.GET.get('prev')
    return redirect(prev)

def card_view(request):
    foodCategories = FoodCategory.objects.all()
    foods_ids = request.session.get('food_cards',[])
    card_foods = Food.objects.filter(id__in = foods_ids)
    for card_food in card_foods:
        card_food.count = foods_ids.count(card_food.id)
        card_food.sum = card_food.count * card_food.sale_price
    return render(request,'card_view.html',{
        'foods_ids': foods_ids,
        'card_foods': card_foods,
        'foodCategories': foodCategories
    })

def order_add(request):
    if request.method == 'POST':
        cards = request.session.get('food_cards',[])
        if len(cards) == 0:
            messages.error(request,'Вы ничего не заказали',extra_tags='danger')
            prev = request.POST.get('prev_url')
            return redirect(prev)


        else:
            client_name = request.POST.get('client_name')
            client_phone = request.POST.get('client_phone')
            client_addres = request.POST.get('client_addres')
