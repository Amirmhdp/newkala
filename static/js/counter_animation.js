
const statsSection = document.getElementById('stats-section');
const counters = document.querySelectorAll('.stat-num');

let started = false;

const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting && !started) {
        started = true;

        counters.forEach(counter => {
            const target = parseFloat(counter.dataset.target);
            const isDecimal = target % 1 !== 0;

            let current = 0;
            const increment = target / 100;

            const updateCounter = () => {
                if (current < target) {
                    current += increment;

                    if (isDecimal) {
                        counter.textContent = current.toFixed(1);
                    } else {
                        counter.textContent = Math.ceil(current).toLocaleString('fa-IR');
                    }

                    requestAnimationFrame(updateCounter);
                } else {
                    if (isDecimal) {
                        counter.textContent = target.toFixed(1);
                    } else {
                        counter.textContent = target.toLocaleString('fa-IR');
                    }
                }
            };

            updateCounter();
        });
    }
});

observer.observe(statsSection);