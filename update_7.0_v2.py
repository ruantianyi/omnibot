import re

def main():
    try:
        with open('7.0.html', 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Update toggleSettings to call renderModelControls()
        toggle_pattern = re.compile(r'function toggleSettings\(\) \{.*?(?=function closeSettings)', re.DOTALL)
        new_toggle = """function toggleSettings() {
                const modal = document.getElementById('settings-modal');
                if (modal.classList.contains('hidden')) {
                    modal.classList.remove('hidden');
                    document.getElementById('api-key-input').value = apiKey;
                    document.getElementById('api-provider').value = apiProvider;
                    const savedAutosave = localStorage.getItem('omni_autosave');
                    if (savedAutosave !== null) {
                        document.getElementById('autosave-toggle').checked = savedAutosave === 'true';
                    }
                    document.querySelector('#settings-modal > div').dataset.keySaved = 'true';
                    
                    if (window.renderModelControls) {
                        window.renderModelControls();
                    }
                } else {
                    modal.classList.add('hidden');
                }
            }

            """
        content = toggle_pattern.sub(new_toggle, content)

        # 2. Update renderModelControls and initialization logic
        render_script_pattern = re.compile(r'// Model Manager UI Rendering Logic.*?(?=</body>)', re.DOTALL)
        
        new_render_script = """// Model Manager UI Rendering Logic
            function renderModelControls() {
                const models = ['potato-planner', 'potato-text', 'potato-coder', 'medium-planner', 'medium-text', 'medium-coder'];
                models.forEach(modelKey => {
                    const container = document.getElementById('controls-' + modelKey);
                    if (!container) return;
                    
                    if (!window.modelManager) {
                        container.innerHTML = `<button onclick="window.modelManager ? window.modelManager.startDownload('${modelKey}') : alert('Model Manager loading...')" class="px-3 py-1 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 text-[10px] font-bold text-black dark:text-white rounded uppercase transition shadow">Download</button>`;
                        return;
                    }
                    
                    const state = window.modelManager.getState(modelKey);
                    let html = '';
                    
                    if (state.status === 'not-downloaded' || state.status === 'error') {
                        html = `<button onclick="window.modelManager.startDownload('${modelKey}')" class="px-3 py-1 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 text-[10px] font-bold text-black dark:text-white rounded uppercase transition shadow">${state.status === 'error' ? 'Retry' : 'Download'}</button>`;
                    } else if (state.status === 'downloading') {
                        html = `<div class="text-[10px] text-slate-500 font-mono mr-2 flex items-center">${state.progress}%</div>
                                <button onclick="window.modelManager.pauseDownload('${modelKey}')" class="px-3 py-1 bg-amber-500 hover:bg-amber-600 text-[10px] font-bold text-white rounded uppercase transition shadow">Pause</button>`;
                    } else if (state.status === 'paused') {
                        html = `<div class="text-[10px] text-slate-500 font-mono mr-2 flex items-center">${state.progress}%</div>
                                <button onclick="window.modelManager.startDownload('${modelKey}')" class="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-[10px] font-bold text-white rounded uppercase transition shadow mr-1">Resume</button>
                                <button onclick="confirmDeleteModel('${modelKey}')" class="px-3 py-1 bg-red-500 hover:bg-red-600 text-[10px] font-bold text-white rounded uppercase transition shadow" title="Delete Model"><i class="fa-solid fa-trash"></i></button>`;
                    } else if (state.status === 'downloaded') {
                        html = `<span class="px-3 py-1 bg-emerald-500 text-[10px] font-bold text-white rounded uppercase shadow flex items-center gap-1 mr-1 select-none"><i class="fa-solid fa-check"></i> Ready</span>
                                <button onclick="confirmDeleteModel('${modelKey}')" class="px-3 py-1 bg-red-500 hover:bg-red-600 text-[10px] font-bold text-white rounded uppercase transition shadow" title="Delete Model"><i class="fa-solid fa-trash"></i></button>`;
                    }
                    container.innerHTML = html;
                });
            }

            function confirmDeleteModel(modelKey) {
                if (confirm('Are you sure you want to delete this model? It will remove it from your offline storage.')) {
                    if (window.modelManager) {
                        window.modelManager.deleteModel(modelKey).then(() => {
                            renderModelControls();
                        });
                    }
                }
            }

            window.renderModelControls = renderModelControls;

            function initControlsHook() {
                if (window.modelManager) {
                    const models = ['potato-planner', 'potato-text', 'potato-coder', 'medium-planner', 'medium-text', 'medium-coder'];
                    models.forEach(modelKey => {
                        window.modelManager.onProgress(modelKey, () => {
                            renderModelControls();
                        });
                    });
                }
                renderModelControls();
            }

            window.addEventListener('modelManagerReady', initControlsHook);
            window.addEventListener('load', () => {
                setTimeout(initControlsHook, 300);
                setTimeout(initControlsHook, 1000);
            });
            document.addEventListener('DOMContentLoaded', renderModelControls);
        </script>
        </body>"""
        
        content = render_script_pattern.sub(new_render_script, content)
        
        with open('7.0.html', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Successfully updated 7.0.html")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
