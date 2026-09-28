const openCloseFilter = () => {
    // تمام دکمه‌های باز و بسته کننده فیلتر رو انتخاب می‌کنیم
    const toggleFilters = document.querySelectorAll('.open-close-filter');
    // برای هر دکمه، یک event listener اضافه می‌کنیم
    toggleFilters.forEach(toggleItem => {
        toggleItem.addEventListener('click', () => {
            // پیدا کردن عنصر filter-by-product مرتبط با این toggleItem
            // فرض می‌کنیم که toggleItem و filter-by-product مربوط به هم، هر دو فرزند یک والد مشترک هستند.
            const parentContainer = toggleItem.parentNode; // والد مشترک را پیدا می‌کنیم

            // حالا از داخل والد مشترک، عنصر filter-by-product مربوطه را پیدا می‌کنیم
            const relatedContent = parentContainer.querySelector('.filter-by-product');

            // اگر عنصر پیدا شد، کلاس‌های مورد نظر رو اضافه و حذف می‌کنیم
            if (relatedContent) {
                relatedContent.classList.add('flex'); // نمایش داده می‌شود (با فرض اینکه 'flex' باعث نمایش می‌شود)
                relatedContent.classList.toggle('hidden'); // پنهان بودن را حذف می‌کنیم

            }
        });
    });
}

// تابع را اجرا می‌کنیم تا event listener ها اضافه شوند
openCloseFilter();


const priceFilterInput = document.getElementById('price-filter'); // فرض می‌کنیم این ID را دارید
if (priceFilterInput) {
    priceFilterInput.addEventListener('input', function () {
        const maxPrice = this.value;
        updateURLAndFetch('max_price', maxPrice);
    });
}



const openFilterPriceMobile = () => {
    const overlayFilter = document.getElementById('filter-overlay');
    const boxFilter = document.getElementById('filter-mobile')
    boxFilter.classList.add('open')
    overlayFilter.classList.add('open')
    document.body.style.overflow = 'hidden'

}
const openFilterSort = () => {
    const overlayFilter = document.getElementById('filter-overlay');
    const sortContent = document.getElementById('filter-mobile-sort');
    sortContent.classList.add('open');
    overlayFilter.classList.add('open')
    document.body.style.overflow = 'hidden'

}
const closeFilter = () => {
    const overlayFilter = document.getElementById('filter-overlay');
    const boxFilter = document.getElementById('filter-mobile')
    const boxFilterCategory = document.getElementById('filter-mobile-category')
    const closeFilterBrand = document.getElementById('filter-mobile-brand')
    const closeFilterColor = document.getElementById('filter-mobile-color')
    const sortContent = document.getElementById('filter-mobile-sort');

    sortContent.classList.remove('open');
    overlayFilter.classList.remove('open')
    boxFilter.classList.remove('open')
    boxFilterCategory.classList.remove('open')
    closeFilterBrand.classList.remove('open')
    closeFilterColor.classList.remove('open')
    document.body.style.overflow = 'auto'

}
const closeFilterOverlay = () => {
    const overlayFilter = document.getElementById('filter-overlay');
    const boxFilter = document.getElementById('filter-mobile')
    const boxFilterCategory = document.getElementById('filter-mobile-category')
    const closeFilterBrand = document.getElementById('filter-mobile-brand')
    const closeFilterColor = document.getElementById('filter-mobile-color')
    const sortContent = document.getElementById('filter-mobile-sort');

    sortContent.classList.remove('open');
    overlayFilter.classList.remove('open')
    boxFilter.classList.remove('open')
    boxFilterCategory.classList.remove('open')
    closeFilterBrand.classList.remove('open')
    closeFilterColor.classList.remove('open')
    document.body.style.overflow = 'auto'
}

const openFilterCategory = () => {
    const overlayFilter = document.getElementById('filter-overlay');
    overlayFilter.classList.add('open')
    const openFilter = document.getElementById('filter-mobile-category')
    openFilter.classList.add('open')
    document.body.style.overflow = 'hidden'

}
const openFilterBrand = () => {
    const openFilter = document.getElementById('filter-mobile-brand')
    openFilter.classList.add('open')
    const overlayFilter = document.getElementById('filter-overlay');
    overlayFilter.classList.add('open')
    document.body.style.overflow = 'hidden'

}
const openFilterColor = () => {
    const openFilter = document.getElementById('filter-mobile-color')
    openFilter.classList.add('open')
    const overlayFilter = document.getElementById('filter-overlay');
    overlayFilter.classList.add('open')
    document.body.style.overflow = 'hidden'
}

