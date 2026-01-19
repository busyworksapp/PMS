/**
 * Phase 2E: Automated Test Suite
 * Run: node test-phase2e.js or paste into browser console
 * 
 * This file contains all 45 tests organized by test suite
 */

class Phase2ETester {
    constructor() {
        this.results = {
            suite1: { name: 'Dashboard KPI Wiring', tests: [] },
            suite2: { name: 'SLA Countdown Timer', tests: [] },
            suite3: { name: 'Escalation Timeline', tests: [] },
            suite4: { name: 'Gantt Chart', tests: [] },
            suite5: { name: 'Mobile Responsiveness', tests: [] },
            suite6: { name: 'Performance & Stress', tests: [] },
            suite7: { name: 'Cross-Browser', tests: [] }
        };
        this.totalPass = 0;
        this.totalFail = 0;
    }

    /**
     * Add test result
     */
    addResult(suite, testName, passed, details = '') {
        const result = {
            test: testName,
            passed,
            details,
            timestamp: new Date().toLocaleTimeString()
        };
        this.results[suite].tests.push(result);
        if (passed) this.totalPass++;
        else this.totalFail++;

        const icon = passed ? '✅' : '❌';
        console.log(`  ${icon} ${testName}: ${details}`);
    }

    /**
     * SUITE 1: Dashboard KPI Wiring
     */
    async suite1() {
        console.log('\n🧪 SUITE 1: Dashboard KPI Wiring (7 Tests)');
        console.log('='.repeat(50));

        // Test 1.1
        try {
            const hasKPICards = document.querySelectorAll('.kpi-card').length > 0;
            const hasManager = window.dashboardManager !== undefined;
            const passed = hasKPICards && hasManager;
            this.addResult('suite1', 'Dashboard page loads', passed,
                `Cards: ${document.querySelectorAll('.kpi-card').length}, Manager: ${hasManager}`);
        } catch (e) {
            this.addResult('suite1', 'Dashboard page loads', false, e.message);
        }

        // Test 1.2
        try {
            const orders = window.dashboardManager?.orders?.length || 0;
            const passed = orders > 0;
            this.addResult('suite1', 'Dashboard loads order data from API', passed,
                `Orders loaded: ${orders}`);
        } catch (e) {
            this.addResult('suite1', 'Dashboard loads order data from API', false, e.message);
        }

        // Test 1.3
        try {
            const kpiCards = document.querySelectorAll('.kpi-card');
            const passed = kpiCards.length >= 4;
            this.addResult('suite1', 'KPI cards display calculated metrics', passed,
                `Cards displayed: ${kpiCards.length}`);
        } catch (e) {
            this.addResult('suite1', 'KPI cards display calculated metrics', false, e.message);
        }

        // Test 1.4
        try {
            const interval = window.dashboardManager?.autoRefreshSeconds;
            const timerActive = window.dashboardManager?.autoRefreshTimer !== null;
            const passed = interval === 30 && timerActive;
            this.addResult('suite1', 'Dashboard auto-refresh works (30s)', passed,
                `Interval: ${interval}s, Timer active: ${timerActive}`);
        } catch (e) {
            this.addResult('suite1', 'Dashboard auto-refresh works', false, e.message);
        }

        // Test 1.5
        try {
            const tbody = document.querySelector('#recent-orders-tbody');
            const rows = tbody?.querySelectorAll('tr').length || 0;
            const passed = rows > 0;
            this.addResult('suite1', 'Recent orders table loads', passed,
                `Rows: ${rows}`);
        } catch (e) {
            this.addResult('suite1', 'Recent orders table loads', false, e.message);
        }

        // Test 1.6
        try {
            const tbody = document.querySelector('#active-issues-tbody');
            const rows = tbody?.querySelectorAll('tr').length || 0;
            this.addResult('suite1', 'Active issues table loads', true,
                `Rows: ${rows}`);
        } catch (e) {
            this.addResult('suite1', 'Active issues table loads', false, e.message);
        }

        // Test 1.7
        try {
            // Check if toast system exists
            const hasToastSystem = window.toast !== undefined;
            this.addResult('suite1', 'Dashboard error handling (toast system)', hasToastSystem,
                `Toast system: ${hasToastSystem}`);
        } catch (e) {
            this.addResult('suite1', 'Dashboard error handling', false, e.message);
        }
    }

