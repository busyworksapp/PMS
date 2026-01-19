# Phase 2E: Quick Testing Guide

Copy-paste ready commands for testing in browser console (F12).

---

## Dashboard KPI Testing

### Load Dashboard
```javascript
// Navigate to dashboard
window.location.href = 'http://127.0.0.1:8080/dashboard.html';
```

### Check Dashboard Manager
```javascript
// Verify dashboard manager initialized
console.log('Dashboard Manager:', window.dashboardManager);
console.log('Number of orders loaded:', window.dashboardManager.orders.length);
console.log('Auto-refresh interval:', window.dashboardManager.autoRefreshSeconds);
```

### Force Manual Refresh
```javascript
// Force immediate refresh of all KPI data
window.dashboardManager.loadDashboardKPIs();
```

### Change Auto-Refresh Frequency
```javascript
// Change from 30 seconds to 10 seconds
window.dashboardManager.autoRefreshSeconds = 10;

// Or disable auto-refresh
window.dashboardManager.stopAutoRefresh();

// Re-enable auto-refresh
window.dashboardManager.startAutoRefresh();
```

### Check Loaded Data
```javascript
// View orders loaded
console.table(window.dashboardManager.orders);

// View calculated KPIs
console.log(window.dashboardManager.calculateKPIs(
    window.dashboardManager.orders,
    [],
    [],
    {}
));
```

---

## SLA Timer Testing

### Create Timer (Normal - Green)
```javascript
// Deadline 3 hours from now
const deadline3h = new Date(Date.now() + 3 * 60 * 60 * 1000).toISOString();
const timer1 = new SLATimer('test-sla', deadline3h);

// In HTML: <div id="test-sla"></div>
```

### Create Timer (Warning - Orange)
```javascript
// Deadline 45 minutes from now (25% threshold for 3-hour SLA)
const deadline45m = new Date(Date.now() + 45 * 60 * 1000).toISOString();
const timer2 = new SLATimer('test-sla2', deadline45m);

// In HTML: <div id="test-sla2"></div>
```

### Create Timer (Critical - Red Pulse)
```javascript
// Deadline 18 minutes from now (10% threshold for 3-hour SLA)
const deadline18m = new Date(Date.now() + 18 * 60 * 1000).toISOString();
const timer3 = new SLATimer('test-sla3', deadline18m);

// In HTML: <div id="test-sla3"></div>
```

### Create Timer (Fast Expiry - Test)
```javascript
// Deadline 5 seconds from now (for testing)
const deadline5s = new Date(Date.now() + 5 * 1000).toISOString();
const timerTest = new SLATimer('test-sla-fast', deadline5s);

// Wait 6 seconds and check
setTimeout(() => {
    console.log('Timer expired:', timerTest.isExpired());
    console.log('Display shows:', document.getElementById('test-sla-fast').textContent);
}, 6000);
```

### Timer Methods Test
```javascript
const timer = new SLATimer('test-sla', 
    new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString()
);

// Get remaining time
console.log('Remaining (ms):', timer.getRemaining());
console.log('Remaining (hours):', timer.getRemaining() / (60 * 60 * 1000));

// Check if expired
console.log('Is expired:', timer.isExpired());

// Update deadline (extend SLA)
timer.updateDeadline(new Date(Date.now() + 4 * 60 * 60 * 1000).toISOString());

// Stop timer
timer.stop();
console.log('After stop - Remaining:', timer.getRemaining());

// Resume timer
timer.start();
console.log('After start - Remaining:', timer.getRemaining());

// Cleanup
timer.destroy();
```

### Custom Timer Options
```javascript
// Timer with custom thresholds and callback
const deadline = new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString();
const customTimer = new SLATimer('test-sla-custom', deadline, {
    warningThreshold: 0.30,      // Warning at 30% (instead of 25%)
    criticalThreshold: 0.15,     // Critical at 15% (instead of 10%)
    updateFrequency: 2000,        // Update every 2 seconds (instead of 1)
    onExpire: () => {
        alert('SLA Timer Expired!');
        console.log('Custom expiry callback executed');
    }
});
```

---

## Escalation Timeline Testing

### Create Test HTML Container
```html
<!-- Add to page for testing -->
<div id="timeline-test"></div>
```

### Render SOP Workflow
```javascript
const timeline = new EscalationTimeline('timeline-test');

const sopTicket = {
    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    acknowledged_at: new Date(Date.now() - 20 * 60 * 60 * 1000).toISOString(),
    review_started_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    status: 'under_review',
    review_deadline: new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString()
};

timeline.renderSOPWorkflow(sopTicket);
```

