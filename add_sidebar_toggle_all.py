import os

templates_dir = 'C:/www/nslookup/templates'

# Define the sidebar toggle HTML and CSS/JS to add
toggle_html = '''        <!-- Sidebar Toggle Button -->
        <button id="sidebarToggle" class="sidebar-toggle-btn" title="Toggle Sidebar">
            <svg id="sidebarToggleIcon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>'''

sidebar_css_js = '''    <style>
        .sidebar-toggle-btn {
            position: fixed;
            top: 12px;
            left: 12px;
            z-index: 1000;
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background: rgba(118, 185, 0, 0.15);
            border: 1px solid rgba(118, 185, 0, 0.3);
            color: #4DFF00;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            opacity: 0;
            pointer-events: none;
        }
        .sidebar-toggle-btn:hover {
            background: rgba(118, 185, 0, 0.3);
            border-color: #4DFF00;
            box-shadow: 0 0 15px rgba(77, 255, 0, 0.3);
        }
        .sidebar-toggle-btn.visible {
            opacity: 1;
            pointer-events: auto;
        }
        .sidebar-toggle-btn.shifted {
            left: 268px;
        }
        #mainSidebar {
            transition: transform 0.3s ease, width 0.3s ease;
        }
        #mainSidebar.collapsed {
            transform: translateX(-268px);
            width: 0;
            overflow: hidden;
        }
        @media (max-width: 768px) {
            #mainSidebar {
                position: fixed;
                z-index: 999;
                height: 100vh;
            }
            #mainSidebar.collapsed {
                transform: translateX(-268px);
            }
        }
    </style>
    <script>
        (function() {
            var toggleBtn = document.getElementById('sidebarToggle');
            var sidebar = document.getElementById('mainSidebar');
            if (!toggleBtn || !sidebar) return;

            var savedState = localStorage.getItem('sidebar-collapsed');
            if (savedState === 'true') {
                sidebar.classList.add('collapsed');
                toggleBtn.classList.add('visible');
                toggleBtn.classList.add('shifted');
            }

            toggleBtn.addEventListener('click', function() {
                sidebar.classList.toggle('collapsed');
                var isCollapsed = sidebar.classList.contains('collapsed');
                localStorage.setItem('sidebar-collapsed', isCollapsed);
                toggleBtn.classList.toggle('visible', isCollapsed);
                toggleBtn.classList.toggle('shifted', isCollapsed);
            });

            if (!sidebar.classList.contains('collapsed')) {
                toggleBtn.classList.add('visible');
            }
        })();
    </script>'''

# Templates to update with their specific sidebar patterns
templates = {
    'dashboard/index.html': {
        'sidebar_marker': '<div class="scan-line"></div>\n\n    <div class="flex min-h-screen">\n        <!-- Sidebar -->\n        <aside class="w-64 glass-effect sidebar-glow flex flex-col">',
        'sidebar_id': 'mainSidebar',
    },
    'dashboard/animations.html': {
        'sidebar_marker': '<div class="scan-line"></div>\n\n    <div class="flex min-h-screen">\n        <aside class="w-64 glass-effect sidebar-glow flex flex-col">',
        'sidebar_id': 'mainSidebar',
    },
    'traceroute/result.html': {
        'sidebar_marker': '<div class="scan-line"></div>\n\n    <div class="flex min-h-screen">\n        <!-- Sidebar -->\n        <aside class="w-64 glass-effect sidebar-glow flex flex-col">',
        'sidebar_id': 'mainSidebar',
    },
    'admin/base_site.html': {
        'sidebar_marker': '<div class="admin-layout">\n    <aside class="admin-sidebar" id="admin-sidebar">',
        'sidebar_id': 'admin-sidebar',
    },
    'admin/dashboard.html': {
        'sidebar_marker': '<div class="scan-line"></div>\n\n    <div class="flex min-h-screen">\n        <!-- Sidebar -->\n        <aside class="w-64 glass-effect sidebar-glow flex flex-col">',
        'sidebar_id': 'mainSidebar',
    },
    'admin/nav_sidebar.html': {
        'sidebar_marker': '<nav class="sticky" id="nav-sidebar" aria-label="{% translate \'Sidebar\' %}">',
        'sidebar_id': 'nav-sidebar',
    },
}

for template_path, config in templates.items():
    full_path = os.path.join(templates_dir, template_path)
    if not os.path.exists(full_path):
        print(f'SKIP (not found): {template_path}')
        continue

    with open(full_path, 'r') as f:
        content = f.read()

    original = content

    # Add toggle button before sidebar
    marker = config['sidebar_marker']
    if marker in content:
        content = content.replace(marker, marker + '\n' + toggle_html)
    else:
        print(f'SKIP (marker not found): {template_path}')
        continue

    # Add CSS/JS before closing body/html
    body_end = '</body>\n</html>'
    if body_end in content:
        content = content.replace(body_end, sidebar_css_js + '\n' + body_end)
    else:
        # Try just </html>
        if '</html>' in content:
            content = content.replace('</html>', sidebar_css_js + '\n</html>')

    with open(full_path, 'w') as f:
        f.write(content)
    print(f'Updated: {template_path}')

print('Done!')