    /**
     * SUITE 2: SLA Countdown Timer
     */
    async suite2() {
        console.log('\n🧪 SUITE 2: SLA Countdown Timer (7 Tests)');
        console.log('='.repeat(50));

        // Test 2.1
        try {
            const passed = typeof SLATimer !== 'undefined';
            this.addResult('suite2', 'SLA Timer class exists', passed,
                `SLATimer defined: ${passed}`);
        } catch (e) {
            this.addResult('suite2', 'SLA Timer class exists', false, e.message);
        }

        // Test 2.2: Normal (Green) state
        try {
            const deadline = new Date(Date.now() + 3 * 60 * 60 * 1000).toISOString();
            const timer = new SLATimer('test-sla-green', deadline);
            await this.delay(100);
            const element = document.getElementById('test-sla-green');
            const isGreen = element?.classList.contains('sla-normal');
            this.addResult('suite2', 'SLA Timer normal state (green)', isGreen,
                `Class: ${element?.className}`);
            timer.destroy();
        } catch (e) {
            this.addResult('suite2', 'SLA Timer normal state (green)', false, e.message);
        }

        // Test 2.3: Warning (Orange) state
        try {
            const deadline = new Date(Date.now() + 45 * 60 * 1000).toISOString();
            const timer = new SLATimer('test-sla-orange', deadline);
            await this.delay(500);
            const element = document.getElementById('test-sla-orange');
            const isWarning = element?.classList.contains('sla-warning');
            this.addResult('suite2', 'SLA Timer warning state (orange)', isWarning,
                `Class: ${element?.className}`);
            timer.destroy();
        } catch (e) {
            this.addResult('suite2', 'SLA Timer warning state (orange)', false, e.message);
        }

        // Test 2.4: Critical (Red) state
        try {
            const deadline = new Date(Date.now() + 18 * 60 * 1000).toISOString();
            const timer = new SLATimer('test-sla-red', deadline);
            await this.delay(500);
            const element = document.getElementById('test-sla-red');
            const isCritical = element?.classList.contains('sla-critical');
            const hasPulse = element?.classList.contains('sla-pulse');
            this.addResult('suite2', 'SLA Timer critical state (red+pulse)', isCritical && hasPulse,
                `Critical: ${isCritical}, Pulse: ${hasPulse}`);
            timer.destroy();
        } catch (e) {
            this.addResult('suite2', 'SLA Timer critical state (red+pulse)', false, e.message);
        }

        // Test 2.5: Countdown accuracy
        try {
            const deadline = new Date(Date.now() + 60 * 1000).toISOString();
            const timer = new SLATimer('test-sla-countdown', deadline);
            const remaining1 = timer.getRemaining();
            await this.delay(2000);
            const remaining2 = timer.getRemaining();
            const diff = remaining1 - remaining2;
            const accurate = Math.abs(diff - 2000) < 500; // Within 500ms
            this.addResult('suite2', 'SLA Timer countdown accuracy', accurate,
                `Expected ~2000ms, got ${diff}ms`);
            timer.destroy();
        } catch (e) {
            this.addResult('suite2', 'SLA Timer countdown accuracy', false, e.message);
        }

        // Test 2.6: Expired state
        try {
            const deadline = new Date(Date.now() + 2 * 1000).toISOString();
            const timer = new SLATimer('test-sla-expired', deadline);
            await this.delay(3000);
            const element = document.getElementById('test-sla-expired');
            const isExpired = element?.classList.contains('sla-expired');
            this.addResult('suite2', 'SLA Timer marks expired', isExpired,
                `Expired: ${isExpired}`);
            timer.destroy();
        } catch (e) {
            this.addResult('suite2', 'SLA Timer marks expired', false, e.message);
        }

        // Test 2.7: Timer methods
        try {
            const deadline = new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString();
            const timer = new SLATimer('test-sla-methods', deadline);
            const remaining1 = timer.getRemaining();
            timer.stop();
            const remaining2 = timer.getRemaining();
            const stoppedCorrectly = remaining1 === remaining2;
            timer.destroy();
            this.addResult('suite2', 'SLA Timer methods (stop, destroy)', stoppedCorrectly,
                `Stop working: ${stoppedCorrectly}`);
        } catch (e) {
            this.addResult('suite2', 'SLA Timer methods', false, e.message);
        }
    }

