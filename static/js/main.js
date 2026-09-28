document.addEventListener('DOMContentLoaded', () => {


    const btnCategory = document.getElementById('btn-category');
    const menuCategory = document.getElementById('menu-category');
    if (btnCategory && menuCategory) {
        let menuTimeout;
        btnCategory.addEventListener('mouseenter', () => {
            clearTimeout(menuTimeout);
            menuCategory.classList.remove('hidden');
            menuCategory.classList.add('flex');
        });


        btnCategory.addEventListener('mouseleave', () => {

            menuTimeout = setTimeout(() => {

                if (!menuCategory.matches(':hover')) {
                    menuCategory.classList.add('hidden');
                    menuCategory.classList.remove('flex');
                }
            }, 150);
        });


        menuCategory.addEventListener('mouseenter', () => {
            clearTimeout(menuTimeout);
            menuCategory.classList.remove('hidden');
            menuCategory.classList.add('flex');
        });


        menuCategory.addEventListener('mouseleave', () => {

            menuTimeout = setTimeout(() => {
                menuCategory.classList.add('hidden');
                menuCategory.classList.remove('flex');

            }, 150);
        });
    }
});





document.addEventListener('DOMContentLoaded', () => {
    // Select all elements with the class 'footer-header'
    const footerHeaders = document.querySelectorAll('.footer-header');

    footerHeaders.forEach(header => {
        header.addEventListener('click', () => {
            // Find the related content, open icon, and close icon within this specific footer section
            const footerSection = header.closest('.flex-col'); // Get the parent container of the entire footer section
            const footerContent = footerSection.querySelector('.footer-content');
            const openIcon = header.querySelector('.open-icon');
            const closeIcon = header.querySelector('.close-icon');

            // Toggle visibility of icons
            openIcon.classList.toggle('hidden');
            openIcon.classList.toggle('inline-block');
            closeIcon.classList.toggle('hidden');
            closeIcon.classList.toggle('inline-block');

            // Toggle visibility of footer content
            footerContent.classList.toggle('hidden');
            footerContent.classList.toggle('flex'); // Assuming 'flex' is the display for showing content
        });
    });

});
const showInformation = () => {
    let productInfo = document.getElementById('product-info');
    let bodyElement = document.body; // دسترسی به عنصر body

    // 1. اضافه کردن کلاس برای نمایش باکس اطلاعات
    productInfo.classList.remove('hidden');
    productInfo.classList.add('flex');

    // 2. غیرفعال کردن اسکرول صفحه اصلی (body)
    bodyElement.style.overflow = 'hidden';
};

const closeInformation = () => {
    let productInfo = document.getElementById('product-info');
    let bodyElement = document.body; // دسترسی به عنصر body

    // 1. مخفی کردن باکس اطلاعات
    productInfo.classList.remove('flex');
    productInfo.classList.add('hidden');

    // 2. فعال کردن مجدد اسکرول صفحه اصلی (body)
    bodyElement.style.overflow = 'auto'; // یا '' (خالی)
};

// تابع نمایش کامل پاراگراف
const completeParagraph = (btn) => {
    // 1. پیدا کردن بلاک کامل کامنت که دکمه در آن قرار دارد.
    // فرض می‌کنیم هر کامنت کامل (شامل متن، دکمه و ...) در یک عنصر با کلاس 'comment-container' قرار دارد.
    const commentContainer = btn.closest('.comment-container');

    if (commentContainer) {
        const comment = commentContainer.querySelector('.comment');
        if (comment) {
            // 2. حذف محدودیت خط برای نمایش متن کامل
            comment.classList.remove('line-clamp-3');
        }
        // 3. مخفی کردن دکمه "ادامه"ی مربوط به همین کامنت
        btn.classList.add('hidden');
    } else {
        console.error("خطا: والد با کلاس 'comment-container' پیدا نشد.");
    }
}

