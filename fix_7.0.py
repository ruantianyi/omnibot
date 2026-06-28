import re

def main():
    try:
        with open('7.0.html', 'r', encoding='utf-8') as f:
            content = f.read()

        script_pattern = re.compile(r'// \u2550\u2550\u2550 Model Manager Logic \(Anthocyan AI 7\.0\) \u2550\u2550\u2550.*?setTimeout\(loadModelManifest, 500\);\n            }\);', re.DOTALL)
        
        new_script = """// Model Manager UI Rendering Logic
            function renderModelControls() {
                const models = ['potato-planner', 'potato-text', 'potato-coder', 'medium-planner', 'medium-text', 'medium-coder'];
                models.forEach(modelKey => {
                    const container = document.getElementById('controls-' + modelKey);
                    if (!container) return;
                    
                    const state = window.modelManager.getState(modelKey);
                    let html = '';
                    
                    if (state.status === 'not-downloaded' || state.status === 'error') {
                        html = `<button onclick="window.modelManager.startDownload('${modelKey}')" class="px-3 py-1 bg-slate-200 hover:bg-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 text-[10px] font-bold text-black dark:text-white rounded uppercase transition shadow">${state.status === 'error' ? 'Retry' : 'Download'}</button>`;
                    } else if (state.status === 'downloading') {
                        html = `<div class="text-[10px] text-slate-500 mr-2 flex items-center">${state.progress}%</div>
                                <button onclick="window.modelManager.pauseDownload('${modelKey}')" class="px-3 py-1 bg-amber-500 hover:bg-amber-600 text-[10px] font-bold text-white rounded uppercase transition shadow">Pause</button>`;
                    } else if (state.status === 'paused') {
                        html = `<div class="text-[10px] text-slate-500 mr-2 flex items-center">${state.progress}%</div>
                                <button onclick="window.modelManager.startDownload('${modelKey}')" class="px-3 py-1 bg-blue-500 hover:bg-blue-600 text-[10px] font-bold text-white rounded uppercase transition shadow">Resume</button>
                                <button onclick="confirmDeleteModel('${modelKey}')" class="px-3 py-1 bg-red-500 hover:bg-red-600 text-[10px] font-bold text-white rounded uppercase transition shadow">Delete</button>`;
                    } else if (state.status === 'downloaded') {
                        html = `<span class="px-3 py-1 bg-emerald-500 text-[10px] font-bold text-white rounded uppercase shadow flex items-center gap-1"><i class="fa-solid fa-check"></i> Ready</span>
                                <button onclick="confirmDeleteModel('${modelKey}')" class="px-3 py-1 bg-red-500 hover:bg-red-600 text-[10px] font-bold text-white rounded uppercase transition shadow"><i class="fa-solid fa-trash"></i></button>`;
                    }
                    container.innerHTML = html;
                });
            }

            function confirmDeleteModel(modelKey) {
                if (confirm('Are you sure you want to delete this model? It will remove it from your offline storage.')) {
                    window.modelManager.deleteModel(modelKey).then(() => {
                        renderModelControls();
                    });
                }
            }

            window.addEventListener('load', () => {
                setTimeout(() => {
                    if (window.modelManager) {
                        const models = ['potato-planner', 'potato-text', 'potato-coder', 'medium-planner', 'medium-text', 'medium-coder'];
                        models.forEach(modelKey => {
                            window.modelManager.onProgress(modelKey, () => {
                                renderModelControls();
                            });
                        });
                        renderModelControls();
                    }
                }, 500);
            });"""
            
        content = script_pattern.sub(new_script, content)
        
        with open('7.0.html', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Replaced script:", script_pattern.search(content) is None)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