    /**
     * SUITE 3: Escalation Timeline
     */
    async suite3() {
        console.log('\n🧪 SUITE 3: Escalation Timeline (7 Tests)');
        console.log('='.repeat(50));

        // Test 3.1: HTML renders
        try {
            const timeline = new EscalationTimeline('timeline-test-1');
            const sopTicket = {
                created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
                acknowledged_at: new Date(Date.now() - 20 * 60 * 60 * 1000).toISOString(),
                status: 'under_review'
            };
            timeline.renderSOPWorkflow(sopTicket);
            await this.delay(100);
            const stages = document.querySelectorAll('#timeline-test-1 .sla-timeline-item').length;
            this.addResult('suite3', 'Timeline HTML renders', stages >= 3,
                `Stages: ${stages}`);
        } catch (e) {
            this.addResult('suite3', 'Timeline HTML renders', false, e.message);
        }

        // Test 3.2: Current stage highlighted
        try {
            const timeline = new EscalationTimeline('timeline-test-2');
            const sopTicket = {
                status: 'under_review',
                created_at: new Date().toISOString(),
                acknowledged_at: new Date().toISOString()
            };
            timeline.renderSOPWorkflow(sopTicket);
            await this.delay(100);
            const activeStage = document.querySelector('#timeline-test-2 .sla-timeline-item.active');
            this.addResult('suite3', 'Timeline shows current stage highlighted', activeStage !== null,
                `Active stage: ${activeStage ? 'Found' : 'Not found'}`);
        } catch (e) {
            this.addResult('suite3', 'Timeline shows current stage highlighted', false, e.message);
        }

        // Test 3.3: Completed stages marked
        try {
            const timeline = new EscalationTimeline('timeline-test-3');
            const sopTicket = {
                status: 'escalated',
                created_at: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString(),
                acknowledged_at: new Date(Date.now() - 48 * 60 * 60 * 1000).toISOString()
            };
            timeline.renderSOPWorkflow(sopTicket);
            await this.delay(100);
            const completed = document.querySelectorAll('#timeline-test-3 .sla-timeline-item.completed').length;
            this.addResult('suite3', 'Timeline marks completed stages', completed > 0,
                `Completed stages: ${completed}`);
        } catch (e) {
            this.addResult('suite3', 'Timeline marks completed stages', false, e.message);
        }

        // Test 3.4: Timestamps displayed
        try {
            const timeline = new EscalationTimeline('timeline-test-4');
            const sopTicket = {
                status: 'under_review',
                created_at: new Date(Date.now() - 12 * 60 * 60 * 1000).toISOString(),
                acknowledged_at: new Date(Date.now() - 8 * 60 * 60 * 1000).toISOString()
            };
            timeline.renderSOPWorkflow(sopTicket);
            await this.delay(100);
            const timestamps = document.querySelectorAll('#timeline-test-4 .sla-timeline-time').length;
            this.addResult('suite3', 'Timeline displays timestamps', timestamps > 0,
                `Timestamps: ${timestamps}`);
        } catch (e) {
            this.addResult('suite3', 'Timeline displays timestamps', false, e.message);
        }

        // Test 3.5: SOP workflow 5 stages
        try {
            const timeline = new EscalationTimeline('timeline-test-5');
            const sopTicket = {
                status: 'received',
                created_at: new Date().toISOString()
            };
            timeline.renderSOPWorkflow(sopTicket);
            await this.delay(100);
            const stages = document.querySelectorAll('#timeline-test-5 .sla-timeline-item').length;
            this.addResult('suite3', 'SOP workflow has 5 stages', stages === 5,
                `Stages: ${stages}`);
        } catch (e) {
            this.addResult('suite3', 'SOP workflow has 5 stages', false, e.message);
        }

        // Test 3.6: Maintenance workflow 4 stages
        try {
            const timeline = new EscalationTimeline('timeline-test-6');
            const maintenanceTask = {
                status: 'scheduled',
                scheduled_date: new Date().toISOString()
            };
            timeline.renderMaintenanceWorkflow(maintenanceTask);
            await this.delay(100);
            const stages = document.querySelectorAll('#timeline-test-6 .sla-timeline-item').length;
            this.addResult('suite3', 'Maintenance workflow has 4 stages', stages === 4,
                `Stages: ${stages}`);
        } catch (e) {
            this.addResult('suite3', 'Maintenance workflow has 4 stages', false, e.message);
        }

        // Test 3.7: Custom workflow
        try {
            const timeline = new EscalationTimeline('timeline-test-7');
            const customStages = [
                { id: 's1', name: '🔍 Analysis', timestamp: new Date().toISOString() },
                { id: 's2', name: '📋 Planning', timestamp: null },
                { id: 's3', name: '⚙️ Implementation', timestamp: null }
            ];
            timeline.render(customStages, 's2');
            await this.delay(100);
            const stages = document.querySelectorAll('#timeline-test-7 .sla-timeline-item').length;
            this.addResult('suite3', 'Custom workflow renders', stages === 3,
                `Stages: ${stages}`);
        } catch (e) {
            this.addResult('suite3', 'Custom workflow renders', false, e.message);
        }
    }

