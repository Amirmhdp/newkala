#  IMPORTS
from django.core.cache import cache
from django.db.models import (
    Avg, Count, FloatField, Max, Min, OuterRef, Prefetch, Q, Subquery, Sum,
)
from django.db.models.functions import Coalesce
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView

from settings_site_module.models import HeaderSettings, errosPicture
from .forms import CommentForm
from .models import (
    Brand, Category, Color, Comment, Favorite, Product, ProductGallery,
)



#  HELPERS
def avg_rating_annotation():

    sub = (
        Comment.objects
        .filter(product=OuterRef('pk'), parent__isnull=True, status='approved')
        .order_by()
        .values('product')
        .annotate(avg=Avg('rating'))
        .values('avg')
    )
    return Coalesce(
        Subquery(sub, output_field=FloatField()),
        0.0,
        output_field=FloatField(),
    )


def get_comments_context(product):
    """
    همه‌ی داده‌های بخش نظرات با ۳ کوئری ثابت:
    نظرات (+ user)، پاسخ‌ها (+ user)، و یک aggregate برای تعداد و میانگین.
    هم در get_context_data و هم در post استفاده می‌شود.
    """
    comments = (
        Comment.objects
        .filter(product=product, parent__isnull=True, status='approved')
        .select_related('user')
        .prefetch_related(
            Prefetch(
                'comment_set',
                queryset=Comment.objects.select_related('user').order_by('created_date'),
            )
        )
        .order_by('-created_date')
    )
    stats = Comment.objects.filter(product=product).aggregate(
        total=Count('id'),
        avg=Avg('rating', filter=Q(parent__isnull=True, status='approved')),
    )
    avg = stats['avg']
    return {
        'comments': comments,
        'comments_count': stats['total'],
        'rating': round(avg, 1) if avg is not None else 0,
    }



#  DETAIL PAGE
class DetailProductView(TemplateView):
    template_name = 'product_module/detail_product_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

   
        product = get_object_or_404(
            Product.objects.select_related('discount'),
            url_title=kwargs['slug'],
        )

        settings_site = HeaderSettings.objects.filter(is_main_setting=True).first()

        favorite = (
            user.is_authenticated
            and Favorite.objects.filter(user=user, product=product).exists()
        )

        gallery_product = [product, *ProductGallery.objects.filter(product=product)]
        colors = Color.objects.filter(product=product)

        similar_products = (
            Product.objects
            .filter(category__in=product.category.values('id'),
                    is_active=True, is_delete=False)
            .exclude(id=product.id)
            .select_related('discount')          
            .order_by('-id')
            .distinct()[:8]
        )

        specifications = (
            product.specifications
            .select_related('attribute__group')
            .prefetch_related('values')
            .order_by('attribute__group__id', 'id')
        )

        context.update(get_comments_context(product))
        context.update({
            'product': product,
            'settings_site': settings_site,
            'favorite': favorite,
            'comment_form': CommentForm(),
            'product_by_categories': similar_products,
            'colors': colors,
            'gallery_product': gallery_product,
            'specifications': specifications,
        })
        return context

    # ثبت نظر 
    def post(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'ابتدا وارد شوید'}, status=401)

       
        product = get_object_or_404(Product.objects.only('id'), url_title=kwargs['slug'])

        comment_form = CommentForm(request.POST)
        if not comment_form.is_valid():
            return JsonResponse({'message': 'فرم نامعتبر است'}, status=400)

        try:
            rating = int(request.POST.get('rating', ''))
        except (TypeError, ValueError):
            rating = None
        if rating is not None and not 1 <= rating <= 5:
            rating = None

        comment, created = Comment.objects.update_or_create(
            user_id=request.user.id,
            product=product,
            defaults={
                'text': comment_form.cleaned_data.get('comment'),
                'rating': rating,
            },
        )
        success_message = (
            'نظر شما با موفقیت ثبت شد و پس از تأیید نمایش داده می‌شود.'
            if created else
            'نظر شما با موفقیت ویرایش شد و پس از تأیید نمایش داده می‌شود.'
        )

        # فقط داده‌ی نظرات (نه کل get_context_data)
        context = get_comments_context(product)
        return JsonResponse({
            'message': render_to_string('product_module/component/comment.html', context),
            'data_comment_mobile': render_to_string('product_module/component/comments_mobile.html', context),
            'data_rating': render_to_string('product_module/component/rating.html', context),
            'data_count_comment': render_to_string('product_module/component/count_comments.html', context),
            'data_all_comment': render_to_string('product_module/component/all_comments.html', context),
            'comment_id': comment.id,
            'success_message': success_message,
        })

    def get(self, request: HttpRequest, *args, **kwargs):
        if 'product-id' in request.GET:
            return self.toggle_wishes(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    # علاقه‌مندی 
    def toggle_wishes(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'ابتدا وارد شوید'}, status=401)

        product_id = request.GET.get('product-id', '')
        if not product_id.isdigit():
            return JsonResponse({'error': 'شناسه نامعتبر است'}, status=400)

        product = get_object_or_404(Product.objects.only('id'), id=product_id)

        deleted, _ = Favorite.objects.filter(user=request.user, product=product).delete()
        if deleted:
            is_favorite = False
        else:
            Favorite.objects.get_or_create(user=request.user, product=product)
            is_favorite = True


        html = render_to_string(
            'product_module/component/like.html',
            {'favorite': is_favorite, 'product': product},
            request,
        )
        return JsonResponse({'html': html, 'is_favorite': is_favorite})


