import json
from pyexpat.errors import messages

from django.db.models import Avg, Q, Sum, Min, Max, Sum
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, TemplateView, FormView, CreateView



from account_module.models import User
from home_module.models import SearchHistory
from .forms import CommentForm,CommentModelForm
from .models import Product, Comment, Color, Category, Brand, ProductGallery, Favorite
from settings_site_module.models import HeaderSettings, errosPicture

# Create your views here.
from django.views.generic.list import ListView

class DetailProductView(TemplateView):
    template_name = 'product_module/detail_product_page.html'
    def get_context_data(self, **kwargs):
        context = super(DetailProductView, self).get_context_data(**kwargs)
        slug = kwargs['slug']

        # current product
        product = get_object_or_404(Product, url_title=slug)
        # sitesettings
        settings_site = HeaderSettings.objects.filter(is_main_setting=True).first()

        # favorite product
        favorite = False

        if self.request.user.is_authenticated:
            favorite = Favorite.objects.filter(
                user=self.request.user,
                product=product
            ).exists()

        # comment
        comments = Comment.objects.filter(product=product, parent=None, status='approved').order_by('-created_date').prefetch_related('comment_set')
        count_comments = Comment.objects.filter(product=product).count()

        # rating avg
        get_rating = comments.aggregate(Avg('rating'))
        convert_rating_to_flote = get_rating['rating__avg']
        if convert_rating_to_flote is not None:
            rating = round(convert_rating_to_flote, 1)
        else:
            rating = 0
        # gallery product
        gallery_product = list(ProductGallery.objects.filter(product=product))
        gallery_product.insert(0,product)

        # comment form
        comment_form = CommentForm()

        # color
        colors = Color.objects.filter(product=product)
        # product_by_category = Product.objects.filter(category=product)
        product_by_category = Product.objects.filter(category__in=product.category.all()).exclude(id=product.id).order_by('-id').distinct()[:8]

        # settings

        specifications = (
            product.specifications
                .select_related(
                'attribute',
                'attribute__group'
            )
                .order_by(
                'attribute__group__id',
                'id'
            )
        )
        print(specifications)


        context['specifications'] = specifications
        context['favorite'] = favorite
        context['product'] = product
        context['settings_site'] = settings_site
        # context['category_attributes'] = category_attributes
        # context['short_category_attributes'] = short_category_attributes
        context['comments'] = comments
        context['comments_count'] = count_comments
        context['comment_form'] = comment_form
        context['product_by_categories'] = product_by_category
        context['rating'] = rating
        context['colors'] = colors
        context['gallery_product'] = gallery_product
        return context

    def post(self, request: HttpRequest, *args, **kwargs):
        slug = kwargs['slug']
        product = get_object_or_404(Product, url_title=slug)
        comment_form = CommentForm(self.request.POST)
        if comment_form.is_valid():
            text_comment = comment_form.cleaned_data.get('comment')
            comment, created = Comment.objects.update_or_create(
                user_id=request.user.id,
                product=product,

                defaults={
                    'text': text_comment,
                    'rating': request.POST.get('rating')
                }
            )
            success_message = 'نظر شما با موفقیت ثبت شد و پس از تأیید نمایش داده می‌شود.' if created else 'نظر شما با موفقیت ویرایش شد و پس از تأیید نمایش داده می‌شود.'

            context = self.get_context_data(**kwargs)
            data_comment = render_to_string('product_module/component/comment.html', context)
            data_comment_mobile = render_to_string('product_module/component/comments_mobile.html', context)
            data_rating = render_to_string('product_module/component/rating.html', context)
            data_count_comment = render_to_string('product_module/component/count_comments.html', context)
            data_all_comment = render_to_string('product_module/component/all_comments.html', context)

            return JsonResponse({
                'message': data_comment,
                'data_comment_mobile': data_comment_mobile,
                'data_rating': data_rating,
                'data_count_comment': data_count_comment,
                'data_all_comment': data_all_comment,
                'comment_id': comment.id,
                'success_message': success_message,
            })

        comment_form.add_error('comment', 'لطفا نظر خود را وارد نمایید')
        return JsonResponse({
            'message': 'فرم نامعتبر است'
        }, status=400)

    def get(self, request: HttpRequest, *args, **kwargs):
        # اگه درخواست AJAX برای wishlist بود
        if 'product-id' in request.GET:
            return self.toggle_wishes(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def toggle_wishes(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'ابتدا وارد شوید'}, status=401)

        product_id = request.GET.get('product-id')
        product = get_object_or_404(Product, id=product_id)

        existing = Favorite.objects.filter(user=request.user, product=product).first()
        if existing:
            existing.delete()
            is_favorite = False
        else:
            Favorite.objects.create(user=request.user, product=product)
            is_favorite = True

        context = self.get_context_data(**kwargs)
        context['favorite'] = is_favorite  # override با مقدار جدید
        context['product'] = product

        html = render_to_string('product_module/component/like.html', context, request)
        return JsonResponse({'html': html, 'is_favorite': is_favorite})


