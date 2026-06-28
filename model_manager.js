import * as webllm from "https://esm.run/@mlc-ai/web-llm";

export const LOCAL_MODELS = {
    'potato-planner': { id: 'Qwen2.5-0.5B-Instruct-q4f16_1-MLC', type: 'planner', name: 'Potato Planner' },
    'potato-text': { id: 'Qwen2.5-0.5B-Instruct-q4f16_1-MLC', type: 'text', name: 'Potato Text' },
    'potato-coder': { id: 'Qwen2.5-Coder-0.5B-Instruct-q4f16_1-MLC', type: 'coder', name: 'Potato Coder' },
    'medium-planner': { id: 'Llama-3.2-3B-Instruct-q4f16_1-MLC', type: 'planner', name: 'Medium Planner' },
    'medium-text': { id: 'Llama-3.2-1B-Instruct-q4f16_1-MLC', type: 'text', name: 'Medium Text' },
    'medium-coder': { id: 'Qwen2.5-Coder-1.5B-Instruct-q4f16_1-MLC', type: 'coder', name: 'Medium Coder' }
};

const STATE_KEY = 'anthocyan_local_models_state';

class ModelManager {
    constructor() {
        this.state = this.loadState();
        this.activeEngines = {}; // Store references to initializing engines
        this.progressCallbacks = {}; // Store callbacks for UI updates
        this.autoResumeDownloads();
    }

    loadState() {
        const saved = localStorage.getItem(STATE_KEY);
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (e) {
                console.error("Failed to parse model state", e);
            }
        }
        // Initialize default state
        const initialState = {};
        for (const key in LOCAL_MODELS) {
            initialState[key] = { status: 'not-downloaded', progress: 0 };
        }
        return initialState;
    }

    saveState() {
        localStorage.setItem(STATE_KEY, JSON.stringify(this.state));
    }

    getState(modelKey) {
        return this.state[modelKey];
    }

    onProgress(modelKey, callback) {
        this.progressCallbacks[modelKey] = callback;
    }

    updateProgress(modelKey, progressEvent) {
        if (this.state[modelKey].status === 'paused') {
            // Ignore progress if paused
            return;
        }
        
        const percentage = Math.round(progressEvent.progress * 100);
        this.state[modelKey].progress = percentage;
        
        if (percentage >= 100 && progressEvent.text.includes("Finish")) {
             this.state[modelKey].status = 'downloaded';
        } else if (this.state[modelKey].status !== 'downloaded') {
             this.state[modelKey].status = 'downloading';
        }
        
        this.saveState();
        
        if (this.progressCallbacks[modelKey]) {
            this.progressCallbacks[modelKey](this.state[modelKey]);
        }
    }

    async startDownload(modelKey) {
        if (!LOCAL_MODELS[modelKey]) return;
        
        this.state[modelKey].status = 'downloading';
        this.state[modelKey].progress = 0;
        this.saveState();
        
        if (this.progressCallbacks[modelKey]) {
            this.progressCallbacks[modelKey](this.state[modelKey]);
        }

        this.triggerWebLLMDownload(modelKey);
    }

    async triggerWebLLMDownload(modelKey) {
        const modelId = LOCAL_MODELS[modelKey].id;
        
        try {
            this.activeEngines[modelKey] = await webllm.CreateMLCEngine(
                modelId,
                { 
                    initProgressCallback: (progress) => this.updateProgress(modelKey, progress)
                }
            );
            
            // If it completed without being paused
            if (this.state[modelKey].status !== 'paused') {
                this.state[modelKey].status = 'downloaded';
                this.state[modelKey].progress = 100;
                this.saveState();
                if (this.progressCallbacks[modelKey]) {
                    this.progressCallbacks[modelKey](this.state[modelKey]);
                }
            }
        } catch (error) {
            console.error(`Error downloading model ${modelKey}:`, error);
            if (this.state[modelKey].status !== 'paused') {
                this.state[modelKey].status = 'error';
                this.saveState();
                if (this.progressCallbacks[modelKey]) {
                    this.progressCallbacks[modelKey](this.state[modelKey]);
                }
            }
        }
    }

    pauseDownload(modelKey) {
        if (this.state[modelKey].status === 'downloading') {
            this.state[modelKey].status = 'paused';
            this.saveState();
            if (this.progressCallbacks[modelKey]) {
                this.progressCallbacks[modelKey](this.state[modelKey]);
            }
            // Note: WebLLM's fetch might still run in the background for the current chunk,
            // but we ignore its progress callbacks and it won't auto-resume on reload.
        }
    }

    async deleteModel(modelKey) {
        const modelId = LOCAL_MODELS[modelKey].id;
        // Reset state
        this.state[modelKey] = { status: 'not-downloaded', progress: 0 };
        this.saveState();
        
        if (this.progressCallbacks[modelKey]) {
            this.progressCallbacks[modelKey](this.state[modelKey]);
        }
        
        // Attempt to clear from Cache API
        try {
            const cacheKeys = await caches.keys();
            for (const key of cacheKeys) {
                if (key.includes('webllm')) {
                    const cache = await caches.open(key);
                    const requests = await cache.keys();
                    for (const req of requests) {
                        if (req.url.includes(modelId)) {
                            await cache.delete(req);
                        }
                    }
                }
            }
        } catch (e) {
            console.error("Failed to clear cache for model", e);
        }
    }

    autoResumeDownloads() {
        for (const key in this.state) {
            if (this.state[key].status === 'downloading') {
                // Resume in background
                this.triggerWebLLMDownload(key);
            }
        }
    }

    getBestTextModel() {
        // Priority: medium-text, then potato-text
        const textModels = Object.entries(LOCAL_MODELS)
            .filter(([k, v]) => v.type === 'text')
            .map(([k, v]) => k);
            
        // Check if medium-text is downloaded
        if (this.state['medium-text']?.status === 'downloaded') {
            return 'medium-text';
        }
        // Check if potato-text is downloaded
        if (this.state['potato-text']?.status === 'downloaded') {
            return 'potato-text';
        }
        
        // Fallback to any downloaded text model
        for (const key of textModels) {
            if (this.state[key]?.status === 'downloaded') {
                return key;
            }
        }
        
        return null;
    }
}

// Make it a singleton attached to window for easy global access
window.modelManager = new ModelManager();
window.webllm = webllm;
