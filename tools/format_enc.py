#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Material Design UI (MDUI) Encrypted HTML Generator for Markdown Files
===========================================================================

This script converts Markdown files into encrypted HTML files using Material Design UI (MDUI) 
for styling. The content is encrypted using AES-256-GCM and requires a password to view.

Based on format.py with encryption features added.
Usage
================
```
python format_enc.py <markdown_file> [password]
```

If password is not provided, you will be prompted to enter one.

Example:
```
python format_enc.py document.md mypassword123
```

Version: 1.0.0-20251124

License: GNU GPL v3
---------------------------------------------------------------------------
'''

import os
import sys
import base64
import hashlib
import secrets
try:
    import markdown
    from bs4 import BeautifulSoup
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ModuleNotFoundError:
    print("正在安装必需的依赖包...")
    os.system('pip install markdown beautifulsoup4 cryptography')
    import markdown
    from bs4 import BeautifulSoup
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="google" content="notranslate" />
    <title>{title}</title>
    <link rel="icon" href="/favicon.png" type="image/png">
    <link rel="shortcut icon" href="/favicon.png" type="image/png">
    <!-- MDUI CSS -->
    <link rel="stylesheet" href="https://unpkg.com/mdui@1.0.2/dist/css/mdui.min.css" onerror="this.onerror=null;this.href='https://cdnjs.cloudflare.com/ajax/libs/mdui/1.0.2/css/mdui.min.css';">
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
            line-height: 1.6; 
            margin: 0; 
            padding: 0; 
        }}
        
        .mdui-container {{ 
            max-width: 900px; 
            padding: 2rem; 
        }}
        
        .mdui-container-with-appbar {{ 
            padding-top: 4rem; 
        }}
        
        pre {{ 
            background: #f6f8fa; 
            padding: 16px; 
            border-radius: 6px; 
            position: relative; 
            overflow-x: auto; 
            white-space: pre-wrap; 
            word-wrap: break-word; 
            transition: all 0.3s; 
        }}
        
        .mdui-theme-layout-dark pre {{ 
            background: #1e1e1e; 
            color: #f0f0f0; 
        }}
        
        code {{ 
            word-wrap: break-word; 
        }}
        
        .copy-btn {{ 
            position: absolute; 
            right: 4px; 
            top: 4px; 
            padding: 4px; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 16px; 
            display: none; 
            z-index: 100; 
            transition: all 0.2s ease-in-out; 
            background-color: rgba(246, 248, 250, 0.7);
            color: #57606a;
            min-width: 32px;
            min-height: 32px;
            box-shadow: none;
        }}
        
        .copy-btn.copy-success {{
            color: #4CAF50 !important;
        }}
        
        .mdui-theme-layout-dark .copy-btn {{ 
            background-color: rgba(30, 30, 30, 0.7);
            color: #9e9e9e;
            border: none;
        }}
        
        @media (hover: hover) and (pointer: fine) {{
            pre:hover .copy-btn {{ 
                display: block; 
                animation: fadeIn 0.3s; 
            }}
        }}
        
        .touch-device .copy-btn {{ 
            display: block; 
            opacity: 0.9; 
        }}
        
        .mdui-table {{ 
            width: 100%; 
            margin: 1em 0; 
            border-collapse: collapse; 
            transition: all 0.3s; 
        }}
        
        .mdui-table-responsive {{ 
            overflow-x: auto; 
            margin-bottom: 1em; 
        }}
        
        img {{ 
            max-width: 100%; 
            height: auto; 
            transition: all 0.3s; 
        }}
        
        blockquote {{ 
            margin: 1em 0; 
            padding: 0 1em; 
            border-left: 0.25em solid; 
            transition: all 0.3s; 
        }}
        
        .mdui-theme-layout-dark blockquote {{ 
            color: #9e9e9e; 
            border-left-color: #555; 
        }}
        
        .theme-switch {{ 
            position: fixed; 
            bottom: 20px; 
            right: 20px; 
            z-index: 9999; 
        }}
        
        .mdui-container {{ 
            animation: slideIn 0.5s ease; 
        }}
        
        @keyframes slideIn {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        h1, h2, h3, h4, h5, h6 {{ 
            animation: slideInFromLeft 0.5s ease; 
            transition: all 0.3s; 
        }}
        
        @keyframes slideInFromLeft {{
            from {{ opacity: 0; transform: translateX(-15px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        @media (max-width: 320px) {{
            .mdui-container {{ padding: 0.8rem; }}
            h1, h2 {{ font-size: 1.2rem; }}
            pre {{ padding: 8px; font-size: 0.8rem; }}
        }}
        
        .mdui-drawer .mdui-card {{
            margin: 16px;
            overflow: hidden; 
        }}
        
        .mdui-drawer .mdui-card-primary {{
            padding: 16px;
        }}
        
        .mdui-drawer .mdui-card-primary-title {{
            font-size: 20px;
            line-height: 1.4;
            word-break: break-word;
            white-space: normal;
            overflow-wrap: break-word;
            max-width: 100%;
        }}
        
        .mdui-drawer .mdui-card-primary-subtitle {{
            font-size: 14px;
            line-height: 1.4;
            word-break: break-word;
            white-space: normal;
            overflow-wrap: break-word;
            cursor: pointer;
            max-width: 100%;
        }}
        
        .mdui-drawer {{
            background-color: #fff;
            transition: top 0.3s, height 0.3s;
        }}
        
        .mdui-theme-layout-dark .mdui-drawer {{
            background-color: #303030;
        }}
        
        @media (min-width: 1024px) {{
            .mdui-drawer-open {{
                padding-top: 12px;
            }}
            
            body.has-appbar .mdui-drawer {{
                height: calc(100% - var(--appbar-height, 64px));
                top: var(--appbar-height, 64px);
            }}
            
            body.appbar-hidden .mdui-drawer {{
                height: 100%;
                top: 0;
            }}
        }}
        
        .mdui-drawer .mdui-list-item {{
            min-height: 36px;
            padding-top: 4px;
            padding-bottom: 4px;
        }}
        
        .mdui-drawer .mdui-list-item-content {{
            line-height: 20px;
        }}
        
        .mdui-toolbar .toc-btn {{
            height: 48px;
            width: 48px;
        }}
        
        /* 密码错误时的摇晃动画 */
        @keyframes shake {{
            0%, 100% {{ transform: translateX(0); }}
            10%, 30%, 50%, 70%, 90% {{ transform: translateX(-4px); }}
            20%, 40%, 60%, 80% {{ transform: translateX(4px); }}
        }}
        
        .mdui-textfield-invalid {{
            animation: shake 0.35s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }}
        
        #encrypted-content {{
            display: none;
        }}
    </style>
    <script src="https://unpkg.com/mdui@1.0.2/dist/js/mdui.min.js" onerror="this.onerror=null;this.src='https://cdnjs.cloudflare.com/ajax/libs/mdui/1.0.2/js/mdui.min.js';"></script>
</head>
<body class="mdui-theme-primary-indigo mdui-theme-accent-blue">
    <div class="mdui-dialog" id="password-dialog">
        <div class="mdui-dialog-title">访问受限</div>
        <div class="mdui-dialog-content">
            <span>请输入密码以查看内容</span>
            <div class="mdui-textfield mdui-textfield-floating-label">
                <i class="mdui-icon material-icons">lock</i>
                <label class="mdui-textfield-label">密码</label>
                <input class="mdui-textfield-input" type="password" id="password-input" autocomplete="off"/>
                <div class="mdui-textfield-error"></div>
            </div>

            
        </div>
        <div class="mdui-dialog-actions">
            <!-- Make explicit type=button to avoid implicit form submit/back navigation -->
            <button type="button" class="mdui-btn mdui-btn-icon mdui-ripple" style="min-width: 0px;" onclick="pastePassword()"><i class="mdui-icon material-icons">content_paste</i></button>
            <button type="button" class="mdui-btn mdui-btn-icon mdui-ripple" style="min-width: 0px;" onclick="togglePasswordVisibility()"><i class="mdui-icon material-icons" id="toggle-password-icon">visibility</i></button>
            <button type="button" class="mdui-btn mdui-ripple" onclick="decryptContent()"><i class="mdui-icon material-icons mdui-icon-right">lock_open</i> 解锁</button>
        </div>
    </div>

    <div id="encrypted-content">
        <div class="mdui-appbar mdui-appbar-fixed">
            <div class="mdui-toolbar mdui-color-theme">
                <button class="mdui-btn mdui-btn-icon toc-btn" mdui-drawer="{{target: '#toc-drawer'}}">
                    <i class="mdui-icon material-icons">&#xe5d2;</i>
                </button>
                <a href="javascript:;" class="mdui-typo-headline">{title}</a>
                <div class="mdui-toolbar-spacer"></div>
                <button class="mdui-btn mdui-btn-icon" mdui-menu="{{target: '#langMenu'}}">
                    <i class="mdui-icon material-icons">&#xe8e2;</i>
                </button>
                <ul class="mdui-menu" id="langMenu">
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('chinese_simplified');">🇨🇳 简体中文</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('chinese_traditional');">🇨🇳 繁體中文</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('english');">🇺🇸 English</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('spanish');">🇪🇸 Español</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('french');">🇫🇷 Français</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('deutsch');">🇩🇪 Deutsch</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('italian');">🇮🇹 italiano</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('russian');">🇷🇺 Русский язык</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('japanese');">🇯🇵 日本語</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('korean');">🇰🇷 한국어</a>
                    </li>
                    <li class="mdui-menu-item">
                        <a href="javascript:translate.changeLanguage('vietnamese');">🇻🇳 Tiếng Việt</a>
                    </li>
                    <li class="mdui-menu-item mdui-rtl mdui-text-right" dir="rtl">
                        <a href="javascript:translate.changeLanguage('arabic');">🇸🇦 بالعربية</a>
                    </li>
                </ul>
            </div>
        </div>

        <div class="mdui-drawer mdui-drawer-close" id="toc-drawer">
            <div class="mdui-card">
                <div class="mdui-card-primary">
                    <div class="mdui-card-primary-title">{title}</div>
                    <div class="mdui-card-primary-subtitle" onclick="copyUrl()" id="current-url"></div>
                </div>
            </div>
            <div class="mdui-list" id="toc-list">
            </div>
        </div>
        
        <div class="mdui-container mdui-typo mdui-container-with-appbar" id="main-content">
        </div>
    </div>
    <noscript>
      <style>
        .no-js-wrap{{position:fixed;inset:0;z-index:2147483647;min-height:40px;display:flex;align-items:center;justify-content:center;padding:24px;box-sizing:border-box;background:#ffffff;color:#111827;font-family: Roboto,Helvetica,Arial}}
        .no-js-card{{max-width:720px;width:100%;border:1px solid #e5e7eb;border-radius:12px;padding:24px;background:#fff;box-shadow:0 1px 2px #0000000d}}
        @media (prefers-color-scheme: dark){{
          .no-js-wrap{{background:#0f1115;color:#e5e7eb}}
          .no-js-card{{background:#0f1115;border-color:#374151;box-shadow:0 1px 2px #00000066}}
        }}
      </style>
      <div class="no-js-wrap">
        <div class="no-js-card">
          <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="#DA954B"><path d="M34.18-116.57 480-886.86l445.82 770.29H34.18Zm448.6-121.99q14.39 0 24.32-10.05 9.94-10.05 9.94-24.43 0-14.39-10.05-24.2-10.05-9.82-24.44-9.82t-24.32 9.93q-9.93 9.93-9.93 24.32t10.05 24.32q10.05 9.93 24.43 9.93ZM449.33-352H516v-213.85h-66.67V-352Z"/></svg>
          <svg xmlns="http://www.w3.org/2000/svg" height="40px" viewBox="0 -960 960 960" width="40px" fill="currentColor"><path d="M800.09-44.96 281.43-563.37l-84.13 84.13 183 183-63.89 63.89L68.52-480l148.26-148.02L44.96-800.09l59.39-59.39 755.13 755.13-59.39 59.39ZM746.8-335.57l-64.65-64.65 80.55-80.54-183-183 63.89-63.89L891.48-480 746.8-335.57Z"/></svg>
          <p>网站应用程序必须启用 JavaScript 才能运作，但是此页面上的 JavaScript 已被拦截。<br />
          请检查你的浏览器设置。
          </p>
          <a href="/">重新加载</a>
        </div>
      </div>
    </noscript>
    <script>
    var ENCRYPTED_DATA = {encrypted_data};
    var SALT = "{salt}";
    var passwordDialog = null;
    // 立即在解密弹窗前初始化主题与悬浮切换按钮，使弹窗显示时能正确渲染深色模式
    (function earlyThemeAndButtonInit() {{
        try {{
            // 根据用户偏好或系统主题设置初始主题
            var storedTheme = null;
            try {{ storedTheme = localStorage.getItem('mdui-theme'); }} catch(e) {{ /* ignore if access denied */ }}
            var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            var theme = storedTheme || (prefersDark ? 'dark' : 'light');
            if (theme === 'dark') {{
                document.body.classList.add('mdui-theme-layout-dark');
            }}

            // 标记触摸设备样式（因为复制按钮、悬浮等交互在弹窗前应正确呈现）
            if (('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) {{
                document.body.classList.add('touch-device');
            }}

            // 创建并添加一个悬浮的主题切换按钮，供用户在解密前切换深色/浅色
            var themeBtn = document.createElement('button');
            themeBtn.className = 'mdui-fab mdui-color-theme-accent mdui-ripple theme-switch';
            themeBtn.setAttribute('aria-label', '切换主题');
            themeBtn.innerHTML = '<i class="mdui-icon material-icons">&#xe3a9;</i>';
            themeBtn.style.display = 'block';
            themeBtn.onclick = function() {{
                var body = document.body;
                var nowDark = body.classList.contains('mdui-theme-layout-dark');
                if (nowDark) {{
                    body.classList.remove('mdui-theme-layout-dark');
                    try {{ localStorage.setItem('mdui-theme', 'light'); }} catch(e) {{}}
                }} else {{
                    body.classList.add('mdui-theme-layout-dark');
                    try {{ localStorage.setItem('mdui-theme', 'dark'); }} catch(e) {{}}
                }}
            }};

            var appendThemeBtn = function() {{
                // 避免重复插入
                if (!document.querySelector('.theme-switch')) {{
                    document.body.appendChild(themeBtn);
                }}
            }};
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', appendThemeBtn);
            }} else {{
                appendThemeBtn();
            }}
        }} catch(e) {{
            console.error('earlyThemeAndButtonInit error:', e);
        }}
    }})();
    
    function base64ToArrayBuffer(base64) {{
        var binaryString = atob(base64);
        var bytes = new Uint8Array(binaryString.length);
        for (var i = 0; i < binaryString.length; i++) {{
            bytes[i] = binaryString.charCodeAt(i);
        }}
        return bytes.buffer;
    }}
    
    function arrayBufferToBase64(buffer) {{
        var binary = '';
        var bytes = new Uint8Array(buffer);
        for (var i = 0; i < bytes.byteLength; i++) {{
            binary += String.fromCharCode(bytes[i]);
        }}
        return btoa(binary);
    }}
    
    async function deriveKey(password, salt) {{
        var enc = new TextEncoder();
        var keyMaterial = await crypto.subtle.importKey(
            'raw',
            enc.encode(password),
            'PBKDF2',
            false,
            ['deriveBits', 'deriveKey']
        );
        
        return crypto.subtle.deriveKey(
            {{
                name: 'PBKDF2',
                salt: salt,
                iterations: 100000,
                hash: 'SHA-256'
            }},
            keyMaterial,
            {{ name: 'AES-GCM', length: 256 }},
            false,
            ['decrypt']
        );
    }}
    
    async function decryptContent() {{
        var passwordInput = document.getElementById('password-input');
        var password = passwordInput.value;
        var textfield = passwordInput.parentElement;
        var errorDiv = textfield.querySelector('.mdui-textfield-error');
        
        if (!password) {{
            textfield.classList.add('mdui-textfield-invalid');
            errorDiv.textContent = '请输入密码';
            return;
        }}
        
        try {{
            var saltBytes = base64ToArrayBuffer(SALT);
            var key = await deriveKey(password, saltBytes);
            
            var encryptedBytes = base64ToArrayBuffer(ENCRYPTED_DATA.ciphertext);
            var iv = base64ToArrayBuffer(ENCRYPTED_DATA.iv);
            
            var decryptedBytes = await crypto.subtle.decrypt(
                {{
                    name: 'AES-GCM',
                    iv: iv
                }},
                key,
                encryptedBytes
            );
            
            var decryptedText = new TextDecoder().decode(decryptedBytes);
            
            if (passwordDialog) {{
                passwordDialog.close();
            }}
            document.getElementById('encrypted-content').style.display = 'block';
            document.getElementById('main-content').innerHTML = decryptedText;
            
            initializePage();
            
        }} catch (e) {{
            console.error('解密失败:', e);
            textfield.classList.add('mdui-textfield-invalid');
            errorDiv.textContent = '密码错误，请重试';
            passwordInput.value = '';
        }}
    }}

    function togglePasswordVisibility() {{
        var input = document.getElementById('password-input');
        var icon = document.getElementById('toggle-password-icon');
        if (input.type === 'password') {{
            input.type = 'text';
            icon.innerHTML = 'visibility_off';
        }} else {{
            input.type = 'password';
            icon.innerHTML = 'visibility';
        }}
    }}
    
    async function pastePassword() {{
        var input = document.getElementById('password-input');
        try {{
            var text = await navigator.clipboard.readText();
            input.value = text;
            input.focus();
        }} catch (err) {{
            console.error('粘贴失败:', err);
            showSnackbar('粘贴失败，请手动输入密码');
        }}
    }}
    
    // Use keydown and prevent default action to avoid unexpected form submission / navigation
    document.getElementById('password-input').addEventListener('keydown', function(e) {{
        if (e.key === 'Enter') {{
            e.preventDefault();
            decryptContent();
        }}
    }});
    
    document.getElementById('password-input').addEventListener('input', function(e) {{
        var textfield = e.target.parentElement;
        var errorDiv = textfield.querySelector('.mdui-textfield-error');
        textfield.classList.remove('mdui-textfield-invalid');
        errorDiv.textContent = '';
    }});
    
    function isTouchDevice() {{
        return ('ontouchstart' in window) || 
               (navigator.maxTouchPoints > 0) || 
               (navigator.msMaxTouchPoints > 0);
    }}
    
    function copyText(btn) {{
        var pre = btn.parentNode;
        var code = pre.querySelector('code');
        var text = code ? (code.innerText || code.textContent) : '';
        
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed"; 
        textArea.style.opacity = "0";
        document.body.appendChild(textArea);
        textArea.select();
        
        try {{
            var successful = document.execCommand('copy');
            if (successful) {{
                showSnackbar('已复制到剪贴板！');
                showCopySuccess(btn);
            }} else {{
                showSnackbar('复制失败，请手动复制');
            }}
        }} catch (err) {{
            console.error('复制失败:', err);
            showSnackbar('复制失败，请手动复制');
        }}
        
        document.body.removeChild(textArea);
    }}
    
    function showCopySuccess(btn) {{
        var icon = btn.querySelector('i');
        var oldHtml = icon.innerHTML;
        icon.innerHTML = '&#xe86c;';
        btn.classList.add('copy-success');
        
        setTimeout(function() {{
            icon.innerHTML = oldHtml;
            btn.classList.remove('copy-success');
        }}, 2000);
    }}
    
    function showSnackbar(message) {{
        if (typeof mdui !== 'undefined' && mdui.snackbar) {{
            mdui.snackbar({{
                message: message,
                position: 'bottom',
                timeout: 2000,
                closeOnOutsideClick: true
            }});
        }}
    }}
    
    function showTranslateComplete(targetlangttl) {{
        var languageMap = {{
            'chinese_simplified': '<i class="mdui-icon material-icons">&#xe8e2;</i> 已翻译为简体中文',
            'chinese_traditional': '<i class="mdui-icon material-icons">&#xe8e2;</i> 已翻譯為繁體中文',
            'english': '<i class="mdui-icon material-icons">&#xe8e2;</i> Translated to English',
            'spanish': '<i class="mdui-icon material-icons">&#xe8e2;</i> Traducido al español',
            'french': '<i class="mdui-icon material-icons">&#xe8e2;</i> Traduit en français',
            'deutsch': '<i class="mdui-icon material-icons">&#xe8e2;</i> Übersetzt auf Deutsch',
            'italian': '<i class="mdui-icon material-icons">&#xe8e2;</i> Tradotto in italiano',
            'russian': '<i class="mdui-icon material-icons">&#xe8e2;</i> Переведено на русский язык',
            'japanese': '<i class="mdui-icon material-icons">&#xe8e2;</i> 日本語に翻訳',
            'korean': '<i class="mdui-icon material-icons">&#xe8e2;</i> 한국어로 번역됨',
            'vietnamese': '<i class="mdui-icon material-icons">&#xe8e2;</i> Đã dịch sang tiếng Việt',
            'arabic': '<i class="mdui-icon material-icons">&#xe8e2;</i> ترجم إلى العربية'
        }};
        var translatedMessage = languageMap[targetlangttl] || '<i class="mdui-icon material-icons">&#xe8e2;</i> Page translated.';
        
        if (targetlangttl === 'arabic') {{
            document.documentElement.setAttribute('dir', 'rtl');
            document.body.classList.add('mdui-rtl');
        }} else {{
            document.documentElement.setAttribute('dir', 'ltr');
            document.body.classList.remove('mdui-rtl');
        }}
        
        if (typeof showTranslateComplete.lastMessage === 'undefined' || showTranslateComplete.lastMessage !== translatedMessage) {{
            showTranslateComplete.lastMessage = translatedMessage;
            showSnackbar(translatedMessage);
        }}
    }}
    
    function toggleTheme() {{
        var body = document.body;
        var hasClass = body.className.indexOf('mdui-theme-layout-dark') > -1;
        
        if (hasClass) {{
            body.className = body.className.replace(/mdui-theme-layout-dark/g, '').trim();
        }} else {{
            body.className = body.className + ' mdui-theme-layout-dark';
        }}
    }}
    
    function updateAppbarHeight() {{
        var appbar = document.querySelector('.mdui-appbar');
        if (appbar) {{
            var height = appbar.offsetHeight;
            document.documentElement.style.setProperty('--appbar-height', height + 'px');
        }}
    }}
    
    function setupAppbarObserver() {{
        var appbar = document.querySelector('.mdui-appbar');
        if (!appbar) return;
        
        updateAppbarHeight();
        
        if ('IntersectionObserver' in window) {{
            var observer = new IntersectionObserver(function(entries) {{
                if (entries[0].isIntersecting) {{
                    document.body.classList.remove('appbar-hidden');
                    document.body.classList.add('appbar-visible');
                }} else {{
                    document.body.classList.remove('appbar-visible');
                    document.body.classList.add('appbar-hidden');
                }}
            }}, {{ threshold: 0.1 }});
            
            observer.observe(appbar);
        }}
    }}
    
    function copyUrl() {{
        var url = window.location.href;
        
        var textArea = document.createElement("textarea");
        textArea.value = url;
        textArea.style.position = "fixed";
        textArea.style.opacity = "0";
        document.body.appendChild(textArea);
        textArea.select();
        
        try {{
            document.execCommand('copy');
            showSnackbar('已复制！');
        }} catch (err) {{
            console.error('复制失败:', err);
            showSnackbar('复制失败，请手动复制');
        }}
        
        document.body.removeChild(textArea);
    }}
    
    function initializePage() {{
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
            document.body.className += ' mdui-theme-layout-dark';
        }}
        
        document.body.className += ' has-appbar';
        
        if (isTouchDevice()) {{
            document.body.className += ' touch-device';
        }}
        
        var tables = document.querySelectorAll('table');
        for (var i = 0; i < tables.length; i++) {{
            var table = tables[i];
            if (table.className.indexOf('mdui-table') === -1) {{
                table.className += ' mdui-table';
                var wrapper = document.createElement('div');
                wrapper.className = 'mdui-table-responsive';
                if (table.parentNode) {{
                    table.parentNode.insertBefore(wrapper, table);
                    wrapper.appendChild(table);
                }}
            }}
        }}
        
        var pres = document.querySelectorAll('pre');
        for (var i = 0; i < pres.length; i++) {{
            var pre = pres[i];
            if (pre.className.indexOf('mdui-shadow-1') === -1) {{
                pre.className += ' mdui-shadow-1';
            }}
            
            var btn = document.createElement('button');
            btn.className = 'copy-btn mdui-btn mdui-btn-icon mdui-ripple';
            btn.onclick = function() {{ copyText(this); }};
            var icon = document.createElement('i');
            icon.className = 'mdui-icon material-icons';
            icon.innerHTML = '&#xe14d;';
            btn.appendChild(icon);
            pre.insertBefore(btn, pre.firstChild);
        }}
        
        var themeBtn = document.createElement('button');
        themeBtn.className = 'mdui-fab mdui-color-theme-accent mdui-ripple theme-switch';
        themeBtn.innerHTML = '<i class="mdui-icon material-icons">&#xe3a9;</i>';
        themeBtn.onclick = toggleTheme;
        // 避免重复添加由早期脚本已创建的按钮
        if (!document.querySelector('.theme-switch')) {{
            document.body.appendChild(themeBtn);
        }}
        
        try {{
            if (typeof mdui !== 'undefined') {{
                mdui.mutation();
                
                if (mdui.Appbar) {{
                    new mdui.Appbar('.mdui-appbar');
                }}
            }}
        }} catch(e) {{
            console.error('MDUI 初始化错误:', e);
        }}
        
        setupAppbarObserver();
        
        var urlElement = document.getElementById('current-url');
        if (urlElement) {{
            urlElement.innerText = window.location.href;
        }}

        var titles = document.querySelectorAll('#main-content h1, #main-content h2, #main-content h3, #main-content h4, #main-content h5, #main-content h6');
        var tocList = document.getElementById('toc-list');
        
        if (tocList && titles.length > 0) {{
            tocList.innerHTML = '';
            titles.forEach(function(title) {{
                var level = parseInt(title.tagName.charAt(1));
                var item = document.createElement('a');
                item.className = 'mdui-list-item mdui-ripple';
                item.style.paddingLeft = (level * 16) + 'px';
                item.innerHTML = '<div class="mdui-list-item-content">' + title.textContent + '</div>';
                
                if (!title.id) {{
                    title.id = 'toc-' + title.textContent.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
                }}
                item.href = '#' + title.id;
                
                item.onclick = function(e) {{
                    if (window.innerWidth <= 1024) {{
                        e.preventDefault();
                        var drawer = new mdui.Drawer('#toc-drawer');
                        drawer.close();
                        setTimeout(function() {{
                            window.location.hash = title.id;
                        }}, 300);
                    }}
                }};
                tocList.appendChild(item);
            }});
        }}
        
        setTimeout(function() {{
            if (typeof translate !== 'undefined') {{
                try {{
                    translate.language.setLocal('chinese_simplified');
                    translate.selectLanguageTag.show = false;
                    translate.ignore.tag.push('tbody');
                    translate.ignore.tag.push('code');
                    translate.ignore.id.push('langMenu');
                    translate.ignore.class.push('code-block');   
                    translate.service.use('client.edge');
                    translate.execute();
                }} catch(e) {{
                    console.error('翻译错误:', e);
                }}
            }}
        }}, 500);
        
        if (typeof translate !== 'undefined') {{
            translate.listener.renderTaskFinish = function(task){{
                showTranslateComplete(translate.language.getCurrent());
            }}
        }};
        mdui.mutation();
    }}
    
    window.addEventListener('resize', function() {{
        updateAppbarHeight();
    }});
    
    window.addEventListener('load', function() {{
        passwordDialog = new mdui.Dialog('#password-dialog', {{
            modal: true,
            closeOnEsc: false,
            closeOnCancel: false,
            history: false
        }});
        passwordDialog.open();
        
        setTimeout(function() {{
            document.getElementById('password-input').focus();
        }}, 300);
    }});
    </script>
    <script src="https://cdn.staticfile.net/translate.js/3.12.0/translate.js" onerror="this.onerror=null;this.src='https://sharepoint.cf.stevezmt.top/js/3rd-party/translate.min.js';"></script>
</body>
</html>
"""


def encrypt_content(content, password):
    """使用 AES-256-GCM 加密内容"""
    # 生成随机盐值
    salt = secrets.token_bytes(32)
    
    # 使用 PBKDF2 从密码派生密钥
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode('utf-8'))
    
    # 生成随机 IV
    iv = secrets.token_bytes(12)
    
    # 使用 AES-GCM 加密
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, content.encode('utf-8'), None)
    
    return {
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'iv': base64.b64encode(iv).decode('utf-8'),
        'salt': base64.b64encode(salt).decode('utf-8')
    }


def add_copy_buttons(soup):
    """为代码块添加复制按钮（在加密前处理）"""
    # 注意：复制按钮会在解密后的客户端 JavaScript 中动态添加
    return soup


def convert_markdown_to_encrypted_html(input_path, password, output_path=None):
    """将 Markdown 文件转换为加密的 HTML 文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 转换 Markdown 为 HTML
    html = markdown.markdown(text, 
                           extensions=['fenced_code', 
                                     'tables', 
                                     'nl2br',
                                     'sane_lists',
                                     'attr_list',
                                     'def_list',
                                     'admonition'])
    
    soup = BeautifulSoup(html, 'html.parser')
    content_html = str(soup)
    
    # 获取标题
    h1 = soup.find('h1')
    title = h1.text if h1 else os.path.basename(input_path).replace('.md', '')
    
    # 加密内容
    encrypted = encrypt_content(content_html, password)
    
    # 生成完整的 HTML
    full_html = HTML_TEMPLATE.format(
        title=title,
        encrypted_data='{{ "ciphertext": "{}", "iv": "{}" }}'.format(
            encrypted['ciphertext'], 
            encrypted['iv']
        ),
        salt=encrypted['salt']
    )
    
    # 确定输出路径
    if output_path is None:
        output_path = input_path.replace('.md', '.html')
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f'✓ 已加密并转换: {input_path} -> {output_path}')
    return output_path


def main():
    if len(sys.argv) < 2:
        print("用法: python format_enc.py <markdown文件> [密码]")
        print("示例: python format_enc.py document.md mypassword123")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        sys.exit(1)
    
    if not input_file.endswith('.md'):
        print("错误: 输入文件必须是 .md 文件")
        sys.exit(1)
    
    # 获取密码
    if len(sys.argv) >= 3:
        password = sys.argv[2]
    else:
        import getpass
        password = getpass.getpass("请输入加密密码: ")
        password_confirm = getpass.getpass("请再次输入密码确认: ")
        
        if password != password_confirm:
            print("错误: 两次输入的密码不一致")
            sys.exit(1)
    
    if not password:
        print("错误: 密码不能为空")
        sys.exit(1)
    
    # 转换文件
    try:
        output_file = convert_markdown_to_encrypted_html(input_file, password)
        print(f"\n✓ 转换成功！")
        print(f"输出文件: {output_file}")
        print(f"请妥善保管密码: {password}")
    except Exception as e:
        print(f"错误: 转换失败 - {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
