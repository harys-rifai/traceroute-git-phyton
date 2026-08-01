filepath = 'C:/www/nslookup/templates/dashboard/unified.html'
with open(filepath, 'r') as f:
    content = f.read()

# Add toggle button to sidebar (after the scan-line div, before the flex container)
old_sidebar_start = '<div class="scan-line"></div>\n\n    <div class="flex min-h-screen">\n        <!-- Sidebar -->\n        <aside class="w-64 glass-effect sidebar-glow flex flex-col">'
new_sidebar_start = '''<div class="scan-line"></div>

    <div class="flex min-h-screen">
        <!-- Sidebar Toggle Button -->
        <button id="sidebarToggle" class="sidebar-toggle-btn" title="Toggle Sidebar">
            <svg id="sidebarToggleIcon" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>

        <!-- Sidebar -->
        <aside class="w-64 glass-effect sidebar-glow flex flex-col" id="mainSidebar">'''

content = content.replace(old_sidebar_start, new_sidebar_start)

# Add sidebar CSS and JS before closing body tag
old_body_end = '</body>\n</html>'
new_body_end = '''    <style>
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
        #mainSidebar.collapsed ~ .scan-line {
            left: 0;
        }
        .main-content-shift {
            transition: margin-left 0.3s ease;
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
            var mainContent = document.querySelector('.admin-main, main, .flex-1');
            if (!toggleBtn || !sidebar) return;

            // Check localStorage for saved state
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

                // Adjust main content margin
                if (mainContent) {
                    if (isCollapsed) {
                        mainContent.style.marginLeft = '0';
                    } else {
                        mainContent.style.marginLeft = '';
                    }
                }
            });

            // Show toggle button when sidebar is expanded
            if (!sidebar.classList.contains('collapsed')) {
                toggleBtn.classList.add('visible');
            }
        })();
    </script>
</body>
</html>'''

content = content.replace(old_body_end, new_body_end)

with open(filepath, 'w') as f:
    f.write(content)
print('unified.html sidebar auto-hide added')