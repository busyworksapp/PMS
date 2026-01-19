// API Client
const API_BASE_URL = "http://localhost:8000/api";

async function apiCall(method, endpoint, body = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  const token = localStorage.getItem("access_token");
  if (token) {
    options.headers["Authorization"] = `Bearer ${token}`;
  }

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "API Error");
    }

    return data;
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
}

// Authentication
async function login(username, password) {
  const data = await apiCall("POST", "/auth/login", {
    username,
    password,
  });
  localStorage.setItem("access_token", data.access_token);
  return data;
}

async function operatorLogin(employeeNumber) {
  const data = await apiCall("POST", "/auth/operator-login", {
    employee_number: employeeNumber,
    password: employeeNumber,
  });
  localStorage.setItem("access_token", data.access_token);
  return data;
}

function logout() {
  localStorage.removeItem("access_token");
  window.location.href = "/login.html";
}

function getToken() {
  return localStorage.getItem("access_token");
}

function isLoggedIn() {
  return !!localStorage.getItem("access_token");
}

// UI Helpers
function showAlert(message, type = "info") {
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type}`;
  alertDiv.textContent = message;
  document.body.insertBefore(alertDiv, document.body.firstChild);
  setTimeout(() => alertDiv.remove(), 5000);
}

function showModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add("active");
}

function hideModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString();
}

function formatDateTime(dateString) {
  return new Date(dateString).toLocaleString();
}

// Redirect if not logged in
function requireAuth() {
  if (!isLoggedIn()) {
    window.location.href = "/login.html";
  }
}

// Close modal when clicking outside
document.addEventListener("click", function (event) {
  if (event.target.classList.contains("modal")) {
    event.target.classList.remove("active");
  }
});

// Close modal with close button
document.addEventListener("click", function (event) {
  if (event.target.classList.contains("modal-close")) {
    const modal = event.target.closest(".modal");
    if (modal) {
      modal.classList.remove("active");
    }
  }
});