### Render Maintenance Workflow
```javascript
const timeline = new EscalationTimeline('timeline-test');

const maintenanceTask = {
    scheduled_date: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    started_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
    status: 'in_progress',
    due_date: new Date(Date.now() - 30 * 60 * 1000).toISOString() // OVERDUE
};

timeline.renderMaintenanceWorkflow(maintenanceTask);
```

### Render Order Workflow
```javascript
const timeline = new EscalationTimeline('timeline-test');

const order = {
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    scheduled_date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    started_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
    completed_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
    status: 'completed',
    due_date: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
};

timeline.renderOrderWorkflow(order);
```

### Render Custom Workflow
```javascript
const timeline = new EscalationTimeline('timeline-test');

const customStages = [
    { 
        id: 'analysis', 
        name: '🔍 Analysis', 
        description: 'Analyzing the issue',
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString()
    },
    { 
        id: 'planning', 
        name: '📋 Planning', 
        description: 'Creating action plan',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
    },
    { 
        id: 'implementation', 
        name: '⚙️ Implementation', 
        description: 'Implementing solution',
        timestamp: null
    },
    { 
        id: 'verification', 
        name: '✅ Verification', 
        description: 'Verifying solution works',
        timestamp: null
    }
];

timeline.render(customStages, 'implementation'); // Current stage: implementation
```

### Timeline Methods Test
```javascript
const timeline = new EscalationTimeline('timeline-test');

// Render initial timeline
timeline.renderSOPWorkflow(sopTicketData);

// Get current stage
console.log('Current stage:', timeline.getCurrentStage());

// Update a stage
timeline.updateStage('under_review', { 
    timestamp: new Date().toISOString() 
});

// Move to next stage
timeline.nextStage();

// Check if complete
console.log('Workflow complete:', timeline.isComplete());
```

---

## Gantt Chart Testing

### Load Job Planning
```javascript
window.location.href = 'http://127.0.0.1:8080/job-planning.html';
```

### Check Gantt Manager
```javascript
// Verify Gantt manager initialized
console.log('Gantt Manager:', window.ganttManager);
console.log('Number of orders:', window.ganttManager.orders.length);
console.log('Days shown:', window.ganttManager.daysToShow);
```

### Force Refresh Orders
```javascript
// Reload orders from API and re-render
await window.ganttManager.refresh();
console.log('Refresh complete');
```

### Zoom Controls
```javascript
const gantt = window.ganttManager;

// Zoom in (show fewer days)
gantt.zoomIn();
console.log('Zoomed in. Days shown:', gantt.daysToShow);

// Zoom out (show more days)
gantt.zoomOut();
console.log('Zoomed out. Days shown:', gantt.daysToShow);

// Zoom multiple times
gantt.zoomOut();
gantt.zoomOut();
gantt.zoomOut();
console.log('Zoomed out 3x. Days shown:', gantt.daysToShow);
```

### Filter Orders
```javascript
const gantt = window.ganttManager;

// Filter by status
gantt.filterByStatus('pending');
console.log('Showing pending orders:', gantt.orders.length);

// Reset and load all
await gantt.refresh();
```

### Highlight Order
```javascript
const gantt = window.ganttManager;

// Highlight first order
if (gantt.orders.length > 0) {
    const firstOrderId = gantt.orders[0].id;
    gantt.highlightOrder(firstOrderId);
    console.log('Highlighted order:', firstOrderId);
}

// Clear highlight
gantt.clearHighlight();
```

### Get Order Details
```javascript
const gantt = window.ganttManager;

// Get first order details
if (gantt.orders.length > 0) {
    const firstOrderId = gantt.orders[0].id;
    const order = gantt.getOrderDetails(firstOrderId);
    console.table(order);
}
```

### Manual Reschedule (Without Drag)
```javascript
const gantt = window.ganttManager;

if (gantt.orders.length > 0) {
    const order = gantt.orders[0];
    
    // New dates (move 5 days forward)
    const newStartDate = new Date(order.start_date);
    newStartDate.setDate(newStartDate.getDate() + 5);
    
    const newEndDate = new Date(order.end_date);
    newEndDate.setDate(newEndDate.getDate() + 5);
    
    // Update via API
    await gantt.updateOrderDates(order.id, newStartDate, newEndDate);
    console.log('Order rescheduled');
    
    // Re-render
    await gantt.refresh();
}
```

---

## Test Data Creation (if needed)

