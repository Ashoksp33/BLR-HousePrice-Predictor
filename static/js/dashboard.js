// dashboard.js - Sidebar Collapse/Expand, Clickable Profile Navigation, Theme Switcher & Meta AI Chatbot

document.addEventListener('DOMContentLoaded', () => {
    // Theme Switcher Logic
    const themeSwitch = document.getElementById('themeSwitch');
    const savedTheme = localStorage.getItem('appTheme') || 'dark';

    function applyTheme(theme) {
        if (theme === 'light') {
            document.body.setAttribute('data-theme', 'light');
            if (themeSwitch) themeSwitch.checked = true;
        } else {
            document.body.removeAttribute('data-theme');
            if (themeSwitch) themeSwitch.checked = false;
        }
        localStorage.setItem('appTheme', theme);
    }

    applyTheme(savedTheme);

    if (themeSwitch) {
        themeSwitch.addEventListener('change', () => {
            const newTheme = themeSwitch.checked ? 'light' : 'dark';
            applyTheme(newTheme);
        });
    }

    // Sidebar Collapse / Expand Toggle
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const btnToggleSidebar = document.getElementById('btnToggleSidebar');

    const savedCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (savedCollapsed && sidebar && mainContent) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
    }

    if (btnToggleSidebar && sidebar && mainContent) {
        btnToggleSidebar.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
            localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
        });
    }

    // Sidebar View Navigation
    const navItems = document.querySelectorAll('.nav-item[data-view]');
    const viewPanels = document.querySelectorAll('.view-panel');

    function switchView(targetView) {
        if (!targetView) return;
        navItems.forEach(n => {
            if (n.getAttribute('data-view') === targetView) {
                n.classList.add('active');
            } else {
                n.classList.remove('active');
            }
        });

        viewPanels.forEach(panel => {
            if (panel.id === `view-${targetView}`) {
                panel.classList.add('active');
            } else {
                panel.classList.remove('active');
            }
        });

        if (targetView === 'valuations') {
            loadSavedValuations();
        }
    }

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            const targetView = item.getAttribute('data-view');
            e.preventDefault();
            switchView(targetView);
        });
    });

    // CLICK USER PROFILE CARD IN SIDEBAR -> NAVIGATE DIRECTLY TO SETTINGS & PROFILE
    const sidebarUser = document.getElementById('sidebarUserCard');
    if (sidebarUser) {
        sidebarUser.addEventListener('click', () => {
            switchView('settings');
        });
    }

    // Profile Sub-Panel Navigation
    const profileMenuItems = document.querySelectorAll('.profile-menu-item[data-subtab]');
    profileMenuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const subtab = item.getAttribute('data-subtab');
            if (!subtab) return;

            profileMenuItems.forEach(m => m.classList.remove('active'));
            item.classList.add('active');

            document.querySelectorAll('.profile-sub-panel').forEach(p => p.style.display = 'none');
            const targetPanel = document.getElementById(`subpanel-${subtab}`);
            if (targetPanel) {
                targetPanel.style.display = 'block';
            }

            if (subtab === 'valuations') {
                loadSavedValuations();
            }
        });
    });

    // Avatar Upload Handler
    const avatarInput = document.getElementById('avatarFileInput');
    const avatarWrapper = document.getElementById('avatarWrapper');

    if (avatarWrapper && avatarInput) {
        avatarWrapper.addEventListener('click', () => avatarInput.click());

        avatarInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = async (evt) => {
                const base64Avatar = evt.target.result;
                
                document.querySelectorAll('.user-avatar, .profile-main-avatar').forEach(img => img.src = base64Avatar);

                try {
                    const res = await fetch('/api/user/avatar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ avatar: base64Avatar })
                    });
                    const data = await res.json();
                    if (data.success) {
                        alert("Profile photo uploaded and saved successfully!");
                    } else {
                        alert(data.message || "Failed to save avatar photo.");
                    }
                } catch (err) {
                    alert("Error uploading profile photo.");
                }
            };
            reader.readAsDataURL(file);
        });
    }

    // Prediction Form Submit
    const predictForm = document.getElementById('predictForm');
    const locationSelect = document.getElementById('location');

    if (predictForm) {
        predictForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            await runPrediction();
        });

        locationSelect.addEventListener('change', async () => {
            const selectedLocation = locationSelect.value;
            await loadLocationInfra(selectedLocation);
        });
    }

    // Public Places Tab switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const tabTarget = btn.getAttribute('data-tab');
            document.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
            const targetEl = document.getElementById(`tab-${tabTarget}`);
            if (targetEl) targetEl.style.display = 'grid';
        });
    });

    // Save Prediction Handler
    const btnSaveValuation = document.getElementById('btnSaveValuation');
    if (btnSaveValuation) {
        btnSaveValuation.addEventListener('click', async () => {
            if (!currentPrediction) {
                alert("Please run a house price prediction first!");
                return;
            }

            try {
                const res = await fetch('/api/valuations/save', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        location: currentPrediction.location,
                        sqft: currentPrediction.sqft,
                        bhk: currentPrediction.bhk,
                        bath: currentPrediction.bath,
                        price_inr: currentPrediction.formatted_price_inr,
                        price_usd: currentPrediction.formatted_price_usd
                    })
                });
                const data = await res.json();
                if (data.success) {
                    alert("Valuation saved to your account history!");
                    loadSavedValuations();
                } else {
                    alert(data.message || "Failed to save valuation");
                }
            } catch (err) {
                alert("Error saving valuation");
            }
        });
    }

    // Profile Update Form Submit
    const profileForm = document.getElementById('profileForm');
    if (profileForm) {
        profileForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('profName').value;
            const email = document.getElementById('profEmail').value;
            const role = document.getElementById('profRole').value;

            try {
                const res = await fetch('/api/user/update', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, role })
                });
                const data = await res.json();
                if (data.success) {
                    alert("Profile updated successfully!");
                    document.getElementById('sidebarUserName').textContent = name;
                    document.getElementById('sidebarUserRole').textContent = role;
                    document.getElementById('profileHeaderName').textContent = name;
                    document.getElementById('profileHeaderEmail').textContent = email;
                } else {
                    alert(data.message || "Failed to update profile.");
                }
            } catch (err) {
                alert("Server error during profile update.");
            }
        });
    }

    // FAQ Accordion click toggle
    document.querySelectorAll('.faq-question').forEach(q => {
        q.addEventListener('click', () => {
            const item = q.parentElement;
            item.classList.toggle('active');
        });
    });

    // META AI / WHATSAPP CHATBOT LOGIC
    const metaChatTrigger = document.getElementById('metaChatTrigger');
    const chatWindow = document.getElementById('chatWindow');
    const btnCloseChat = document.getElementById('btnCloseChat');
    const chatInput = document.getElementById('chatInput');
    const btnSendChat = document.getElementById('btnSendChat');
    const chatMessages = document.getElementById('chatMessages');

    if (metaChatTrigger && chatWindow) {
        metaChatTrigger.addEventListener('click', () => {
            const isVisible = chatWindow.style.display === 'flex';
            chatWindow.style.display = isVisible ? 'none' : 'flex';
            if (!isVisible && chatInput) chatInput.focus();
        });

        if (btnCloseChat) {
            btnCloseChat.addEventListener('click', () => chatWindow.style.display = 'none');
        }

        async function sendChatMessage(msgText) {
            const text = msgText || (chatInput ? chatInput.value.trim() : '');
            if (!text) return;

            // Append User Message Bubble
            appendChatBubble(text, 'user');
            if (chatInput) chatInput.value = '';

            // Append AI Typing Indicator
            const typingBubble = appendChatBubble('typing...', 'ai');

            try {
                const res = await fetch('/api/chatbot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });
                const data = await res.json();
                typingBubble.remove();
                appendChatBubble(data.reply || "I couldn't fetch that information right now.", 'ai');
            } catch (err) {
                typingBubble.remove();
                appendChatBubble("Sorry, I experienced a connection error. Please try again!", 'ai');
            }
        }

        if (btnSendChat) {
            btnSendChat.addEventListener('click', () => sendChatMessage());
        }

        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendChatMessage();
            });
        }

        // Chip Prompts Click Handler
        document.querySelectorAll('.chip-prompt').forEach(chip => {
            chip.addEventListener('click', () => {
                const promptText = chip.getAttribute('data-prompt') || chip.textContent;
                sendChatMessage(promptText);
            });
        });
    }

    function appendChatBubble(text, sender) {
        if (!chatMessages) return;
        const bubble = document.createElement('div');
        bubble.className = `msg-bubble ${sender}`;
        bubble.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return bubble;
    }

    // Run initial prediction
    runPrediction();
});

