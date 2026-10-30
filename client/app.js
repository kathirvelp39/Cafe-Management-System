const API_BASE = 'http://localhost:8000';

// --- DOM ELEMENTS ---
const toastEl = document.getElementById('toast');
const authSection = document.getElementById('auth-section');
const dashboardSection = document.getElementById('dashboard-section');
const navLogout = document.getElementById('nav-logout');

// Auth Tabs & Forms
const tabs = document.querySelectorAll('.tab');
const authForms = document.querySelectorAll('.auth-form');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const resetForm = document.getElementById('reset-form');

// OTP Elements
const btnRequestOtp = document.getElementById('btn-request-otp');
const btnVerifyOtp = document.getElementById('btn-verify-otp');
const otpStep1 = document.getElementById('otp-step-1');
const otpStep2 = document.getElementById('otp-step-2');

// Profile Dashboard Elements
const userGreeting = document.getElementById('user-greeting');
const userEmail = document.getElementById('user-email');
const loyaltyTotal = document.getElementById('loyalty-total');
const ordersList = document.getElementById('orders-list');
const loyaltyHistoryList = document.getElementById('loyalty-history-list');
const addLoyaltyForm = document.getElementById('add-loyalty-form');

// Sidebar Navigation
const navBtns = document.querySelectorAll('.nav-btn');
const dashboardViews = document.querySelectorAll('.dashboard-view');

// Tables & Data Elements
const tableMenu = document.getElementById('table-menu');
const tableAdminOrders = document.getElementById('table-admin-orders');
const tableInventory = document.getElementById('table-inventory');
const tableReservations = document.getElementById('table-reservations');
const tableFeedback = document.getElementById('table-feedback');

// Report Elements
const reportOrders = document.getElementById('report-orders');
const reportRevenue = document.getElementById('report-revenue');
const reportAov = document.getElementById('report-aov');

// Refresh Buttons
document.getElementById('btn-refresh-menu')?.addEventListener('click', loadMenu);
document.getElementById('btn-refresh-admin-orders')?.addEventListener('click', loadAdminOrders);
document.getElementById('btn-refresh-inventory')?.addEventListener('click', loadInventory);
document.getElementById('btn-refresh-reports')?.addEventListener('click', loadReports);
document.getElementById('btn-refresh-reservations')?.addEventListener('click', loadReservations);
document.getElementById('btn-refresh-feedback')?.addEventListener('click', loadFeedback);

// Billing Form
const generateInvoiceForm = document.getElementById('generate-invoice-form');
const billingResult = document.getElementById('billing-result');

// State
let token = localStorage.getItem('access_token');

// --- UTILITIES ---
function showToast(message, type = 'success') {
    toastEl.textContent = message;
    toastEl.className = `toast ${type}`;
    toastEl.classList.remove('hidden', 'hide');
    
    setTimeout(() => {
        toastEl.classList.add('hide');
        setTimeout(() => toastEl.classList.add('hidden'), 300);
    }, 3000);
}

async function fetchWithAuth(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    if (options.body instanceof URLSearchParams) {
        delete headers['Content-Type'];
    }

    const response = await fetch(`${API_BASE}${url}`, { ...options, headers });
    
    if (response.status === 401) {
        logout();
        throw new Error('Unauthorized');
    }
    
    return response;
}

// --- AUTH LOGIC ---
function checkAuth() {
    if (token) {
        authSection.classList.add('hidden');
        dashboardSection.classList.remove('hidden');
        navLogout.classList.remove('hidden');
        loadProfileData(); // This will now handle RBAC
    } else {
        authSection.classList.remove('hidden');
        dashboardSection.classList.add('hidden');
        navLogout.classList.add('hidden');
        document.getElementById('user-role-badge').classList.add('hidden');
    }
}

function logout() {
    token = null;
    localStorage.removeItem('access_token');
    checkAuth();
    showToast('Logged out successfully');
}
navLogout?.addEventListener('click', logout);

