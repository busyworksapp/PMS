# Phase 2E Testing Checklist

Quick reference checklist for testing all Phase 2 features.

**Start Date:** ___________  
**Tester:** ___________  
**Browser:** ___________  

---

## Environment Setup

- [ ] Backend API running on `http://127.0.0.1:8000`
- [ ] Frontend running on `http://127.0.0.1:8080`
- [ ] Browser DevTools open (F12)
- [ ] Network tab visible
- [ ] Console clear (no pre-existing errors)
- [ ] Test data available in backend

---

## Test Suite 1: Dashboard KPI Wiring

### Test 1.1: Dashboard Loads Successfully
- [ ] Page loads at `http://127.0.0.1:8080/dashboard.html`
- [ ] No console errors
- [ ] No red error messages
- [ ] Console shows "Dashboard initialized" or similar
- [ ] DashboardManager instance visible in console

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 1.2: KPI Cards Load Data
- [ ] KPI cards show numbers (not 0 or placeholder)
- [ ] "Total Orders" card has value
- [ ] "Capacity Utilization" shows percentage
- [ ] "Active Issues" shows number
- [ ] "Maintenance Tasks" shows number
- [ ] All API calls returned 200 OK (Network tab)
- [ ] `/api/orders/` called successfully
- [ ] `/api/maintenance/` called successfully
- [ ] `/api/defects/` called successfully

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 1.3: KPI Cards Update Every 30 Seconds
- [ ] KPI cards fade and update (visible animation)
- [ ] Cards update without page refresh
- [ ] Updates occur approximately every 30 seconds
- [ ] Values change when new data available

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 1.4: Recent Orders Table Loads
- [ ] "Recent Orders" section visible
- [ ] Table shows order data
- [ ] At least 5 rows of data visible
- [ ] Columns: Order #, Customer, Product, Status, Due Date
- [ ] Order numbers formatted correctly (#ORD-001 style)
- [ ] Status badges color-coded

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 1.5: Active Issues Table Loads
- [ ] "Active Issues & Alerts" section visible
- [ ] Table shows defect/issue data
- [ ] Type, Order, Description, Severity columns visible
- [ ] Severity badges color-coded (high=red, medium=orange, low=green)
- [ ] Timestamps show correctly

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 1.6: Error Handling - Network Disconnect
- [ ] Unplug network / disable WiFi
- [ ] Force refresh: `window.dashboardManager.loadDashboardKPIs()`
- [ ] Error toast appears (red background)
- [ ] Error message readable
- [ ] App doesn't crash
- [ ] Auto-refresh continues in background
- [ ] Data recovers when network restored

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 1.7: Error Handling - Invalid API Endpoint
- [ ] Change API URL: `window.api.baseUrl = 'http://127.0.0.1:9999'`
- [ ] Trigger refresh: `window.dashboardManager.loadDashboardKPIs()`
- [ ] Error toast appears
- [ ] App doesn't crash
- [ ] Dashboard still renders (shows old data)
- [ ] Restore URL: `window.api.baseUrl = 'http://127.0.0.1:8000'`
- [ ] Dashboard recovers after restore

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

## Test Suite 2: SLA Countdown Timer

### Test 2.1: Timer HTML Element
- [ ] Timer container exists in DOM
- [ ] CSS styles applied correctly
- [ ] Container visible and readable
- [ ] Text area ready for time display

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 2.2: Timer Initializes and Counts Down
- [ ] Create timer: `new SLATimer('element-id', deadline)`
- [ ] Timer displays in HH:MM:SS format
- [ ] Timer counts down (time decreases)
- [ ] 5 seconds pass → display decreases by ~5 seconds
- [ ] No JavaScript errors

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 2.3: Timer Color - Normal (Green)
- [ ] Deadline 3+ hours away
- [ ] Timer text is green color
- [ ] Container has green left border
- [ ] No animations or pulsing
- [ ] CSS class `sla-normal` applied

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 2.4: Timer Color - Warning (Orange)
- [ ] Deadline at 25% or less time remaining
- [ ] Timer text turns orange
- [ ] Container has orange left border
- [ ] Toast notification appears: "⚠️ SLA Deadline Approaching"
- [ ] CSS class `sla-warning` applied

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 2.5: Timer Color - Critical (Red with Pulse)
- [ ] Deadline at 10% or less time remaining
- [ ] Timer text turns red
- [ ] Timer pulses/flickers (opacity changes)
- [ ] Text size increases slightly
- [ ] Container has red left border
- [ ] Toast notification appears: "🚨 CRITICAL: SLA Deadline in Last 10%"
- [ ] CSS class `sla-critical` applied

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 2.6: Timer Expiry
- [ ] Deadline passes (5 seconds)
- [ ] Timer shows "EXPIRED"
- [ ] Text is large and red
- [ ] Toast appears: "⏰ SLA Deadline Breached"
- [ ] Timer stops (doesn't go negative)
- [ ] Timer interval clears (manual check: `timer.timerInterval === null`)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 2.7: Timer Methods
```javascript
const timer = new SLATimer('element-id', deadline);

// Get remaining
- [ ] timer.getRemaining() returns valid milliseconds

// Check expired
- [ ] timer.isExpired() returns boolean (true/false)

// Update deadline
- [ ] timer.updateDeadline(newDate) updates countdown

// Stop timer
- [ ] timer.stop() pauses countdown
- [ ] timer.getRemaining() stays same value

// Start timer
- [ ] timer.start() resumes countdown
- [ ] timer.getRemaining() decreases again

// Cleanup
- [ ] timer.destroy() removes element
- [ ] No errors after destroy
```

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

## Test Suite 3: Escalation Timeline

### Test 3.1: Timeline HTML Element
- [ ] Timeline container renders
- [ ] CSS styles applied
- [ ] Visual structure clear (vertical timeline)
- [ ] No layout issues

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 3.2: SOP Workflow Stages Render
- [ ] All 5 stages visible:
  - [ ] 🔔 Received
  - [ ] ✓ Acknowledged
  - [ ] 📋 Under Review
  - [ ] ⚠️ Escalated to HOD
  - [ ] ✅ Closed
- [ ] Stage names display
- [ ] Stage descriptions show
- [ ] Icons visible

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 3.3: Timeline Active Stage Highlighted
- [ ] Current stage is highlighted (orange/bright color)
- [ ] Previous stages show as completed (green)
- [ ] Future stages show as pending (gray)
- [ ] Current stage has visual emphasis (pulsing animation optional)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 3.4: Timeline Timestamps
- [ ] Completed stages show timestamps
- [ ] Date format: "Jan 15, 2026 10:30 AM"
- [ ] Pending stages don't show timestamp (or show "Pending")
- [ ] Times are accurate

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 3.5: Maintenance Workflow
- [ ] 4 stages render:
  - [ ] 📅 Scheduled
  - [ ] 🔧 In Progress
  - [ ] ✅ Completed
  - [ ] 👤 Verified
- [ ] Current stage highlighted
- [ ] Overdue indication shows if past deadline

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 3.6: Order Workflow
- [ ] 5 stages render:
  - [ ] 📝 Created
  - [ ] 📅 Scheduled
  - [ ] ⚙️ In Progress
  - [ ] ✅ Completed
  - [ ] 🚚 Delivered
- [ ] Current stage highlighted
- [ ] On-time/late indicator shows

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 3.7: Custom Workflow
- [ ] Custom stages render correctly
- [ ] Correct stage highlighted
- [ ] All stages have markers and labels
- [ ] Layout consistent with pre-built workflows

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

## Test Suite 4: Gantt Chart with Drag-Drop

### Test 4.1: Gantt Chart Loads
- [ ] Page loads at `http://127.0.0.1:8080/job-planning.html`
- [ ] No console errors
- [ ] Gantt chart visible
- [ ] GanttManager initialized
- [ ] Timeline header shows (60 days)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 4.2: Order Bars Display Correctly
- [ ] Order bars visible for each order
- [ ] Bar width reflects duration
- [ ] Bar position shows correct start date
- [ ] Order number displayed on bar
- [ ] Bars within 60-day window visible
- [ ] Out-of-range bars hidden

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 4.3: Hover Effects
- [ ] Mouse over bar shows "move" cursor
- [ ] Visual feedback on hover (highlight or opacity change)
- [ ] Tooltip appears (if implemented)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 4.4: Drag-Drop Reschedule
- [ ] Grab order bar with mouse
- [ ] Drag bar to new position (5+ days away)
- [ ] Release mouse
- [ ] Network tab shows `PUT /api/orders/{id}` request
- [ ] Toast shows: "Order #XXX rescheduled"
- [ ] Bar stays in new position after API response
- [ ] Duration preserved (bar width unchanged)
- [ ] Start/end dates updated correctly

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 4.5: Drag-Drop Error Handling
- [ ] Change API URL: `window.api.baseUrl = 'http://127.0.0.1:9999'`
- [ ] Try to drag-drop order
- [ ] Error toast appears
- [ ] Bar reverts to original position
- [ ] No partial updates
- [ ] App doesn't crash
- [ ] Restore API URL and verify recovery

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 4.6: Gantt Responsiveness
- [ ] Resize browser to 900px wide
- [ ] Chart adapts to smaller screen
- [ ] Bars still visible and draggable
- [ ] Timeline readable
- [ ] No unwanted scroll bars

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 4.7: Gantt Methods
```javascript
const gantt = window.ganttManager;

// Refresh
- [ ] await gantt.refresh() reloads data

// Zoom in
- [ ] gantt.zoomIn() shows fewer days

// Zoom out
- [ ] gantt.zoomOut() shows more days

// Highlight
- [ ] gantt.highlightOrder(id) adds visual emphasis

// Clear highlight
- [ ] gantt.clearHighlight() removes emphasis

// Get details
- [ ] gantt.getOrderDetails(id) returns order data
```

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

## Test Suite 5: Mobile Responsiveness

### Test 5.1: Dashboard on Mobile (480px)
- [ ] Open DevTools and toggle device toolbar
- [ ] Select 480px width
- [ ] KPI cards stack vertically
- [ ] Text is readable
- [ ] Buttons are large enough to tap
- [ ] Tables scroll horizontally
- [ ] Toasts appear in correct position

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 5.2: SLA Timer on Mobile
- [ ] Timer display is large and readable
- [ ] Container has appropriate padding
- [ ] Text size clear on small screen
- [ ] Color changes visible

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 5.3: Gantt Chart on Mobile
- [ ] Chart is scrollable
- [ ] Order bars visible
- [ ] Information readable
- [ ] Drag-drop may not work (acceptable limitation)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

## Test Suite 6: Performance & Stress Testing

### Test 6.1: Large Dataset - Dashboard (100+ Orders)
- [ ] Dashboard loads in < 3 seconds
- [ ] No freezing or lag
- [ ] Tables are scrollable
- [ ] Auto-refresh works with large dataset

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 6.2: Large Dataset - Gantt (100+ Orders)
- [ ] Gantt renders in < 2 seconds
- [ ] Drag-drop still responsive
- [ ] No significant lag

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Test 6.3: Concurrent Operations
- [ ] Dashboard auto-refreshing (30 sec)
- [ ] SLA timer counting down
- [ ] Gantt ready for drag-drop
- [ ] All features work smoothly together
- [ ] No performance degradation

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

## Test Suite 7: Cross-Browser Compatibility

### Chrome 90+ (if available)
- [ ] Suite 1: Dashboard KPI (Test 1.2 minimum)
- [ ] Suite 2: SLA Timer (Test 2.2 minimum)
- [ ] Suite 3: Timeline (Test 3.2 minimum)
- [ ] Suite 4: Gantt (Test 4.2 minimum)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Firefox 88+ (if available)
- [ ] Suite 1: Dashboard KPI (Test 1.2 minimum)
- [ ] Suite 2: SLA Timer (Test 2.2 minimum)
- [ ] Suite 3: Timeline (Test 3.2 minimum)
- [ ] Suite 4: Gantt (Test 4.2 minimum)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

### Safari 14+ (if available)
- [ ] Suite 1: Dashboard KPI (Test 1.2 minimum)
- [ ] Suite 2: SLA Timer (Test 2.2 minimum)
- [ ] Suite 3: Timeline (Test 3.2 minimum)
- [ ] Suite 4: Gantt (Test 4.2 minimum)

**Status:** ☐ PASS ☐ FAIL  
**Notes:** _______________________

---

## Summary

### Tests Passed: _____ / 45

### Critical Issues Found: _____
(List any critical bugs below)

1. ___________________________
2. ___________________________
3. ___________________________

### High Priority Issues: _____
1. ___________________________
2. ___________________________

### Medium Priority Issues: _____
1. ___________________________
2. ___________________________

### Low Priority Issues: _____
1. ___________________________
2. ___________________________

---

## Overall Status

☐ **PASS** - All tests passed, ready for Phase 3  
☐ **PASS WITH NOTES** - Mostly passed, minor issues only  
☐ **FAIL** - Critical issues found, needs fixes  
☐ **BLOCKED** - Major blocker, cannot proceed  

---

## Sign Off

**Tester Name:** ___________________________

**Date Completed:** ___________________________

**Signature:** ___________________________

**Approved by:** ___________________________

---

**Next Steps:**
- [ ] Phase 3: QA & Refinement
- [ ] Phase 4: Production Deployment
- [ ] Schedule post-deployment review