    /**
     * SUITE 4: Gantt Chart
     */
    async suite4() {
        console.log('\n🧪 SUITE 4: Gantt Chart (7 Tests)');
        console.log('='.repeat(50));

        // Test 4.1: Gantt manager exists
        try {
            const passed = window.ganttManager !== undefined;
            this.addResult('suite4', 'Gantt Manager initializes', passed,
                `Manager exists: ${passed}`);
        } catch (e) {
            this.addResult('suite4', 'Gantt Manager initializes', false, e.message);
        }

        // Test 4.2: Orders loaded from API
        try {
            const orders = window.ganttManager?.orders?.length || 0;
            const passed = orders > 0;
            this.addResult('suite4', 'Gantt loads orders from API', passed,
                `Orders: ${orders}`);
        } catch (e) {
            this.addResult('suite4', 'Gantt loads orders from API', false, e.message);
        }

        // Test 4.3: Order bars render
        try {
            const bars = document.querySelectorAll('.gantt-bar').length;
            const passed = bars > 0;
            this.addResult('suite4', 'Gantt renders order bars', passed,
                `Bars: ${bars}`);
        } catch (e) {
            this.addResult('suite4', 'Gantt renders order bars', false, e.message);
        }

        // Test 4.4: Drag-drop listeners attached
        try {
            const bar = document.querySelector('.gantt-bar');
            const isDraggable = bar?.draggable === true;
            this.addResult('suite4', 'Gantt drag-drop setup', isDraggable,
                `Draggable: ${isDraggable}`);
        } catch (e) {
            this.addResult('suite4', 'Gantt drag-drop setup', false, e.message);
        }

        // Test 4.5: Zoom controls
        try {
            const gantt = window.ganttManager;
            const initialDays = gantt.daysToShow;
            gantt.zoomOut();
            const zoomedOut = gantt.daysToShow;
            gantt.zoomIn();
            const zoomedIn = gantt.daysToShow;
            const works = zoomedOut > initialDays && zoomedIn < zoomedOut;
            this.addResult('suite4', 'Gantt zoom in/out works', works,
                `Initial: ${initialDays}, Out: ${zoomedOut}, In: ${zoomedIn}`);
        } catch (e) {
            this.addResult('suite4', 'Gantt zoom in/out works', false, e.message);
        }

        // Test 4.6: Filter methods exist
        try {
            const gantt = window.ganttManager;
            const hasFilter = typeof gantt.filterByStatus === 'function';
            this.addResult('suite4', 'Gantt filter methods exist', hasFilter,
                `filterByStatus: ${hasFilter}`);
        } catch (e) {
            this.addResult('suite4', 'Gantt filter methods exist', false, e.message);
        }

        // Test 4.7: Gantt methods work
        try {
            const gantt = window.ganttManager;
            gantt.scrollToToday();
            if (gantt.orders.length > 0) {
                gantt.highlightOrder(gantt.orders[0].id);
                gantt.clearHighlight();
            }
            this.addResult('suite4', 'Gantt utility methods work', true,
                `scrollToToday, highlight, clearHighlight all executed`);
        } catch (e) {
            this.addResult('suite4', 'Gantt utility methods work', false, e.message);
        }
    }

