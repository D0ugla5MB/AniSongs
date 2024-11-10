from django.shortcuts import get_list_or_404, redirect, render
from django.http import HttpResponse
from django.db.models import Q
from .models import Song


def search_song(request):
    if request.method == 'GET':
        return HttpResponse('<h1>Hello, my first Django guineapig</h1>')
    return HttpResponse('If u are seeing me, some shit happened')

def anisong_searchBar(request):
    query = request.GET.get('query', '')

    if query:
        results = get_list_or_404(
            Song.objects.select_related('anime', 'artist').filter(
                Q(anime__default_title__icontains=query) |
                Q(anime__eng_title__icontains=query) |
                Q(anime__jp_title__icontains=query)
            )
        )
    else:
        results = []

    return render(request, 'search_engine/index.html', {
        'query': query,
        'results': results,
    })

def submit_feedback(request):
    song_id = request.POST.get('song_id')
    suggestion = request.POST.get('suggestion')
    
    if song_id and suggestion:
        """ song = get_object_or_404(Song, id=song_id)
        song.suggestion = suggestion
        song.save() """
        print(f'Feedback for Song ID {song_id}: {suggestion}')
        
    return redirect('search_engine:anisong')