// 龙溪企服官方网站JavaScript功能

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 初始化导航栏
    initNavbar();
    
    // 初始化滚动效果
    initScrollEffects();
    
    // 初始化表单验证
    initFormValidation();
});

// 导航栏初始化
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    // 添加导航链接点击效果
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // 如果是内部链接，平滑滚动
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    smoothScrollTo(targetElement);
                }
            }
        });
    });
    
    // 滚动时改变导航栏透明度
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            navbar.style.backgroundColor = '#495057';
        } else {
            navbar.style.backgroundColor = '#495057';
        }
    });
}

// 平滑滚动到指定元素
function smoothScrollTo(element) {
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - 80;
    
    window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
    });
}

// 滚动效果初始化
function initScrollEffects() {
    // 卡片动画
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.12)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.08)';
        });
    });
    
    // 服务卡片动画
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.12)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.08)';
        });
    });
}

// 表单验证初始化
function initFormValidation() {
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 获取表单数据
            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const phone = document.getElementById('phone').value.trim();
            const message = document.getElementById('message').value.trim();
            
            // 验证表单
            let isValid = true;
            
            // 验证姓名
            if (!name) {
                showError('name', '请输入姓名');
                isValid = false;
            } else {
                clearError('name');
            }
            
            // 验证邮箱
            if (!email) {
                showError('email', '请输入邮箱');
                isValid = false;
            } else if (!validateEmail(email)) {
                showError('email', '请输入有效的邮箱地址');
                isValid = false;
            } else {
                clearError('email');
            }
            
            // 验证电话
            if (!phone) {
                showError('phone', '请输入联系电话');
                isValid = false;
            } else if (!validatePhone(phone)) {
                showError('phone', '请输入有效的电话号码');
                isValid = false;
            } else {
                clearError('phone');
            }
            
            // 验证留言
            if (!message) {
                showError('message', '请输入留言内容');
                isValid = false;
            } else {
                clearError('message');
            }
            
            if (isValid) {
                // 显示提交成功消息
                showSuccessMessage();
                
                // 重置表单
                contactForm.reset();
            }
        });
    }
}

// 验证邮箱格式
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.(com|cn|net)$/;
    return emailRegex.test(email);
}

// 验证电话号码格式
function validatePhone(phone) {
    const phoneRegex = /^1[3-9]\d{9}$|^\d{3}-\d{8}$|^\d{4}-\d{7}$/;
    return phoneRegex.test(phone);
}

// 显示错误信息
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorDiv = document.getElementById(`${fieldId}-error`);
    
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    } else {
        const errorElement = document.createElement('div');
        errorElement.id = `${fieldId}-error`;
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        errorElement.style.color = '#dc3545';
        errorElement.style.fontSize = '14px';
        errorElement.style.marginTop = '5px';
        
        field.parentNode.appendChild(errorElement);
    }
    
    field.style.borderColor = '#dc3545';
}

// 清除错误信息
function clearError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorDiv = document.getElementById(`${fieldId}-error`);
    
    if (errorDiv) {
        errorDiv.style.display = 'none';
    }
    
    field.style.borderColor = '#ced4da';
}

// 显示成功消息
function showSuccessMessage() {
    const successMessage = document.createElement('div');
    successMessage.id = 'success-message';
    successMessage.className = 'success-message';
    successMessage.textContent = '表单提交成功！我们会尽快联系您。';
    successMessage.style.backgroundColor = '#d4edda';
    successMessage.style.color = '#155724';
    successMessage.style.padding = '15px';
    successMessage.style.borderRadius = '5px';
    successMessage.style.marginTop = '20px';
    successMessage.style.textAlign = 'center';
    
    const contactForm = document.getElementById('contact-form');
    contactForm.appendChild(successMessage);
    
    // 3秒后移除成功消息
    setTimeout(() => {
        successMessage.remove();
    }, 3000);
}

// 页面滚动到顶部
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// 页面滚动到底部
function scrollToBottom() {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
}

// 切换主题颜色
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'light');
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
    }
}

// 图片懒加载
function initImageLazyLoad() {
    const images = document.querySelectorAll('img[data-src]');
    
    images.forEach(img => {
        const src = img.getAttribute('data-src');
        if (src) {
            img.setAttribute('src', src);
            img.removeAttribute('data-src');
        }
    });
}

// 页面加载进度
function showLoadingProgress() {
    const progressBar = document.createElement('div');
    progressBar.id = 'loading-progress';
    progressBar.style.position = 'fixed';
    progressBar.style.top = '0';
    progressBar.style.left = '0';
    progressBar.style.width = '0%';
    progressBar.style.height = '3px';
    progressBar.style.backgroundColor = '#007bff';
    progressBar.style.zIndex = '1001';
    
    document.body.appendChild(progressBar);
    
    // 模拟加载进度
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(interval);
            setTimeout(() => {
                progressBar.remove();
            }, 500);
        }
    }, 100);
}