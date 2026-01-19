# Phase 2 Implementation Guide

Complete guide for using the Phase 2 features: Dashboard KPI wiring, SLA timers, Escalation timelines, and Gantt charts.

---

## Overview

Phase 2 adds **4 major features** to the production dashboard:

1. **Dashboard KPI Wiring** - Real-time data from backend APIs
2. **SLA Countdown Timer** - Visual urgency indicators  
3. **Escalation Timeline** - Workflow status visualization
4. **Gantt Chart** - Enhanced with drag-drop rescheduling

---

## 1. Dashboard KPI Wiring

### What Changed

The dashboard now automatically:
- ✅ Fetches real-time KPI data from backend APIs
- ✅ Updates every 30 seconds (configurable)
- ✅ Shows loading spinners while fetching
- ✅ Displays error toasts if API fails
- ✅ Refreshes when user returns to tab

### Files Modified

- `dashboard.html` - Added script tag for `js/dashboard.js`
- `js/api.js` - No changes (uses existing API client)

### Files Created

- `js/dashboard.js` - DashboardManager class (300+ lines)

### Implementation

The DashboardManager automatically initializes when dashboard loads:

```javascript
// Called automatically on page load
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new DashboardManager();
    dashboard.initialize();
});
```

### What It Does

**On Page Load:**
1. Fetches orders, maintenance tasks, defects from API
2. Calculates KPIs (totals, on-time %, capacity %, etc.)
3. Updates all KPI cards in the dashboard
4. Loads recent orders table
5. Loads active issues table

**Every 30 Seconds:**
1. Auto-refreshes all KPI data
2. Updates card values with fade animation
3. Updates tables with latest data

