document.addEventListener('DOMContentLoaded', function () {

    const openBtn   = document.getElementById('open-search-box');
    const searchBox = document.getElementById('searchbox-md');
    const searchContent = document.getElementById('search-content');
    const inputMd   = document.getElementById('search-box-md');

    // ── Swiper instance — تاریخچه دسکتاپ ──
    let desktopHistorySwiper = null;

    function initOrUpdateDesktopSwiper() {
        if (desktopHistorySwiper) {
            desktopHistorySwiper.update();
        } else {
            desktopHistorySwiper = new Swiper('.history-swiper-desktop', {
                slidesPerView: 'auto',
                spaceBetween: 8,
                freeMode: true,
                rtl: true,
                observer: true,
                observeParents: true,
            });
        }
    }

    // ── باز/بسته کردن dropdown ──
    if (openBtn) {
        openBtn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            openSearchDropdown();
        });
    }

    if (searchContent) {
        searchContent.addEventListener('click', e => e.stopPropagation());
    }

    document.addEventListener('click', function () {
        closeSearchDropdown();
    });

    function openSearchDropdown() {
        searchBox.classList.remove('hidden');
        searchBox.classList.add('flex');

        const historySection = document.getElementById('search-history-section');
        if (!inputMd || inputMd.value.trim().length < 2) {
            loadHistory(historySection);
        }
    }

    function closeSearchDropdown() {
        if (searchBox && !searchBox.classList.contains('hidden')) {
            searchBox.classList.add('hidden');
            searchBox.classList.remove('flex');
        }
    }

    // ── Live Search ──
    let debounceTimer = null;

    window.liveSearch = function (value) {
        openSearchDropdown();
        clearTimeout(debounceTimer);

        const trending = document.getElementById('search-trending-section');
        const suggestSection = document.getElementById('search-suggestions-section');
        const historySection = document.getElementById('search-history-section');

        if (!value || value.trim().length < 2) {
            if (trending) trending.classList.remove('hidden');
            if (suggestSection) suggestSection.classList.add('hidden');
            return;
        }

        if (trending) trending.classList.add('hidden');
        if (historySection) historySection.classList.add('hidden');

        debounceTimer = setTimeout(() => {
            fetch(`/api/search-suggestions/?q=${encodeURIComponent(value.trim())}`)
                .then(r => r.json())
                .then(data => renderSuggestions(data.products, suggestSection))
                .catch(console.error);
        }, 300);
    };

    function loadHistory(section) {
        if (!section) return;
        const list = document.getElementById('search-history-list');
        if (!list) return;

        fetch('/api/search-suggestions/?q=')
            .then(r => r.json())
            .then(data => {
                if (data.history && data.history.length) {
                    list.innerHTML = data.history.map(q =>
                        `<a href="/product/?q=${encodeURIComponent(q)}"
                            class="search-tag text-sm swiper-slide !w-max"
                            onclick="saveHistory('${q.replace(/'/g,"\\'")}')">
                           ${q}
                         </a>`
                    ).join('');
                    section.classList.remove('hidden');
                    initOrUpdateDesktopSwiper(); // 👈 مهم: بعد از پر شدن DOM
                } else {
                    section.classList.add('hidden');
                }
            })
            .catch(console.error);
    }

    function renderSuggestions(products, section) {
        const list = document.getElementById('search-suggestions-list');
        if (!list || !section) return;

        if (!products || products.length === 0) {
            list.innerHTML = '<p class="text-sm text-gray-400 text-center py-2">نتیجه‌ای یافت نشد</p>';
        } else {
            list.innerHTML = products.map(p =>
                `<a href="${p.url}"
                    class="flex items-center gap-2 px-2 py-1.5 rounded-lg hover:bg-gray-50 transition"
                    onclick="saveHistory('${p.title.replace(/'/g,"\\'")}')">
                   ${p.image
                       ? `<img src="${p.image}" class="w-8 h-8 object-contain rounded" alt="">`
                       : `<div class="w-8 h-8 bg-gray-100 rounded"></div>`
                   }
                   <span class="text-sm text-gray-700">${p.title}</span>
                 </a>`
            ).join('');
        }

        section.classList.remove('hidden');
    }

    // ── ذخیره تاریخچه هنگام کلیک/submit ──
    window.saveHistory = function (query) {
        if (!query) return;
        fetch('/api/save-search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrf(),
            },
            body: JSON.stringify({ q: query }),
        }).catch(console.error);
    };

    window.handleSearchSubmit = function (e) {
        const q = document.getElementById('search-box-md')?.value.trim();
        if (q) saveHistory(q);
    };

    function getCsrf() {
        return document.cookie.split(';')
            .find(c => c.trim().startsWith('csrftoken='))
            ?.split('=')[1] || '';
    }

});

