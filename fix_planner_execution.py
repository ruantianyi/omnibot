import re

with open('7.0.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update generateAIResponse planner loading
old_exec = '''                            if (window.isPlannerMode && useLocalModel) {
                                let plannerKey = localModelSelector.value;
                                if (plannerKey.includes('-text') || plannerKey.includes('-coder')) {
                                    plannerKey = plannerKey.replace(/-text|-coder/, '-planner');
                                }
                                const engine = window.modelManager?.activeEngines?.[plannerKey];
                                
                                if (!engine) {
                                    response = `<div class="no-humanize mb-3 px-3 py-2 bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-400 text-[10px] rounded-lg">Planner engine not fully loaded in memory yet. Please wait a moment.</div>`;
                                    appendBotMessage(response);
                                    if (chatTypingEl) chatTypingEl.classList.add('hidden');
                                    return;
                                }'''

new_exec = '''                            if (window.isPlannerMode && useLocalModel) {
                                let plannerKey = localModelSelector.value;
                                if (plannerKey.includes('-text') || plannerKey.includes('-coder')) {
                                    plannerKey = plannerKey.replace(/-text|-coder/, '-planner');
                                }
                                let engine = window.modelManager?.activeEngines?.[plannerKey];
                                
                                if (!engine) {
                                    appendBotMessage(`<div class="text-[10px] text-slate-800 mb-1 italic dark:text-slate-200" id="planner-status">Loading planner engine (${plannerKey}) into memory...</div>`);
                                    await window.modelManager.triggerWebLLMDownload(plannerKey);
                                    engine = window.modelManager?.activeEngines?.[plannerKey];
                                }
                                
                                if (!engine) {
                                    response = `<div class="no-humanize mb-3 px-3 py-2 bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-400 text-[10px] rounded-lg">Planner engine failed to load.</div>`;
                                    appendBotMessage(response);
                                    if (chatTypingEl) chatTypingEl.classList.add('hidden');
                                    return;
                                }'''

c = c.replace(old_exec, new_exec)

# 2. Update handleLocalModelChange to also load planner model if thinking mode is on
old_handle = '''                const modelKey = selectEl.value;
                if (window.modelManager) {
                    console.log("Ensuring local engine is ready in memory: " + modelKey);
                    // triggerWebLLMDownload will load it into memory if already downloaded.
                    window.modelManager.triggerWebLLMDownload(modelKey);
                }'''

new_handle = '''                const modelKey = selectEl.value;
                if (window.modelManager) {
                    console.log("Ensuring local engine is ready in memory: " + modelKey);
                    window.modelManager.triggerWebLLMDownload(modelKey);
                    
                    if (window.isPlannerMode && (modelKey.includes('-text') || modelKey.includes('-coder'))) {
                        const plannerKey = modelKey.replace(/-text|-coder/, '-planner');
                        console.log("Ensuring local planner engine is ready in memory: " + plannerKey);
                        window.modelManager.triggerWebLLMDownload(plannerKey);
                    }
                }'''

c = c.replace(old_handle, new_handle)


# 3. Update togglePlannerMode to also trigger download for planner model when toggled ON
old_toggle = '''                // Sync all UI toggles
                const toggles = document.querySelectorAll('.planner-mode-toggle-class');
                toggles.forEach(t => { t.checked = isChecked; });

                populateModelSelectors();
                
                
            }'''

new_toggle = '''                // Sync all UI toggles
                const toggles = document.querySelectorAll('.planner-mode-toggle-class');
                toggles.forEach(t => { t.checked = isChecked; });

                populateModelSelectors();
                
                if (window.isPlannerMode) {
                    const selectEl = document.getElementById('chat-local-model');
                    if (selectEl && selectEl.value !== 'none' && selectEl.value !== 'cloud') {
                        const modelKey = selectEl.value;
                        if (modelKey.includes('-text') || modelKey.includes('-coder')) {
                            const plannerKey = modelKey.replace(/-text|-coder/, '-planner');
                            console.log("Ensuring local planner engine is ready in memory: " + plannerKey);
                            if (window.modelManager) window.modelManager.triggerWebLLMDownload(plannerKey);
                        }
                    }
                }
            }'''

c = c.replace(old_toggle, new_toggle)


with open('7.0.html', 'w', encoding='utf-8') as f:
    f.write(c)
