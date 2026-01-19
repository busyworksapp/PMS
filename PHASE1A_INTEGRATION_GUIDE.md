# Phase 1A Integration Guide

Quick guide for developers to use the new Phase 1A features in your HTML pages.

---

## 1. Include Toast Notification System

Add this to your HTML `<head>` section:

```html
<script src="js/toast.js"></script>
```

Then use it in your code:

```javascript
// Success notification
toast.success('Operation completed successfully!');

// Error notification
toast.error('An error occurred: ' + error.message);

// Warning notification
toast.warning('This action cannot be undone');

// Info notification
toast.info('Please wait...');

// Auto-dismiss after 5 seconds (default)
// Or customize duration:
toast.success('Saved!', 3000);  // 3 seconds

// Manually close all toasts
toast.clear();
```

---

## 2. Using Error Handling in Forms

### Pattern 1: Simple Form with Toast

```html
<form id="createDefectForm">
    <input type="text" name="order_id" required>
    <input type="text" name="defect_type" required>
    <input type="text" name="description" required>
    <button type="submit">Create Defect</button>
</form>

<script>
document.getElementById('createDefectForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        const data = api.getFormData(e.target);
        await api.post('/api/defects/', data);
        toast.success('Defect created successfully!');
        e.target.reset();  // Clear form
    } catch (error) {
        toast.error(`Error: ${error.message}`);
    }
});
</script>
```

### Pattern 2: Using handleFormSubmit Helper

```html
<form id="createOrderForm">
    <input type="text" name="order_number" required>
    <input type="number" name="quantity" required>
    <button type="submit">
        <span>Create Order</span>
        <span class="spinner hidden"></span>
    </button>
</form>

<script>
document.getElementById('createOrderForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    api.handleFormSubmit(e.target, async () => {
        const data = api.getFormData(e.target);
        const result = await api.post('/api/orders/', data);
        e.target.reset();
        return result;
    });
});
</script>
```

---

## 3. Loading Spinners

### Auto Spinner (with handleFormSubmit)

The `handleFormSubmit()` method automatically handles the spinner:

```javascript
api.handleFormSubmit(form, async () => {
    return api.post('/api/endpoint/', data);
});
// Spinner shows automatically ✓
// Success/error toast shown automatically ✓
// Button disabled during submission ✓
```

### Manual Spinner Control

```html
<button type="submit" id="submitBtn">
    <span>Submit</span>
    <span class="spinner hidden"></span>
</button>

<script>
const btn = document.getElementById('submitBtn');
const spinner = btn.querySelector('.spinner');

// Show spinner
spinner.classList.remove('hidden');
btn.disabled = true;

// Do work...
try {
    await api.post('/api/endpoint/', data);
} finally {
    // Hide spinner
    spinner.classList.add('hidden');
    btn.disabled = false;
}
</script>
```

---

## 4. Automatic Features (No Code Needed)

These features are **automatic** for all API calls:

### Timeout (10 seconds)
```javascript
// All requests now timeout after 10 seconds
// If timeout occurs, user sees toast error
const data = await api.get('/api/jobs/');  // Auto-timeout
```

### Retry Logic (3 attempts with exponential backoff)
```javascript
// Fails → waits 1s → retries
// Fails → waits 2s → retries
// Fails → waits 4s → retries
// Fails → throws error with toast
const data = await api.get('/api/jobs/');  // Auto-retry
```

### Environment Detection
```javascript
// Automatically detects:
// - Development: http://127.0.0.1:8000
// - Production: https://yourdomain.com:8000
// No code needed! ✓
```

---

## 5. API Client Methods

### Get Form Data
```javascript
const form = document.getElementById('myForm');
const data = api.getFormData(form);
// Returns: { field1: 'value1', field2: 'value2' }
```

### Handle Form Submit
```javascript
api.handleFormSubmit(form, async () => {
    // Your async code here
    return api.post('/api/endpoint/', data);
});
// Automatically handles:
// - Loading state
// - Error handling
// - Success/error toast
// - Button disabled state
// - Spinner show/hide
```