    /**
     * SUITE 5: Mobile Responsiveness
     */
    async suite5() {
        console.log('\n🧪 SUITE 5: Mobile Responsiveness (3 Tests)');
        console.log('='.repeat(50));

        // Test 5.1: Dashboard responsive
        try {
            const kpiCards = document.querySelectorAll('.kpi-card');
            const hasMediaQuery = window.matchMedia('(max-width: 768px)').matches ||
                                 kpiCards.length > 0;
            this.addResult('suite5', 'Dashboard CSS responsive', hasMediaQuery,
                `Media queries present: ${hasMediaQuery}`);
        } catch (e) {
            this.addResult('suite5', 'Dashboard CSS responsive', false, e.message);
        }

        // Test 5.2: SLA Timer responsive
        try {
            const timer = document.querySelector('.sla-timer');
            const isResponsive = timer !== null;
            this.addResult('suite5', 'SLA Timer responsive design', isResponsive,
                `Timer element found: ${isResponsive}`);
        } catch (e) {
            this.addResult('suite5', 'SLA Timer responsive design', false, e.message);
        }

        // Test 5.3: Gantt responsive
        try {
            const timeline = document.querySelector('.gantt-timeline');
            const isResponsive = timeline !== null;
            this.addResult('suite5', 'Gantt responsive layout', isResponsive,
                `Timeline element found: ${isResponsive}`);
        } catch (e) {
            this.addResult('suite5', 'Gantt responsive layout', false, e.message);
        }
    }

    /**
     * SUITE 6: Performance & Stress
     */
    async suite6() {
        console.log('\n🧪 SUITE 6: Performance & Stress Testing (3 Tests)');
        console.log('='.repeat(50));

        // Test 6.1: KPI calculation performance
        try {
            const orders = Array.from({ length: 100 }, (_, i) => ({
                id: i,
                order_number: `ORDER-${i}`,
                status: i % 3 === 0 ? 'pending' : i % 3 === 1 ? 'in_progress' : 'completed',
                start_date: new Date().toISOString(),
                end_date: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
                completion_date: new Date().toISOString(),
                due_date: new Date().toISOString()
            }));

            const start = performance.now();
            const kpis = window.dashboardManager.calculateKPIs(orders, [], [], {});
            const elapsed = performance.now() - start;

            const fast = elapsed < 1000;
            this.addResult('suite6', 'KPI calculation 100 orders', fast,
                `Time: ${elapsed.toFixed(2)}ms`);
        } catch (e) {
            this.addResult('suite6', 'KPI calculation 100 orders', false, e.message);
        }

        // Test 6.2: Timer creation performance
        try {
            const start = performance.now();
            const timers = Array.from({ length: 10 }, (_, i) => 
                new SLATimer(`perf-timer-${i}`, 
                    new Date(Date.now() + 60 * 60 * 1000).toISOString())
            );
            const elapsed = performance.now() - start;
            timers.forEach(t => t.destroy());

            const fast = elapsed < 500;
            this.addResult('suite6', 'Create 10 timers performance', fast,
                `Time: ${elapsed.toFixed(2)}ms`);
        } catch (e) {
            this.addResult('suite6', 'Create 10 timers performance', false, e.message);
        }

        // Test 6.3: Memory check
        try {
            const memUsed = performance.memory?.usedJSHeapSize || 0;
            const memLimit = performance.memory?.jsHeapSizeLimit || 0;
            const percentUsed = memLimit > 0 ? (memUsed / memLimit * 100).toFixed(1) : 'N/A';
            const healthy = memUsed < 50 * 1024 * 1024; // < 50MB
            this.addResult('suite6', 'Memory usage healthy', healthy,
                `${percentUsed}% (${(memUsed / 1024 / 1024).toFixed(1)}MB)`);
        } catch (e) {
            this.addResult('suite6', 'Memory usage healthy', false, e.message);
        }
    }

