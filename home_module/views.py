from django.db.models import Count, Prefetch, Sum
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
from django.utils import timezone
import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Q
from .models import SearchHistory
from  product_module.models import Product
from home_module.models import SearchHistory
from product_module.models import Product, Slider, Category, Discount, Ads, Brand
# Create your views here.
from django.views.generic import TemplateView, ListView

from settings_site_module.models import HeaderSettings, Footer



#  HomeView
class HomeView(TemplateView):
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()

  
        sliders = (
            Slider.objects
            .filter(is_active=True)
            .select_related('category')[:5]
        )

        categories = Category.objects.filter(is_active=True, is_delete=False)

 
        Discount.objects.filter(is_active=True).exclude(
            start_date__lte=now, end_date__gte=now
        ).update(is_active=False)

        context['discount_amazing_product_time'] = (
            Discount.objects
            .filter(start_date__lte=now, end_date__gte=now, product__is_amazing=True)
            .first()
        )

   
        amazing_qs = (
            Product.objects
            .filter(is_active=True, is_delete=False, is_amazing=True, discount__is_active=True)
            .select_related('discount')
        )
        products_amazing = amazing_qs[:8]
        products_amazing_2 = amazing_qs.order_by('-id')[:8]

      
        products_category = (
            Category.objects
            .filter(is_active=True, is_delete=False)
            .prefetch_related(
                Prefetch(
                    'product_set',
                    queryset=(
                        Product.objects
                        .filter(is_active=True, is_delete=False)
                        .select_related('discount')[:8]
                    ),
                )
            )[:2]
        )

 
        collection_categories = (
            Category.objects
            .filter(is_delete=False, is_active=True)
            .prefetch_related(
                Prefetch(
                    'product_set',
                    queryset=Product.objects.filter(is_active=True, is_delete=False)[:4],
                )
            )
            .order_by('-id')[:4]
        )

  
        most_bought_products = (
            Product.objects
            .filter(order_detail__order__is_paid=True)
            .annotate(count_bought_product=Sum('order_detail__count'))
            .order_by('-count_bought_product')
            .only('title_fa', 'url_title', 'image')
        )

        context.update({
            'sliders': sliders,
            'categories': categories,
            'products_amazing': products_amazing,
            'products_amazing_2': products_amazing_2,
            'ads': Ads.objects.filter(is_active=True),
            'products': products_category,
            'collection_categories': collection_categories,
            'most_bought_products': most_bought_products,
        })
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'home_module/component/amazing_time_box.html', context)
        return super().render_to_response(context, **response_kwargs)
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)


        slider = Slider.objects.filter(is_active=True).select_related('category')[:5]
        category = Category.objects.filter(is_active=True, is_delete=False)
        discounts = Discount.objects.filter(is_active=True)
        get_time_now = timezone.now()
        for discount in discounts:
            if discount.end_date >= get_time_now and discount.start_date <= get_time_now:
                discount.is_active = True
                discount.save()
            else:
                discount.is_active = False
                discount.save()
        discount_amazing_product_time = Discount.objects.filter(
            start_date__lte=get_time_now,
            end_date__gte=get_time_now,
            product__is_amazing=True
        ).first()
        context['discount_amazing_product_time'] = discount_amazing_product_time

        products_amazing = Product.objects.filter(Q(is_active=True, is_delete=False, is_amazing=True, discount__is_active=True))[:8]
        products_amazing_2 = Product.objects.filter(is_active=True, is_delete=False, is_amazing=True, discount__is_active=True).order_by('-id')[:8]
        ads = Ads.objects.filter(is_active=True)
        products_category = Category.objects.filter(is_active=True, is_delete=False)[:2]
        collection_categories = Category.objects.filter(is_delete=False, is_active=True).order_by('-id')[:4]
        most_bought_products = Product.objects.filter(order_detail__order__is_paid=True).annotate(count_bought_product=Sum(
            'order_detail__count'
        )).order_by('-count_bought_product')



        context['categories'] = category
        context['sliders'] = slider
        context['products_amazing'] = products_amazing
        context['products_amazing_2'] = products_amazing_2
        context['ads'] = ads
        context['products'] = products_category
        context['collection_categories'] = collection_categories
        context['most_bought_products'] = most_bought_products

        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'home_module/component/amazing_time_box.html', context)
        return super().render_to_response(context, **response_kwargs)


#  Category page
def category(request: HttpRequest):
    categories = (
        Category.objects
        .filter(is_active=True, is_delete=False)
        .annotate(product_count=Count('product', distinct=True))
    )
    return render(request, 'home_module/category_page.html', {'categories': categories})


def header_partial(request):
    active_products = Product.objects.filter(is_active=True, is_delete=False)
    logo = HeaderSettings.objects.filter(is_main_setting=True)
    categories = Category.objects.filter(is_active=True, is_delete=False).prefetch_related(
        Prefetch(
            'brand_set',
            queryset=Brand.objects.filter(is_active=True).prefetch_related(
                Prefetch('products', queryset=active_products)
            ),
        )
    )
    top_searches = (
        SearchHistory.objects
        .values('query')
        .annotate(total=Count('id'))
        .order_by('-total')[:7]
    )
    context = {'logo': logo, 'categories': categories, 'top_searches': top_searches}
    return render(request, 'shared/header.html', context)


def footer_partial(request):
    settings = HeaderSettings.objects.filter(is_main_setting=True).first()
    footer_settings = Footer.objects.all().prefetch_related('footeritem_set')
    context = {'settings': settings, 'footer_settings': footer_settings}
    return render(request, 'shared/footer.html', context)



#  Search (بدون رابطه، نیازی به select/prefetch نیست)
@require_GET
def search_suggestions(request):
    try:
        q = request.GET.get('q', '').strip()
        result = {'products': [], 'history': []}

        if request.user.is_authenticated:
            history_qs = (
                SearchHistory.objects
                .filter(user=request.user)
                .order_by('-created_at')
                .values_list('query', flat=True)
                .distinct()[:6]
            )
            result['history'] = list(history_qs)

        if len(q) >= 2:
            products = (
                Product.objects
                .filter(Q(title_fa__icontains=q) | Q(title_en__icontains=q))
                .only('title_fa', 'url_title', 'image')[:8]
            )
            result['products'] = [
                {
                    'title': p.title_fa,
                    'url': f"/product/{p.url_title}",
                    'image': p.image.url if p.image else '',
                }
                for p in products
            ]
        return JsonResponse(result)

    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)


@require_POST
@login_required
def save_search_history(request):
    try:
        q = json.loads(request.body).get('q', '').strip()
    except (ValueError, AttributeError):
        q = ''

    if q:
        SearchHistory.objects.create(user=request.user, query=q)

    return JsonResponse({'ok': True})