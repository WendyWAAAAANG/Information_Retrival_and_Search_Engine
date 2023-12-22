from django.shortcuts import render
from .es_call import drugsearch
from .blacklist import black_list
# from .drug_query import drugsearch_core
# Create your views here.
from django.http import HttpResponse

#def search_index(request): 
#    return HttpResponse("Search site coming soon!")

def search_index(request):
    results = []
    black = []
    name_term = ""
    type_term = ""
    if request.GET.get('name') and request.GET.get('type'):
        name_term = request.GET['name']
        type_term = request.GET['type']
        black.extend(black_list(keyword = name_term))
        black.extend(black_list(keyword = type_term))
    elif request.GET.get('name'):
        name_term = request.GET['name']
        black.extend(black_list(keyword = name_term))
    elif request.GET.get('type'):
        type_term = request.GET['type']
        black.extend(black_list(keyword = type_term))
    search_term = name_term or type_term
    #black1 = black_list(keyword = name_term)
    #black2 = black_list(keyword = type_term)
    results = drugsearch(name = name_term, typee=type_term)
    # results = drugsearch(name = name_term, typee=type_term)
    
    recommdation = results[1]
    suggestion = results[2]
    
    print(recommdation)

    #context = { 'name_black': black1, 'type_black': black2, 'results': results[0], 'count': len(results[0]), 'search_term':  search_term, 'recommdation': recommdation, 'suggest': suggestion, 'history': results[3], 'hotword': results[4], 'hislen': results[5], 'hotlen': results[6]}
    context = { 'black': black, 'results': results[0], 'count': len(results[0]), 'search_term':  search_term, 'recommdation': recommdation, 'suggest': suggestion, 'history': results[3], 'hotword': results[4], 'hislen': results[5], 'hotlen': results[6]}
    return render(request,'index_t.html',context)


def home(request):
    return render(request,'home.html')
    




    
    
    