// تابع نمایش باکس نظرات
const showComment = () => {
    let bodyElement = document.body;
    let commentBox = document.getElementById('all-comment');

    commentBox.classList.remove('hidden'); // استفاده از remove به جای toggle برای اطمینان از نمایش
    bodyElement.style.overflow = 'hidden'; // جلوگیری از اسکرول صفحه اصلی
}

// تابع بستن باکس نظرات
const closeCommentBox = () => {
    let bodyElement = document.body;
    let commentBox = document.getElementById('all-comment');

    commentBox.classList.add('hidden'); // استفاده از add به جای toggle برای اطمینان از مخفی شدن
    bodyElement.style.overflow = 'auto'; // فعال سازی مجدد اسکرول صفحه اصلی
}


const openSellerInfo = () => {
    let bodyElement = document.body;
    const selectSellerSection = document.getElementById('sellers-section');
    selectSellerSection.classList.toggle('hidden');
    selectSellerSection.classList.add('flex');
    bodyElement.style.overflow = 'hidden';
}
const closeSellerSection = () => {
    let bodyElement = document.body;
    const selectSellerSection = document.getElementById('sellers-section');
    selectSellerSection.classList.toggle('hidden');
    selectSellerSection.classList.remove('flex');
    bodyElement.style.overflow = 'auto';
}

document.addEventListener("DOMContentLoaded", function () {

})

