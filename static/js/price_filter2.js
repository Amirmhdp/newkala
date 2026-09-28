const addToWishesList = async (productId) => {
    try {
        const response = await fetch(`?product-id=${productId}`)

        if (response.status === 401) {
            window.location.href = '/login/'  // آدرس صفحه لاگینت رو بذار
            return
        }

        const data = await response.json()
        document.getElementById('wishes').outerHTML = data.html
    } catch (error) {
        console.error('خطا:', error)
    }
}
  // category mega menu toggle
  function toggleCategory(e) {
    e.preventDefault();
    const menu = document.getElementById('menu-category');
    const isOpen = menu.classList.contains('open');
    menu.classList.toggle('open', !isOpen);
    document.getElementById('btn-category').querySelector('.fa-chevron-down').style.transform = isOpen ? '' : 'rotate(180deg)';
  }
  // close mega menu on outside click
  document.addEventListener('click', function(e) {
    const menu = document.getElementById('menu-category');
    const btn = document.getElementById('btn-category');
    if (menu && !menu.contains(e.target) && !btn.contains(e.target)) {
      menu.classList.remove('open');
      btn.querySelector('.fa-chevron-down').style.transform = '';
    }
  });
  // mobile search
  function openSearchBox() { document.getElementById('search-mobile').classList.add('open'); }
  function closeSearchBox() { document.getElementById('search-mobile').classList.remove('open'); }


  document.getElementById('category-search-input').addEventListener('input', function(e) {
    const query = e.target.value.trim().toLowerCase();
    const items = document.querySelectorAll('.category-item');
    let visibleCount = 0;

    items.forEach(item => {
      const name = item.dataset.name.toLowerCase();
      const match = name.includes(query);
      item.style.display = match ? '' : 'none';
      if (match) visibleCount++;
    });

    const emptyState = document.getElementById('no-category-result');
    if (emptyState) {
      emptyState.style.display = (visibleCount === 0 && query !== '') ? 'flex' : 'none';
    }
  });
    function toggleFooterAccordion(header) {
    const content = header.nextElementSibling;
    const openIcon = header.querySelector('.open-icon');
    const closeIcon = header.querySelector('.close-icon');
    const isOpen = content.style.display === 'flex';

    content.style.display = isOpen ? 'none' : 'flex';
    openIcon.classList.toggle('hidden', !isOpen);
    closeIcon.classList.toggle('hidden', isOpen);
  }
