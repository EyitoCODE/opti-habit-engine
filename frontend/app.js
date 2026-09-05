/**
 * Opti-Habit Engine: Client-Side Controller
 * Communicates with the FastAPI backend to render habits and initiate verification.
 */
const API_BASE_URL = "/api/habits";

const habitsList = document.getElementById("habits-list");
const habitForm = document.getElementById("habit-form");
const toast = document.getElementById("status-toast");

function showToast(message, duration = 3000) {
    toast.textContent = message;
    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("hidden");
    }, duration);
}

async function loadHabits() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (!response.ok) throw new Error("Could not retrieve habit records.");
        const habits = await response.json();
        renderHabits(habits);
    } catch (error) {
        habitsList.innerHTML = `<p class="error-msg">Error loading habits: ${error.message}</p>`;
    }
}

function renderHabits(habits) {
    if (habits.length === 0) {
        habitsList.innerHTML = `<p class="empty-msg">No active habits registered yet.</p>`;
        return;
    }

    habitsList.innerHTML = habits.map(h => {
        const percent = Math.min(100, Math.round((h.current_momentum / h.weight) * 100));
        return `
            <div class="habit-item">
                <div>
                    <div class="habit-name">${escapeHtml(h.title)}</div>
                    <div class="habit-stats">
                        <div class="stat-row">
                            <span>Momentum:</span>
                            <span class="stat-val">${h.current_momentum.toFixed(2)}</span>
                        </div>
                        <div class="stat-row">
                            <span>Target Weight:</span>
                            <span class="stat-val">${h.weight.toFixed(1)}</span>
                        </div>
                        <div class="progress-bar-bg">
                            <div class="progress-bar-fill" style="width: ${percent}%;"></div>
                        </div>
                    </div>
                </div>
                <button class="btn verify-btn" onclick="verifyHabit(${h.id})">
                    Scan Object to Verify
                </button>
            </div>
        `;
    }).join("");
}

async function verifyHabit(id) {
    showToast("Launching optical sensor. Please present physical object to camera...");
    try {
        const response = await fetch(`${API_BASE_URL}/${id}/verify`, { method: "POST" });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.detail || "Verification failed.");
        }
        showToast(`Verification success. New score: ${result.new_momentum_score}`);
        loadHabits();
    } catch (error) {
        showToast(`Error: ${error.message}`, 4000);
    }
}

habitForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const titleInput = document.getElementById("habit-title");
    const weightInput = document.getElementById("habit-weight");

    const payload = {
        title: titleInput.value.trim(),
        weight: parseFloat(weightInput.value)
    };

    try {
        const response = await fetch(`${API_BASE_URL}/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        if (!response.ok) throw new Error("Could not create habit record.");
        titleInput.value = "";
        weightInput.value = "1.0";
        showToast("Habit registered successfully.");
        loadHabits();
    } catch (error) {
        showToast(`Error: ${error.message}`);
    }
});

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

// Initial data load on startup
loadHabits();