// const s = () => {
//     const listItemNavProduct = document.getElementsByClassName('nav-product');
//     const listItemNavProductBorder = document.getElementsByClassName('nav-product-border');
//
//     Array.from(listItemNavProduct).forEach((item, index) => {
//         item.addEventListener('click', () => {
//             // حذف حالت فعال از همه
//             Array.from(listItemNavProduct).forEach(i =>
//                 i.classList.remove('text-red-600') // این کلاس باید به المنت والد اضافه شود
//             );
//             Array.from(listItemNavProductBorder).forEach(b =>
//                 b.classList.add('hidden')
//             );
//
//             // فعال کردن آیتم کلیک‌شده
//             item.classList.add('text-red-600'); // کلاس فعال‌سازی اضافه شد
//             listItemNavProductBorder[index].classList.remove('hidden');
//         });
//     });
// }
//
// s();
//
//
// const setupProductNavbar = () => {
//     const navItems = document.querySelectorAll('.item-detail-product');
//     const sectionMapping = {
//         'مشخصات کالا': 'information-product', // آیدی برای مشخصات کالا
//         'نظرات کاربران': 'newComment',         // آیدی برای نظرات کاربران
//         'کالاهای مشابه': 'same-product-item',      // آیدی برای کالاهای مشابه
//     };
//
//     // نگاشت معکوس: آیدی بخش‌ها به متن آیتم نوار ناوبری
//     const idToNavItemTextMap = {
//         'information-product': 'مشخصات کالا',
//         'newComment': 'نظرات کاربران',
//         'same-product-item': 'کالاهای مشابه'
//     };
//
//     // تابع کمکی برای فعال/غیرفعال کردن آیتم نوار ناوبری
//     const updateNavActiveState = (activeSectionId) => {
//         navItems.forEach(item => {
//             const correspondingSectionId = sectionMapping[item.textContent.trim()]; // trim() برای حذف فاصله‌های اضافی احتمالی
//             if (correspondingSectionId === activeSectionId) {
//                 // فعال کردن آیتم
//                 item.classList.add('font-bold', 'text-red-600');
//                 const nextSpan = item.nextElementSibling;
//                 if (nextSpan) {
//                     nextSpan.classList.remove('hidden');
//                 }
//             } else {
//                 // غیر فعال کردن آیتم
//                 item.classList.remove('font-bold', 'text-red-600');
//                 const nextSpan = item.nextElementSibling;
//                 if (nextSpan) {
//                     nextSpan.classList.add('hidden');
//                 }
//             }
//         });
//     };
//
//     // مدیریت کلیک‌ها برای اسکرول نرم
//     navItems.forEach(item => {
//         item.addEventListener('click', () => {
//             const sectionTitle = item.textContent.trim(); // trim() برای اطمینان از تطابق دقیق
//             const sectionId = sectionMapping[sectionTitle];
//
//             if (sectionId) {
//                 const targetSection = document.getElementById(sectionId);
//                 if (targetSection) {
//                     // اسکرول به بخش مورد نظر
//                     targetSection.scrollIntoView({ behavior: 'smooth', block: 'center' }); // یا 'start' یا 'nearest'
//                     // بعد از کلیک، بلافاصله وضعیت فعال را به‌روز می‌کنیم
//                     // (اگرچه اسکرول خودکار هم وضعیت را به‌روز خواهد کرد، این کار تضمین می‌کند که بلافاصله درست شود)
//                     updateNavActiveState(sectionId);
//                 }
//             }
//         });
//     });
//
//     // گوش دادن به رویداد اسکرول صفحه
//     window.addEventListener('scroll', () => {
//         let currentActiveSectionId = null;
//         let maxTop = -1000; // مقدار اولیه کوچک برای مقایسه
//
//         // پیمایش معکوس بخش‌ها برای یافتن اولین بخشی که در بالای صفحه قرار دارد
//         // (یا بخشی که بیشترین قسمت آن در بالای صفحه است)
//         const sections = Object.entries(sectionMapping);
//         for (let i = sections.length - 1; i >= 0; i--) {
//             const [sectionText, sectionId] = sections[i];
//             const sectionElement = document.getElementById(sectionId);
//
//             if (sectionElement) {
//                 const rect = sectionElement.getBoundingClientRect();
//                 // اگر بالای بخش در view-port باشد (یا کمی بالاتر)
//                 if (rect.top < window.innerHeight * 0.6 && rect.bottom >= 0) { // 0.6 یعنی 60% از ارتفاع صفحه
//                     // اگر این بخش بالاتر از بخش قبلی فعال است، آن را به عنوان فعال در نظر بگیر
//                     // این منطق اطمینان می‌دهد که وقتی بین دو بخش هستیم، بخش بالاتر فعال بماند
//                     if (rect.top > maxTop) {
//                         maxTop = rect.top;
//                         currentActiveSectionId = sectionId;
//                     }
//                 }
//             }
//         }
//
//         // اگر بخشی پیدا شد که فعال است، وضعیت نوار ناوبری را به‌روز کن
//         if (currentActiveSectionId) {
//             updateNavActiveState(currentActiveSectionId);
//         } else {
//             // اگر هیچ بخشی فعال نبود (مثلاً در ابتدای صفحه هستیم)، اولین آیتم را فعال کن
//             // یا هیچ کدام را فعال نکن، بسته به نیاز
//             // در اینجا، اگر هیچ بخشی فعال نبود، همه را غیرفعال می‌کنیم
//             navItems.forEach(item => {
//                 item.classList.remove('font-bold', 'text-red-600');
//                 const nextSpan = item.nextElementSibling;
//                 if (nextSpan) {
//                     nextSpan.classList.add('hidden');
//                 }
//             });
//         }
//     });
//
//     // مقداردهی اولیه وضعیت فعال بر اساس موقعیت فعلی صفحه هنگام بارگذاری
//     // این کار باعث می‌شود که اگر صفحه با اسکرول باز شد، آیتم درست فعال باشد
//     window.dispatchEvent(new Event('scroll'));
// };