// ── Mobile Search ──
(function initMobileSearch() {
    const inputMobile = document.getElementById('search-box');
    if (!inputMobile) return;

    const mobileSuggestSection  = document.getElementById('search-suggestions-mobile');
    const mobileHistorySection  = document.getElementById('mobile-history-section');
    const mobileHistoryList     = document.getElementById('mobile-history-list');
    const mobileTrendingSection = document.getElementById('mobile-trending-section');

    // ── Swiper instance — تاریخچه موبایل ──
    let mobileHistorySwiper = null;

    function initOrUpdateMobileSwiper() {
        if (mobileHistorySwiper) {
            mobileHistorySwiper.update();
        } else {
            mobileHistorySwiper = new Swiper('.history-swiper-mobile', {
                slidesPerView: 'auto',
                spaceBetween: 8,
                freeMode: true,
                rtl: true,
                observer: true,
                observeParents: true,
            });
        }
    }

    loadMobileHistory();

    inputMobile.addEventListener('input', function () {
        mobileLiveSearch(this.value.trim());
    });

    let mobileTimer = null;

    function mobileLiveSearch(value) {
        clearTimeout(mobileTimer);

        if (!value || value.length < 2) {
            if (mobileSuggestSection) mobileSuggestSection.classList.add('hidden');
            if (mobileHistorySection) mobileHistorySection.classList.remove('hidden');
            if (mobileTrendingSection) mobileTrendingSection.classList.remove('hidden');
            if (mobileHistorySwiper) mobileHistorySwiper.update(); // 👈 بعد از remove('hidden')
            return;
        }

        if (mobileHistorySection) mobileHistorySection.classList.add('hidden');
        if (mobileTrendingSection) mobileTrendingSection.classList.add('hidden');

        mobileTimer = setTimeout(() => {
            fetch(`/api/search-suggestions/?q=${encodeURIComponent(value)}`)
                .then(r => r.json())
                .then(data => renderMobileSuggestions(data.products))
                .catch(console.error);
        }, 300);
    }

    function loadMobileHistory() {
        fetch('/api/search-suggestions/?q=')
            .then(r => r.json())
            .then(data => {
                if (!mobileHistoryList) return;

                if (data.history && data.history.length) {
                    mobileHistoryList.innerHTML = data.history.map(q =>
                        `<a href="/product/?q=${encodeURIComponent(q)}"
                            class="search-tag swiper-slide !w-max"
                            onclick="saveHistory('${q.replace(/'/g, "\\'")}')">
                            ${q}
                            
                         </a>`
                    ).join('');
                    if (mobileHistorySection) mobileHistorySection.classList.remove('hidden');
                    initOrUpdateMobileSwiper(); // 👈 مهم: بعد از پر شدن DOM
                } else {
                    if (mobileHistorySection) mobileHistorySection.classList.add('hidden');
                }
            })
            .catch(console.error);
    }

    function renderMobileSuggestions(products) {
        if (!mobileSuggestSection) return;

        mobileSuggestSection.innerHTML = (!products || products.length === 0)
            ? '<p class="text-sm text-gray-400 text-center py-3">نتیجه‌ای یافت نشد</p>'
            : products.map(p =>
                `<a href="${p.url}"
                    class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-50 transition"
                    onclick="saveHistory('${p.title.replace(/'/g, "\\'")}')">
                    ${p.image
                        ? `<img src="${p.image}" class="w-9 h-9 object-contain rounded" alt="">`
                        : `<div class="w-9 h-9 bg-gray-100 rounded"></div>`
                    }
                    <span class="text-sm text-gray-700">${p.title}</span>
                 </a>`
            ).join('');

        mobileSuggestSection.classList.remove('hidden');
    }
})();