### Create Test Order
```javascript
// In browser console on dashboard/planning page
const api = new APIClient();

const newOrder = {
    order_number: 'TEST-' + Date.now(),
    customer_name: 'Test Customer',
    product_name: 'Test Product',
    quantity: 10,
    start_date: new Date().toISOString().split('T')[0],
    end_date: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    status: 'pending'
};

try {
    const response = await api.post('/api/orders/', newOrder);
    console.log('Order created:', response.data);
} catch (error) {
    console.error('Failed to create order:', error);
}
```

### Create Test Defect
```javascript
const api = new APIClient();

const newDefect = {
    order_id: 1,
    type: 'defect',
    description: 'Test defect for Phase 2E testing',
    severity: 'medium',
    status: 'open'
};

try {
    const response = await api.post('/api/defects/', newDefect);
    console.log('Defect created:', response.data);
} catch (error) {
    console.error('Failed to create defect:', error);
}
```

---

## Common Troubleshooting

### No Data Showing
```javascript
// Check if API is responding
const api = new APIClient();

// Test endpoints
try {
    const orders = await api.get('/api/orders/');
    console.log('Orders endpoint working:', orders.data?.length, 'orders');
} catch (error) {
    console.error('Orders endpoint failed:', error.message);
}

try {
    const maintenance = await api.get('/api/maintenance/');
    console.log('Maintenance endpoint working:', maintenance.data?.length, 'tasks');
} catch (error) {
    console.error('Maintenance endpoint failed:', error.message);
}

try {
    const defects = await api.get('/api/defects/');
    console.log('Defects endpoint working:', defects.data?.length, 'defects');
} catch (error) {
    console.error('Defects endpoint failed:', error.message);
}
```

### API URL Issue
```javascript
// Check current API URL
console.log('Current API base URL:', window.api.baseUrl);

// If wrong, change it
window.api.baseUrl = 'http://127.0.0.1:8000';
console.log('API URL updated to:', window.api.baseUrl);

// Then reload page or refresh data
window.dashboardManager.loadDashboardKPIs();
```

### Clear All Toasts
```javascript
// If toasts are stuck
if (window.toast) {
    window.toast.clear();
    console.log('All toasts cleared');
}
```

### Check JavaScript Errors
```javascript
// Open console (F12) and check for red errors
// If errors, copy them and report in bug report

// To test error handling, simulate API failure:
window.api.baseUrl = 'http://127.0.0.1:9999'; // Wrong port
window.dashboardManager.loadDashboardKPIs(); // Should show error toast
window.api.baseUrl = 'http://127.0.0.1:8000'; // Fix and try again
```

---

## Performance Monitoring

### Check API Response Times
```javascript
// Enable performance monitoring in Network tab (F12)
// Look for:
// - /api/orders/ → should be < 500ms
// - /api/maintenance/ → should be < 500ms
// - /api/defects/ → should be < 500ms

// Manual timing:
const start = performance.now();
await api.get('/api/orders/');
const end = performance.now();
console.log(`API call took ${end - start}ms`);
```

### Check Memory Usage
```javascript
// Chrome DevTools > Performance > Memory
// Look for:
// - Initial: ~2MB for dashboard
// - After 5 min: no significant increase (no memory leak)

// Or in console:
if (performance.memory) {
    console.log('Memory usage:', {
        used: (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + 'MB',
        limit: (performance.memory.jsHeapSizeLimit / 1048576).toFixed(2) + 'MB'
    });
}
```

---

## Sign-Off Commands

After testing, run these to confirm everything works:

```javascript
// Final verification
console.log('=== FINAL PHASE 2E VERIFICATION ===');
console.log('Dashboard Manager:', window.dashboardManager ? '✅' : '❌');
console.log('SLA Timer Class:', typeof SLATimer !== 'undefined' ? '✅' : '❌');
console.log('Timeline Class:', typeof EscalationTimeline !== 'undefined' ? '✅' : '❌');
console.log('Gantt Manager:', window.ganttManager ? '✅' : '❌');
console.log('Toast System:', window.toast ? '✅' : '❌');
console.log('=== ALL SYSTEMS READY ===');
```

Expected output:
```
=== FINAL PHASE 2E VERIFICATION ===
Dashboard Manager: ✅
SLA Timer Class: ✅
Timeline Class: ✅
Gantt Manager: ✅
Toast System: ✅
=== ALL SYSTEMS READY ===
```

---

**Happy Testing!** 🎉

Report any issues to your team with console logs and screenshots.
