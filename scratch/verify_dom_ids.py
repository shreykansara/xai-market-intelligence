with open('web/index.html', encoding='utf-8') as f:
    html = f.read()

required_ids = [
    'view-user-dashboard', 'dash-banner-avatar', 'dash-banner-name', 'dash-banner-sub',
    'dash-kpi-cvp-count', 'dash-kpi-rev-count', 'dash-kpi-chat-count', 'dash-kpi-risk-val', 'dash-kpi-risk-label',
    'dash-tab-count-all', 'dash-tab-count-cvp', 'dash-tab-count-revenue',
    'dash-search-input', 'dash-analyses-feed', 'dash-threads-list',
    'foot-link-dashboard', 'brand-logo-dash',
    'btn-dash-to-hub', 'btn-dash-new-cvp', 'btn-dash-new-revenue', 'btn-dash-new-chat',
    'btn-launch-cvp-act', 'btn-launch-rev-act'
]

missing = [i for i in required_ids if f'id="{i}"' not in html]
if missing:
    print('MISSING IDs:', missing)
    exit(1)
else:
    print(f'ALL {len(required_ids)} DOM IDs verified successfully in index.html!')