### Manual API Calls
```javascript
try {
    // GET
    const data = await api.get('/api/jobs/');
    
    // POST
    const result = await api.post('/api/defects/', { order_id: '123' });
    
    // PUT
    const updated = await api.put('/api/jobs/1', { status: 'completed' });
    
    // DELETE
    await api.delete('/api/orders/1');
    
    // All have automatic: timeout + retry + error handling
    toast.success('Operation successful!');
} catch (error) {
    toast.error(error.message);
}
```

---

## 6. Common Patterns

### Form with Validation & Loading

```html
<form id="defectForm">
    <fieldset id="defectFieldset">
        <input type="text" name="order_id" placeholder="Order ID" required>
        <select name="defect_type" required>
            <option value="">Select Type</option>
            <option value="surface">Surface Defect</option>
            <option value="structural">Structural</option>
        </select>
        <textarea name="description" placeholder="Description" required></textarea>
        <button type="submit">Submit Defect</button>
    </fieldset>
</form>

<script>
const form = document.getElementById('defectForm');
const fieldset = document.getElementById('defectFieldset');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Disable inputs during submission
    fieldset.disabled = true;
    
    api.handleFormSubmit(form, async () => {
        const data = api.getFormData(form);
        return api.post('/api/defects/', data);
    }).finally(() => {
        // Re-enable inputs
        fieldset.disabled = false;
    });
});
</script>
```

### Real-time Data with Retry

```javascript
async function loadDashboardData() {
    try {
        // All of these auto-retry and timeout
        const jobs = await api.get('/api/jobs/');
        const defects = await api.get('/api/defects/');
        const orders = await api.get('/api/orders/');
        
        updateDashboard(jobs, defects, orders);
        toast.info('Dashboard updated!');
    } catch (error) {
        toast.error('Failed to load dashboard: ' + error.message);
    }
}

// Load every 30 seconds
setInterval(loadDashboardData, 30000);
loadDashboardData();  // Initial load
```

### Error Handling with Retry Info

```javascript
api.get('/api/jobs/')
    .then(data => {
        console.log('Success on first try or after retries');
        toast.success('Data loaded!');
    })
    .catch(error => {
        if (error.message.includes('timeout')) {
            toast.error('Server not responding (timeout)');
        } else if (error.message.includes('Unauthorized')) {
            // Auto-redirect to login happens
            toast.error('Please login again');
        } else {
            toast.error('Error: ' + error.message);
        }
    });
```

---

## 7. Styling Toast Notifications

Customize toast appearance in CSS:

```css
/* Change toast position */
#toast-container {
    top: 50px;  /* Move down */
    right: 30px; /* Move left */
}

/* Change toast width on mobile */
@media (max-width: 480px) {
    #toast-container {
        left: 5px;
        right: 5px;
        max-width: none;
    }
}

/* Customize success toast color */
.toast.success {
    background: #28a745;  /* Different green */
}

/* Customize error toast */
.toast.error {
    background: #c82333;  /* Darker red */
}
```

---

## 8. Testing Your Implementation

### Test Form Submission
```javascript
// 1. Click submit button
// 2. Should see spinner appear on button
// 3. Should see success toast after 1-2 seconds
// 4. Button spinner should disappear
// 5. Form should be cleared or page updated
```

### Test Error Handling
```javascript
// Try these in browser console:
api.get('/api/jobs/invalid')  // 404 error
// Should see error toast with specific error message
```

### Test Timeout
```javascript
// Kill backend server
api.get('/api/jobs/')  // No server running
// Should timeout after 10 seconds
// Should retry 3 times with delays
// Should show error toast after final attempt
```

### Test API URL Detection
```javascript
// Check in browser console:
console.log(api.baseUrl)  // Should show correct URL
// If localhost: http://127.0.0.1:8000
// If production: https://yourdomain.com:8000
```

---

## 9. Next Steps

1. **Add Toast Script** to your HTML pages
2. **Wrap Form Submissions** with error handling
3. **Test in Browser** - verify spinners and toasts work
4. **Deploy** - no backend changes needed
5. **Gather Feedback** - users will love the UX improvements

---

## Questions?

See `PHASE1A_COMPLETE.md` for:
- Detailed explanation of each fix
- Before/after comparisons
- Code examples

Or check `ACTION_PLAN.md` Phase 2 for next features to implement.
