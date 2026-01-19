# Phase 2E: Integration Testing Plan

**Date:** January 18, 2026  
**Status:** In Progress  
**Objective:** Verify all Phase 2 features work correctly in production environment

---

## Test Environment Setup

### Prerequisites
- [ ] Backend API running on `http://127.0.0.1:8000`
- [ ] Frontend running on `http://127.0.0.1:8080`
- [ ] Browser DevTools open (F12) to check console for errors
- [ ] Network tab open to monitor API calls
- [ ] Test data exists in backend (orders, maintenance tasks, defects)

### Quick Start Backend
```powershell
cd "app/backend"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Quick Start Frontend
```powershell
cd "app/frontend"
python -m http.server 8080
```

---

## Test Suite 1: Dashboard KPI Wiring

### Test 1.1: Dashboard Loads Successfully
**Steps:**
1. Navigate to `http://127.0.0.1:8080/dashboard.html`
2. Wait for page to load (should show loading spinner briefly)
3. Check browser console (F12) for errors

**Expected Results:**
- ✅ Page loads without errors
- ✅ Console shows "Dashboard initialized"
- ✅ No red error messages in console
- ✅ Dashboard Manager class initializes

**Notes:**
```javascript
// In browser console, verify:
console.log(window.dashboardManager); // Should show DashboardManager instance
```

---

### Test 1.2: KPI Cards Load Data
**Steps:**
1. Open dashboard (should see loading spinner in cards)
2. Wait 3-5 seconds for API calls to complete
3. Check that KPI cards show numbers (not "0" or placeholder text)
4. Verify in Network tab that `/api/orders/`, `/api/maintenance/`, `/api/defects/` were called

**Expected Results:**
- ✅ "Total Orders" card shows a number > 0
- ✅ "Capacity Utilization" shows a percentage
- ✅ "Active Issues" shows a number
- ✅ "Maintenance Tasks" shows a number
- ✅ All API calls returned 200 OK

**If Fails:**
- Check backend is running (`http://127.0.0.1:8000/docs`)
- Check API endpoints exist: `/api/orders/`, `/api/maintenance/`, `/api/defects/`
- Check browser console for specific error messages

**Example Log Output:**
```
Dashboard KPIs updated successfully: {
    totalOrders: 15,
    onTimePercent: 87,
    capacityPercent: 78,
    totalActiveIssues: 3,
    ...
}
```

---

### Test 1.3: KPI Cards Update Every 30 Seconds
**Steps:**
1. Note the current values on KPI cards (e.g., "Total Orders: 15")
2. In backend, create a new order: `POST /api/orders/` with test data
3. Wait 30 seconds for dashboard to auto-refresh
4. Verify "Total Orders" increased to 16

**Expected Results:**
- ✅ KPI cards fade out and fade back in after 30 seconds
- ✅ Cards show updated numbers after each refresh
- ✅ No manual page refresh needed

**Manual Test Alternative:**
```javascript
// In browser console, force refresh:
window.dashboardManager.loadDashboardKPIs();
```

**Notes:**
- Refresh frequency is 30 seconds by default
- To change: `window.dashboardManager.autoRefreshSeconds = 15;` (in seconds)

---

