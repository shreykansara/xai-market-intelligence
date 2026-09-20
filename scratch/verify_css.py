with open('web/style.css', encoding='utf-8') as f:
    css = f.read()

classes = [
    '.btn-outline-sm',
    '.btn-primary-sm',
    '.btn-auth-submit',
    '.auth-tab',
    '.btn-demo-chip',
    '.user-profile-toggle',
    '.btn-history-restore',
    '.btn-history-delete',
    '.dashboard-page-container',
    '.dashboard-hero-banner',
    '.dashboard-kpis-grid',
    '.dash-kpi-card',
    '.dashboard-main-grid',
    '.dash-workspace-col',
    '.dash-side-col',
    '.dash-card',
    '.dash-analyses-feed',
    '.dash-item-card',
    '.dash-threads-list',
    '.dash-launchpad-items'
]

missing = [c for c in classes if c not in css]
if missing:
    print('MISSING CLASSES in CSS:', missing)
    exit(1)
else:
    print(f'ALL {len(classes)} required CSS classes verified successfully in style.css!')