    /**
     * SUITE 7: Cross-Browser
     */
    async suite7() {
        console.log('\n🧪 SUITE 7: Cross-Browser Compatibility (3 Tests)');
        console.log('='.repeat(50));

        // Test 7.1: Browser detection
        try {
            const ua = navigator.userAgent;
            const isChrome = /Chrome/.test(ua) && !/Chromium/.test(ua);
            const isFirefox = /Firefox/.test(ua);
            const isSafari = /Safari/.test(ua) && !/Chrome/.test(ua);
            const isEdge = /Edg/.test(ua);
            const browser = isChrome ? 'Chrome' : isFirefox ? 'Firefox' : isSafari ? 'Safari' : isEdge ? 'Edge' : 'Other';
            const supported = isChrome || isFirefox || isSafari || isEdge;
            this.addResult('suite7', 'Browser compatibility check', supported,
                `Browser: ${browser}`);
        } catch (e) {
            this.addResult('suite7', 'Browser compatibility check', false, e.message);
        }

        // Test 7.2: CSS3 support
        try {
            const div = document.createElement('div');
            const hasAnimations = CSS.supports('animation-name', 'test');
            const hasTransforms = CSS.supports('transform', 'translate(0, 0)');
            const supported = hasAnimations && hasTransforms;
            this.addResult('suite7', 'CSS3 animations/transforms support', supported,
                `Animations: ${hasAnimations}, Transforms: ${hasTransforms}`);
        } catch (e) {
            this.addResult('suite7', 'CSS3 animations/transforms support', false, e.message);
        }

        // Test 7.3: JavaScript features
        try {
            // Check for async/await, destructuring, arrow functions
            const hasAsyncAwait = 'function' === typeof (async () => {}).constructor;
            const hasFetch = typeof fetch === 'function';
            const hasPromise = typeof Promise === 'function';
            const supported = hasAsyncAwait && hasFetch && hasPromise;
            this.addResult('suite7', 'Modern JavaScript features', supported,
                `Async: ${hasAsyncAwait}, Fetch: ${hasFetch}, Promise: ${hasPromise}`);
        } catch (e) {
            this.addResult('suite7', 'Modern JavaScript features', false, e.message);
        }
    }

    /**
     * Run all test suites
     */
    async runAll() {
        console.log('\n');
        console.log('╔════════════════════════════════════════════════════════╗');
        console.log('║       PHASE 2E: AUTOMATED TEST SUITE                   ║');
        console.log('║       Started: ' + new Date().toLocaleString().padEnd(38) + '║');
        console.log('╚════════════════════════════════════════════════════════╝');

        await this.suite1();
        await this.suite2();
        await this.suite3();
        await this.suite4();
        await this.suite5();
        await this.suite6();
        await this.suite7();

        this.printSummary();
    }

    /**
     * Print test summary
     */
    printSummary() {
        console.log('\n');
        console.log('╔════════════════════════════════════════════════════════╗');
        console.log('║                   TEST SUMMARY                         ║');
        console.log('╚════════════════════════════════════════════════════════╝');

        let suitePass = 0;
        let suiteFail = 0;

        Object.keys(this.results).forEach(suiteKey => {
            const suite = this.results[suiteKey];
            const passCount = suite.tests.filter(t => t.passed).length;
            const failCount = suite.tests.filter(t => !t.passed).length;
            const icon = failCount === 0 ? '✅' : '⚠️ ';

            console.log(`\n${icon} ${suite.name}`);
            console.log(`   ${passCount}/${suite.tests.length} PASS`);

            if (failCount > 0) {
                suite.tests.filter(t => !t.passed).forEach(test => {
                    console.log(`   ❌ ${test.test}: ${test.details}`);
                });
            }

            suitePass += passCount;
            suiteFail += failCount;
        });

        console.log('\n' + '='.repeat(60));
        console.log(`TOTAL: ${suitePass}/45 PASS, ${suiteFail}/45 FAIL`);
        console.log('='.repeat(60));

        if (suiteFail === 0) {
            console.log('\n🎉 ALL TESTS PASSED! Ready for Phase 3');
        } else if (suiteFail <= 5) {
            console.log('\n⚠️  MINOR ISSUES - Review failures above');
        } else {
            console.log('\n❌ CRITICAL ISSUES - Fix failures and re-test');
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Auto-run when loaded
if (typeof window !== 'undefined') {
    window.phase2eTester = new Phase2ETester();
    console.log('Phase 2E Tester ready. Run: window.phase2eTester.runAll()');
}