function applyRBAC(role) {
    const roleBadge = document.getElementById('user-role-badge');
    if (roleBadge) {
        roleBadge.textContent = role;
        roleBadge.classList.remove('hidden');
    }

    let firstVisible = null;
    navBtns.forEach(btn => {
        const roles = btn.dataset.role ? btn.dataset.role.split(',') : ['all'];
        if (roles.includes('all') || roles.includes(role.toLowerCase())) {
            btn.style.display = 'block';
            if (!firstVisible) firstVisible = btn;
        } else {
            btn.style.display = 'none';
        }
    });
    // Click the first visible button if current is hidden
    const currentActive = document.querySelector('.nav-btn.active');
    if (currentActive && currentActive.style.display === 'none' && firstVisible) {
        firstVisible.click();
    }
}

// Auth Tab Switching
tabs.forEach(tab => {
    tab?.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        authForms.forEach(f => f.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.target).classList.add('active');
    });
});

// Sidebar View Switching
navBtns.forEach(btn => {
    btn?.addEventListener('click', () => {
        navBtns.forEach(b => b.classList.remove('active'));
        dashboardViews.forEach(v => v.classList.add('hidden', 'active')); // Reset
        dashboardViews.forEach(v => v.classList.remove('active'));
        
        btn.classList.add('active');
        const targetViewId = btn.dataset.view;
        const targetView = document.getElementById(targetViewId);
        targetView.classList.remove('hidden');
        targetView.classList.add('active');

        // Load data based on view
        if (targetViewId === 'view-profile') loadProfileData();
        if (targetViewId === 'view-menu') loadMenu();
        if (targetViewId === 'view-orders') loadAdminOrders();
        if (targetViewId === 'view-inventory') loadInventory();
        if (targetViewId === 'view-reports') loadReports();
        if (targetViewId === 'view-reservations') loadReservations();
        if (targetViewId === 'view-feedback') loadFeedback();
        if (targetViewId === 'view-employees') loadEmployees();
    });
});

