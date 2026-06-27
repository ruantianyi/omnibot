import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/transformers.min.js';

// Optimize for potato phones
env.allowLocalModels = false;
env.useBrowserCache = true;

class PipelineSingleton {
    static task = 'text-generation';
    static model = 'Xenova/Qwen1.5-0.5B-Chat';
    static instance = null;

    static async getInstance(progress_callback = null) {
        if (this.instance === null) {
            this.instance = pipeline(this.task, this.model, { 
                progress_callback,
                dtype: 'q4' // 4-bit quantization reduces RAM drastically
            });
        }
        return this.instance;
    }
}

self.addEventListener('message', async (event) => {
    const { type, prompt, context, mode } = event.data;

    if (type === 'generate') {
        try {
            // Retrieve pipeline (will download if first time)
            const generator = await PipelineSingleton.getInstance((x) => {
                self.postMessage({ type: 'progress', data: x, mode });
            });

            let systemPrompt = "";
            if (mode === 'ai_search') {
                systemPrompt = "You are a highly concise AI recommender for Anthocyan AI. Based on the user's prompt, recommend the most suitable lessons from the catalog and explain why. Keep the overview brief (2-3 sentences max) and explicitly name the lessons. \n\nCatalog Metadata:\n" + context;
            } else {
                systemPrompt = "You are a concise AI assistant. Provide a brief overview of the concepts mentioned in the user's search query. Keep it under 2 sentences. \n\nCatalog Metadata:\n" + context;
            }

            // Format ChatML prompt for Qwen
            const messages = [
                { role: "system", content: systemPrompt },
                { role: "user", content: prompt }
            ];

            // Manual ChatML formatting since we use basic text-generation
            let formattedPrompt = "";
            for (const msg of messages) {
                formattedPrompt += `<|im_start|>${msg.role}\n${msg.content}<|im_end|>\n`;
            }
            formattedPrompt += "<|im_start|>assistant\n";

            // Generate
            const output = await generator(formattedPrompt, {
                max_new_tokens: 150,
                temperature: 0.4,
                repetition_penalty: 1.1,
                // Stream chunks back to main thread
                callback_function: (x) => {
                    // Extract only the generated assistant text
                    const fullText = x[0].generated_text;
                    if (fullText.includes("<|im_start|>assistant\n")) {
                        const generated = fullText.split("<|im_start|>assistant\n")[1];
                        self.postMessage({ type: 'update', data: generated, mode });
                    }
                }
            });

            const finalText = output[0].generated_text.split("<|im_start|>assistant\n")[1].replace("<|im_end|>", "").trim();
            self.postMessage({ type: 'complete', data: finalText, mode });
            
        } catch (error) {
            self.postMessage({ type: 'error', data: error.message });
        }
    }
});
