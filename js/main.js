/**
 * 龙溪企服 LongC-ES 官网 - 主要交互脚本
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initNavbarScroll();
    initSmoothScroll();
    initContactForm();
    initScrollAnimations();
});

function initMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            navMenu.classList.toggle('active');
            const spans = hamburger.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
        
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                // 确保链接可以正常跳转，同时关闭菜单
                navMenu.classList.remove('active');
                const spans = hamburger.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
        
        // 点击页面其他地方关闭菜单
        document.addEventListener('click', function(e) {
            if (navMenu.classList.contains('active') && 
                !hamburger.contains(e.target) && 
                !navMenu.contains(e.target)) {
                navMenu.classList.remove('active');
                const spans = hamburger.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }
}

function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
            } else {
                navbar.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
            }
        });
    }
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.offsetTop - navbarHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

function initContactForm() {
    const form = document.querySelector('.contact-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            
            if (!data.name || !data.phone || !data.service) {
                showNotification('请填写必填项', 'error');
                return;
            }
            
            const phoneRegex = /^1[3-9]\d{9}$/;
            if (!phoneRegex.test(data.phone.replace(/-/g, ''))) {
                showNotification('请输入正确的手机号码', 'error');
                return;
            }
            
            showNotification('提交成功！我们会尽快与您联系', 'success');
            form.reset();
            console.log('表单数据：', data);
        });
    }
}

function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-message">${message}</span>
        <button class="notification-close">&times;</button>
    `;
    
    document.body.appendChild(notification);
    
    notification.querySelector('.notification-close').addEventListener('click', function() {
        notification.remove();
    });
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideDown 0.3s ease reverse';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

window.addEventListener('load', function() {
    document.body.classList.add('loaded');
});

// ========== 资讯中心 ==========
function initNewsCenter() {
    const grid = document.getElementById('newsGrid');
    const pagination = document.getElementById('pagination');
    if (!grid || typeof NEWS_DATA === 'undefined') return;

    const ITEMS_PER_PAGE = 6;
    let currentPage = 1;
    let currentCategory = 'all';

    function renderNews(page, category) {
        let filtered = NEWS_DATA;
        if (category !== 'all') {
            filtered = NEWS_DATA.filter(n => n.category === category);
        }

        const totalPages = Math.ceil(filtered.length / ITEMS_PER_PAGE);
        const start = (page - 1) * ITEMS_PER_PAGE;
        const items = filtered.slice(start, start + ITEMS_PER_PAGE);

        grid.innerHTML = items.map(n => `
            <article class="news-card">
                <div class="news-image">
                    <img src="${n.image}" alt="${n.title}" loading="lazy" onerror="this.style.display='none'">
                </div>
                <div class="news-content">
                    <span class="news-category">${n.category}</span>
                    <span class="news-date">${n.date}</span>
                    <h3>${n.title}</h3>
                    <p>${n.summary}</p>
                    <a href="news-detail.html?id=${n.id}" class="news-link">阅读更多 →</a>
                </div>
            </article>
        `).join('');

        // Pagination
        if (totalPages > 1) {
            let html = '';
            for (let i = 1; i <= totalPages; i++) {
                html += `<button class="page-btn${i === page ? ' active' : ''}" data-page="${i}">${i}</button>`;
            }
            pagination.innerHTML = html;
            pagination.querySelectorAll('.page-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    currentPage = parseInt(this.dataset.page);
                    renderNews(currentPage, currentCategory);
                    window.scrollTo({ top: grid.offsetTop - 100, behavior: 'smooth' });
                });
            });
        } else {
            pagination.innerHTML = '';
        }
    }

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentCategory = this.dataset.cat;
            currentPage = 1;
            renderNews(currentPage, currentCategory);
        });
    });

    renderNews(currentPage, currentCategory);
}

document.addEventListener('DOMContentLoaded', initNewsCenter);

function initScrollAnimations() {
    if (!('IntersectionObserver' in window)) return;
    
    const animatedElements = document.querySelectorAll('.business-card, .culture-card, .service-item, .advantage-item, .client-card, .other-card');
    
    animatedElements.forEach(el => {
        el.classList.add('scroll-animate');
    });
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}