// Forms Submit Logic
registerForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const full_name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    try {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name, email, password })
        });
        if (res.ok) {
            showToast('Registration successful! Please login.');
            tabs[0].click();
            registerForm.reset();
        } else {
            const data = await res.json();
            showToast(data.detail || 'Registration failed', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

loginForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append('username', document.getElementById('login-email').value);
    formData.append('password', document.getElementById('login-password').value);

    try {
        const res = await fetch(`${API_BASE}/auth/login`, { method: 'POST', body: formData });
        if (res.ok) {
            const data = await res.json();
            token = data.access_token;
            localStorage.setItem('access_token', token);
            showToast('Login successful!');
            loginForm.reset();
            checkAuth();
        } else {
            const data = await res.json();
            showToast(data.detail || 'Login failed', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

btnRequestOtp?.addEventListener('click', async () => {
    const email = document.getElementById('otp-email').value;
    if (!email) return showToast('Please enter email', 'error');
    try {
        const res = await fetch(`${API_BASE}/auth/request-otp`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email })
        });
        if (res.ok) {
            showToast('OTP sent to your email');
            otpStep1.classList.add('hidden');
            otpStep2.classList.remove('hidden');
        } else {
            const data = await res.json();
            showToast(data.detail || 'Failed to request OTP', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

btnVerifyOtp?.addEventListener('click', async () => {
    const email = document.getElementById('otp-email').value;
    const code = document.getElementById('otp-code').value;
    if (!code) return showToast('Please enter OTP code', 'error');
    try {
        const res = await fetch(`${API_BASE}/auth/verify-otp`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, otp_code: code })
        });
        if (res.ok) {
            const data = await res.json();
            token = data.access_token;
            localStorage.setItem('access_token', token);
            showToast('OTP verified successfully!');
            checkAuth();
        } else {
            const data = await res.json();
            showToast(data.detail || 'Invalid OTP', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

resetForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('reset-email').value;
    const new_password = document.getElementById('reset-password-new').value;
    try {
        const res = await fetch(`${API_BASE}/auth/reset-password`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, new_password })
        });
        if (res.ok) {
            showToast('Password reset successful! Please login.');
            tabs[0].click();
            resetForm.reset();
        } else {
            const data = await res.json();
            showToast(data.detail || 'Password reset failed', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

// --- DATA FETCHING FUNCTIONS ---

async function loadProfileData() {
    // 1. Profile
    try {
        const res = await fetchWithAuth('/customers/me');
        if (res.ok) {
            const data = await res.json();
            userGreeting.textContent = `Hello, ${data.full_name}`;
            userEmail.textContent = data.email;
            window.currentUserId = data.id;
            
            // Apply RBAC based on the user's role from the server
            const userRole = data.role || 'admin';
            applyRBAC(userRole);
        }
    } catch (err) { console.error(err); }

    // 2. Loyalty Total
    try {
        const res = await fetchWithAuth('/customers/me/loyalty/total');
        if (res.ok) {
            const data = await res.json();
            loyaltyTotal.textContent = data.total_points !== undefined ? data.total_points : data;
        }
    } catch (err) { console.error(err); }

    // 3. Orders
    try {
        const res = await fetchWithAuth('/customers/me/orders');
        if (res.ok) {
            const orders = await res.json();
            ordersList.innerHTML = '';
            if (orders.length === 0) {
                ordersList.innerHTML = '<div class="empty-state">No orders found.</div>';
            } else {
                orders.forEach(order => {
                    const date = new Date(order.created_at).toLocaleDateString();
                    ordersList.innerHTML += `
                        <div class="list-item">
                            <div class="order-header">
                                <span>Order #${order.id} (${order.order_type})</span>
                                <span>${date}</span>
                            </div>
                            <div class="order-header">
                                <span style="color:var(--text-secondary)">Status: ${order.status}</span>
                                <span class="order-total">₹${order.total_amount.toFixed(2)}</span>
                            </div>
                        </div>`;
                });
            }
        }
    } catch (err) { console.error(err); }

    // 4. Loyalty History
    try {
        const res = await fetchWithAuth('/customers/me/loyalty');
        if (res.ok) {
            const history = await res.json();
            loyaltyHistoryList.innerHTML = '';
            if (history.length === 0) {
                loyaltyHistoryList.innerHTML = '<div class="empty-state">No loyalty points history.</div>';
            } else {
                history.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                history.forEach(item => {
                    const date = new Date(item.created_at).toLocaleDateString();
                    const ptsClass = item.points > 0 ? 'positive' : '';
                    loyaltyHistoryList.innerHTML += `
                        <div class="list-item">
                            <div class="loyalty-header">
                                <span>${item.description || 'Points updated'}</span>
                                <span>${date}</span>
                            </div>
                            <div>
                                <span class="loyalty-points ${ptsClass}">${item.points > 0 ? '+' : ''}${item.points} pts</span>
                            </div>
                        </div>`;
                });
            }
        }
    } catch (err) { console.error(err); }
}

addLoyaltyForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const points = parseInt(document.getElementById('loyalty-points-input').value);
    const description = document.getElementById('loyalty-reason-input').value;
    try {
        const res = await fetchWithAuth('/customers/me/loyalty', {
            method: 'POST', body: JSON.stringify({ points, description })
        });
        if (res.ok) {
            showToast('Loyalty points added!');
            addLoyaltyForm.reset();
            loadProfileData();
        } else showToast('Failed to add points', 'error');
    } catch (err) { showToast('Network error', 'error'); }
});


async function loadMenu() {
    try {
        const res = await fetchWithAuth('/menu');
        if (res.ok) {
            const items = await res.json();
            tableMenu.innerHTML = '';
            if (items.length === 0) {
                tableMenu.innerHTML = '<tr><td colspan="6" class="empty-state">No menu items found.</td></tr>';
                return;
            }
            items.forEach(item => {
                tableMenu.innerHTML += `
                    <tr>
                        <td>#${item.id}</td>
                        <td>${item.name}</td>
                        <td>${item.category}</td>
                        <td>₹${item.price.toFixed(2)}</td>
                        <td>${item.is_available ? 'Available' : 'Unavailable'}</td>
                        <td>
                            <button class="btn btn-sm btn-outline" onclick="editMenuItem(${item.id})">Edit</button>
                            <button class="btn btn-sm btn-outline" style="color: var(--error-color); border-color: var(--error-color);" onclick="deleteMenuItem(${item.id})">Delete</button>
                        </td>
                    </tr>`;
            });
        }
    } catch (err) { console.error(err); showToast('Failed to load menu', 'error'); }
}

const btnAddMenu = document.getElementById('btn-add-menu');
const btnCancelMenu = document.getElementById('btn-cancel-menu');
const menuItemForm = document.getElementById('menu-item-form');
const menuFormTitle = document.getElementById('menu-form-title');

btnAddMenu?.addEventListener('click', () => {
    menuItemForm.reset();
    document.getElementById('menu-id').value = '';
    menuFormTitle.textContent = 'Create Menu Item';
    menuItemForm.classList.add('active');
});

btnCancelMenu?.addEventListener('click', () => {
    menuItemForm.classList.remove('active');
});

menuItemForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('menu-id').value;
    const itemData = {
        name: document.getElementById('menu-name').value,
        description: document.getElementById('menu-description').value,
        category: document.getElementById('menu-category').value,
        price: parseFloat(document.getElementById('menu-price').value),
        is_available: document.getElementById('menu-available').checked
    };

    try {
        const url = id ? `/menu/${id}` : '/menu';
        const method = id ? 'PUT' : 'POST';
        
        const res = await fetchWithAuth(url, {
            method: method,
            body: JSON.stringify(itemData)
        });
        
        if (res.ok) {
            showToast(`Menu item ${id ? 'updated' : 'created'} successfully!`);
            menuItemForm.classList.remove('active');
            loadMenu();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to save menu item', 'error');
        }
    } catch (err) {
        showToast('Network error', 'error');
    }
});

window.editMenuItem = async (id) => {
    try {
        const res = await fetchWithAuth(`/menu/${id}`);
        if (res.ok) {
            const item = await res.json();
            document.getElementById('menu-id').value = item.id;
            document.getElementById('menu-name').value = item.name;
            document.getElementById('menu-description').value = item.description || '';
            document.getElementById('menu-category').value = item.category;
            document.getElementById('menu-price').value = item.price;
            document.getElementById('menu-available').checked = item.is_available;
            
            menuFormTitle.textContent = 'Edit Menu Item';
            menuItemForm.classList.add('active');
        } else {
            showToast('Failed to load item details', 'error');
        }
    } catch (err) {
        showToast('Network error', 'error');
    }
};

window.deleteMenuItem = async (id) => {
    if (!confirm('Are you sure you want to delete this menu item?')) return;
    try {
        const res = await fetchWithAuth(`/menu/${id}`, { method: 'DELETE' });
        if (res.ok) {
            showToast('Menu item deleted');
            loadMenu();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to delete item', 'error');
        }
    } catch (err) {
        showToast('Network error', 'error');
    }
};

async function loadAdminOrders() {
    try {
        const res = await fetchWithAuth('/orders/kitchen/tickets');
        if (res.ok) {
            const orders = await res.json();
            tableAdminOrders.innerHTML = '';
            if (orders.length === 0) {
                tableAdminOrders.innerHTML = '<tr><td colspan="6" class="empty-state">No active orders.</td></tr>';
                return;
            }
            orders.forEach(order => {
                tableAdminOrders.innerHTML += `
                    <tr>
                        <td>#${order.id}</td>
                        <td>${order.order_type}</td>
                        <td>${order.table_number || 'N/A'}</td>
                        <td>₹${order.total_amount.toFixed(2)}</td>
                        <td>
                            <select onchange="updateOrderStatus(${order.id}, this.value)" style="background:transparent; color:inherit; border:1px solid var(--glass-border); padding:2px; border-radius:4px;">
                                <option value="Pending" ${order.status === 'Pending' ? 'selected' : ''} style="color:black;">Pending</option>
                                <option value="Preparing" ${order.status === 'Preparing' ? 'selected' : ''} style="color:black;">Preparing</option>
                                <option value="Completed" ${order.status === 'Completed' ? 'selected' : ''} style="color:black;">Completed</option>
                                <option value="Served" ${order.status === 'Served' ? 'selected' : ''} style="color:black;">Served</option>
                            </select>
                        </td>
                        <td>
                            <button class="btn btn-sm btn-outline" style="color: var(--error-color); border-color: var(--error-color);" onclick="cancelOrder(${order.id})">Cancel</button>
                        </td>
                    </tr>`;
            });
        }
    } catch (err) { console.error(err); showToast('Failed to load orders', 'error'); }
}

const btnAddOrder = document.getElementById('btn-add-order');
const btnCancelOrderForm = document.getElementById('btn-cancel-order-form');
const orderForm = document.getElementById('order-form');

btnAddOrder?.addEventListener('click', async () => {
    orderForm.reset();
    orderForm.classList.add('active');
    
    const container = document.getElementById('order-menu-items-container');
    container.innerHTML = '<div class="empty-state">Loading menu items...</div>';
    
    try {
        const res = await fetchWithAuth('/menu');
        if (res.ok) {
            const items = await res.json();
            container.innerHTML = '';
            if (items.length === 0) {
                container.innerHTML = '<div class="empty-state">No menu items available.</div>';
                return;
            }
            items.filter(i => i.is_available).forEach(item => {
                container.innerHTML += `
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                        <div>
                            <div style="font-weight: 500;">${item.name} (₹${item.price.toFixed(2)})</div>
                        </div>
                        <div>
                            <input type="number" min="0" value="0" class="order-item-qty" data-id="${item.id}" style="width: 60px; padding: 4px;">
                        </div>
                    </div>
                `;
            });
        }
    } catch (err) {
        container.innerHTML = '<div class="empty-state">Failed to load menu items.</div>';
    }
});

btnCancelOrderForm?.addEventListener('click', () => {
    orderForm.classList.remove('active');
});

orderForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const type = document.getElementById('order-type').value;
    const table = document.getElementById('order-table').value;
    // Gather items from dynamic list
    const items = [];
    const qtyInputs = document.querySelectorAll('.order-item-qty');
    qtyInputs.forEach(input => {
        const qty = parseInt(input.value);
        if (qty > 0) {
            items.push({ menu_item_id: parseInt(input.getAttribute('data-id')), quantity: qty });
        }
    });

    if (items.length === 0) {
        showToast('Please add at least one item', 'error');
        return;
    }

    const payload = {
        order_type: type,
        table_number: table ? parseInt(table) : null,
        items: items
    };

    try {
        const res = await fetchWithAuth('/orders', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Order placed successfully!');
            orderForm.classList.remove('active');
            loadAdminOrders();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to place order', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

window.updateOrderStatus = async (id, status) => {
    try {
        const res = await fetchWithAuth(`/orders/${id}/status?status=${encodeURIComponent(status)}`, { method: 'PUT' });
        if (res.ok) {
            showToast('Order status updated');
            loadAdminOrders();
        } else {
            showToast('Failed to update status', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
};

window.cancelOrder = async (id) => {
    if (!confirm('Are you sure you want to cancel this order?')) return;
    try {
        const res = await fetchWithAuth(`/orders/${id}`, { method: 'DELETE' });
        if (res.ok) {
            showToast('Order cancelled');
            loadAdminOrders();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to cancel order', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
};

generateInvoiceForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const orderId = document.getElementById('invoice-order-id').value;
    try {
        const res = await fetchWithAuth(`/billing/generate/${orderId}`, { method: 'POST' });
        if (res.ok) {
            const invoice = await res.json();
            billingResult.innerHTML = `
                <div style="color:var(--success-color); margin-bottom:10px;">Invoice #${invoice.id} Generated Successfully</div>
                <div>Subtotal: ₹${invoice.subtotal.toFixed(2)}</div>
                <div>Tax: ₹${invoice.tax_amount.toFixed(2)}</div>
                <div><strong>Total: ₹${invoice.total_amount.toFixed(2)}</strong></div>
                <div>Status: ${invoice.payment_status}</div>
            `;
            showToast('Invoice generated!');
        } else {
            const data = await res.json();
            showToast(data.detail || 'Failed to generate invoice', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

async function loadInventory() {
    try {
        const res = await fetchWithAuth('/inventory/ingredients');
        if (res.ok) {
            const items = await res.json();
            tableInventory.innerHTML = '';
            if (items.length === 0) {
                tableInventory.innerHTML = '<tr><td colspan="5" class="empty-state">No inventory ingredients found.</td></tr>';
                return;
            }
            items.forEach(item => {
                tableInventory.innerHTML += `
                    <tr>
                        <td>#${item.id}</td>
                        <td>${item.name}</td>
                        <td style="color:${item.stock_level < item.minimum_stock_level ? 'var(--error-color)' : 'inherit'}">
                            ${item.stock_level.toFixed(2)} ${item.stock_level < item.minimum_stock_level ? ' (Low)' : ''}
                        </td>
                        <td>${item.unit}</td>
                        <td>
                            <button class="btn btn-sm btn-outline" onclick="updateStock(${item.id})">Update Stock</button>
                        </td>
                    </tr>`;
            });
        }
    } catch (err) { console.error(err); showToast('Failed to load inventory', 'error'); }
}

const btnAddIngredient = document.getElementById('btn-add-ingredient');
const btnCancelIngredient = document.getElementById('btn-cancel-ingredient');
const ingredientForm = document.getElementById('ingredient-form');

btnAddIngredient?.addEventListener('click', () => {
    ingredientForm.reset();
    ingredientForm.classList.add('active');
});

btnCancelIngredient?.addEventListener('click', () => {
    ingredientForm.classList.remove('active');
});

ingredientForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('ingredient-name').value,
        unit: document.getElementById('ingredient-unit').value,
        minimum_stock_level: parseFloat(document.getElementById('ingredient-min-stock').value),
        stock_level: parseFloat(document.getElementById('ingredient-initial-stock').value),
        supplier_id: null
    };

    try {
        const res = await fetchWithAuth('/inventory/ingredients', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Ingredient added successfully!');
            ingredientForm.classList.remove('active');
            loadInventory();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to add ingredient', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

const btnAddSupplier = document.getElementById('btn-add-supplier');
const btnCancelSupplier = document.getElementById('btn-cancel-supplier');
const supplierForm = document.getElementById('supplier-form');

btnAddSupplier?.addEventListener('click', () => {
    supplierForm.reset();
    supplierForm.classList.add('active');
});

btnCancelSupplier?.addEventListener('click', () => {
    supplierForm.classList.remove('active');
});

supplierForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('supplier-name').value,
        contact_person: document.getElementById('supplier-contact').value,
        email: document.getElementById('supplier-email').value || null,
        phone: document.getElementById('supplier-phone').value || null
    };

    try {
        const res = await fetchWithAuth('/inventory/suppliers', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Supplier added successfully!');
            supplierForm.classList.remove('active');
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to add supplier', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

window.updateStock = async (id) => {
    const input = prompt("Enter quantity to add (use negative number to subtract):");
    if (input === null || input.trim() === '') return;
    
    const qty = parseFloat(input);
    if (isNaN(qty) || qty === 0) {
        showToast('Please enter a valid non-zero quantity.', 'error');
        return;
    }

    const payload = {
        transaction_type: qty > 0 ? 'IN' : 'OUT',
        quantity: Math.abs(qty),
        remarks: 'Manual update from dashboard'
    };

    try {
        const res = await fetchWithAuth(`/inventory/ingredients/${id}/stock`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Stock updated successfully!');
            loadInventory();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to update stock', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
};

// REPORTS LOGIC

async function loadReports() {
    try {
        const [salesRes, topItemsRes, revRes, invRes, custRes] = await Promise.all([
            fetchWithAuth('/reports/sales'),
            fetchWithAuth('/reports/top-items'),
            fetchWithAuth('/reports/revenue'),
            fetchWithAuth('/reports/inventory-consumption'),
            fetchWithAuth('/reports/customers')
        ]);

        if (salesRes.ok) {
            const summary = await salesRes.json();
            reportOrders.textContent = summary.total_orders;
            reportRevenue.textContent = `₹${summary.total_revenue.toFixed(2)}`;
            reportAov.textContent = `₹${summary.average_order_value.toFixed(2)}`;
        }

        if (topItemsRes.ok) {
            const topItems = await topItemsRes.json();
            const tableTopItems = document.getElementById('table-report-top-items');
            tableTopItems.innerHTML = topItems.length ? '' : '<tr><td colspan="2" class="empty-state">No data</td></tr>';
            topItems.forEach(i => tableTopItems.innerHTML += `<tr><td>${i.name}</td><td>${i.total_quantity_sold}</td></tr>`);
        }

        if (revRes.ok) {
            const revenue = await revRes.json();
            const tableRevenue = document.getElementById('table-report-revenue');
            tableRevenue.innerHTML = revenue.length ? '' : '<tr><td colspan="2" class="empty-state">No data</td></tr>';
            revenue.forEach(r => tableRevenue.innerHTML += `<tr><td>${r.payment_method}</td><td>₹${r.total_revenue.toFixed(2)}</td></tr>`);
        }

        if (invRes.ok) {
            const inventory = await invRes.json();
            const tableInv = document.getElementById('table-report-inventory');
            tableInv.innerHTML = inventory.length ? '' : '<tr><td colspan="2" class="empty-state">No data</td></tr>';
            inventory.forEach(i => tableInv.innerHTML += `<tr><td>${i.name}</td><td>${i.total_consumed.toFixed(2)} ${i.unit}</td></tr>`);
        }

        if (custRes.ok) {
            const customers = await custRes.json();
            const tableCust = document.getElementById('table-report-customers');
            tableCust.innerHTML = customers.length ? '' : '<tr><td colspan="3" class="empty-state">No data</td></tr>';
            customers.forEach(c => tableCust.innerHTML += `<tr><td>#${c.customer_id}</td><td>${c.total_orders}</td><td>₹${c.total_spent.toFixed(2)}</td></tr>`);
        }

    } catch (err) { console.error(err); showToast('Failed to load reports', 'error'); }
}

// RESERVATIONS LOGIC

async function loadReservations() {
    loadTables();
    try {
        const res = await fetchWithAuth('/reservations');
        if (res.ok) {
            const resvs = await res.json();
            tableReservations.innerHTML = '';
            if (resvs.length === 0) {
                tableReservations.innerHTML = '<tr><td colspan="6" class="empty-state">No reservations found.</td></tr>';
                return;
            }
            resvs.forEach(r => {
                const date = new Date(r.reservation_time).toLocaleString();
                let actions = '';
                if (r.status === 'Pending' || r.status === 'Approved') {
                    actions = `
                        <button class="btn btn-sm btn-outline" onclick="updateReservationStatus(${r.id}, 'Completed')">Complete</button>
                        <button class="btn btn-sm btn-outline" onclick="updateReservationStatus(${r.id}, 'Cancelled')">Cancel</button>
                    `;
                }
                tableReservations.innerHTML += `
                    <tr>
                        <td>#${r.id}</td>
                        <td>${r.table_id}</td>
                        <td>${date}</td>
                        <td>${r.number_of_guests} Guests</td>
                        <td>${r.status}</td>
                        <td>${actions}</td>
                    </tr>`;
            });
        }
    } catch (err) { console.error(err); showToast('Failed to load reservations', 'error'); }
}

async function loadTables() {
    try {
        const res = await fetchWithAuth('/reservations/tables');
        if (res.ok) {
            const tables = await res.json();
            const select = document.getElementById('book-table-id');
            if(select) {
                select.innerHTML = '<option value="">Select Table...</option>';
                tables.forEach(t => select.innerHTML += `<option value="${t.id}">Table ${t.table_number} (Cap: ${t.capacity})</option>`);
            }
        }
    } catch (err) { console.error(err); }
}

document.getElementById('form-add-table')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        table_number: document.getElementById('res-table-number').value,
        capacity: parseInt(document.getElementById('res-table-capacity').value)
    };
    try {
        const res = await fetchWithAuth('/reservations/tables', { method: 'POST', body: JSON.stringify(payload) });
        if(res.ok) {
            showToast('Table added successfully');
            document.getElementById('form-add-table').reset();
            loadTables();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to add table', 'error');
        }
    } catch(err) { showToast('Error', 'error'); }
});

document.getElementById('form-book-table')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        customer_id: window.currentUserId,
        table_id: parseInt(document.getElementById('book-table-id').value),
        reservation_time: document.getElementById('book-time').value,
        number_of_guests: parseInt(document.getElementById('book-guests').value)
    };
    try {
        const res = await fetchWithAuth('/reservations', { method: 'POST', body: JSON.stringify(payload) });
        if(res.ok) {
            showToast('Table booked successfully');
            document.getElementById('form-book-table').reset();
            loadReservations();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to book table', 'error');
        }
    } catch(err) { showToast('Error', 'error'); }
});

window.updateReservationStatus = async (id, status) => {
    try {
        const res = await fetchWithAuth(`/reservations/${id}/status`, { 
            method: 'PUT',
            body: JSON.stringify({ status: status }) 
        });
        if(res.ok) {
            showToast(`Reservation marked as ${status}`);
            loadReservations();
        } else showToast('Failed to update status', 'error');
    } catch (err) { showToast('Error', 'error'); }
};

// FEEDBACK LOGIC
document.getElementById('form-submit-feedback')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        customer_id: parseInt(document.getElementById('fb-customer-id').value),
        rating: parseInt(document.getElementById('fb-rating').value),
        is_complaint: document.getElementById('fb-is-complaint').checked
    };
    
    const orderId = document.getElementById('fb-order-id').value;
    if (orderId) payload.order_id = parseInt(orderId);
    
    const comments = document.getElementById('fb-comments').value;
    if (comments) payload.comments = comments;

    try {
        const res = await fetchWithAuth('/feedback', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Feedback submitted successfully!');
            e.target.reset();
            loadFeedback();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to submit feedback', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

async function loadFeedback() {
    try {
        const res = await fetchWithAuth('/feedback');
        if (res.ok) {
            const fbs = await res.json();
            tableFeedback.innerHTML = '';
            if (fbs.length === 0) {
                tableFeedback.innerHTML = '<tr><td colspan="7" class="empty-state">No feedback found.</td></tr>';
                return;
            }
            fbs.forEach(fb => {
                let actions = '';
                if (fb.is_complaint && fb.status !== 'Resolved') {
                    actions = `<button class="btn btn-sm btn-outline" onclick="resolveFeedback(${fb.id})">Resolve</button>`;
                }
                tableFeedback.innerHTML += `
                    <tr>
                        <td>#${fb.id}</td>
                        <td>Cust #${fb.customer_id}</td>
                        <td>${fb.order_id ? '#' + fb.order_id : '-'}</td>
                        <td>${fb.rating} / 5</td>
                        <td>${fb.comments || '-'}</td>
                        <td>${fb.status}</td>
                        <td>${actions}</td>
                    </tr>`;
            });
        }
    } catch (err) { console.error(err); showToast('Failed to load feedback', 'error'); }
}

window.resolveFeedback = async (id) => {
    const notes = prompt("Enter resolution notes:");
    if (notes === null) return;
    
    try {
        const res = await fetchWithAuth(`/feedback/${id}/resolve`, {
            method: 'PUT',
            body: JSON.stringify({ status: 'Resolved', resolution_notes: notes })
        });
        if (res.ok) {
            showToast('Feedback resolved!');
            loadFeedback();
        } else showToast('Failed to resolve feedback', 'error');
    } catch (err) { showToast('Error', 'error'); }
};

// EMPLOYEES LOGIC
const tableEmployees = document.getElementById('table-employees');
document.getElementById('btn-refresh-employees')?.addEventListener('click', loadEmployees);

async function loadEmployees() {
    try {
        const res = await fetchWithAuth('/employees');
        if (res.ok) {
            const emps = await res.json();
            tableEmployees.innerHTML = '';
            if (emps.length === 0) {
                tableEmployees.innerHTML = '<tr><td colspan="5" class="empty-state">No employees found.</td></tr>';
                return;
            }
            emps.forEach(emp => {
                tableEmployees.innerHTML += `
                    <tr>
                        <td>#${emp.id}</td>
                        <td>${emp.name}</td>
                        <td>${emp.role}</td>
                        <td>${emp.is_active ? 'Active' : 'Inactive'}</td>
                        <td>
                            <button class="btn btn-sm btn-outline" onclick="markAttendance(${emp.id})">Mark Present</button>
                        </td>
                    </tr>`;
            });
        }
    } catch (err) { console.error(err); showToast('Failed to load employees', 'error'); }
}

const btnAddEmployee = document.getElementById('btn-add-employee');
const btnCancelEmployee = document.getElementById('btn-cancel-employee');
const employeeForm = document.getElementById('employee-form');

btnAddEmployee?.addEventListener('click', () => {
    employeeForm.reset();
    employeeForm.classList.add('active');
});

btnCancelEmployee?.addEventListener('click', () => {
    employeeForm.classList.remove('active');
});

employeeForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById('emp-name').value,
        email: document.getElementById('emp-email').value,
        phone: document.getElementById('emp-phone').value || null,
        role: document.getElementById('emp-role').value,
        salary: parseFloat(document.getElementById('emp-salary').value) || 0
    };

    try {
        const res = await fetchWithAuth('/employees', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Employee added successfully!');
            employeeForm.classList.remove('active');
            loadEmployees();
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to add employee', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
});

window.markAttendance = async (id) => {
    const payload = { status: 'Present' };
    try {
        const res = await fetchWithAuth(`/employees/${id}/attendance`, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            showToast('Attendance marked successfully!');
        } else {
            const err = await res.json();
            showToast(err.detail || 'Failed to mark attendance', 'error');
        }
    } catch (err) { showToast('Network error', 'error'); }
};


// Init
checkAuth();