const openLargeIme = (imageSrc) => {
    $('#main-image-product').attr('src', imageSrc);
    $('#large-img-src').attr('href', imageSrc)
}


const addToOrder = (productId) => {
    console.log(productId)
    $.get('/order/add-product-to-order?product_id=' + productId).then(res => {
        swal({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            button: res.button
        }).then((result) => {
            if (result && res.status == 'not_auth') {
                window.location.href = '/login'
            }
        });
    })
}


const changeCountProduct = (detail_id, state) => {
    console.log(detail_id, state)
    $.get('change-count-product?detail_id=' + detail_id + '&state=' + state).then(res => {
        $('#order-product-section').html(res.data_html)
    })
}


// const bestSellingFilterAjax = (category) =>{
//     console.log(category)
//     $.get('?category=' + category).then(res =>{
//         $('#best-selling-product-box').html(res.html_data)
//     })
// }


function bestSellingFilterAjax(event, category) {
    event.preventDefault();

    fetch(`?category=${category}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => response.text())
        .then(html => {
            document.getElementById('best-selling-product-box').innerHTML = html;
        });
}

// const endDate = new Date("{{ discount_amazing_product_time.end_date|date:'c' }}")
// const unix = Math.floor(endDate.getTime() / 1000)
//
// new FlipDown(unix)
//     .start()







const countdowns = document.querySelectorAll('.countdown')

countdowns.forEach(countdown => {

    const endTime = dayjs(countdown.dataset.time)

    function updateCountdown() {

        const now = dayjs()

        const diff = endTime.diff(now)

        if (diff <= 0) {
            countdown.innerHTML = `
                <div class="text-red-500 font-bold">
                    تخفیف تمام شد
                </div>
            `
            return
        }
        const hours = Math.floor(
            (diff % (1000 * 60 * 60 * 24)) /
            (1000 * 60 * 60)
        )

        const minutes = Math.floor(
            (diff % (1000 * 60 * 60)) /
            (1000 * 60)
        )

        const seconds = Math.floor(
            (diff % (1000 * 60)) /
            1000
        )
        countdown.querySelector('.hours').innerText = hours
        countdown.querySelector('.minutes').innerText = minutes
        countdown.querySelector('.seconds').innerText = seconds
    }
    updateCountdown()

    setInterval(updateCountdown, 1000)
})



// let slider = document.getElementById('price-slider');
//
// // noUiSlider.create(slider,{
// //     start:[100,1000],
// //     connect:true,
// //     range:{
// //         min:0,
// //         max:5000
// //     }
// // });




// const submitFilterPrice = parent.querySelector('.submit-filter-price');
// submitFilterPrice.addEventListener('click', () => {
//     fetch(`?min-price=${currentMin}&max-price=${currentMax}`, {
//         headers: { 'X-Requested-With': 'XMLHttpRequest' }
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('list-of-product').innerHTML = data.html;
//     });
// });





// const itemFilter = document.querySelectorAll('.filter-product');
//
// itemFilter.forEach(filter => {
//     filter.addEventListener('click', async function (e) {
//         e.preventDefault();
//         params = new URLSearchParams();
//         const value_category = this.dataset.value;
//         const value_brand = this.dataset.brandValue;
//         const value_color = this.dataset.colorValue;
//         if (value_category){
//             params.append('category', value_category)
//         }
//         if (value_brand){
//             params.append('brand', value_brand)
//         }
//         if (value_color){
//             params.append('color', value_color)
//         }
//         console.log(params.toString())
//         const content = document.getElementById('list-of-product')
//         const response = await fetch(`?${params.toString()}`, {
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         });
//         const data = await response.json();
//         content.innerHTML = data.html
//
//     });
// });
const itemFilter = document.querySelectorAll('.filter-product');
const clearFilter = document.querySelectorAll('.clear-filter');
const content = document.getElementById('list-of-product');

// state فیلترها
const filters = {
    category: null,
    brand: null,
    color: null,
    minPrice: null,
    maxPrice: null,
    expensive: null,
    cheap: null,
    newest: null,
    ratingFilter: null,
    available: null,
    q: null,
    discount: null
};
// ✅ اینجا - مقدار اولیه q رو از URL میخونه
const urlParams = new URLSearchParams(window.location.search);
filters.q = urlParams.get('q');
filters.category = urlParams.get('category');
filters.brand = urlParams.get('brand');
filters.color = urlParams.get('color');
filters.minPrice = urlParams.get('minPrice');
filters.maxPrice = urlParams.get('maxPrice');
filters.discount = urlParams.get('discount');
// 🔥 تابع مرکزی ارسال درخواست
async function fetchProducts() {
    const params = new URLSearchParams();

    Object.keys(filters).forEach(key => {
        if (filters[key] !== null && filters[key] !== undefined) {
            params.append(key, filters[key]);
        }
    });

    const response = await fetch(`?${params.toString()}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });

    const data = await response.json();
    content.innerHTML = data.html;
}