### Test 1.4: Recent Orders Table Loads
**Steps:**
1. Dashboard should show "Recent Orders" section
2. Wait for table to load
3. Verify table shows order data (Order #, Customer, Product, Status, Due Date)
4. Check at least 5 rows of data

**Expected Results:**
- ✅ Table shows 10 most recent orders
- ✅ All columns populated with real data
- ✅ Order numbers start with "#" (e.g., "#ORD-001")
- ✅ Status badges show colors (completed=green, pending=orange, etc.)

**If No Data:**
- Check `/api/orders/` endpoint returns data
- Verify orders have `created_at` field (for sorting)

---

### Test 1.5: Active Issues Table Loads
**Steps:**
1. Dashboard should show "Active Issues & Alerts" section
2. Wait for table to load
3. Verify table shows defects/SOP violations (Type, Order, Description, Severity)

**Expected Results:**
- ✅ Shows defects and SOP violations
- ✅ Severity badges color-coded (high=red, medium=orange, low=green)
- ✅ Timestamps show issue creation date

**If No Issues:**
- Dashboard might actually be working fine (no issues!)
- Verify by creating test defect in backend

---

### Test 1.6: Error Handling - Network Disconnect
**Steps:**
1. Dashboard should be loading data
2. Unplug network cable or disable WiFi
3. Wait for next API call to fail (or trigger manually: `window.dashboardManager.loadDashboardKPIs()`)
4. Check for error toast

**Expected Results:**
- ✅ Error toast appears (red background)
- ✅ Message: "Failed to load KPIs: [error message]"
- ✅ Dashboard doesn't crash
- ✅ Auto-refresh continues trying in background

**Restore Network:**
- Plug network back in
- Wait 30 seconds for auto-refresh
- Dashboard should recover and show data again

---

### Test 1.7: Error Handling - Invalid API Endpoint
**Steps:**
1. In browser console, modify API endpoint:
   ```javascript
   window.api.baseUrl = 'http://127.0.0.1:9999'; // Wrong port
   ```
2. Trigger refresh: `window.dashboardManager.loadDashboardKPIs();`
3. Check for error toast

**Expected Results:**
- ✅ Error toast appears
- ✅ App doesn't crash
- ✅ Dashboard still renders (shows old data or empty state)

---

## Test Suite 2: SLA Countdown Timer

### Test 2.1: Timer HTML Element Exists
**Steps:**
1. Open a page that should have SLA timer (e.g., maintenance detail page, or add test element to dashboard)
2. Create test HTML:
   ```html
   <div class="sla-timer">
       <div class="sla-timer-label">SLA Deadline:</div>
       <div class="sla-time" id="test-sla"></div>
   </div>
   ```

**Expected Results:**
- ✅ HTML renders correctly
- ✅ Container shows with styling
- ✅ Time display area is visible

---

### Test 2.2: Timer Initializes and Counts Down
**Steps:**
1. In browser console:
   ```javascript
   // Create deadline 2 hours from now
   const deadline = new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString();
   const timer = new SLATimer('test-sla', deadline);
   ```
2. Observe timer display
3. Wait 5 seconds
4. Verify time decreased by 5 seconds

**Expected Results:**
- ✅ Timer shows "02:00:00" (or close to 2 hours)
- ✅ Countdown is visible (HH:MM:SS format)
- ✅ Time decreases every second
- ✅ No JavaScript errors in console

---

### Test 2.3: Timer Color - Normal (Green)
**Steps:**
1. Create timer with deadline 3 hours from now
2. Wait 1 second for initialization
3. Check color of timer display

**Expected Results:**
- ✅ Timer text is green color (CSS class `sla-normal`)
- ✅ Container has green left border
- ✅ No animations or pulsing

---

### Test 2.4: Timer Color - Warning (Orange)
**Steps:**
1. Create timer with deadline 45 minutes from now
   ```javascript
   const deadline = new Date(Date.now() + 45 * 60 * 1000).toISOString();
   const timer = new SLATimer('test-sla', deadline);
   ```
2. Wait for timer to update
3. Check color

**Expected Results:**
- ✅ Timer text turns orange (CSS class `sla-warning`)
- ✅ Toast notification appears: "⚠️ SLA Deadline Approaching (25% time remaining)"
- ✅ Container has orange left border

**Note:** Warning threshold is 25% of total time. For 3-hour SLA, warning at 45 minutes remaining.

---

### Test 2.5: Timer Color - Critical (Red with Pulse)
**Steps:**
1. Create timer with deadline 18 minutes from now
   ```javascript
   const deadline = new Date(Date.now() + 18 * 60 * 1000).toISOString();
   const timer = new SLATimer('test-sla', deadline);
   ```
2. Wait for timer to update
3. Check color and animation

**Expected Results:**
- ✅ Timer text turns red (CSS class `sla-critical`)
- ✅ Timer pulses (opacity changes every 0.5 seconds)
- ✅ Toast appears: "🚨 CRITICAL: SLA Deadline in Last 10%"
- ✅ Container has red left border
- ✅ Text size increases slightly

---

### Test 2.6: Timer Expiry
**Steps:**
1. Create timer with deadline 5 seconds from now
   ```javascript
   const deadline = new Date(Date.now() + 5 * 1000).toISOString();
   const timer = new SLATimer('test-sla', deadline);
   ```
2. Wait 6 seconds
3. Check display

**Expected Results:**
- ✅ Timer shows "EXPIRED"
- ✅ Text is red and large
- ✅ Toast appears: "⏰ SLA Deadline Breached"
- ✅ Timer stops counting (doesn't go negative)
- ✅ Timer interval clears (no CPU waste)

---

### Test 2.7: Timer Methods
**Steps:**
In browser console, test these methods:
```javascript
// Get remaining time
timer.getRemaining(); // Should return milliseconds

// Check if expired
timer.isExpired(); // true/false

// Update deadline (SLA extension)
timer.updateDeadline(new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString());

// Stop timer
timer.stop();

// Restart timer
timer.start();

// Get remaining
timer.getRemaining(); // Should still count down

// Cleanup
timer.destroy();
```

**Expected Results:**
- ✅ All methods work without errors
- ✅ Timer updates when deadline changed
- ✅ Timer pauses when stopped
- ✅ Timer resumes after restart
- ✅ No memory leaks after destroy

---

## Test Suite 3: Escalation Timeline

### Test 3.1: Timeline HTML Element Exists
**Steps:**
1. Add test HTML to a page:
   ```html
   <div id="timeline-test"></div>
   ```
2. In browser console, render timeline:
   ```javascript
   const timeline = new EscalationTimeline('timeline-test');
   const sopData = {
       created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
       status: 'under_review',
       review_deadline: new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString() // 6 hours
   };
   timeline.renderSOPWorkflow(sopData);
   ```

**Expected Results:**
- ✅ Timeline renders with 5 stages
- ✅ No JavaScript errors
- ✅ Timeline container populated with HTML

---

### Test 3.2: SOP Workflow Stages Render
**Steps:**
1. Render SOP timeline (see Test 3.1)
2. Inspect rendered HTML
3. Verify all 5 stages visible

**Expected Results:**
- ✅ 5 stages visible: Received → Acknowledged → Under Review → Escalated → Closed
- ✅ Icons show for each stage (🔔, ✓, 📋, ⚠️, ✅)
- ✅ Stage names display correctly
- ✅ Descriptions show under each stage

---

### Test 3.3: Timeline Active Stage Highlighted
**Steps:**
1. Render timeline with status 'under_review'
2. Check styling of stages

**Expected Results:**
- ✅ "Under Review" stage is highlighted (orange color)
- ✅ Previous stages (Received, Acknowledged) show as completed (green)
- ✅ Future stages (Escalated, Closed) show as pending (gray)
- ✅ Orange stage has pulsing animation

---

### Test 3.4: Timeline Stage Timestamps
**Steps:**
1. Render timeline with timestamps
2. Verify dates display

**Expected Results:**
- ✅ Each completed stage shows timestamp (creation/completion date)
- ✅ Dates formatted as "Jan 15, 2026 10:30 AM"
- ✅ Current/future stages don't show timestamp (or show "Pending")

---

### Test 3.5: Maintenance Workflow
**Steps:**
```javascript
const timeline = new EscalationTimeline('timeline-test');
const maintenanceData = {
    scheduled_date: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
    status: 'in_progress',
    started_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(), // 1 hour ago
    due_date: new Date(Date.now() - 30 * 60 * 1000).toISOString() // 30 min ago (OVERDUE)
};
timeline.renderMaintenanceWorkflow(maintenanceData);
```

**Expected Results:**
- ✅ 4 stages render: Scheduled → In Progress → Completed → Verified
- ✅ "In Progress" is active (orange)
- ✅ Overdue indicator shows (red) because `due_date` passed

---

### Test 3.6: Order Workflow
**Steps:**
```javascript
const timeline = new EscalationTimeline('timeline-test');
const orderData = {
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
    status: 'completed',
    completed_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(), // 12 hours ago
    due_date: new Date(Date.now() - 18 * 60 * 60 * 1000).toISOString() // 18 hours ago
};
timeline.renderOrderWorkflow(orderData);
```

**Expected Results:**
- ✅ 5 stages render: Created → Scheduled → In Progress → Completed → Delivered
- ✅ "Completed" stage is active
- ✅ All previous stages show as completed (green)
- ✅ Shows on-time/late indicator

---

### Test 3.7: Custom Workflow
**Steps:**
```javascript
const timeline = new EscalationTimeline('timeline-test');
const customStages = [
    { id: 'step1', name: '1️⃣ Analysis', description: 'Analyzing issue' },
    { id: 'step2', name: '2️⃣ Planning', description: 'Creating action plan' },
    { id: 'step3', name: '3️⃣ Implementation', description: 'Implementing fix' },
    { id: 'step4', name: '4️⃣ Verification', description: 'Testing fix' }
];
timeline.render(customStages, 'step2');
```

**Expected Results:**
- ✅ Custom stages render
- ✅ "Planning" is active (current stage)
- ✅ "Analysis" shows as completed
- ✅ "Implementation" and "Verification" pending

---

## Test Suite 4: Gantt Chart with Drag-Drop

### Test 4.1: Gantt Chart Loads
**Steps:**
1. Navigate to `http://127.0.0.1:8080/job-planning.html`
2. Wait for page to load
3. Verify Gantt chart renders with timeline

**Expected Results:**
- ✅ Page loads without errors
- ✅ Gantt chart visible (gray background with grid)
- ✅ Timeline header shows (60 days)
- ✅ Order bars display

**Console Check:**
```javascript
console.log(window.ganttManager); // Should show GanttManager instance
console.log(window.ganttManager.orders.length); // Number of orders loaded
```

---

### Test 4.2: Order Bars Display Correctly
**Steps:**
1. Gantt chart should show order bars
2. Verify bar styling: colored background with order number
3. Check multiple orders

**Expected Results:**
- ✅ Each order shows as a colored bar
- ✅ Bar width reflects duration (longer bars = longer jobs)
- ✅ Bar position shows start date (left side of timeline)
- ✅ Order number displayed on bar (e.g., "ORD-001")
- ✅ Bars within 60-day window visible
- ✅ Out-of-range orders hidden

---

### Test 4.3: Hover Effects
**Steps:**
1. Move mouse over an order bar
2. Observe visual feedback

**Expected Results:**
- ✅ Cursor changes to "move" (drag cursor)
- ✅ Bar highlights or changes opacity
- ✅ Tooltip shows order details (optional)

---

### Test 4.4: Drag-Drop Reschedule
**Steps:**
1. Note current position of an order bar
2. Grab order bar with mouse
3. Drag it 5 days to the right
4. Release mouse
5. Wait for API call to complete

**Expected Results:**
- ✅ Bar becomes slightly transparent while dragging
- ✅ Bar moves smoothly to new position
- ✅ Network tab shows `PUT /api/orders/{id}` call
- ✅ Request payload includes new `start_date` and `end_date`
- ✅ Toast shows: "Order #XXX rescheduled"
- ✅ Bar returns to normal opacity

**Verify Save:**
```javascript
// Check API response
// Should update start_date and end_date
// Duration should remain same
```

---

### Test 4.5: Drag-Drop Error Handling
**Steps:**
1. Simulate API failure by changing API URL:
   ```javascript
   window.api.baseUrl = 'http://127.0.0.1:9999'; // Wrong port
   ```
2. Try to drag-drop an order bar
3. Check error handling

**Expected Results:**
- ✅ Error toast appears: "Failed to reschedule: [error]"
- ✅ Bar reverts to original position
- ✅ No partial updates to database
- ✅ App doesn't crash

**Restore:**
```javascript
window.api.baseUrl = 'http://127.0.0.1:8000'; // Restore
```

---

### Test 4.6: Gantt Responsiveness
**Steps:**
1. Resize browser window
2. Make viewport smaller (900px wide)
3. Check Gantt chart layout

**Expected Results:**
- ✅ Chart adapts to smaller screen
- ✅ Bars still visible and draggable
- ✅ No horizontal scroll issues
- ✅ Timeline readable

---

### Test 4.7: Gantt Methods
**Steps:**
In browser console, test these:
```javascript
const gantt = window.ganttManager;

// Refresh orders
await gantt.refresh();

// Zoom in (show fewer days)
gantt.zoomIn(); // Should show 50 days instead of 60

// Zoom out (show more days)
gantt.zoomOut(); // Should show 70 days

// Highlight an order (if multiple orders visible)
gantt.highlightOrder(1); // Order ID: 1

// Clear highlight
gantt.clearHighlight();

// Get order details
const order = gantt.getOrderDetails(1);
console.log(order);
```

**Expected Results:**
- ✅ Refresh reloads orders from API and re-renders
- ✅ Zoom in shows fewer days (timeline more compressed)
- ✅ Zoom out shows more days (timeline more spread out)
- ✅ Highlight adds visual emphasis to order bar
- ✅ Get order details returns correct data

---

## Test Suite 5: Mobile Responsiveness

### Test 5.1: Dashboard on Mobile (480px)
**Steps:**
1. Open dashboard.html
2. Open DevTools (F12)
3. Toggle device toolbar (Ctrl+Shift+M)
4. Select "iPhone SE" or 480px width
5. Test functionality

**Expected Results:**
- ✅ Dashboard layouts adapt
- ✅ KPI cards stack vertically
- ✅ Text is readable
- ✅ Buttons are large enough to tap
- ✅ Tables scroll horizontally
- ✅ Toasts appear in correct position

---

### Test 5.2: SLA Timer on Mobile
**Steps:**
1. Create SLA timer on mobile viewport
2. Verify styling and readability

**Expected Results:**
- ✅ Timer display is large and readable
- ✅ Container has appropriate padding
- ✅ Text size increases on critical state
- ✅ Color changes clearly visible

---

### Test 5.3: Gantt Chart on Mobile (View-Only)
**Steps:**
1. Open job-planning.html on mobile (480px)
2. Try to scroll chart
3. Try to drag-drop

**Expected Results:**
- ✅ Chart is scrollable
- ✅ Drag-drop may not work well (expected limitation)
- ✅ Can view order bars
- ✅ Information is visible (read-only mode acceptable)

---

## Test Suite 6: Performance & Stress Testing

### Test 6.1: Large Dataset - Dashboard (100+ Orders)
**Steps:**
1. Create 100+ orders in backend via script or API
2. Load dashboard
3. Measure load time and responsiveness

**Expected Results:**
- ✅ Dashboard loads in < 3 seconds
- ✅ No freezing or lag
- ✅ Tables are scrollable
- ✅ Auto-refresh still works

**Performance Tip:** If slow, optimize by limiting results:
```javascript
// In api.js, add pagination
GET /api/orders/?limit=50&offset=0
```

---

### Test 6.2: Large Dataset - Gantt (100+ Orders)
**Steps:**
1. 100+ orders visible in Gantt
2. Try to drag-drop orders
3. Measure performance

**Expected Results:**
- ✅ Gantt renders in < 2 seconds
- ✅ Drag-drop still responsive
- ✅ No significant lag

---

### Test 6.3: Concurrent Operations
**Steps:**
1. Dashboard auto-refreshing (30-second interval)
2. SLA timer counting down
3. While both running, try to interact with Gantt chart

**Expected Results:**
- ✅ All features run smoothly together
- ✅ No performance degradation
- ✅ No race conditions or data conflicts

---

## Test Suite 7: Cross-Browser Compatibility

| Browser | Version | Status | Notes |
|---------|---------|--------|-------|
| Chrome | 90+ | ✅ Test | Primary browser |
| Firefox | 88+ | ✅ Test | Good support |
| Safari | 14+ | ✅ Test | May have minor issues |
| Edge | 90+ | ✅ Test | Chromium-based |
| IE 11 | - | ❌ Not Supported | Uses modern JS |

**Test Steps:**
1. For each browser, repeat Test 1.2, 2.2, 3.2, 4.2
2. Check console for errors
3. Verify visual styling consistent

---

## Bug Report Template

If you find an issue, use this format:

```
## Bug: [Brief Title]

**Severity:** Critical / High / Medium / Low

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Result:**
- 

**Actual Result:**
- 

**Console Errors:**
- 

**Browser/Device:**
- 

**Workaround:**
- 
```

---

## Success Criteria

**Phase 2E Testing is COMPLETE when:**

- [ ] All Dashboard KPI tests pass (1.1-1.7)
- [ ] All SLA Timer tests pass (2.1-2.7)
- [ ] All Timeline tests pass (3.1-3.7)
- [ ] All Gantt tests pass (4.1-4.7)
- [ ] Mobile responsiveness confirmed (5.1-5.3)
- [ ] Performance tests pass (6.1-6.3)
- [ ] At least 2 browsers tested (7.0)
- [ ] Zero critical/high severity bugs
- [ ] All error handling works correctly

**Result: READY FOR PHASE 3 QA** ✅

---

## Notes for Testers

1. **API Availability:** Ensure backend API is running before testing
2. **Test Data:** Create realistic test data for better validation
3. **Network Throttling:** Test with throttled connection (Chrome DevTools)
4. **Dark Mode:** Some CSS uses colors, test in both light and dark modes
5. **Accessibility:** Test with keyboard navigation (Tab key)
6. **Documentation:** Report any documentation gaps

---

## Next Steps After Testing

### If All Tests Pass ✅
→ Proceed to **Phase 3: QA & Refinement**
- Performance optimization
- Accessibility audit (WCAG 2.1)
- Code review
- Load testing

### If Tests Find Issues ⚠️
→ Create bug reports with details above
→ Prioritize and fix critical/high severity bugs
→ Re-test fixed areas
→ Document any limitations

### If Tests Find Major Issues ❌
→ Assess impact on production readiness
→ May need to iterate Phase 2 or skip certain features
→ Document decision in PHASE2_TESTING_RESULTS.md

---

## Testing Timeline

- **Estimated Time:** 4-6 hours (comprehensive manual testing)
- **Quick Test:** 1-2 hours (spot-check critical features)
- **Automated Test:** N/A (manual testing required for UI)

---

**Last Updated:** January 18, 2026  
**Test Status:** Ready to Begin
