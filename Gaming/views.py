import time, random, socket
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from .forms import *
from .models import *

def dtny(request):
    from datetime import datetime, timedelta 
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("",0))
    sock.listen(1)
    #sock.shutdown()
    # accept can throw socket.timeout
    #sock.settimeout(5.0)
    conn, addr = sock.accept()

    # recv can throw socket.timeout
    conn.settimeout(5.0)
    conn.recv(1024)

    return render(request, 'Gaming/dtny.html', context)


def change_action(request):
    if request.method == "GET":
        for x in request.GET:
            name = take_action(x.split('_')[1])
            act = name.objects.filter(id=int(x.split('_')[0]))
            if request.GET[x]=="Удалить":
                name.delete(act[0])  
                break
            elif request.GET[x]=="Редактировать":
                return render(request, 'Gaming/add.html', context={'title': 'Изменение элемента', 'name':name.__name__, 'value':act[0].text, 'act_id':act[0].id})
        return render(request, 'Gaming/settings.html', context={'acting': name.__name__,'title': 'Настройки', 'acts': name.objects.all()})

def adding_action(request):
    if request.method == "GET":
        name = take_action(request.GET)
        for x in request.GET:
            if request.GET[x]=="Добавить":
                act = name.objects.filter(id=int(x))
                f = name.objects.get(id=act[0].id)
                f.text = request.GET[name.__name__]
                f.save()                
                return render(request, 'Gaming/settings.html', context={'acting': name.__name__,'title': 'Настройки', 'acts': name.objects.all()})
            
        object = name.objects.create(text=request.GET[name.__name__], use=True) 
        return render(request, 'Gaming/settings.html', context={'acting': name.__name__,'title': 'Настройки', 'acts': name.objects.all()})
        #return render(request, 'Gaming/add.html', context={'title': 'Добавим новый элемент', 'name':name.__name__})
      
def add_action(request):
    name = take_action(request.GET)
    return render(request, 'Gaming/add.html', context={'title': 'Добавим новый элемент', 'name':name.__name__})

def take_action(GET):
    if 'Action' in GET:
        return Action
    elif "Easy" in GET:
        return Easy
    elif "Medium" in GET:
        return Medium
    elif "HardForMen" in GET:
        return HardForMen
    elif "HardForWomen" in GET:
        return HardForWomen
    elif "Bonus" in GET:
        return Bonus

def setings(request):
    if request.method == "GET":
        if "Home" in request.GET:
            return render(request, 'Gaming/get_names.html', context = {'form':TagForm(), 'title': 'Игра начинается'})
        else:
            f=take_action(request.GET)
            return render(request, 'Gaming/settings.html', context={'acting': take_action(request.GET).__name__,'title': 'Настройки', 'acts': take_action(request.GET).objects.all()})

def choise_name(request):
    if request.method == "GET":
        if 'player_name' in request.GET:
            name = request.GET['player_name']
            request.session['first'] = name
        else:
            return HttpResponse("Вы сломали игру")
        
        return game_it(request)
        #return render(request, 'Gaming/game_page.html', context={'title': 'Игра начинается', 'name': request.GET['man_name']})

def game_it(request):

    #if request.method == "GET":
    #    if 'player_name' in request.GET:
    #        man_name = request.GET['man_name']
    #    elif 'woman_name' in request.GET:
    #        woman_name = request.GET['woman_name']
    #    else:
    #        return HttpResponse("Вы сломали игру")
    man_name   = request.session.get('man_name')  
    woman_name = request.session.get('woman_name')
    step  = request.session.get('step')

    if step!=0:
        first = request.session.get('next_name')
    else:
        first = request.session.get('first')

    if step <= 10:
        all = Easy.objects.all()
    elif step > 10 and step <= 20:
        all = Medium.objects.all()
    elif step > 20 and first == man_name:
        all = HardForMen.objects.all()
    elif step > 20 and first == woman_name:
        all = HardForWomen.objects.all()

    if step > 25 and random.choice(range(8)) == 5:
        all = Bonus.objects.all()
        part_to_action = all[random.randint(0, len(all)-1)].text
    else:
        part_to_action = all[random.randint(0, len(all)-1)].text
        all_action = Action.objects.all()
        action = all_action[random.randint(0, len(all_action)-1)].text

        request.session['next_name'] = woman_name if first == man_name else man_name
        number_of_second = random.choice([15,20,25,30])
        request.session['number_of_second'] = number_of_second


        request.session['step'] +=1

        cont = {}
        cont['title'] = 'Игра'
        cont['text_1'] = '{a}, следующие {b} секунд твои'.format(a=first, b=number_of_second)
        cont['text_2'] = action
        cont['text_3'] = part_to_action
        cont['button'] = "Понеслась"#request.session['next_name'] 

    return render(request, 'Gaming/game_page.html', context=cont)

def timer(request):
    return render(request, 'Gaming/timer.html', context = {'title':'Время удовольствий', 'seconds': request.session.get('number_of_second')})

class TagCreate(View):
    def get(self, request):
        form = TagForm()
        return render(request, 'Gaming/get_names.html', context = {'form':form, 'title': 'Игра начинается'})

    def post(self, request):
        bound_form = TagForm(request.POST)
        if bound_form.is_valid():
            man_name    = bound_form.cleaned_data["man_name"]
            woman_name  = bound_form.cleaned_data["woman_name"]
            request.session['man_name'] = man_name
            request.session['woman_name'] = woman_name
            request.session['step'] = 0

            return render(request, 'Gaming/first_player.html', context={'title': 'Игра начинается','qustion':'Кто начнет игру?','man_name':man_name.title(), 'woman_name':woman_name.title()})