let currentPrediction = null;

async function runPrediction() {
    const location = document.getElementById('location').value;
    const sqft = document.getElementById('sqft').value;
    const bhk = document.getElementById('bhk').value;
    const bath = document.getElementById('bath').value;
    const balcony = document.getElementById('balcony').value;
    const area_type = document.getElementById('area_type').value;
    const ready_status = document.getElementById('ready_status').value;

    const btnPredict = document.getElementById('btnPredict');
    btnPredict.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Calculating Price...`;
    btnPredict.disabled = true;

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ location, sqft, bhk, bath, balcony, area_type, ready_status })
        });
        const data = await res.json();

        if (data.success) {
            currentPrediction = data.prediction;
            const p = data.prediction;
            document.getElementById('resLocation').textContent = p.location;
            
            document.getElementById('resPriceInr').textContent = p.formatted_price_inr;
            document.getElementById('resPriceUsd').textContent = `${p.formatted_price_usd} (Est. Valuation)`;
            document.getElementById('resRupees').textContent = `INR Total: ₹ ${p.rupees.toLocaleString('en-IN')}`;
            document.getElementById('resRange').textContent = `Range: ${p.formatted_price_inr} (${p.min_price_lakhs}L - ${p.max_price_lakhs}L)  •  $${p.min_price_usd.toLocaleString()} - $${p.max_price_usd.toLocaleString()} USD`;
            
            document.getElementById('resPriceSqft').innerHTML = `₹ ${p.price_per_sqft_inr.toLocaleString('en-IN')}<br><small style="font-size:11px; opacity:0.8">($${p.price_per_sqft_usd} USD / sqft)</small>`;
            document.getElementById('resEmi').innerHTML = `₹ ${p.estimated_emi_inr.toLocaleString('en-IN')}<br><small style="font-size:11px; opacity:0.8">($${p.estimated_emi_usd.toLocaleString()} USD / mo)</small>`;

            await loadLocationInfra(location);
        } else {
            alert(data.message || "Failed to calculate prediction");
        }
    } catch (err) {
        console.error(err);
    } finally {
        btnPredict.innerHTML = `<i class="fa-solid fa-calculator"></i> Predict House Price`;
        btnPredict.disabled = false;
    }
}

async function loadSavedValuations() {
    try {
        const res = await fetch('/api/valuations');
        const data = await res.json();
        
        ['savedValuationsContainer', 'savedValuationsContainerSettings'].forEach(containerId => {
            const container = document.getElementById(containerId);
            if (!container) return;

            if (data.success && data.valuations.length > 0) {
                container.innerHTML = `
                    <table class="valuations-table">
                        <thead>
                            <tr>
                                <th>Location</th>
                                <th>Details</th>
                                <th>INR Price</th>
                                <th>USD Price</th>
                                <th>Date</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.valuations.map(v => `
                                <tr>
                                    <td><strong>${v.location}</strong></td>
                                    <td>${v.sqft} sqft (${v.bhk} BHK, ${v.bath} Bath)</td>
                                    <td style="color:#10b981; font-weight:700">${v.price_inr}</td>
                                    <td style="color:#38bdf8; font-weight:700">${v.price_usd}</td>
                                    <td style="font-size:12px; color:var(--text-muted)">${new Date(v.created_at).toLocaleDateString()}</td>
                                    <td>
                                        <button class="btn-delete" onclick="deleteValuation(${v.id})">
                                            <i class="fa-solid fa-trash"></i> Delete
                                        </button>
                                    </td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;
            } else {
                container.innerHTML = `<p style="color:var(--text-muted); font-size:14px;">No saved valuations yet. Click <strong>Save Prediction</strong> on the Dashboard to bookmark predictions!</p>`;
            }
        });
    } catch (err) {
        console.error(err);
    }
}

async function deleteValuation(id) {
    if (!confirm("Are you sure you want to delete this saved valuation?")) return;
    try {
        const res = await fetch(`/api/valuations/${id}`, { method: 'DELETE' });
        const data = await res.json();
        if (data.success) {
            loadSavedValuations();
        }
    } catch (err) {
        console.error(err);
    }
}

async function loadLocationInfra(locationName) {
    try {
        const res = await fetch(`/api/location_info/${encodeURIComponent(locationName)}`);
        const infra = await res.json();

        // Populate Hospitals
        const hospGrid = document.getElementById('tab-hospitals');
        if (hospGrid) {
            hospGrid.innerHTML = infra.hospitals.map(h => `
                <div class="infra-card">
                    <div class="title"><i class="fa-solid fa-hospital-user" style="color:#ef4444"></i> ${h.name}</div>
                    <div class="tag">${h.type}</div>
                    <div class="detail"><i class="fa-solid fa-location-dot"></i> Distance: <strong>${h.distance}</strong></div>
                    <div class="detail"><i class="fa-solid fa-map-pin"></i> Area: ${h.address}</div>
                    <div class="detail"><i class="fa-solid fa-phone"></i> Emergency: ${h.contact}</div>
                    <div class="detail"><i class="fa-solid fa-star" style="color:#f59e0b"></i> Rating: ${h.rating} / 5.0</div>
                </div>
            `).join('');
        }

        // Populate Metro
        const metroGrid = document.getElementById('tab-metro');
        if (metroGrid) {
            metroGrid.innerHTML = infra.metro.map(m => `
                <div class="infra-card">
                    <div class="title"><i class="fa-solid fa-train-subway" style="color:#a855f7"></i> ${m.station}</div>
                    <div class="tag"><i class="fa-solid fa-subway"></i> ${m.line}</div>
                    <div class="detail"><i class="fa-solid fa-location-dot"></i> Distance: <strong>${m.distance}</strong></div>
                    <div class="detail"><i class="fa-solid fa-door-open"></i> Gate Info: ${m.gate || 'Main Station Entrance'}</div>
                    <div class="detail"><i class="fa-solid fa-circle-check" style="color:#10b981"></i> Status: ${m.status}</div>
                </div>
            `).join('');
        }

        // Populate Bus Stops
        const busGrid = document.getElementById('tab-bus');
        if (busGrid) {
            busGrid.innerHTML = infra.bus_stops.map(b => `
                <div class="infra-card">
                    <div class="title"><i class="fa-solid fa-bus" style="color:#3b82f6"></i> ${b.name}</div>
                    <div class="detail"><i class="fa-solid fa-location-dot"></i> Distance: <strong>${b.distance}</strong></div>
                    <div class="detail"><i class="fa-solid fa-map"></i> Location: ${b.location || 'Main Junction'}</div>
                    <div class="detail"><i class="fa-solid fa-route"></i> BMTC Routes: ${b.routes}</div>
                </div>
            `).join('');
        }

        // Populate Airport
        const airportGrid = document.getElementById('tab-airport');
        if (airportGrid) {
            const a = infra.airport;
            airportGrid.innerHTML = `
                <div class="infra-card" style="grid-column: 1 / -1">
                    <div class="title"><i class="fa-solid fa-plane-departure" style="color:#38bdf8"></i> Kempegowda International Airport (BLR)</div>
                    <div class="detail" style="margin-top:6px;"><i class="fa-solid fa-route"></i> <strong>Highway Distance:</strong> ${a.distance}</div>
                    <div class="detail"><i class="fa-solid fa-clock"></i> <strong>Est. Travel Time:</strong> ${a.travel_time}</div>
                    <div class="detail"><i class="fa-solid fa-bus-simple"></i> <strong>Vaju Veer Airport Shuttle (KIAS):</strong> ${a.kias_bus}</div>
                </div>
            `;
        }

        // Populate Schools
        const schoolGrid = document.getElementById('tab-schools');
        if (schoolGrid) {
            schoolGrid.innerHTML = infra.schools.map(s => `
                <div class="infra-card">
                    <div class="title"><i class="fa-solid fa-graduation-cap" style="color:#f59e0b"></i> ${s.name}</div>
                    <div class="tag">Board: ${s.board}</div>
                    <div class="detail"><i class="fa-solid fa-location-dot"></i> Distance: ${s.distance}</div>
                </div>
            `).join('');
        }

        // Populate Tech Parks
        const techGrid = document.getElementById('tab-tech');
        if (techGrid) {
            techGrid.innerHTML = infra.tech_parks.map(t => `
                <div class="infra-card">
                    <div class="title"><i class="fa-solid fa-building" style="color:#10b981"></i> ${t.name}</div>
                    <div class="detail"><i class="fa-solid fa-location-dot"></i> Distance: ${t.distance}</div>
                    <div class="detail"><i class="fa-solid fa-laptop-code"></i> Companies: ${t.companies}</div>
                </div>
            `).join('');
        }

    } catch (err) {
        console.error("Error loading location infra:", err);
    }
}
