let accessToken = "";

const loginForm = document.getElementById("login-form");
const patientForm = document.getElementById("patient-form");
const visitForm = document.getElementById("visit-form");
const patientList = document.getElementById("patient-list");
const searchInput = document.getElementById("search-input");

function setStatus(id, message, isError = false) {
  const el = document.getElementById(id);
  el.textContent = message;
  el.style.color = isError ? "#8a1c1c" : "";
}

async function api(path, options = {}) {
  const headers = options.headers || {};
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const response = await fetch(path, { ...options, headers });
  if (!response.ok) {
    let detail = "Request failed";
    try {
      const data = await response.json();
      detail = data.detail || detail;
    } catch (error) {
      detail = response.statusText || detail;
    }
    throw new Error(detail);
  }

  if (response.status === 204) {
    return null;
  }
  return response.json();
}

function normalizePayload(payload) {
  return Object.fromEntries(
    Object.entries(payload).map(([key, value]) => [key, value === "" ? null : value])
  );
}

function renderPatients(items) {
  if (!items.length) {
    patientList.innerHTML = '<p class="muted">No patients found.</p>';
    return;
  }

  patientList.innerHTML = items
    .map(
      (patient) => `
        <div class="list-item">
          <strong>${patient.first_name} ${patient.last_name}</strong><br />
          ID ${patient.id} · ${patient.patient_code}<br />
          DOB ${patient.date_of_birth}${patient.phone ? ` · ${patient.phone}` : ""}
        </div>
      `
    )
    .join("");
}

async function loadPatients(query = "") {
  if (!accessToken) {
    return;
  }

  try {
    const suffix = query ? `?q=${encodeURIComponent(query)}` : "";
    const items = await api(`/api/v1/patients${suffix}`);
    renderPatients(items);
  } catch (error) {
    setStatus("patient-status", error.message, true);
  }
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);
  try {
    const result = await api("/api/v1/auth/login", {
      method: "POST",
      body: formData,
    });
    accessToken = result.access_token;
    setStatus("login-status", `Signed in as ${result.user.full_name}`);
    setStatus("patient-status", "");
    setStatus("visit-status", "");
    loadPatients();
  } catch (error) {
    setStatus("login-status", error.message, true);
  }
});

patientForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = normalizePayload(Object.fromEntries(new FormData(patientForm).entries()));

  try {
    const patient = await api("/api/v1/patients", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setStatus("patient-status", `Saved patient #${patient.id}`);
    patientForm.reset();
    loadPatients(searchInput.value);
  } catch (error) {
    setStatus("patient-status", error.message, true);
  }
});

visitForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = normalizePayload(Object.fromEntries(new FormData(visitForm).entries()));
  payload.patient_id = Number(payload.patient_id);
  payload.visit_date = new Date(payload.visit_date).toISOString();

  try {
    const visit = await api("/api/v1/visits", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    setStatus("visit-status", `Saved visit #${visit.id}`);
    visitForm.reset();
  } catch (error) {
    setStatus("visit-status", error.message, true);
  }
});

searchInput.addEventListener("input", (event) => {
  loadPatients(event.target.value);
});