**On Errors:**
1. Shows error toast to user
2. Continues running (doesn't crash)
3. Retries on next auto-refresh

### API Endpoints Used

```
GET /api/orders/           → List all orders
GET /api/maintenance/      → List maintenance tasks
GET /api/defects/          → List defects and issues
GET /api/dashboard/        → Dashboard summary (optional)
```

### Customizing Auto-Refresh

In `js/dashboard.js`, change:

```javascript
this.autoRefreshSeconds = 30; // Change to any number (in seconds)
```

Or disable auto-refresh:

```javascript
// In DashboardManager.initialize()
// Comment out: this.startAutoRefresh();
```

### Example: Manual Refresh

```javascript
const dashboard = window.dashboardManager; // Access global instance
dashboard.loadDashboardKPIs(); // Force refresh now
```

---

## 2. SLA Countdown Timer

### What It Does

Displays countdown timer with color changes based on urgency:

- **Green (✓)** - More than 25% time remaining
- **Orange (⚠)** - 25% or less time remaining  
- **Red (🚨)** - 10% or less time remaining
- **EXPIRED** - Deadline passed

### Files Created

- `js/sla-timer.js` - SLATimer class (180 lines)
- CSS styles in `css/global.css` (100+ lines added)

### How to Use

### Basic Usage

```html
<!-- Add timer element to your HTML -->
<div class="sla-timer">
    <div class="sla-timer-label">SLA Time Remaining:</div>
    <div class="sla-time" id="sla-countdown"></div>
</div>

<script src="js/sla-timer.js"></script>
<script>
    // Initialize timer
    const deadline = '2026-01-20T18:00:00Z'; // ISO date string
    const timer = new SLATimer('sla-countdown', deadline);
</script>
```

### Advanced Options

```javascript
// Customize thresholds and behavior
const timer = new SLATimer('sla-countdown', deadline, {
    warningThreshold: 0.25,    // Change color at 25% (default)
    criticalThreshold: 0.10,   // Change color at 10% (default)
    updateFrequency: 1000,     // Update every 1 second (default)
    onExpire: () => {
        console.log('SLA expired!');
        // Do something when deadline is reached
    }
});
```

### Timer States

```css
/* Timer colors automatically change */
.sla-time.sla-normal   { color: green; }   /* > 25% remaining */
.sla-time.sla-warning  { color: orange; }  /* 25% - 10% remaining */
.sla-time.sla-critical { color: red; animation: pulse; } /* < 10% remaining */
.sla-time.sla-expired  { color: red; font-size: 28px; } /* Time's up */
```

### Helper Function

```javascript
// Use global helper if you prefer
initSLATimer('timer-id', '2026-01-20T18:00:00Z');
```

### Methods

```javascript
// Get time remaining in milliseconds
timer.getRemaining(); // → 86400000 (1 day)

// Check if expired
timer.isExpired(); // → true/false

// Update deadline (if SLA is extended)
timer.updateDeadline('2026-01-21T18:00:00Z');

// Stop timer
timer.stop();

// Restart timer
timer.start();

// Clean up
timer.destroy();
```

### Real-World Example

```html
<div class="sla-timer">
    <div class="sla-timer-label">Maintenance SLA:</div>
    <div id="maintenance-sla"></div>
</div>

<script>
// Load maintenance task
const task = await api.get(`/api/maintenance/${taskId}`);

// Initialize timer with callback
const timer = new SLATimer('maintenance-sla', task.due_date, {
    onExpire: () => {
        toast.error('🚨 SLA Breach: Maintenance not completed in time');
        // Mark task as overdue
        api.put(`/api/maintenance/${taskId}`, { sla_breached: true });
    }
});
</script>
```

---

## 3. Escalation Timeline

### What It Does

Shows workflow progression visually with status stages:

```
🔔 Received → ✓ Acknowledged → 📋 Under Review → ⚠️ Escalated → ✅ Closed
```

### Files Created

- `js/escalation-timeline.js` - EscalationTimeline class (250+ lines)
- CSS styles in `css/global.css` (150+ lines added)

### How to Use

### Basic Usage

```html
<!-- Container for timeline -->
<div id="workflow-timeline"></div>

<script src="js/escalation-timeline.js"></script>
<script>
    // Load SOP ticket
    const sopTicket = await api.get(`/api/sop-tickets/${ticketId}`);
    
    // Render timeline
    const timeline = initEscalationTimeline('workflow-timeline', sopTicket, 'sop');
</script>
```

### Timeline Types

#### SOP-NCR Workflow
```javascript
const timeline = initEscalationTimeline('timeline-id', sopTicket, 'sop');
```

Shows stages:
1. 🔔 Received
2. ✓ Acknowledged  
3. 📋 Under Review
4. ⚠️ Escalated to HOD
5. ✅ Closed

#### Maintenance Workflow
```javascript
const timeline = initEscalationTimeline('timeline-id', maintenanceTask, 'maintenance');
```

Shows stages:
1. 📅 Scheduled
2. 🔧 In Progress
3. ✅ Completed
4. 👤 Verified

#### Order Workflow
```javascript
const timeline = initEscalationTimeline('timeline-id', order, 'order');
```

Shows stages:
1. 📝 Created
2. 📅 Scheduled
3. ⚙️ In Progress
4. ✅ Completed
5. 🚚 Delivered

### Custom Workflow

```javascript
const timeline = new EscalationTimeline('timeline-id');

const customStages = [
    { id: 'stage1', name: '1️⃣ Stage One', description: 'First step' },
    { id: 'stage2', name: '2️⃣ Stage Two', description: 'Second step' },
    { id: 'stage3', name: '3️⃣ Stage Three', description: 'Final step' }
];

timeline.render(customStages, 'stage2'); // Current stage: stage2
```

### Timeline States

```css
/* Automatically color-coded */
.sla-timeline-item.completed .sla-timeline-marker { color: green; }
.sla-timeline-item.active .sla-timeline-marker    { color: orange; animation: pulse; }
.sla-timeline-item.overdue .sla-timeline-marker    { color: red; }
```

### Methods

```javascript
// Get current stage
timeline.getCurrentStage(); // → { id: 'escalated', name: '⚠️ Escalated to HOD', ... }

// Move to next stage
timeline.nextStage();

// Update specific stage
timeline.updateStage('under_review', { timestamp: new Date().toISOString() });

// Check if workflow is complete
timeline.isComplete(); // → true/false

// Render new workflow
timeline.renderSOPWorkflow(newSopTicket);
timeline.renderMaintenanceWorkflow(newTask);
timeline.renderOrderWorkflow(newOrder);
```

### Real-World Example

```html
<h3>SOP Escalation Status</h3>
<div id="sop-timeline"></div>
<button onclick="escalateToHOD()">Escalate to HOD</button>

<script>
let timeline;

async function loadSOPStatus(ticketId) {
    const ticket = await api.get(`/api/sop-tickets/${ticketId}`);
    timeline = initEscalationTimeline('sop-timeline', ticket, 'sop');
}

async function escalateToHOD() {
    await api.put(`/api/sop-tickets/${ticketId}`, { status: 'escalated' });
    timeline.nextStage();
    toast.success('SOP escalated to Head of Department');
}
</script>
```

---

## 4. Gantt Chart with Drag-Drop

### What Changed

Job planning Gantt chart now:
- ✅ Loads real-time order data from API
- ✅ Auto-updates on page load
- ✅ Supports drag-drop to reschedule orders
- ✅ Saves changes to backend API
- ✅ Shows tooltips and order details

### Files Modified

- `job-planning.html` - Added script tag for `js/gantt-manager.js`

### Files Created

- `js/gantt-manager.js` - GanttManager class (300+ lines)

### How It Works

**On Page Load:**
1. Fetches orders with status in_progress or pending
2. Renders Gantt chart with 60-day timeline
3. Positions bars based on start/end dates
4. Enables drag-drop functionality

**When Dragging Order:**
1. Grab order bar and drag horizontally
2. Drop on new date in timeline
3. Calculates new start/end dates (preserves duration)
4. Sends update to API: `PUT /api/orders/{id}`
5. Re-renders chart with new position
6. Shows success toast

**On Error:**
1. Shows error toast
2. Reverts bar to original position
3. No changes saved to database

### API Endpoints

```
GET /api/orders/?status=in_progress,pending  → Load orders
PUT /api/orders/{id}                          → Update order dates
```

### Customizing the Gantt

```javascript
const gantt = window.ganttManager; // Access global instance

// Show more/fewer days
gantt.daysToShow = 90;      // Default: 60
gantt.renderGantt();

// Zoom in/out
gantt.zoomIn();             // Show fewer days
gantt.zoomOut();            // Show more days

// Filter orders
gantt.filterByStatus('pending');
gantt.filterByMachine(machineId);

// Refresh chart
gantt.refresh();

// Highlight specific order
gantt.highlightOrder(orderId);
gantt.clearHighlight();
```

### Methods

```javascript
// Get order details from chart
const order = gantt.getOrderDetails(orderId);

// Update order dates
await gantt.updateOrderDates(orderId, startDate, endDate);

// Scroll to today
gantt.scrollToToday();

// Get visible orders
gantt.orders.forEach(order => console.log(order));
```

### Styling

The Gantt chart uses CSS that's already included in `global.css`. Key classes:

```css
.gantt-bar         { background: #ff6b35; }
.gantt-bar:hover   { cursor: move; }
.gantt-timeline    { Border-bottom shows days }
.gantt-day.today   { Highlighted in orange }
```

### Real-World Example

```html
<div id="ganttChart"></div>

<script>
document.addEventListener('DOMContentLoaded', () => {
    const gantt = window.ganttManager;
    
    // Listen for updates
    window.addEventListener('focus', () => {
        gantt.refresh(); // Refresh when user returns to tab
    });
});

// Reschedule order button
async function rescheduleOrder(orderId, newStartDate, newEndDate) {
    try {
        await gantt.updateOrderDates(orderId, newStartDate, newEndDate);
        toast.success('Order rescheduled successfully');
    } catch (error) {
        toast.error(`Failed to reschedule: ${error.message}`);
    }
}
</script>
```

---

## Integration Checklist

- [ ] Dashboard.html loads `js/dashboard.js`
- [ ] Dashboard.html loads `js/toast.js`
- [ ] Job-planning.html loads `js/gantt-manager.js`
- [ ] Job-planning.html loads `js/toast.js`
- [ ] CSS global.css has SLA and timeline styles (160+ lines)
- [ ] SLA timer elements have `<div id="sla-time">` containers
- [ ] Timeline elements have `<div id="timeline-container">` containers
- [ ] API endpoints `/api/orders/`, `/api/maintenance/`, `/api/defects/` working
- [ ] `PUT /api/orders/{id}` endpoint working for Gantt drag-drop
- [ ] Toast system working (shows success/error messages)

---

## Testing

### Test Dashboard KPIs
1. Open dashboard.html
2. Check if KPI cards show numbers (not "0")
3. Wait 30 seconds, verify cards update
4. Check browser console for no errors
5. Unplug network, verify error toast appears

### Test SLA Timer
1. Create SLA timer with deadline 5 minutes from now
2. Verify countdown shows "00:05:00"
3. After 1 minute, verify color changes to orange
4. After 4 minutes, verify color changes to red and pulses
5. After 5 minutes, verify shows "EXPIRED"

### Test Escalation Timeline
1. Load SOP ticket with status "under_review"
2. Verify timeline shows all 5 stages
3. Verify "Under Review" stage is highlighted (active)
4. Click to move to next stage
5. Verify timeline updates visually

### Test Gantt Chart
1. Open job-planning.html
2. Verify chart loads with orders
3. Hover over bar, verify tooltip shows order number
4. Click and drag bar to new date
5. Release, verify bar moves and API is called
6. Refresh page, verify bar stays in new position

---

## Troubleshooting

### Dashboard shows "0" for all KPIs
- Check browser console for API errors
- Verify `/api/orders/` endpoint returns data
- Check network tab to see API response
- Verify API client baseUrl is correct

### SLA timer doesn't update
- Check if `js/sla-timer.js` is loaded
- Verify timer ID matches HTML element ID
- Check browser console for JavaScript errors
- Verify deadline date format is ISO (YYYY-MM-DDTHH:MM:SSZ)

### Timeline doesn't show stages
- Check if `js/escalation-timeline.js` is loaded
- Verify container element exists with correct ID
- Check that data object has required fields
- Verify timeline type is correct (sop/maintenance/order)

### Gantt chart doesn't load
- Check if `js/gantt-manager.js` is loaded
- Verify `/api/orders/` endpoint returns data
- Check browser console for errors
- Try clicking "Refresh" button (if available)

### Drag-drop doesn't work
- Verify mouse over bar shows "move" cursor
- Check browser console for errors
- Verify `PUT /api/orders/{id}` endpoint is working
- Try in Chrome/Firefox (some older browsers don't support HTML5 drag-drop)

---

## Performance Tips

1. **Reduce auto-refresh frequency** if API is slow
   ```javascript
   dashboard.autoRefreshSeconds = 60; // Every 60 seconds instead of 30
   ```

2. **Limit number of orders in Gantt**
   ```javascript
   gantt.orders = gantt.orders.slice(0, 20); // Show only first 20
   ```

3. **Disable auto-refresh on slow connections**
   ```javascript
   // In dashboard.js initialize():
   // dashboard.stopAutoRefresh();
   ```

4. **Cache API responses** if hitting rate limits
   ```javascript
   // Store last response and reuse for 30 seconds
   ```

---

## Next Steps

After Phase 2 is working:

1. **Phase 3** - End-to-end testing and QA
2. **Phase 4** - Production deployment  
3. **Phase 5** - WhatsApp integration (advanced)

See `ACTION_PLAN.md` for full timeline.