#  PRODUCT LIST
class ListProductView(ListView):
    template_name = 'product_module/products_page.html'
    model = Product
    context_object_name = 'products'
    ordering = '-id'
    paginate_by = 12

    def get_queryset(self):
        params = self.request.GET

        query = (
            super().get_queryset()
            .filter(is_active=True, is_delete=False)
            .select_related('discount')
            .annotate(avg_rating=avg_rating_annotation())
        )

        needs_distinct = False   

        # PRICE
        if params.get('minPrice'):
            query = query.filter(price__gte=params['minPrice'])
        if params.get('maxPrice'):
            query = query.filter(price__lte=params['maxPrice'])

        # SEARCH
        search_value = params.get('q')
        if search_value:
            query = query.filter(
                Q(title_fa__icontains=search_value) |
                Q(title_en__icontains=search_value) |
                Q(brand__title__icontains=search_value) |
                Q(category__title__icontains=search_value)
            )
            needs_distinct = True

        # CATEGORY (url_title یکتاست ⇒ ردیف تکراری نمی‌سازد)
        if params.get('category'):
            query = query.filter(category__url_title__iexact=params['category'])

        # BRAND (FK ⇒ بدون تکرار)
        if params.get('brand'):
            query = query.filter(brand__url_title__iexact=params['brand'])

        # COLOR (url_title یکتا نیست ⇒ distinct)
        if params.get('color'):
            query = query.filter(color__url_title__iexact=params['color'])
            needs_distinct = True

        # DISCOUNT
        if params.get('discount') == 'True':
            query = query.filter(is_amazing=True)

        if needs_distinct:
            query = query.distinct()

        # SORT
        if params.get('expensive'):
            query = query.order_by('-price', '-id')
        elif params.get('cheap'):
            query = query.order_by('price', '-id')
        elif params.get('ratingFilter'):
            query = query.order_by('-avg_rating', '-id')
        elif params.get('newest'):
            query = query.order_by('-id')

        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
     
        if not context['products']:
            context['error_image'] = errosPicture.objects.filter(title='not-found').first()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(
                'product_module/component/product_list.html',
                context,
                request=self.request,
            )
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


# ═══════════════════════════════════════════════
#  FILTER SIDEBAR (render_partial)
# ═══════════════════════════════════════════════
FILTER_CACHE_KEY = 'product_filter_data'
FILTER_CACHE_SECONDS = 300      


def _build_filter_data():
    price = (
        Product.objects
        .filter(is_active=True, is_delete=False)
        .aggregate(min_price=Min('price'), max_price=Max('price'))
    )
    return {
        'categories': list(
            Category.objects.filter(is_active=True, is_delete=False).only('title', 'url_title')
        ),
        'brands': list(Brand.objects.filter(is_active=True).only('title', 'url_title')),
        'colors': list(Color.objects.filter(is_active=True).only('color', 'url_title')),
        'min_price': price['min_price'] or 0,
        'max_price': price['max_price'] or 0,
    }


def filter_product(request):
    data = cache.get_or_set(FILTER_CACHE_KEY, _build_filter_data, FILTER_CACHE_SECONDS)
    return render(request, 'product_module/component/filter_product.html', {
        'categories': data['categories'],
        'brands': data['brands'],
        'colors': data['colors'],
        'min_price_product': data['min_price'],
        'max_price_product': data['max_price'],
    })



#  BEST SELLING
class BestSellingProductView(ListView):
    template_name = 'product_module/best_selling.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = (
            Product.objects
            .filter(is_active=True, is_delete=False, order_detail__order__is_paid=True)
            .select_related('discount')
        )

        category = self.request.GET.get('category')
        if category:
            query = query.filter(category__url_title=category)

  
        return (
            query
            .annotate(
                count_bought_product=Sum('order_detail__count'),
                avg_rating=avg_rating_annotation(),
            )
            .order_by('-count_bought_product', '-id')  
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = (
            Category.objects.filter(is_active=True, is_delete=False).only('title', 'url_title')
        )
        if not context['products']:
            context['error_image'] = errosPicture.objects.filter(title='not-found').first()
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'product_module/component/product_list2.html', context)
        return super().render_to_response(context, **response_kwargs)