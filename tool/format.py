#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Material Design UI (MDUI) HTML Generator for Markdown Files
===========================================================================

This script converts Markdown files in the current directory and its 
subdirectories into HTML files using Material Design UI (MDUI) for styling. 

It also adds copy buttons to code blocks and generates a table of contents 
based on the headers in the Markdown files.

This script rely on [MDUI v1](https://github.com/zdhxiong/mdui).

[Github Gist link](https://gist.github.com/SteveZMTstudios/11c348d4db33716cc78cf74329271b33)

Usage
================
```
$> git submodule add https://gist.github.com/11c348d4db33716cc78cf74329271b33.git
python 11c348d4db33716cc78cf74329271b33/format.py
```
If you want to use this script in your project please keep this header.


Bug report
================

Feel free to comment below this gist!

Version: 1.0.6-20250318-stable

Last changelog：
- add favicon.png

License
================

```
# Material Design UI (MDUI) HTML Generator for Markdown Files
# 版权所有 Copyright (C) 2025 SteveZMTstudios
#
# 本程序是自由软件：您可以根据自由软件基金会发布的 GNU 通用公共许可证的
# 条款（无论是第三版还是您选择的任何后续版本）来重新分发和/或修改它。
#
# 本程序发布的目的是希望它有用，但没有任何担保；甚至没有适销性或针对
# 特定用途的适用性的暗示担保。详情请见 GNU 通用公共许可证。
# 您应该已经随本程序收到了一份 GNU 通用公共许可证的副本。如果不是，请访问 
# <https://www.gnu.org/licenses/>。
#
# This program is free software: you can redistribute it and/or modify
# #it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
---------------------------------------------------------------------------
'''


import os
try:
    import markdown
    from bs4 import BeautifulSoup
    import glob
except ModuleNotFoundError:
    if os.name == 'posix':
        os.system('sudo apt install python3-full python3-markdown')
    os.system('pip install markdown beautifulsoup4')
    import markdown
    from bs4 import BeautifulSoup
    import glob


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
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; }}
        
        .mdui-container {{ max-width: 900px; padding: 2rem; }}
        .mdui-container-with-appbar {{ padding-top: 4rem; }}
        pre {{ background: #f6f8fa; padding: 16px; border-radius: 6px; position: relative; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; transition: all 0.3s; }}
        
        .mdui-theme-layout-dark pre {{ background: #1e1e1e; color: #f0f0f0; }}
        
        code {{ word-wrap: break-word; }}
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
        
        img {{ max-width: 100%; height: auto; transition: all 0.3s; }}
        
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
        
        * html .copy-btn {{ 
            position: static; 
            margin-top: -30px; 
            margin-right: 5px; 
            float: right; 
        }}
        
        * html .theme-switch {{ 
            position: absolute; 
            bottom: auto; 
            top: expression(eval(document.documentElement.scrollTop+document.documentElement.clientHeight-60)); 
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
    </style>
    <!--[if IE]>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/es6-promise/4.2.8/es6-promise.auto.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://gcore.jsdelivr.net/npm/classlist-polyfill@1.2.0/src/index.min.js"></script>
    <script src="https://gcore.jsdelivr.net/npm/eligrey-classlist-js-polyfill@1.2.20171210/classList.min.js"></script>
    <![endif]-->
    <script src="https://unpkg.com/mdui@1.0.2/dist/js/mdui.min.js" onerror="this.onerror=null;this.src='https://cdnjs.cloudflare.com/ajax/libs/mdui/1.0.2/js/mdui.min.js';"></script>
    <script>
    // fxxk ie
    function isIE() {{
        return window.navigator.userAgent.indexOf('MSIE ') > -1 || window.navigator.userAgent.indexOf('Trident/') > -1;
    }}
    
    function detectBrowser() {{
        var ua = window.navigator.userAgent;
        var isIE = ua.indexOf('MSIE ') > -1 || ua.indexOf('Trident/') > -1;
        var isOldEdge = ua.indexOf('Edge/') > -1;
        var isChrome = ua.indexOf('Chrome/') > -1 && !isOldEdge;
        var isFirefox = ua.indexOf('Firefox/') > -1;
        
        var isOldBrowser = isIE || (isOldEdge && ua.indexOf('Edge/') > 0 && parseInt(ua.split('Edge/')[1]) < 18);
        
        return {{
            isOldBrowser: isOldBrowser,
            isIE: isIE,
            browserName: isIE ? 'Internet Explorer' : 
                       isOldEdge ? 'Microsoft Edge Legacy' :
                       isChrome ? 'Chrome' : 
                       isFirefox ? 'Firefox' : 
                       'Unknown Browser'
        }};
    }}
    
    function isTouchDevice() {{
        return ('ontouchstart' in window) || 
               (navigator.maxTouchPoints > 0) || 
               (navigator.msMaxTouchPoints > 0);
    }}
    
    function showBrowserNotice() {{
        var browserInfo = detectBrowser();
        if (browserInfo.isOldBrowser) {{
            try {{
                if (typeof mdui !== 'undefined' && mdui.snackbar) {{
                    mdui.snackbar({{
                        message: 'Seems you are using unsupported ' + browserInfo.browserName + ', some features may not work properly.',
                        buttonText: 'OK',
                        position: 'bottom',
                        timeout: 50000,
                        closeOnOutsideClick: true
                    }});
                }} else {{
                    alert('You are using an unsupported ' + browserInfo.browserName + ', some features may not work properly.');
                }}
            }} catch (e) {{
                console.error('show browser err :', e);
            }}
        }}
    }}
    
    function copyText(btn) {{
        var pre = btn.parentNode;
        var code = pre.querySelector('code');
        var text = code ? (code.innerText || code.textContent) : '';
        
        if (window.clipboardData && window.clipboardData.setData) {{
            window.clipboardData.setData("Text", text);
            showSnackbar('Copied to clipboard!');
            showCopySuccess(btn);
            return;
        }}
        
        var textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed"; 
        textArea.style.opacity = "0";
        document.body.appendChild(textArea);
        textArea.select();
        
        try {{
            var successful = document.execCommand('copy');
            if (successful) {{
                showSnackbar('Copied to clipboard!');
                showCopySuccess(btn);
            }} else {{
                showSnackbar('Failed to copy, please copy manually');
            }}
        }} catch (err) {{
            console.error('Failed copy:', err);
            showSnackbar('Failed to copy, please copy manually');
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
        }} else {{
            alert(message);
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
            if (typeof mdui !== 'undefined' && mdui.snackbar) {{
                mdui.snackbar({{
                    message: translatedMessage,
                    position: 'top',
                    buttonText: 'OK',
                    timeout: 5000,
                    closeOnOutsideClick: true
                }});
            }} else {{
                console.log(translatedMessage);
            }}
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
    
    function ready(fn) {{
        if (document.readyState !== 'loading') {{
            fn();
        }} else if (document.addEventListener) {{
            document.addEventListener('DOMContentLoaded', fn);
        }} else {{
            document.attachEvent('onreadystatechange', function() {{
                if (document.readyState !== 'loading') fn();
            }});
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
        
        if ('ResizeObserver' in window) {{
            var resizeObserver = new ResizeObserver(function() {{
                updateAppbarHeight();
            }});
            
            resizeObserver.observe(appbar);
        }}
    }}
    
    ready(function() {{
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
            document.body.className += ' mdui-theme-layout-dark';
        }}
        
        document.body.className += ' has-appbar';
        
        if (isTouchDevice()) {{
            document.body.className += ' touch-device';
        }}
        
        showBrowserNotice();
        
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
        }}
        
        var btn = document.createElement('button');
        btn.className = 'mdui-fab mdui-color-theme-accent mdui-ripple theme-switch';
        btn.innerHTML = '<i class="mdui-icon material-icons">&#xe3a9;</i>';
        btn.onclick = toggleTheme;
        document.body.appendChild(btn);
        
        try {{
            if (typeof mdui !== 'undefined') {{
                mdui.mutation();
                
                if (mdui.Appbar) {{
                    new mdui.Appbar('.mdui-appbar');
                }}
            }}
        }} catch(e) {{
            console.error('MDUI init err:', e);
        }}

        if (isIE()) {{
            var copyBtns = document.querySelectorAll('.copy-btn');
            for (var i = 0; i < copyBtns.length; i++) {{
                copyBtns[i].style.display = 'block';
            }}
            
            var appbar = document.querySelector('.mdui-appbar');
            if (appbar) {{
                appbar.style.position = 'fixed';
                appbar.style.top = '0';
                appbar.style.width = '100%';
                appbar.style.zIndex = '1000';
            }}
        }}
        
        setupAppbarObserver();
        
        var urlElement = document.getElementById('current-url');
        if (urlElement) {{
            urlElement.innerText = window.location.href;
        }}

        var titles = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        var tocList = document.getElementById('toc-list');
        
        if (tocList && titles.length > 0) {{
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
                
                item.onclick = function() {{
                    if (window.innerWidth <= 1024) {{
                        toggleToc();
                    }}
                }};
                tocList.appendChild(item);
            }});
        }}
    }});
    
    window.addEventListener('resize', function() {{
        updateAppbarHeight();
    }});
    
    if (window.matchMedia) {{
        try {{
            var darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
            var darkModeHandler = function(e) {{
                if (e.matches) {{
                    document.body.className += ' mdui-theme-layout-dark';
                }} else {{
                    document.body.className = document.body.className.replace(/mdui-theme-layout-dark/g, '').trim();
                }}
            }};
            
            if (darkModeQuery.addListener) {{
                darkModeQuery.addListener(darkModeHandler);
            }} else if (darkModeQuery.addEventListener) {{
                darkModeQuery.addEventListener('change', darkModeHandler);
            }}
        }} catch(e) {{
            console.error('media query err:', e);
        }}
    }}
    
    function copyUrl() {{
        var url = window.location.href;
        if (window.clipboardData && window.clipboardData.setData) {{
            clipboardData.setData("Text", url);
            showSnackbar('Copied!');
            return;
        }}
        
        var textArea = document.createElement("textarea");
        textArea.value = url;
        textArea.style.position = "fixed";
        textArea.style.opacity = "0";
        document.body.appendChild(textArea);
        textArea.select();
        
        try {{
            document.execCommand('copy');
            showSnackbar('Copied!');
        }} catch (err) {{
            console.error('Copy failed:', err);
            showSnackbar('Failed to copy, please copy manually.');
        }}
        
        document.body.removeChild(textArea);
    }}
    
    function toggleToc() {{
        var drawer = new mdui.Drawer('#toc-drawer');
        drawer.toggle();
    }}
    </script>
</head>
<body class="mdui-theme-primary-indigo mdui-theme-accent-blue">
    <div class="mdui-appbar mdui-appbar-fixed">
        <div class="mdui-toolbar mdui-color-theme">
            <button class="mdui-btn mdui-btn-icon toc-btn" onclick="toggleToc()">
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
    
    <div class="mdui-container mdui-typo mdui-container-with-appbar">
        {content}
    </div>
<script src="https://cdn.staticfile.net/translate.js/3.12.0/translate.js" onerror="this.onerror=null;this.src='https://sharepoint.cf.stevezmt.top/js/3rd-party/translate.min.js';"></script>
<script>
setTimeout(function() {{
    var isTranslated = 0;
    if (typeof translate !== 'undefined') {{
        try {{
            translate.language.setLocal('chinese_simplified');
            translate.selectLanguageTag.show = false;
            translate.ignore.tag.push('tbody');
            translate.ignore.tag.push('code');
            translate.ignore.id.push('langMenu');
            translate.ignore.id.push('igTrans');
            translate.ignore.class.push('igTrans');
            translate.ignore.class.push('code-block');   
            translate.service.use('client.edge');
            showTranslateComplete(translate.language.getCurrent());
            translate.execute();
        }} catch(e) {{
            console.error('Translate err:', e);
        }}
    }}
}}, 500);
translate.listener.renderTaskFinish = function(task){{
    showTranslateComplete(translate.language.getCurrent());
}}
</script>
</html>
"""

def add_copy_buttons(soup):
    for pre in soup.find_all('pre'):
        button = soup.new_tag('button')
        icon = soup.new_tag('i')
        icon['class'] = 'mdui-icon material-icons'
        icon.append("\ue14d")  # Using Unicode character directly instead of HTML entity
        button.append(icon)
        button['class'] = 'copy-btn mdui-btn mdui-btn-icon mdui-ripple'
        button['onclick'] = 'copyText(this)'
        pre.insert(0, button)
    return soup

def convert_markdown_file(input_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    html = markdown.markdown(text, 
                           extensions=['fenced_code', 
                                     'tables', 
                                     'nl2br',
                                     'sane_lists',
                                     'attr_list',
                                     'def_list',
                                     'admonition'])
    
    soup = BeautifulSoup(html, 'html.parser')
    soup = add_copy_buttons(soup)
    
    title = os.path.basename(input_path).replace('.md', '')
    
    h1 = soup.find('h1')
    title = h1.text if h1 else os.path.basename(input_path).replace('.md', '')
    
    full_html = HTML_TEMPLATE.format(
        title=title,
        content=str(soup)
    )
    
    output_path = input_path.replace('.md', '.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f'已转换: {input_path} -> {output_path}')

def process_all_markdown_files(directory):
    parent_dir = os.path.dirname(directory)
    md_files = glob.glob(os.path.join(parent_dir, '**/*.md'), recursive=True)
    for md_file in md_files:
        try:
            convert_markdown_file(md_file)
        except Exception as e:
            print(f'处理 {md_file} 时出错: {str(e)}')
            raise e

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # print(f'Current directory: {current_dir}')
    process_all_markdown_files(current_dir)
    print('所有 Markdown 文件处理完成！')