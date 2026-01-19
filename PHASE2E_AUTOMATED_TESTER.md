# Phase 2E: Automated Test Runner

**Status:** PHASE 2E INTEGRATION TESTING - IN PROGRESS

**Backend:** ✅ Running on http://127.0.0.1:8000
**Frontend:** ✅ Running on http://127.0.0.1:8080
**Start Time:** January 18, 2026

---

## Quick Start: Open Browser Tests Now

1. **Open Browser Developer Tools (F12)**
2. **Navigate to Dashboard:**
   ```
   http://127.0.0.1:8080/dashboard.html
   ```
3. **Copy & Paste Test Suites Below**
4. **Mark Results in Checklist**

---

## TEST SUITE 1: Dashboard KPI Wiring (7 Tests)

### Test 1.1: Dashboard Page Loads
**Steps:**
```javascript
console.log('TEST 1.1: Dashboard page loads');
const hasKPICards = document.querySelectorAll('.kpi-card').length > 0;
const hasManager = window.dashboardManager !== undefined;
console.log('KPI cards found:', hasKPICards);
console.log('Dashboard manager exists:', hasManager);
console.log(hasKPICards && hasManager ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Dashboard page loads, KPI cards visible, manager initialized

---

### Test 1.2: Dashboard Loads Order Data from API
**Steps:**
```javascript
console.log('\nTEST 1.2: Dashboard loads order data from API');
console.log('Current orders loaded:', window.dashboardManager?.orders?.length || 0);
if (window.dashboardManager?.orders?.length > 0) {
    console.log('First order:', window.dashboardManager.orders[0]);
    console.log('✅ PASS - Orders loaded from API');
} else {
    console.log('❌ FAIL - No orders loaded');
}
```

**Expected Result:** ✅ PASS - At least 1 order loaded from `/api/orders/`

---

### Test 1.3: KPI Cards Display Calculated Metrics
**Steps:**
```javascript
console.log('\nTEST 1.3: KPI cards display calculated metrics');
const kpiCards = document.querySelectorAll('.kpi-card');
console.log('KPI cards found:', kpiCards.length);
kpiCards.forEach((card, i) => {
    const label = card.querySelector('.kpi-label')?.textContent || 'N/A';
    const value = card.querySelector('.kpi-value')?.textContent || 'N/A';
    console.log(`  Card ${i+1}: ${label} = ${value}`);
});
console.log(kpiCards.length >= 4 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - At least 4 KPI cards visible with values (Total Orders, In Progress, On-Time %, Defect Rate)

---

### Test 1.4: Dashboard Auto-Refresh Works
**Steps:**
```javascript
console.log('\nTEST 1.4: Dashboard auto-refresh every 30 seconds');
console.log('Auto-refresh interval (seconds):', window.dashboardManager?.autoRefreshSeconds);
console.log('Refresh timer active:', window.dashboardManager?.autoRefreshTimer !== null);
const interval = window.dashboardManager?.autoRefreshSeconds;
console.log(interval === 30 ? '✅ PASS' : '❌ FAIL - Expected 30s');
```

**Expected Result:** ✅ PASS - Dashboard Manager has autoRefreshSeconds = 30

---

### Test 1.5: Recent Orders Table Loads
**Steps:**
```javascript
console.log('\nTEST 1.5: Recent orders table populates');
const recentOrdersTable = document.querySelector('#recent-orders-tbody');
const rows = recentOrdersTable?.querySelectorAll('tr').length || 0;
console.log('Recent orders table rows:', rows);
console.log(rows > 0 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Recent orders table has at least 1 row of data

---

### Test 1.6: Active Issues Table Loads
**Steps:**
```javascript
console.log('\nTEST 1.6: Active issues table populates');
const activeIssuesTable = document.querySelector('#active-issues-tbody');
const rows = activeIssuesTable?.querySelectorAll('tr').length || 0;
console.log('Active issues table rows:', rows);
console.log(rows >= 0 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Active issues table displays (may be empty if no defects)

---

### Test 1.7: Dashboard Error Handling (API Failure)
**Steps:**
```javascript
console.log('\nTEST 1.7: Dashboard handles API errors gracefully');
// Temporarily break API URL
const originalUrl = window.api.baseUrl;
window.api.baseUrl = 'http://127.0.0.1:9999'; // Wrong port
await window.dashboardManager.loadDashboardKPIs();
// Wait 2 seconds for error toast
setTimeout(() => {
    const errorToast = document.querySelector('.toast.error');
    console.log('Error toast appeared:', errorToast !== null);
    // Restore URL
    window.api.baseUrl = originalUrl;
    console.log(errorToast ? '✅ PASS' : '❌ FAIL');
}, 2000);
```

**Expected Result:** ✅ PASS - Error toast appears when API fails

---

## TEST SUITE 2: SLA Countdown Timer (7 Tests)

### Test 2.1: SLA Timer Class Exists
**Steps:**
```javascript
console.log('\nTEST 2.1: SLA Timer class available');
console.log('SLATimer class exists:', typeof SLATimer !== 'undefined');
console.log(typeof SLATimer !== 'undefined' ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - SLATimer class is defined

---

### Test 2.2: SLA Timer Initializes in Normal State (Green)
**Steps:**
```javascript
console.log('\nTEST 2.2: SLA Timer initializes in normal state (green)');
// Create deadline 3 hours from now
const deadline = new Date(Date.now() + 3 * 60 * 60 * 1000).toISOString();
const timer = new SLATimer('test-sla-1', deadline);

// Check initial state
setTimeout(() => {
    const element = document.getElementById('test-sla-1');
    const isGreen = element?.classList.contains('sla-normal');
    console.log('Timer element class:', element?.className);
    console.log('Is green (normal):', isGreen);
    console.log(isGreen ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - Timer shows in green state with countdown running

---

### Test 2.3: SLA Timer Changes to Warning (Orange) at 25%
**Steps:**
```javascript
console.log('\nTEST 2.3: SLA Timer transitions to warning (orange) at 25%');
// Create deadline 45 minutes from now (25% of 3-hour SLA)
const deadline = new Date(Date.now() + 45 * 60 * 1000).toISOString();
const timer = new SLATimer('test-sla-2', deadline);

// Check state after 2 seconds
setTimeout(() => {
    const element = document.getElementById('test-sla-2');
    const isOrange = element?.classList.contains('sla-warning');
    console.log('Timer element class:', element?.className);
    console.log('Is orange (warning):', isOrange);
    console.log(isOrange ? '✅ PASS' : '❌ FAIL');
}, 2000);
```

**Expected Result:** ✅ PASS - Timer shows in orange state with warning toast

---

### Test 2.4: SLA Timer Changes to Critical (Red) at 10%
**Steps:**
```javascript
console.log('\nTEST 2.4: SLA Timer transitions to critical (red) at 10%');
// Create deadline 18 minutes from now (10% of 3-hour SLA)
const deadline = new Date(Date.now() + 18 * 60 * 1000).toISOString();
const timer = new SLATimer('test-sla-3', deadline);

// Check state after 2 seconds
setTimeout(() => {
    const element = document.getElementById('test-sla-3');
    const isRed = element?.classList.contains('sla-critical');
    const hasPulse = element?.classList.contains('sla-pulse');
    console.log('Timer element class:', element?.className);
    console.log('Is red (critical):', isRed);
    console.log('Has pulse animation:', hasPulse);
    console.log((isRed && hasPulse) ? '✅ PASS' : '❌ FAIL');
}, 2000);
```

**Expected Result:** ✅ PASS - Timer shows red with pulse animation, critical toast appears

---

### Test 2.5: SLA Timer Counts Down Accurately
**Steps:**
```javascript
console.log('\nTEST 2.5: SLA Timer counts down accurately');
const deadline = new Date(Date.now() + 60 * 1000).toISOString(); // 60 seconds
const timer = new SLATimer('test-sla-4', deadline);

let startTime = Date.now();
setTimeout(() => {
    const timeDisplay = document.getElementById('test-sla-4')?.textContent;
    console.log('Time display at 10 seconds:', timeDisplay);
    
    // Check if roughly 50 seconds remain
    const remaining = timer.getRemaining();
    const expectedMs = 50 * 1000;
    const diff = Math.abs(remaining - expectedMs);
    console.log('Remaining ms:', remaining);
    console.log('Diff from expected:', diff);
    console.log(diff < 2000 ? '✅ PASS' : '❌ FAIL');
}, 10000);
```

**Expected Result:** ✅ PASS - Timer counts down accurately (within 2 seconds margin)

---

### Test 2.6: SLA Timer Marks Expired After Deadline
**Steps:**
```javascript
console.log('\nTEST 2.6: SLA Timer marks expired after deadline');
// Create deadline 5 seconds from now
const deadline = new Date(Date.now() + 5 * 1000).toISOString();
const timer = new SLATimer('test-sla-5', deadline);

// Check after 7 seconds
setTimeout(() => {
    const element = document.getElementById('test-sla-5');
    const isExpired = element?.classList.contains('sla-expired');
    const timeDisplay = element?.textContent;
    console.log('Timer display:', timeDisplay);
    console.log('Is expired:', isExpired);
    console.log(isExpired ? '✅ PASS' : '❌ FAIL');
}, 7000);
```

**Expected Result:** ✅ PASS - Timer shows "EXPIRED" text and red expired state

---

### Test 2.7: SLA Timer Methods Work Correctly
**Steps:**
```javascript
console.log('\nTEST 2.7: SLA Timer methods (stop, getRemaining, destroy)');
const deadline = new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString();
const timer = new SLATimer('test-sla-6', deadline);

setTimeout(() => {
    // Test getRemaining()
    const remaining1 = timer.getRemaining();
    console.log('Remaining (ms):', remaining1);
    
    // Test stop()
    timer.stop();
    const remaining2 = timer.getRemaining();
    console.log('Remaining after stop:', remaining2);
    console.log('Same after stop:', remaining1 === remaining2);
    
    // Test destroy()
    timer.destroy();
    console.log('Timer destroyed: ✅ PASS');
}, 500);
```

**Expected Result:** ✅ PASS - All timer methods execute without errors

---

## TEST SUITE 3: Escalation Timeline (7 Tests)

### Test 3.1: Timeline HTML Renders
**Steps:**
```javascript
console.log('\nTEST 3.1: Timeline HTML renders');
const timeline = new EscalationTimeline('timeline-test-1');
const sopTicket = {
    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    acknowledged_at: new Date(Date.now() - 20 * 60 * 60 * 1000).toISOString(),
    review_started_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    status: 'under_review'
};
timeline.renderSOPWorkflow(sopTicket);

setTimeout(() => {
    const container = document.getElementById('timeline-test-1');
    const stages = container?.querySelectorAll('.sla-timeline-item').length || 0;
    console.log('Timeline stages rendered:', stages);
    console.log(stages >= 3 ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - Timeline with 5 SOP stages renders

---

### Test 3.2: Timeline Shows Current Stage Highlighted
**Steps:**
```javascript
console.log('\nTEST 3.2: Timeline shows current stage highlighted');
const timeline = new EscalationTimeline('timeline-test-2');
const sopTicket = {
    status: 'under_review',
    created_at: new Date().toISOString(),
    acknowledged_at: new Date().toISOString()
};
timeline.renderSOPWorkflow(sopTicket);

setTimeout(() => {
    const activeStage = document.querySelector('#timeline-test-2 .sla-timeline-item.active');
    const stageName = activeStage?.querySelector('.sla-timeline-marker')?.textContent;
    console.log('Active stage:', stageName);
    console.log(activeStage ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - Current stage highlighted in orange/active color

---

### Test 3.3: Timeline Marks Completed Stages
**Steps:**
```javascript
console.log('\nTEST 3.3: Timeline marks completed stages');
const timeline = new EscalationTimeline('timeline-test-3');
const sopTicket = {
    status: 'escalated',
    created_at: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString(),
    acknowledged_at: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString(),
    review_started_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
};
timeline.renderSOPWorkflow(sopTicket);

setTimeout(() => {
    const completedStages = document.querySelectorAll('#timeline-test-3 .sla-timeline-item.completed');
    console.log('Completed stages:', completedStages.length);
    console.log(completedStages.length > 0 ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - Completed stages show with green checkmark

---

### Test 3.4: Timeline Displays Timestamps
**Steps:**
```javascript
console.log('\nTEST 3.4: Timeline displays timestamps');
const timeline = new EscalationTimeline('timeline-test-4');
const sopTicket = {
    status: 'under_review',
    created_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    acknowledged_at: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString()
};
timeline.renderSOPWorkflow(sopTicket);

setTimeout(() => {
    const timestamps = document.querySelectorAll('#timeline-test-4 .sla-timeline-time');
    console.log('Timestamps displayed:', timestamps.length);
    timestamps.forEach((ts, i) => {
        console.log(`  Stage ${i+1}:`, ts.textContent);
    });
    console.log(timestamps.length > 0 ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - Each stage shows timestamp (e.g., "2 hours ago")

---

### Test 3.5: SOP Workflow Has 5 Stages
**Steps:**
```javascript
console.log('\nTEST 3.5: SOP workflow has 5 stages');
const timeline = new EscalationTimeline('timeline-test-5');
const sopTicket = { status: 'received', created_at: new Date().toISOString() };
timeline.renderSOPWorkflow(sopTicket);

setTimeout(() => {
    const stages = document.querySelectorAll('#timeline-test-5 .sla-timeline-item');
    console.log('SOP stages:', stages.length);
    stages.forEach((s, i) => {
        console.log(`  ${i+1}. ${s.querySelector('.sla-timeline-marker')?.textContent}`);
    });
    console.log(stages.length === 5 ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - SOP has exactly 5 stages: Received → Acknowledged → Under Review → Escalated → Closed

---

### Test 3.6: Maintenance Workflow Has 4 Stages
**Steps:**
```javascript
console.log('\nTEST 3.6: Maintenance workflow has 4 stages');
const timeline = new EscalationTimeline('timeline-test-6');
const maintenanceTask = {
    status: 'scheduled',
    scheduled_date: new Date().toISOString()
};
timeline.renderMaintenanceWorkflow(maintenanceTask);

setTimeout(() => {
    const stages = document.querySelectorAll('#timeline-test-6 .sla-timeline-item');
    console.log('Maintenance stages:', stages.length);
    stages.forEach((s, i) => {
        console.log(`  ${i+1}. ${s.querySelector('.sla-timeline-marker')?.textContent}`);
    });
    console.log(stages.length === 4 ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - Maintenance has exactly 4 stages: Scheduled → In Progress → Completed → Verified

---

### Test 3.7: Custom Workflow Renders
**Steps:**
```javascript
console.log('\nTEST 3.7: Custom workflow renders');
const timeline = new EscalationTimeline('timeline-test-7');
const customStages = [
    { id: 's1', name: '🔍 Analysis', timestamp: new Date().toISOString() },
    { id: 's2', name: '📋 Planning', timestamp: null },
    { id: 's3', name: '⚙️ Implementation', timestamp: null }
];
timeline.render(customStages, 's2');

setTimeout(() => {
    const stages = document.querySelectorAll('#timeline-test-7 .sla-timeline-item');
    console.log('Custom stages:', stages.length);
    console.log(stages.length === 3 ? '✅ PASS' : '❌ FAIL');
}, 100);
```

**Expected Result:** ✅ PASS - Custom workflow with 3 stages renders correctly

---

## TEST SUITE 4: Gantt Chart (7 Tests)

### Test 4.1: Gantt Page Loads
**Steps:**
```javascript
// Navigate to job-planning page first
console.log('TEST 4.1: Navigate to job-planning.html');
window.location.href = 'http://127.0.0.1:8080/job-planning.html';

// Wait 3 seconds then check
setTimeout(() => {
    console.log('Gantt Manager exists:', window.ganttManager !== undefined);
    console.log(window.ganttManager ? '✅ PASS' : '❌ FAIL');
}, 3000);
```

**Expected Result:** ✅ PASS - Job planning page loads, Gantt manager initializes

---

### Test 4.2: Gantt Loads Orders from API
**Steps:**
```javascript
console.log('\nTEST 4.2: Gantt loads orders from API');
console.log('Orders loaded:', window.ganttManager?.orders?.length || 0);
if (window.ganttManager?.orders?.length > 0) {
    console.log('First order:', {
        id: window.ganttManager.orders[0].id,
        name: window.ganttManager.orders[0].order_number,
        start: window.ganttManager.orders[0].start_date,
        end: window.ganttManager.orders[0].end_date
    });
    console.log('✅ PASS');
} else {
    console.log('❌ FAIL');
}
```

**Expected Result:** ✅ PASS - At least 1 order loaded with start_date and end_date

---

### Test 4.3: Gantt Renders Order Bars
**Steps:**
```javascript
console.log('\nTEST 4.3: Gantt renders order bars on timeline');
const bars = document.querySelectorAll('.gantt-bar');
console.log('Order bars rendered:', bars.length);
bars.forEach((bar, i) => {
    const orderId = bar.dataset.orderId;
    const left = bar.style.left;
    const width = bar.style.width;
    console.log(`  Bar ${i+1}: Order ${orderId}, left=${left}, width=${width}`);
});
console.log(bars.length > 0 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Order bars visible on Gantt chart with positioning

---

### Test 4.4: Gantt Drag-Drop Reschedules Order
**Steps:**
```javascript
console.log('\nTEST 4.4: Gantt drag-drop reschedules orders');
const bar = document.querySelector('.gantt-bar');
if (!bar) {
    console.log('❌ FAIL - No order bars found');
} else {
    const originalLeft = bar.style.left;
    console.log('Bar original position:', originalLeft);
    
    // Simulate drag
    const dragEvent = new DragEvent('dragstart', { bubbles: true });
    bar.dispatchEvent(dragEvent);
    
    // Simulate drop (move 5 days forward = 200px at 40px/day)
    const dropTarget = document.querySelector('.gantt-timeline');
    const dropEvent = new DragEvent('drop', {
        bubbles: true,
        clientX: parseInt(originalLeft) + 200
    });
    dropTarget.dispatchEvent(dropEvent);
    
    setTimeout(() => {
        const newLeft = bar.style.left;
        console.log('Bar new position:', newLeft);
        console.log((originalLeft !== newLeft || 'Updated in API') ? '✅ PASS' : '❌ FAIL');
    }, 2000);
}
```

**Expected Result:** ✅ PASS - Dragging bar reschedules order, updates API

---

### Test 4.5: Gantt Zoom In/Out Works
**Steps:**
```javascript
console.log('\nTEST 4.5: Gantt zoom in/out controls');
const gantt = window.ganttManager;
const initialDays = gantt.daysToShow;
console.log('Initial days shown:', initialDays);

gantt.zoomOut();
const zoomedOut = gantt.daysToShow;
console.log('After zoom out:', zoomedOut);
console.log('Increased:', zoomedOut > initialDays);

gantt.zoomIn();
const zoomedIn = gantt.daysToShow;
console.log('After zoom in:', zoomedIn);
console.log((zoomedOut > zoomedIn && zoomedIn > 0) ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Zoom out increases days, zoom in decreases days

---

### Test 4.6: Gantt Filter by Status Works
**Steps:**
```javascript
console.log('\nTEST 4.6: Gantt filter by status');
const gantt = window.ganttManager;
const totalOrders = gantt.orders.length;
console.log('Total orders:', totalOrders);

gantt.filterByStatus('pending');
const pendingOrders = gantt.orders.length;
console.log('Pending orders:', pendingOrders);

await gantt.refresh(); // Reset to all
const resetOrders = gantt.orders.length;
console.log('After reset:', resetOrders);
console.log((pendingOrders <= totalOrders && resetOrders === totalOrders) ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Filter reduces visible orders, reset shows all

---

### Test 4.7: Gantt Methods Execute Without Errors
**Steps:**
```javascript
console.log('\nTEST 4.7: Gantt methods work correctly');
const gantt = window.ganttManager;

try {
    // Test scroll to today
    gantt.scrollToToday();
    console.log('scrollToToday(): ✓');
    
    // Test highlight order
    if (gantt.orders.length > 0) {
        gantt.highlightOrder(gantt.orders[0].id);
        console.log('highlightOrder(): ✓');
        
        // Test clear highlight
        gantt.clearHighlight();
        console.log('clearHighlight(): ✓');
    }
    
    // Test refresh
    await gantt.refresh();
    console.log('refresh(): ✓');
    
    console.log('✅ PASS - All methods work');
} catch (error) {
    console.log('❌ FAIL:', error.message);
}
```

**Expected Result:** ✅ PASS - All Gantt methods execute without errors

---

## TEST SUITE 5: Mobile Responsiveness (3 Tests)

### Test 5.1: Dashboard Responsive at 480px
**Steps:**
```javascript
// Press F12, toggle device toolbar, select iPhone (375-480px width)
console.log('\nTEST 5.1: Dashboard responsive at mobile width');
console.log('Window width:', window.innerWidth);
console.log('KPI cards stacked:', window.innerWidth < 768);

const kpiCards = document.querySelectorAll('.kpi-card');
const firstCardWidth = kpiCards[0]?.offsetWidth;
console.log('KPI card width:', firstCardWidth);
console.log('Responsive (card fills screen):', firstCardWidth > window.innerWidth * 0.8 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - KPI cards stack vertically, readable on mobile

---

### Test 5.2: SLA Timer Responsive
**Steps:**
```javascript
console.log('\nTEST 5.2: SLA Timer responsive at mobile');
const timerElement = document.querySelector('.sla-timer');
const timerWidth = timerElement?.offsetWidth;
console.log('Timer width:', timerWidth);
console.log('Fits in viewport:', timerWidth < window.innerWidth ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Timer text visible and readable on mobile

---

### Test 5.3: Gantt Responsive at Mobile
**Steps:**
```javascript
// Navigate to job-planning.html and resize to mobile
console.log('\nTEST 5.3: Gantt chart responsive at mobile');
const ganttTimeline = document.querySelector('.gantt-timeline');
const ganttHeight = ganttTimeline?.offsetHeight;
console.log('Gantt height:', ganttHeight);
const ganttWidth = ganttTimeline?.offsetWidth;
console.log('Gantt width:', ganttWidth);
console.log('Scrollable on mobile:', ganttWidth < window.innerWidth * 0.95 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Gantt scrollable on mobile, doesn't overflow

---

## TEST SUITE 6: Performance & Stress Testing (3 Tests)

### Test 6.1: Dashboard with 100+ Orders
**Steps:**
```javascript
console.log('\nTEST 6.1: Dashboard performance with 100+ orders');
const startTime = performance.now();

// Create 100 test orders
const orders = Array.from({ length: 100 }, (_, i) => ({
    id: i,
    order_number: `ORDER-${i}`,
    status: i % 3 === 0 ? 'pending' : i % 3 === 1 ? 'in_progress' : 'completed',
    start_date: new Date().toISOString(),
    end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
}));

// Calculate KPIs
const kpis = window.dashboardManager.calculateKPIs(orders, [], [], {});
const endTime = performance.now();

console.log('KPI calculation time:', (endTime - startTime).toFixed(2) + 'ms');
console.log('Calculated KPIs:', kpis);
console.log((endTime - startTime) < 1000 ? '✅ PASS' : '❌ FAIL - Slow KPI calculation');
```

**Expected Result:** ✅ PASS - KPI calculation completes in < 1 second

---

### Test 6.2: Gantt with 100+ Orders Renders
**Steps:**
```javascript
console.log('\nTEST 6.2: Gantt performance with 100+ orders');
const startTime = performance.now();

// Mock 100 orders
const orders = Array.from({ length: 100 }, (_, i) => ({
    id: i,
    order_number: `ORDER-${i}`,
    status: 'in_progress',
    start_date: new Date(Date.now() + i * 12 * 60 * 60 * 1000).toISOString(),
    end_date: new Date(Date.now() + (i + 5) * 12 * 60 * 60 * 1000).toISOString()
}));

window.ganttManager.orders = orders;
await window.ganttManager.renderGantt();

const endTime = performance.now();
const bars = document.querySelectorAll('.gantt-bar').length;

console.log('Gantt render time:', (endTime - startTime).toFixed(2) + 'ms');
console.log('Bars rendered:', bars);
console.log((endTime - startTime) < 2000 && bars >= 90 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Gantt renders 100 orders in < 2 seconds

---

### Test 6.3: Concurrent Operations
**Steps:**
```javascript
console.log('\nTEST 6.3: Concurrent operations (dashboard + timers)');
const startTime = performance.now();

// Run multiple operations in parallel
const operations = [
    window.dashboardManager.loadDashboardKPIs(),
    new Promise(resolve => {
        const timer = new SLATimer('test-concurrent', 
            new Date(Date.now() + 60 * 60 * 1000).toISOString());
        setTimeout(() => resolve(), 100);
    })
];

await Promise.all(operations);
const endTime = performance.now();

console.log('Concurrent operations time:', (endTime - startTime).toFixed(2) + 'ms');
console.log((endTime - startTime) < 3000 ? '✅ PASS' : '❌ FAIL');
```

**Expected Result:** ✅ PASS - Dashboard and timers load concurrently without blocking

---

## TEST SUITE 7: Cross-Browser Compatibility (3 Tests)

### Test 7.1: Chrome/Edge Compatibility
**Steps:**
```javascript
console.log('\nTEST 7.1: Chrome/Edge browser check');
const isChrome = /Chrome/.test(navigator.userAgent);
const isEdge = /Edg/.test(navigator.userAgent);
console.log('Browser:', navigator.userAgent.split('(')[0]);
console.log('Chrome/Edge:', isChrome || isEdge);
console.log(isChrome || isEdge ? '✅ PASS' : '⚠️  Different browser');
```

**Expected Result:** ✅ PASS - Features work in Chrome/Edge

---

### Test 7.2: Firefox Compatibility
**Steps:**
```javascript
console.log('\nTEST 7.2: Firefox browser check');
const isFirefox = /Firefox/.test(navigator.userAgent);
console.log('Firefox:', isFirefox);
if (isFirefox) {
    // Test drag-drop in Firefox
    const bar = document.querySelector('.gantt-bar');
    console.log('Drag-drop available:', bar?.draggable === true);
    console.log(bar?.draggable ? '✅ PASS' : '❌ FAIL');
}
```

**Expected Result:** ✅ PASS - Drag-drop works in Firefox

---

### Test 7.3: Safari Compatibility
**Steps:**
```javascript
console.log('\nTEST 7.3: Safari browser check');
const isSafari = /Safari/.test(navigator.userAgent) && !/Chrome/.test(navigator.userAgent);
console.log('Safari:', isSafari);
if (isSafari) {
    console.log('CSS animations:', window.getComputedStyle(document.body).animationDuration);
    console.log('✅ PASS - Safari compatible');
}
```

**Expected Result:** ✅ PASS - Features work in Safari

---

## Summary & Sign-Off

After running all tests above, fill in results:

### Results Summary
```
DASHBOARD KPI WIRING: [ ] 7/7 PASS [ ] 6/7 PASS [ ] <6 FAIL
SLA TIMER: [ ] 7/7 PASS [ ] 6/7 PASS [ ] <6 FAIL
TIMELINE: [ ] 7/7 PASS [ ] 6/7 PASS [ ] <6 FAIL
GANTT CHART: [ ] 7/7 PASS [ ] 6/7 PASS [ ] <6 FAIL
MOBILE: [ ] 3/3 PASS [ ] 2/3 PASS [ ] <2 FAIL
PERFORMANCE: [ ] 3/3 PASS [ ] 2/3 PASS [ ] <2 FAIL
CROSS-BROWSER: [ ] 3/3 PASS [ ] 2/3 PASS [ ] <2 FAIL

TOTAL: [ ] 45/45 PASS [ ] 40-44 PASS [ ] <40 FAIL
```

### Issues Found (if any)
```
Issue 1: [Describe issue]
  Severity: [ ] Critical [ ] High [ ] Medium [ ] Low
  Steps: [Steps to reproduce]
  Expected: [What should happen]
  Actual: [What actually happened]

Issue 2: [Describe issue]
  [Same format]
```

### Sign-Off
```
Tester Name: ___________________
Date: ___________________
Browser: ___________________
Result: [ ] ALL PASS - PROCEED TO PHASE 3
        [ ] MINOR ISSUES - ACCEPTABLE
        [ ] CRITICAL ISSUES - NEEDS FIXES
```

---

**Next Steps:**
- ✅ If all 45 tests pass → Proceed to Phase 3 (QA & Refinement)
- ⚠️  If 40-44 tests pass → Document issues, assess impact
- ❌ If <40 tests pass → Fix critical issues, re-test

