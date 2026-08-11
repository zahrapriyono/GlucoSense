/**
 * GlucoSense — Global JavaScript
 * Handles: scroll animations, ripple effects,
 * navbar scroll state, scroll-to-top, counter animation
 */

/* ================================================
   1. SCROLL REVEAL (IntersectionObserver)
   ================================================ */
function initScrollReveal() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

/* ================================================
   2. NAVBAR SCROLL STATE
   ================================================ */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
}

/* ================================================
   3. SCROLL TO TOP BUTTON
   ================================================ */
function initScrollTop() {
    const btn = document.getElementById('scrollTopBtn');
    if (!btn) return;
    window.addEventListener('scroll', () => {
        btn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

/* ================================================
   4. RIPPLE EFFECT ON BUTTONS
   ================================================ */
function initRipple() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = btn.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height) * 2;
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top  - size / 2;
            const ripple = document.createElement('span');
            ripple.className = 'ripple-effect';
            ripple.style.cssText = `width:${size}px;height:${size}px;left:${x}px;top:${y}px;`;
            btn.appendChild(ripple);
            setTimeout(() => ripple.remove(), 700);
        });
    });
}

/* ================================================
   5. COUNTER ANIMATION
   ================================================ */
function animateCounter(el, target, duration = 1500) {
    const start = performance.now();
    function update(ts) {
        const progress = Math.min((ts - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(target * eased).toLocaleString();
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

function initCounters() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                entry.target.dataset.counted = 'true';
                animateCounter(entry.target, parseInt(entry.target.dataset.count, 10));
            }
        });
    }, { threshold: 0.5 });
    document.querySelectorAll('[data-count]').forEach(el => observer.observe(el));
}

/* ================================================
   6. HAMBURGER MENU (mobile)
   ================================================ */
function initHamburger() {
    const btn   = document.getElementById('hamburgerBtn');
    const links = document.querySelector('.navbar__links');
    if (!btn || !links) return;
    btn.addEventListener('click', () => {
        links.classList.toggle('open');
        btn.textContent = links.classList.contains('open') ? '✕' : '☰';
    });
    document.addEventListener('click', (e) => {
        if (!btn.contains(e.target) && !links.contains(e.target)) {
            links.classList.remove('open');
            btn.textContent = '☰';
        }
    });
}

/* ================================================
   7. FILTER TAGS
   ================================================ */
function initFilterTags() {
    document.querySelectorAll('.filter-tag').forEach(tag => {
        tag.addEventListener('click', function() {
            this.closest('.filter-tags')
                ?.querySelectorAll('.filter-tag')
                .forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

/* ================================================
   8. PROFILE TABS
   ================================================ */
function initProfileTabs() {
    document.querySelectorAll('.profile-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            document.querySelectorAll('.profile-tab').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

/* ================================================
   9. AUTO-APPLY REVEAL CLASS TO CARDS & SECTIONS
   ================================================ */
function applyRevealToElements() {
    const selectors = [
        { sel: '.feature-card', delay: 100 },
        { sel: '.article-card', delay: 100 },
        { sel: '.doctor-card',  delay: 80  },
        { sel: '.how-step',     delay: 150 },
    ];
    selectors.forEach(({ sel, delay }) => {
        document.querySelectorAll(sel).forEach((el, i) => {
            el.classList.add('reveal');
            el.style.transitionDelay = `${i * delay}ms`;
        });
    });
    document.querySelectorAll('.section-title, .section-subtitle').forEach(el => {
        el.classList.add('reveal');
    });
}

/* ================================================
   INIT
   ================================================ */
document.addEventListener('DOMContentLoaded', () => {
    applyRevealToElements();
    initScrollReveal();
    initNavbarScroll();
    initScrollTop();
    initRipple();
    initCounters();
    initHamburger();
    initFilterTags();
    initProfileTabs();
});