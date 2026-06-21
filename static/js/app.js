// ============================================================
// SemanticPath - Frontend Application Logic
// ============================================================

document.addEventListener("DOMContentLoaded", () => {
    // ----- Element references -----
    const inputView = document.getElementById("input-view");
    const loadingView = document.getElementById("loading-view");
    const resultsView = document.getElementById("results-view");
    const careerSelect = document.getElementById("career-select");
    const skillsInput = document.getElementById("skills-input");
    const tagsArea = document.getElementById("tags-area");
    const tagContainer = document.getElementById("tag-container");
    const analyzeBtn = document.getElementById("analyze-btn");
    const backBtn = document.getElementById("back-btn");
    const errorMsg = document.getElementById("error-msg");
    const themeToggle = document.getElementById("theme-toggle");
    const aboutBtn = document.getElementById("about-btn");
    const aboutModal = document.getElementById("about-modal");
    const modalClose = document.getElementById("modal-close");

    let careers = [];         // Cached career data from API
    let skillTags = [];       // Current list of confirmed skill tags
    let validationCache = {}; // Cache for skill validation results

    // ============================================================
    // Theme Toggle
    // ============================================================
    const savedTheme = localStorage.getItem("sp-theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

    themeToggle.addEventListener("click", () => {
        const current = document.documentElement.getAttribute("data-theme");
        const next = current === "dark" ? "light" : "dark";
        document.documentElement.setAttribute("data-theme", next);
        localStorage.setItem("sp-theme", next);
    });

    // ============================================================
    // About Modal
    // ============================================================
    aboutBtn.addEventListener("click", () => aboutModal.classList.add("active"));
    modalClose.addEventListener("click", () => aboutModal.classList.remove("active"));
    aboutModal.addEventListener("click", (e) => {
        if (e.target === aboutModal) aboutModal.classList.remove("active");
    });

    // ============================================================
    // Load Careers from API
    // ============================================================
    async function loadCareers() {
        try {
            const res = await fetch("/api/careers");
            const data = await res.json();

            if (data.error) {
                showError(data.error);
                return;
            }

            careers = data.careers;
            careerSelect.innerHTML = '<option value="" disabled selected>Select a target career...</option>';

            careers.forEach(c => {
                const opt = document.createElement("option");
                opt.value = c.career_uri;
                opt.textContent = c.career_name;
                opt.title = `${c.source_title} (${c.source_code})`;
                careerSelect.appendChild(opt);
            });

            updateAnalyzeBtn();
        } catch (err) {
            showError("Failed to load careers. Is the server running?");
        }
    }

    // ============================================================
    // Tag Input System
    // ============================================================
    tagContainer.addEventListener("click", () => skillsInput.focus());

    skillsInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === ",") {
            e.preventDefault();
            const raw = skillsInput.value.trim().replace(/,/g, "");
            if (raw) addSkillTag(raw);
            skillsInput.value = "";
        }
        if (e.key === "Backspace" && skillsInput.value === "" && skillTags.length > 0) {
            removeTag(skillTags.length - 1);
        }
    });

    // Also handle paste with commas
    skillsInput.addEventListener("paste", (e) => {
        e.preventDefault();
        const pasted = (e.clipboardData || window.clipboardData).getData("text");
        const items = pasted.split(",").map(s => s.trim()).filter(Boolean);
        items.forEach(item => addSkillTag(item));
    });

    async function addSkillTag(rawInput) {
        const lower = rawInput.toLowerCase().trim();
        if (!lower) return;

        // Check if already added
        if (skillTags.some(t => t.lower === lower || t.official?.toLowerCase() === lower)) return;

        // Validate against backend
        let tagData = { raw: rawInput, lower: lower, official: null, type: "pending" };

        if (validationCache[lower]) {
            tagData = { ...tagData, ...validationCache[lower] };
        } else {
            try {
                const res = await fetch(`/api/validate-skill?skill=${encodeURIComponent(lower)}`);
                const result = await res.json();

                if (result.status === "matched") {
                    tagData.official = result.official_name;
                    tagData.type = "matched";
                } else if (result.status === "suggestion") {
                    tagData.official = result.suggested;
                    tagData.type = "corrected";
                } else {
                    tagData.type = "unknown";
                }

                validationCache[lower] = { official: tagData.official, type: tagData.type };
            } catch {
                tagData.type = "unknown";
            }
        }

        // Prevent duplicate official names
        if (tagData.official && skillTags.some(t => t.official === tagData.official)) return;

        skillTags.push(tagData);
        renderTags();
        updateAnalyzeBtn();
    }

    function removeTag(index) {
        skillTags.splice(index, 1);
        renderTags();
        updateAnalyzeBtn();
    }

    function renderTags() {
        tagsArea.innerHTML = "";
        skillTags.forEach((tag, i) => {
            const el = document.createElement("span");
            const label = tag.type === "corrected"
                ? `${tag.official} (was "${tag.raw}")`
                : (tag.official || tag.raw);

            el.className = `skill-tag ${tag.type === "corrected" ? "corrected" : ""} ${tag.type === "unknown" ? "unknown-tag" : ""}`;
            el.innerHTML = `${escapeHtml(label)}<button class="tag-remove" data-idx="${i}">&times;</button>`;
            tagsArea.appendChild(el);
        });

        tagsArea.querySelectorAll(".tag-remove").forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                removeTag(parseInt(btn.dataset.idx));
            });
        });
    }

    function updateAnalyzeBtn() {
        const hasCareer = careerSelect.value && careerSelect.value !== "";
        const hasSkills = skillTags.length > 0;
        analyzeBtn.disabled = !(hasCareer && hasSkills);
    }

    careerSelect.addEventListener("change", updateAnalyzeBtn);

    // ============================================================
    // Run Analysis
    // ============================================================
    analyzeBtn.addEventListener("click", runAnalysis);

    async function runAnalysis() {
        hideError();

        const careerUri = careerSelect.value;
        const skillsStr = skillTags
            .map(t => t.official || t.raw)
            .join(", ");

        if (!careerUri) { showError("Please select a target career."); return; }
        if (!skillsStr) { showError("Please enter at least one skill."); return; }

        // Show loading state
        inputView.style.display = "none";
        loadingView.style.display = "flex";
        resultsView.style.display = "none";

        try {
            const res = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ career_uri: careerUri, skills: skillsStr })
            });

            const data = await res.json();

            if (data.error) {
                showError(data.error);
                loadingView.style.display = "none";
                inputView.style.display = "block";
                return;
            }

            // Small delay to show loading animation
            setTimeout(() => {
                loadingView.style.display = "none";
                renderResults(data);
                resultsView.style.display = "block";
                window.scrollTo({ top: 0, behavior: "smooth" });
            }, 800);

        } catch (err) {
            showError("Analysis failed. Check server connection.");
            loadingView.style.display = "none";
            inputView.style.display = "block";
        }
    }

    // ============================================================
    // Render Results Dashboard
    // ============================================================
    function renderResults(data) {
        // Summary
        document.getElementById("summary-career-name").textContent = data.selected_career.career_name;
        document.getElementById("summary-onet-title").textContent = data.selected_career.source_title;
        document.getElementById("summary-onet-code").textContent = data.selected_career.source_code;
        document.getElementById("summary-level").textContent = data.selected_career.career_level;

        // Score ring
        animateScoreRing(data.readiness_score);

        // Corrections banner
        const corrBanner = document.getElementById("corrections-banner");
        if (data.corrections && data.corrections.length > 0) {
            const corrText = data.corrections.map(c => `"${c.original}" → ${c.corrected}`).join(", ");
            document.getElementById("corrections-text").textContent = `Auto-corrected: ${corrText}`;
            corrBanner.style.display = "flex";
        } else {
            corrBanner.style.display = "none";
        }

        // Unknown banner
        const unkBanner = document.getElementById("unknown-banner");
        if (data.unknown_skills && data.unknown_skills.length > 0) {
            document.getElementById("unknown-text").textContent =
                `Unrecognized inputs: ${data.unknown_skills.join(", ")}`;
            unkBanner.style.display = "flex";
        } else {
            unkBanner.style.display = "none";
        }

        // Matched skills
        const matchedList = document.getElementById("matched-skills-list");
        if (data.matched_skills.length > 0) {
            matchedList.innerHTML = data.matched_skills.map(s =>
                `<span class="skill-chip matched">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                    ${escapeHtml(s.skill_name)}
                </span>`
            ).join("");
        } else {
            matchedList.innerHTML = '<span class="skill-chip" style="color:var(--text-muted)">None</span>';
        }

        // Missing skills by priority
        const missingContainer = document.getElementById("missing-skills-container");
        missingContainer.innerHTML = "";

        const priorities = ["High", "Medium", "Low"];
        const cssClasses = { High: "missing-high", Medium: "missing-medium", Low: "missing-low" };
        let hasMissing = false;

        priorities.forEach(p => {
            const skills = data.grouped_missing[p];
            if (skills && skills.length > 0) {
                hasMissing = true;
                const group = document.createElement("div");
                group.className = "priority-group";
                group.innerHTML = `
                    <div class="priority-label ${p.toLowerCase()}">${p} Priority</div>
                    <div class="skill-list">
                        ${skills.map(s => `<span class="skill-chip ${cssClasses[p]}">${escapeHtml(s.skill_name)} <small>(${s.category})</small></span>`).join("")}
                    </div>`;
                missingContainer.appendChild(group);
            }
        });

        if (!hasMissing) {
            missingContainer.innerHTML = '<p style="color:var(--green);font-size:0.85rem;">✓ No missing skills. You meet all requirements!</p>';
        }

        // Course timeline
        const timeline = document.getElementById("course-timeline");
        if (data.recommended_courses.length > 0) {
            timeline.innerHTML = data.recommended_courses.map(c => {
                const prereqs = c.prerequisite_skills.length > 0
                    ? `Prerequisite(s): ${c.prerequisite_skills.join(", ")}`
                    : "No prerequisites";
                return `
                    <div class="course-card">
                        <div class="course-name">${escapeHtml(c.course_name)}</div>
                        <div class="course-detail">Teaches: ${c.teaches_missing_skills.join(", ")}</div>
                        <div class="course-prereq">${prereqs}</div>
                    </div>`;
            }).join("");
        } else {
            timeline.innerHTML = '<p class="no-courses">No course recommendations needed — you already have all required skills!</p>';
        }

        // Alternative careers
        const altGrid = document.getElementById("alternatives-grid");
        if (data.alternative_careers.length > 0) {
            altGrid.innerHTML = data.alternative_careers.map(c => {
                const scoreClass = c.match_score >= 60 ? "high-match" : (c.match_score >= 30 ? "mid-match" : "low-match");
                return `
                    <div class="alt-card">
                        <div class="alt-name">${escapeHtml(c.career_name)}</div>
                        <div class="alt-score ${scoreClass}">${c.match_score}%</div>
                        <div class="alt-label">skill match</div>
                    </div>`;
            }).join("");
        } else {
            altGrid.innerHTML = '<p class="no-courses">No alternative careers available.</p>';
        }
    }

    // ============================================================
    // Score Ring Animation
    // ============================================================
    function animateScoreRing(score) {
        const circle = document.getElementById("score-ring-progress");
        const valueEl = document.getElementById("score-value");
        const circumference = 2 * Math.PI * 52; // r=52
        const offset = circumference - (score / 100) * circumference;

        // Color based on score
        let color;
        if (score >= 75) color = "var(--green)";
        else if (score >= 40) color = "var(--yellow)";
        else color = "var(--red)";

        circle.style.stroke = color;
        valueEl.style.color = color;

        // Animate
        setTimeout(() => {
            circle.style.strokeDashoffset = offset;
        }, 100);

        // Count up number
        let current = 0;
        const step = Math.max(1, Math.floor(score / 30));
        const interval = setInterval(() => {
            current += step;
            if (current >= score) { current = score; clearInterval(interval); }
            valueEl.textContent = current + "%";
        }, 30);
    }

    // ============================================================
    // Back to Input
    // ============================================================
    backBtn.addEventListener("click", () => {
        resultsView.style.display = "none";
        inputView.style.display = "block";

        // Reset score ring
        const circle = document.getElementById("score-ring-progress");
        circle.style.strokeDashoffset = 326.73;

        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // ============================================================
    // Helpers
    // ============================================================
    function showError(msg) {
        errorMsg.textContent = msg;
        errorMsg.style.display = "block";
    }
    function hideError() { errorMsg.style.display = "none"; }

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    // ============================================================
    // Initialize
    // ============================================================
    loadCareers();
});
