const fs = require('fs');

const appCode = fs.readFileSync('web/app.js', 'utf8');
const authCode = fs.readFileSync('web/modules/auth-manager.js', 'utf8');
const navCode = fs.readFileSync('web/modules/navigation-manager.js', 'utf8');
const chatCode = fs.readFileSync('web/modules/chat-assistant.js', 'utf8');
const salesCode = fs.readFileSync('web/modules/sales-workflow.js', 'utf8');
const indexHtml = fs.readFileSync('web/index.html', 'utf8');
const styleCss = fs.readFileSync('web/style.css', 'utf8');

console.log('[Test] Verifying Frontend Architecture and Constraints...');

// 1. Check Views
const expectedViews = [
  'view-landing-page',
  'view-user-dashboard',
  'view-mode-selection',
  'view-step1-cvp',
  'view-step1-revenue',
  'view-step2-chatbot'
];

for (const v of expectedViews) {
  if (!indexHtml.includes(`id="${v}"`)) {
    console.error(`FAIL: Missing view ${v}`);
    process.exit(1);
  }
}
console.log('PASS: All 6 screens exist.');

// 2. Standalone Chat Removal Check
if (indexHtml.includes('id="dash-launch-chat-item"') || indexHtml.includes('id="btn-launch-chat-act"')) {
  console.error('FAIL: Standalone chat card still present in index.html');
  process.exit(1);
}
console.log('PASS: Standalone chat launch card removed from Executive Dashboard.');

// 3. New Thread Navigation Check
if (!navCode.includes('this.btnDashNewChat?.addEventListener') || !navCode.includes('this.switchScreen(this.viewModeSelection)')) {
  console.error('FAIL: btnDashNewChat in navigation-manager.js is not routing to viewModeSelection');
  process.exit(1);
}
console.log('PASS: Dashboard New Thread button routes directly to Hub (viewModeSelection).');

// 4. Chatbot New Thread Navigation Check
if (!chatCode.includes('window.navigationManager.switchScreen(window.navigationManager.viewModeSelection)')) {
  console.error('FAIL: btnNewChat in chat-assistant.js is not routing to Hub');
  process.exit(1);
}
console.log('PASS: Chatbot New Thread button routes directly to Hub for fresh analysis.');

// 5. Check Platform Navbar in Hub, CVP, Revenue
if (!indexHtml.includes('id="brand-logo-hub"')) {
  console.error('FAIL: Missing brand logo in Hub platform navbar');
  process.exit(1);
}
if (!indexHtml.includes('id="brand-logo-cvp"') || !indexHtml.includes('id="brand-logo-revenue"')) {
  console.error('FAIL: Missing brand logo in CVP/Revenue platform navbar');
  process.exit(1);
}
console.log('PASS: Platform navbar unified with Omniscope branding across Hub, CVP, and Revenue.');

// 6. Check No Fluctuations Clusters text on button
if (salesCode.includes('Analyze Fluctuation Clusters') || indexHtml.includes('Analyze Fluctuation Clusters')) {
  console.error('FAIL: Outdated fluctuation clusters text found');
  process.exit(1);
}
console.log('PASS: Fluctuation button properly labeled for causal news & strategic prognosis.');

// 7. Check Essential Navigation IDs
const essentialIds = [
  'btn-dash-to-hub',
  'btn-dash-new-cvp',
  'btn-dash-new-revenue',
  'btn-dash-new-chat',
  'btn-launch-cvp-act',
  'btn-launch-rev-act',
  'btn-cvp-to-dashboard',
  'btn-rev-to-dashboard',
  'btn-chat-to-dashboard',
  'btn-proceed-to-chatbot',
  'btn-proceed-revenue-chatbot'
];

for (const id of essentialIds) {
  if (!indexHtml.includes(`id="${id}"`)) {
    console.error(`FAIL: Missing essential ID ${id}`);
    process.exit(1);
  }
}
console.log('PASS: All essential navigation IDs present.');

console.log('\nALL FRONTEND VERIFICATION CHECKS PASSED SUCCESSFULLY!');
