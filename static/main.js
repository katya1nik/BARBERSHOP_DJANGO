// Обработка формы записи
document.addEventListener('DOMContentLoaded', function() {
    const bookingForm = document.querySelector('.booking-form');
    
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            // Получаем данные формы
            const name = this.querySelector('input[name="name"]').value;
            const phone = this.querySelector('input[name="phone"]').value;
            const master = this.querySelector('select[name="master"]').value;
            const service = this.querySelector('select[name="service"]').value;
            const date = this.querySelector('input[name="date"]').value;
            const time = this.querySelector('input[name="time"]').value;
            
            // Простая валидация
            if (!name || !phone || !master || !service) {
                e.preventDefault();
                alert('Пожалуйста, заполните обязательные поля: имя, телефон, мастер, услуга!');
                return;
            }
            
            // Проверка телефона
            const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
            if (!phoneRegex.test(phone)) {
                e.preventDefault();
                alert('Пожалуйста, введите корректный номер телефона!');
                return;
            }
            
            // Проверка даты (если заполнена)
            if (date) {
                const selectedDate = new Date(date);
                const today = new Date();
                today.setHours(0, 0, 0, 0);
                
                if (selectedDate < today) {
                    e.preventDefault();
                    alert('Нельзя записаться на прошедшую дату!');
                    return;
                }
            }
        });
    }
    
   

    // Функция для получения имени мастера по ID
    function getMasterName(masterId) {
        const masters = {
            '1': 'Алексей Петров',
            '2': 'Дмитрий Иванов',
            '3': 'Сергей Сидоров'
        };
        return masters[masterId] || 'Неизвестный мастер';
    }
    
    // Анимация карточек при загрузке
    const cards = document.querySelectorAll('.service-card, .master-card, .order-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Подсветка активных элементов
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.05)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Автоматическое обновление времени на странице
    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('ru-RU');
        const dateString = now.toLocaleDateString('ru-RU');
        
        // Если есть элемент для отображения времени
        const timeElement = document.querySelector('.current-time');
        if (timeElement) {
            timeElement.textContent = `${dateString} ${timeString}`;
        }
    }
    
    // Обновляем время каждую секунду
    setInterval(updateTime, 1000);
    updateTime();
});

// Функция для плавной прокрутки к элементам
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Обработка клавиш для быстрой навигации
document.addEventListener('keydown', function(e) {
    // Ctrl + H - на главную
    if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        window.location.href = '/';
    }
    
    // Ctrl + O - к заявкам
    if (e.ctrlKey && e.key === 'o') {
        e.preventDefault();
        window.location.href = '/orders/';
    }
});

console.log('Барбершоп "Золотые Ножницы" загружен!');
