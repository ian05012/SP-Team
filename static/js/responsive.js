// 響應式導航欄交互功能

document.addEventListener('DOMContentLoaded', function() {
    // 創建移動端菜單按鈕
    const header = document.querySelector('.glass-header');
    const navContainer = document.querySelector('.nav-container');
    const navLinks = document.querySelector('.nav-links');
    const searchContainer = document.querySelector('.search-container');
    
    // 創建搜尋圖標按鈕
    const searchIconBtn = document.createElement('button');
    searchIconBtn.className = 'search-icon-btn nav-icon-btn';
    searchIconBtn.innerHTML = '<i class="fas fa-search"></i>';
    searchIconBtn.style.display = 'none'; // 默認隱藏
    
    // 創建搜尋背景遮罩
    const searchBackdrop = document.createElement('div');
    searchBackdrop.className = 'search-backdrop';
    
    // 創建移動端菜單按鈕
    const mobileMenuBtn = document.createElement('button');
    mobileMenuBtn.className = 'mobile-menu-btn nav-icon-btn';
    mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
    mobileMenuBtn.style.display = 'none'; // 默認隱藏
    // 移除內聯z-index樣式，改用CSS控制
    
    // 創建移動端菜單背景遮罩
    const mobileMenuBackdrop = document.createElement('div');
    mobileMenuBackdrop.className = 'mobile-menu-backdrop';
    
    // 創建移動端菜單覆蓋層
    const mobileMenuOverlay = document.createElement('div');
    mobileMenuOverlay.className = 'mobile-menu-overlay';
    
    // 創建移動端菜單頭部
    const mobileMenuHeader = document.createElement('div');
    mobileMenuHeader.className = 'mobile-menu-header';
    mobileMenuHeader.innerHTML = '<h2>SP-HUB</h2>';
    
    // 創建關閉按鈕
    const mobileMenuClose = document.createElement('button');
    mobileMenuClose.className = 'mobile-menu-close';
    mobileMenuClose.innerHTML = '<i class="fas fa-times"></i>';
    
    // 創建移動端菜單鏈接容器
    const mobileMenuLinks = document.createElement('div');
    mobileMenuLinks.className = 'mobile-menu-links';
    
    // 將元素添加到DOM
    mobileMenuHeader.appendChild(mobileMenuClose);
    mobileMenuOverlay.appendChild(mobileMenuHeader);
    mobileMenuOverlay.appendChild(mobileMenuLinks);
    document.body.appendChild(mobileMenuOverlay);
    document.body.appendChild(mobileMenuBackdrop);
    document.body.appendChild(searchBackdrop);
    navContainer.appendChild(mobileMenuBtn);
    navContainer.appendChild(searchIconBtn);
    
    // 響應式處理函數
    function handleResponsive() {
        if (window.innerWidth <= 768) {
            // 移動端顯示
            mobileMenuBtn.style.display = 'flex';
            // 移除內聯樣式，使用CSS類別控制
            mobileMenuBtn.classList.add('nav-icon-btn');
            navLinks.classList.remove('active');
            
            // 顯示搜尋圖標按鈕，隱藏搜尋欄
            searchIconBtn.style.display = 'flex';
            // 移除內聯樣式，使用CSS類別控制
            searchIconBtn.classList.add('nav-icon-btn');
            searchContainer.classList.remove('active');
            
            // 複製導航鏈接到移動端菜單，排除用戶名稱鏈接
            mobileMenuLinks.innerHTML = '';
            const links = navLinks.querySelectorAll('a:not(.dropdown-content a):not(.user-dropdown a):not(.user-profile a):not([href*="profile_with_username"])');
            links.forEach(link => {
                const newLink = link.cloneNode(true);
                mobileMenuLinks.appendChild(newLink);
            });
            
            // 處理用戶下拉菜單
            const userDropdown = navLinks.querySelector('.user-dropdown');
            if (userDropdown) {
                const dropdownBtn = userDropdown.querySelector('button');
                const dropdownContent = userDropdown.querySelector('.dropdown-content');
                
                if (dropdownBtn && dropdownContent) {
                    // 不再添加用戶按鈕，因為用戶名稱已經在導航鏈接中
                    // 直接添加下拉菜單中的鏈接
                    const dropdownLinks = dropdownContent.querySelectorAll('a');
                    dropdownLinks.forEach(link => {
                        const newLink = link.cloneNode(true);
                        mobileMenuLinks.appendChild(newLink);
                    });
                }
            }
        } else {
            // 桌面端顯示
            mobileMenuBtn.style.display = 'none';
            searchIconBtn.style.display = 'none';
            searchContainer.style.display = 'flex';
            searchContainer.style.opacity = '1';
            searchContainer.style.transform = 'translateY(0)';
            mobileMenuOverlay.classList.remove('active');
        }
    }
    
    // 初始化響應式處理
    handleResponsive();
    
    // 窗口大小變化時重新處理
    window.addEventListener('resize', handleResponsive);
    
    // 搜尋圖標按鈕點擊事件
    searchIconBtn.addEventListener('click', function(event) {
        event.stopPropagation(); // 防止事件冒泡
        searchContainer.classList.toggle('active');
        searchBackdrop.classList.toggle('active');
        if (searchContainer.classList.contains('active')) {
            // 確保搜尋欄顯示後再聚焦，避免動畫過程中聚焦問題
            setTimeout(() => {
                searchContainer.querySelector('.search-bar').focus(); // 自動聚焦到搜尋欄
            }, 300);
            document.body.style.overflow = 'hidden'; // 防止背景滾動
            // 確保搜尋框背景為白色
            searchContainer.style.backgroundColor = '#ffffff';
            searchContainer.style.setProperty('background-color', '#ffffff', 'important');
            // 確保淡入效果
            searchContainer.style.opacity = '1';
            searchContainer.style.transform = 'translateY(0)';
        } else {
            document.body.style.overflow = ''; // 恢復背景滾動
            // 淡出效果
            searchContainer.style.opacity = '0';
            searchContainer.style.transform = 'translateY(-20px)';
        }
    });
    
    // 點擊頁面其他地方關閉搜尋欄
    document.addEventListener('click', function(event) {
        if (searchContainer.classList.contains('active') && 
            !searchContainer.contains(event.target) && 
            event.target !== searchIconBtn && 
            !searchIconBtn.contains(event.target)) {
            searchContainer.classList.remove('active');
            searchBackdrop.classList.remove('active');
            document.body.style.overflow = ''; // 恢復背景滾動
        }
    });
    
    // 點擊背景遮罩層關閉搜尋欄
    searchBackdrop.addEventListener('click', function() {
        searchContainer.classList.remove('active');
        searchBackdrop.classList.remove('active');
        document.body.style.overflow = ''; // 恢復背景滾動
    });
    
    // 移動端菜單按鈕點擊事件
    mobileMenuBtn.addEventListener('click', function(event) {
        event.stopPropagation(); // 防止事件冒泡
        mobileMenuOverlay.classList.add('active');
        mobileMenuBackdrop.classList.add('active');
        document.body.style.overflow = 'hidden'; // 防止背景滾動
    });
    
    // 移動端菜單關閉按鈕點擊事件
    mobileMenuClose.addEventListener('click', function() {
        closeMenu();
    });
    
    // 點擊背景遮罩層關閉菜單
    mobileMenuBackdrop.addEventListener('click', function() {
        closeMenu();
    });
    
    // 點擊覆蓋層外部關閉菜單
    document.addEventListener('click', function(event) {
        if (mobileMenuOverlay.classList.contains('active') && 
            !mobileMenuOverlay.contains(event.target) && 
            event.target !== mobileMenuBtn) {
            closeMenu();
        }
    });
    
    // 關閉菜單的通用函數
    function closeMenu() {
        mobileMenuOverlay.classList.remove('active');
        mobileMenuBackdrop.classList.remove('active');
        document.body.style.overflow = ''; // 恢復背景滾動
    }
    
    // 防止點擊搜尋欄時關閉菜單
    searchContainer.addEventListener('click', function(event) {
        event.stopPropagation();
    });
});