class ListProductView(ListView):
    template_name = 'product_module/products_page.html'
    model = Product
    context_object_name = 'products'
    ordering = '-id'
    paginate_by = 12

    def get_queryset(self):
        query = super().get_queryset()

        search_value = self.request.GET.get('q')
        min_price = self.request.GET.get('minPrice')
        max_price = self.request.GET.get('maxPrice')


        # ✅ PRICE FILTER (اصلاح شده کامل)
        if min_price:
            query = query.filter(price__gte=min_price)

        if max_price:
            query = query.filter(price__lte=max_price)

        # SEARCH
        if search_value:
            query = query.filter(
                Q(title_fa__icontains=search_value) |
                Q(title_en__icontains=search_value) |
                Q(brand__title__icontains=search_value) |
                Q(category__title__icontains=search_value)
            )

        category = self.request.GET.get('category')
        brand = self.request.GET.get('brand')
        color = self.request.GET.get('color')
        is_amazing = self.request.GET.get('discount')
        expensive_product = self.request.GET.get('expensive')
        cheapest_product = self.request.GET.get('cheap')
        rating_product = self.request.GET.get('ratingFilter')
        newest_product = self.request.GET.get('newest')
        query = query.annotate(
            avg_rating=Avg('comments__rating')
        )

        sort = None

        if expensive_product:
            sort = '-price'

        elif cheapest_product:
            sort = 'price'

        elif rating_product:
            sort = '-avg_rating'

        elif newest_product:
            sort = '-id'
        if sort:
            query = query.order_by(sort)


        # CATEGORY
        if category:
            query = query.filter(category__url_title__iexact=category)

        # BRAND
        if brand:
            query = query.filter(brand__url_title__iexact=brand)

        # COLOR
        if color:
            query = query.filter(color__url_title__iexact=color)

        # DISCOUNT


        if is_amazing == 'True':
            query = query.filter(
                is_amazing=True,

            )

        return query
    def get_context_data(self, *args, **kwargs):
        context = super(ListProductView, self).get_context_data(*args,*kwargs)
        context['error_image'] = errosPicture.objects.filter(title='not-found').first()
        return context
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render(self.request, 'product_module/component/product_list.html',context).content.decode('utf-8')
            return JsonResponse({'html': html})
        return super(ListProductView, self).render_to_response(context, **response_kwargs)

def filter_product(request):
    categories = Category.objects.filter(is_active=True, is_delete=False)
    brands = Brand.objects.filter(is_active=True)
    colors = Color.objects.filter(is_active=True)
    price_product = Product.objects.aggregate(min_price=Min('price'), max_price=Max('price'))


    context = {
        'categories': categories,
        'brands': brands,
        'colors': colors,
        'min_price_product': price_product['min_price'],
        'max_price_product': price_product['max_price'],

    }
    return render(request, 'product_module/component/filter_product.html', context)






class BestSellingProductView(ListView):
    template_name = 'product_module/best_selling.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        query = Product.objects.filter(
            order_detail__order__is_paid=True,
            is_active=True
        )
        query = query.annotate(
            avg_rating=Avg('comments__rating')
        )
        

        get_category = self.request.GET.get('category')
        if get_category:
            query = query.filter(category__url_title=get_category)

        return query.annotate(
            count_bought_product=Sum('order_detail__count'),
            avg_rating=Avg('comments__rating')
        ).order_by('-count_bought_product')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.filter(is_active=True, is_delete=False)
        context['error_image'] = errosPicture.objects.filter(title='not-found').first()
    
        return context
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(self.request, 'product_module/component/product_list2.html', context)
        return super().render_to_response(context, **response_kwargs)





