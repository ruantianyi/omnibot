import re

with open('7.0.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update Tab 2 planner toggle
c = c.replace(
    'id="planner-mode-toggle" class="sr-only peer" onchange="togglePlannerMode()"',
    'id="planner-mode-toggle" class="sr-only peer planner-mode-toggle-class" onchange="togglePlannerMode(event)"'
)

# 2. Update Tab 6 humanizer toggle
c = c.replace(
    '<input type="checkbox" id="humanize-toggle" class="sr-only peer" checked>',
    '<input type="checkbox" id="humanize-toggle" class="sr-only peer" checked onchange="toggleHumanizerEngineVisibility()">'
)

# 3. Update Tab 6 AI Engine section
old_engine_section = '''                        <div class="mt-2">
                            <label class="text-xs text-slate-800 dark:text-slate-100 font-medium flex items-center justify-between">
                                Local AI Engine
                                <span class="text-[9px] bg-emerald-500/10 text-emerald-600 px-1.5 rounded">Offline</span>
                            </label>
                            <select id="rephraser-local-model" class="local-model-selector w-full mt-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-700 dark:text-slate-200 focus:outline-none focus:border-emerald-500">
                                <option value="">(Use Cloud API)</option>
                            </select>
                        </div>'''

new_engine_section = '''                        <div class="mt-2" id="humanizer-engine-container" style="display: none;">
                            <label class="text-xs text-slate-800 dark:text-slate-100 font-medium flex items-center justify-between">
                                Local AI Engine
                                <div class="flex items-center gap-2">
                                    <label class="relative inline-flex items-center cursor-pointer" title="Thinking Mode">
                                        <input type="checkbox" class="sr-only peer planner-mode-toggle-class" onchange="togglePlannerMode(event)">
                                        <div class="w-7 h-4 bg-slate-250 dark:bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:bg-indigo-500"></div>
                                        <span class="ml-2 text-[9px] font-bold text-slate-800 dark:text-slate-100 uppercase">Thinking</span>
                                    </label>
                                    <span class="text-[9px] bg-emerald-500/10 text-emerald-600 px-1.5 rounded">Offline</span>
                                </div>
                            </label>
                            <select id="rephraser-local-model" class="local-model-selector w-full mt-2 bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-700 dark:text-slate-200 focus:outline-none focus:border-emerald-500">
                                <option value="">(Use Cloud API)</option>
                            </select>
                        </div>'''

c = c.replace(old_engine_section, new_engine_section)

# Update the definition of togglePlannerMode to sync all elements
old_toggle_func = '''            function togglePlannerMode() {
                const toggle = document.getElementById('planner-mode-toggle');
                if (toggle) {
                    window.isPlannerMode = toggle.checked;
                    localStorage.setItem('omni_planner_mode', window.isPlannerMode ? 'true' : 'false');
                }
                populateModelSelectors();
                
                if (window.isPlannerMode) {'''

new_toggle_func = '''            function togglePlannerMode(event = null) {
                let isChecked = false;
                if (event && event.target) {
                    isChecked = event.target.checked;
                } else {
                    const toggle = document.getElementById('planner-mode-toggle');
                    if (toggle) isChecked = toggle.checked;
                }
                
                window.isPlannerMode = isChecked;
                localStorage.setItem('omni_planner_mode', window.isPlannerMode ? 'true' : 'false');
                
                // Sync all UI toggles
                const toggles = document.querySelectorAll('.planner-mode-toggle-class');
                toggles.forEach(t => { t.checked = isChecked; });

                populateModelSelectors();
                
                if (window.isPlannerMode) {'''

c = c.replace(old_toggle_func, new_toggle_func)

# Add the new toggleHumanizerEngineVisibility function
humanizer_visibility_func = '''            function toggleHumanizerEngineVisibility() {
                const toggle = document.getElementById('humanize-toggle');
                const container = document.getElementById('humanizer-engine-container');
                if (toggle && container) {
                    container.style.display = toggle.checked ? 'none' : 'block';
                }
            }
'''
# inject before runHumanizerUI
c = c.replace('async function runHumanizerUI()', humanizer_visibility_func + '            async function runHumanizerUI()')

with open('7.0.html', 'w', encoding='utf-8') as f:
    f.write(c)