itemFilter.forEach(filter => {
    filter.addEventListener('click', async function (e) {
        e.preventDefault();

        if (this.dataset.value) {
            filters.category = this.dataset.value;
        }

        if (this.dataset.brandValue) {
            filters.brand = this.dataset.brandValue;
        }

        if (this.dataset.colorValue) {
            filters.color = this.dataset.colorValue;
        }
        if (this.dataset.expensiveValue) {
            filters.expensive = this.dataset.expensiveValue;
            filters.cheap = null;
            filters.newest = null;
            filters.ratingFilter = null;
        }

        if (this.dataset.cheapestValue) {
            filters.cheap = this.dataset.cheapestValue;
            filters.expensive = null;
            filters.newest = null;
            filters.ratingFilter = null;
        }

        if (this.dataset.newestValue) {
            filters.newest = this.dataset.newestValue;
            filters.expensive = null;
            filters.cheap = null;
            filters.ratingFilter = null;
        }

        if (this.dataset.ratingValue) {
            filters.ratingFilter = this.dataset.ratingValue;
            filters.expensive = null;
            filters.cheap = null;
            filters.newest = null;
        }


        await fetchProducts();
    });
});
        const searchInput = document.getElementById('search-box-md');
        if (searchInput) {
            searchInput.addEventListener('input', function() {
                filters.q = this.value || null;
                fetchProducts();
            });
        }

clearFilter.forEach(remove => {
    remove.addEventListener('click', async function (e) {
        e.preventDefault();

        filters.category = null;
        filters.brand = null;
        filters.color = null;
        filters.minPrice = null;
        filters.maxPrice = null;
        filters.expensive = null;
        filters.cheap = null;
        filters.ratingFilter = null;
        filters.newest = null;
        filters.available = null;

        const response = await fetch(window.location.pathname, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const data = await response.json();
        content.innerHTML = data.html;
    });
})





const sliders = document.querySelectorAll('.price-slider');

sliders.forEach(slider => {
    const min = Number(slider.dataset.min);
    const max = Number(slider.dataset.max);

    noUiSlider.create(slider, {
        start: [
            Number(slider.dataset.startMin),
            Number(slider.dataset.startMax)
        ],
        connect: true,
        range: { min, max }
    });

    const parent = slider.closest('.filter-by-product');
    const minPrice = parent.querySelector('.min-price');
    const maxPrice = parent.querySelector('.max-price');

    let timeout;

    slider.noUiSlider.on('update', function (values) {
        const currentMin = Math.round(values[0]);
        const currentMax = Math.round(values[1]);

        filters.minPrice = currentMin;
        filters.maxPrice = currentMax;

        minPrice.textContent = currentMin.toLocaleString('fa-IR');
        maxPrice.textContent = currentMax.toLocaleString('fa-IR');

        clearTimeout(timeout);

        timeout = setTimeout(() => {
            fetchProducts();
        }, 300);
    });
});

setTimeout(function () {
    const messages = document.querySelectorAll('.message-box');
    messages.forEach(msg => {
        msg.style.transition = '0.5s';
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 500);
    });
}, 6000); // 3 ثانیه

const avatar = document.getElementById('id_avatar');
const formAvatar = document.getElementById('avatar-form');
avatar.addEventListener('change',() =>{
    formAvatar.submit();
})


// filter cities by province with AJAX
const province = document.getElementById('id_province');

province.addEventListener('change', async function (){
    const value = this.value;
    const response = await fetch(`loaded-cities?province=${value}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const data = await response.json()
    const citiesList = document.getElementById('cities-list-input-add');
    citiesList.innerHTML = data.cities

})

const deleteAddress = async (addressId) =>{
   const response = await fetch(`delete-address?address-id=${addressId}`, {
    headers: {
        'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const data = await response.json()
    const listAddress = document.getElementById('my-address')
    listAddress.innerHTML = data.list_address
}



const deleteWish = async (wish_id) =>{
    console.log(wish_id)
    const response = await fetch(`delete-wishes?wish-id=${wish_id}`,{
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const data = await response.json()
    const listWishes = document.getElementById('wishlist')
    listWishes.innerHTML = data.html
}
