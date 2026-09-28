
// const swiper = new Swiper('.swiper', {
//     loop: true, // چرخش بی‌نهایت
//     pagination: {
//         el: '.swiper-pagination',
//         clickable: true,
//     },
//     navigation: {
//         nextEl: '.swiper-button-next',
//         prevEl: '.swiper-button-prev',
//     },
//     autoplay: {
//         delay: 3000, // هر ۳ ثانیه به بعدی بره
//         disableOnInteraction: false,
//     },
//     speed: 600, // سرعت انیمیشن
// });

const swiper = new Swiper('.swiper', {
  loop: true,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  pagination: {
    el: '.swiper-pagination',
    clickable: true,
  },
    autoplay: {
      delay: 5000, // زمان تاخیر بین هر اسلاید به میلی‌ثانیه (مثلا 5 ثانیه)
      disableOnInteraction: false, // ادامه دادن پخش خودکار حتی بعد از تعامل کاربر (کلیک، اسکرول)
    },
});

document.addEventListener('DOMContentLoaded', function () {
    const swiper = new Swiper('.img-product-slider', {
        loop: true,
        pagination: {
            el: '.img-product-pagination',
            clickable: true,
        },
        autoplay: false
    });
});
const swiperbox = new Swiper('.mySwiper', {
  slidesPerView: 'auto', // اجازه می دهد تعداد محصولات بر اساس عرضشان نمایش داده شوند
  spaceBetween: 5,      // فاصله بین محصولات (اگر در flex gap-4 تعریف شده، اینجا هم می توانید تنظیم کنید)
  freeMode: true,        // فعال کردن اسکرول آزاد
  loop: false,           // حلقه ای نباشد
});

const swipergallery = new Swiper('.product-gallery', {
  slidesPerView: 'auto', // اجازه می دهد تعداد محصولات بر اساس عرضشان نمایش داده شوند
  spaceBetween: 5,      // فاصله بین محصولات (اگر در flex gap-4 تعریف شده، اینجا هم می توانید تنظیم کنید)
  freeMode: true,        // فعال کردن اسکرول آزاد
  loop: false,           // حلقه ای نباشد
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
});