document.addEventListener('DOMContentLoaded', () => {
    const items = document.querySelectorAll('.nav-item-product');
    const IDS = ['description-product', 'information-product', 'slider_mobile_comments', 'same-product-item'];
    let isClicking = false;

    const activate = (id) => {
        items.forEach(item => {
            const isActive = item.dataset.target === id;
            item.querySelector('.nav-title').classList.toggle('text-red-600', isActive);
            item.querySelector('.nav-title').classList.toggle('text-slate-500', !isActive);
            item.querySelector('.nav-border').classList.toggle('hidden', !isActive);
        });
    };

    items.forEach(item => {
        item.addEventListener('click', () => {
            const target = document.getElementById(item.dataset.target);
            if (!target) return;
            isClicking = true;
            activate(item.dataset.target);
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            setTimeout(() => isClicking = false, 800);
        });
    });

    const observer = new IntersectionObserver((entries) => {
        if (isClicking) return;
        entries.forEach(entry => {
            if (entry.isIntersecting) activate(entry.target.id);
        });
    }, { threshold: 0.3, rootMargin: '-10% 0px -60% 0px' });

    IDS.forEach(id => {
        const el = document.getElementById(id);
        if (el) observer.observe(el);
    });

    activate(IDS[0]);
});




document.addEventListener('DOMContentLoaded', () => {
    const sameLink = document.getElementById('same');
    const sameProduct = document.getElementById('same-product-item');
    const elseProduct = document.getElementById('else-product');
    const elseProductMd = document.getElementById('else-product-md');


    if (sameLink && sameProduct) {
        sameLink.addEventListener('click', e => {
            sameProduct.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }

    if (elseProduct && sameProduct) {
        elseProduct.addEventListener('click', e => {
            e.preventDefault();
            sameProduct.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
    if (elseProductMd) {
        elseProductMd.addEventListener('click', e => {
            e.preventDefault();
            sameProduct.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    }
});




const openSendCommentBox = () => {
    const openCommentBox = document.getElementById('show-send-comment-box')
    const sendCommentBox = document.getElementById('send-comment-box')
    let bodyElement = document.body
    openCommentBox.addEventListener('click', () => {
        sendCommentBox.classList.remove('hidden')
        bodyElement.style.overflow = 'hidden';

    })


}
const closeSendCommentBox = () => {
    let bodyElement = document.body
    const sendCommentBox = document.getElementById('send-comment-box')
    sendCommentBox.classList.add('hidden')
    bodyElement.style.overflow = 'auto';
}
openSendCommentBox()

function setRating(value,) {
    document.getElementById('rating-value').value = value;
}


const rating = document.querySelectorAll('#stars img')
const valueStar = document.getElementById('star-count')

rating.forEach((star, index) => {
    star.addEventListener('click', value => {
        const getValuStar = index + 1
        valueStar.value = getValuStar
        rating.forEach((s, i) => {
            if (i < getValuStar) {
                s.src = "/static/img/star-svgrepo-com.svg"
            } else {
                s.src = "/static/img/star-svgrepo-com (1).svg"
            }
        })
    })
})

function showToast(message) {
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        background: #1e293b;
        color: #fff;
        padding: 12px 24px;
        border-radius: 8px;
        font-family: IRANSansXFaNum;
        font-size: 14px;
        z-index: 9999;
        opacity: 0;
        transition: opacity 0.3s;
    `;
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.style.opacity = '1');
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


const commentForm = document.getElementById('comment-form');
const overlyForm = document.getElementById('send-comment-box');
const errorComment = document.getElementById('error-comment');
const successComment = document.getElementById('success-comment');
console.log(successComment)
commentForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(commentForm);

    try {
        const response = await fetch('', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            console.log(await response.text());
            errorComment.textContent = 'لطفا فرم را کامل کنید'
            return;
        }

        const data = await response.json();

        if (data.message) {
            overlyForm.classList.add('hidden');
            document.body.style.overflow = 'auto';
            commentForm.reset();
                showToast(data.success_message);

            document.getElementById('content-comments').innerHTML = data.message;
            document.getElementById('content-comments-mobile').innerHTML = data.data_comment_mobile;
            document.getElementById('avg-star').innerHTML = data.data_rating;
            document.getElementById('number-of-comments').innerHTML = data.data_count_comment;
            document.getElementById('all-comment').innerHTML = data.data_all_comment;
            document.getElementById(`comment_${data.comment_id}`).style.scrollMarginTop = "381px";
            document.getElementById('slider_mobile_comments').style.scrollMarginTop = "126px";
            document.getElementById(`comment_${data.comment_id}`).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            document.getElementById('slider_mobile_comments').scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }

    } catch (error) {
        console.error(error);
    }
});




const showAllDescription = () => {
    const showAllDescriptionBtn = document.getElementById('show-description-btn');
    const descriptionProduct = document.getElementById('description');

    const isCollapsed = descriptionProduct.classList.toggle('line-clamp-4');

    showAllDescriptionBtn.textContent = isCollapsed ? 'بیشتر' : 'بستن';
}
// document.getElementById('newest-comment').scrollIntoView({
//     behavior: 'smooth',
//     block: 'start'
// });

function showPanel(name) {
    document.querySelectorAll('.panel-section').forEach(p => p.classList.remove('active'));
    const target = document.getElementById('panel-' + name);
    if (target) {
        target.classList.add('active');
        target.style.animation = 'none';
        target.offsetHeight;
        target.style.animation = 'fadeUp .35s ease both';
    }
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('onclick') && item.getAttribute('onclick').includes(name)) {
            item.classList.add('active');
        }
    });
}

function setMobActive(el) {
    document.querySelectorAll('.mob-nav-btn').forEach(b => b.classList.remove('active'));
    el.classList.add('active');
}

function openModal(id) {
    const m = document.getElementById(id);
    if (m) { m.classList.add('open'); document.body.style.overflow = 'hidden'; }
}

function closeModal(id) {
    const m = document.getElementById(id);
    if (m) { m.classList.remove('open'); document.body.style.overflow = ''; }
}

function showAllOrders() { openModal('modal-all-orders'); }

async function setOrderTab(el) {
    el.closest('.filter-tabs').querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
    const value = el.dataset.filter

    const response = await fetch(`?data-filter=${value}`,{
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    const result_html = await response.json()
    const order_list = document.getElementById('all-orders-list');
    order_list.innerHTML = result_html.html

    const filter = el.getAttribute('data-filter');
    const items = document.querySelectorAll('#all-orders-list .order-item');
    let visibleCount = 0;

    // items.forEach(item => {
    //     if (filter === 'all' || item.getAttribute('data-status') === filter) {
    //         item.style.display = 'flex';
    //         visibleCount++;
    //     } else {
    //         item.style.display = 'none';
    //     }
    // });

    const empty = document.getElementById('orders-empty');
    empty.style.display = visibleCount === 0 ? 'flex' : 'none';
}

// close on overlay click
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', function (e) {
        if (e.target === this) closeModal(this.id);
    });
});
const elseProductBtn = document.getElementById('else-product-lg');

elseProductBtn.addEventListener('click', result =>{
    const elseProducContent = document.getElementById('same-product-item');
    elseProducContent.scrollIntoView({
        'behavior': 'smooth',
        'block': 'start'
    })

})


// ── ویرایش آدرس ──
async function openEditAddress(id, receiver_name, mobile, province_id, city_id, full_address, postal_code, title, is_default) {
    document.getElementById('edit-address-id').value = id;
    document.getElementById('edit-receiver-name').value = receiver_name;
    document.getElementById('edit-mobile').value = mobile;
    document.getElementById('edit-full-address').value = full_address;
    document.getElementById('edit-postal-code').value = postal_code;
    document.getElementById('edit-title').value = title;
    document.getElementById('edit-is-default').checked = is_default;

    // set province
    const provinceSelect = document.querySelector('#modal-edite-address [name="province"]');
    if (provinceSelect) provinceSelect.value = province_id;

    // load cities for this province then set city
    if (province_id) {
        const response = await fetch(`loaded-cities?province=${province_id}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });
        const data = await response.json();
        document.getElementById('cities-list-input-edit').innerHTML = data.cities;

        if (city_id) {
            const citySelect = document.querySelector('#modal-edite-address [name="city"]');
            if (citySelect) citySelect.value = city_id;
        }
    }

    openModal('modal-edite-address');
}

