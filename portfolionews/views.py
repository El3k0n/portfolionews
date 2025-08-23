from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

# Create your views here.
from django.views.generic import ListView, DetailView

from .models import Article, Ticker

class IndexView(View):
    """
    View principale che mostra i ticker esistenti e permette di aggiungerne di nuovi
    """
    template_name = 'portfolionews/index.html'
    
    def get(self, request):
        tickers = Ticker.objects.all().order_by('symbol')
        context = {
            'tickers': tickers,
            'ticker_count': tickers.count()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        symbol = request.POST.get('symbol', '').strip().upper()
        name = request.POST.get('name', '').strip()
        
        if not symbol:
            messages.error(request, 'Il simbolo del ticker è obbligatorio')
            return redirect('index')
        
        # Se non è fornito un nome, usa il simbolo
        if not name:
            name = symbol
        
        # Controlla se il ticker esiste già
        if Ticker.objects.filter(symbol=symbol).exists():
            messages.warning(request, f'Il ticker {symbol} esiste già nel database')
        else:
            try:
                Ticker.objects.create(symbol=symbol, name=name)
                messages.success(request, f'Ticker {symbol} ({name}) aggiunto con successo')
            except Exception as e:
                messages.error(request, f'Errore nell\'aggiunta del ticker: {e}')
        
        return redirect('index')


class ArticleListView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'portfolionews/article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'portfolionews/article_detail.html'
