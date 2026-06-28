import re

def main():
    try:
        with open('lessons.html', 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Inject model_manager.js import
        if 'model_manager.js' not in content:
            content = content.replace('<script src="https://cdn.tailwindcss.com"></script>', 
                                      '<script src="https://cdn.tailwindcss.com"></script>\n    <script type="module" src="./model_manager.js"></script>')
                                      
        # 2. Add the Modal HTML right before </main>
        modal_html = """
            <!-- Download Modal -->
            <div id="downloadModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
                <div class="bg-slate-900 border border-slate-700 rounded-2xl p-6 max-w-sm w-full mx-4 shadow-2xl">
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-download text-indigo-400 mr-2"></i>Offline Model Required</h3>
                    <p class="text-sm text-slate-400 mb-4">You need an offline text model to use AI features. Would you like to download one now?</p>
                    
                    <div class="space-y-3 mb-6">
                        <div class="border border-slate-700 rounded-lg p-3 bg-slate-800/50 hover:bg-slate-800 cursor-pointer transition" onclick="startModelDownload('potato-text')">
                            <h4 class="text-sm font-bold text-white">Potato Text (Qwen-2.5)</h4>
                            <p class="text-xs text-slate-400">Fast, ~350MB. Good for standard usage.</p>
                        </div>
                        <div class="border border-slate-700 rounded-lg p-3 bg-slate-800/50 hover:bg-slate-800 cursor-pointer transition" onclick="startModelDownload('medium-text')">
                            <h4 class="text-sm font-bold text-white">Medium Text (Llama-3.2)</h4>
                            <p class="text-xs text-slate-400">Higher quality, ~750MB. Best experience.</p>
                        </div>
                    </div>
                    
                    <div class="flex justify-end gap-2">
                        <button onclick="document.getElementById('downloadModal').classList.add('hidden')" class="px-4 py-2 rounded-lg text-sm font-bold text-slate-300 hover:text-white transition">Cancel</button>
                    </div>
                </div>
            </div>
            
            <script>
                function startModelDownload(modelKey) {
                    if (window.modelManager) {
                        window.modelManager.startDownload(modelKey);
                        document.getElementById('downloadModal').classList.add('hidden');
                        alert("Download started in the background! You can view progress in Settings.");
                    }
                }
            </script>
"""
        if 'id="downloadModal"' not in content:
            content = content.replace('</main>', modal_html + '\n    </main>')

        # 3. Replace the old aiWorker logic with WebLLM logic
        # We need to replace from "if (!aiWorker) {" up to "});\n            }" for the triggerAISearch function
        
        # We can just match the body of triggerAISearch
        old_body_pattern = re.compile(r'function triggerAISearch\(\) \{.*?(?=function highlightRecommendedCards)', re.DOTALL)
        
        new_body = """function triggerAISearch() {
                const prompt = searchInput.value.trim();
                if (!prompt) {
                    searchInput.focus();
                    return;
                }

                const bestModelKey = window.modelManager ? window.modelManager.getBestTextModel() : null;
                if (!bestModelKey) {
                    document.getElementById('downloadModal').classList.remove('hidden');
                    return;
                }

                // Show UI
                aiOverviewContainer.classList.remove('hidden');
                
                // Ensure expanded
                aiExpanded = true;
                aiOverviewContent.style.display = 'block';
                aiOverviewChevron.classList.replace('fa-chevron-down', 'fa-chevron-up');
                
                aiOutputText.innerText = "Initializing Model...";
                aiStatusBadge.innerText = "Loading";
                aiStatusBadge.className = "text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 ml-auto";
                aiModelLoadingText.classList.remove('hidden');
                
                generateResponse(prompt, bestModelKey);
            }
            
            async function generateResponse(prompt, modelKey) {
                try {
                    const modelId = window.modelManager.LOCAL_MODELS[modelKey].id;
                    const engine = await window.webllm.CreateMLCEngine(modelId, {
                        initProgressCallback: (progress) => {
                            aiStatusBadge.innerText = "Loading Model...";
                            const pct = Math.round(progress.progress * 100);
                            downloadPct.innerText = pct;
                            aiProgressBar.style.width = pct + "%";
                        }
                    });

                    aiStatusBadge.innerText = "Generating...";
                    aiStatusBadge.className = "text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-400 ml-auto";
                    aiModelLoadingText.classList.add('hidden');
                    aiProgressBar.style.width = "100%";

                    let systemPrompt = "";
                    if (currentMode === 'ai_search') {
                        systemPrompt = "You are a highly concise AI recommender for Anthocyan AI. Based on the user's prompt, recommend the most suitable lessons from the catalog and explain why. Keep the overview brief (2-3 sentences max) and explicitly name the lessons. \\n\\nCatalog Metadata:\\n" + lessonCatalog;
                    } else {
                        systemPrompt = "You are a concise AI assistant. Provide a brief overview of the concepts mentioned in the user's search query. Keep it under 2 sentences. \\n\\nCatalog Metadata:\\n" + lessonCatalog;
                    }

                    const messages = [
                        { role: "system", content: systemPrompt },
                        { role: "user", content: prompt }
                    ];

                    aiOutputText.innerText = "";
                    aiProgressBar.style.width = "0%";
                    
                    const chunks = await engine.chat.completions.create({ messages, stream: true, temperature: 0.4, max_tokens: 150 });
                    for await (const chunk of chunks) {
                        const text = chunk.choices[0]?.delta?.content || "";
                        aiOutputText.innerText += text;
                        if (currentMode === 'ai_search') {
                            highlightRecommendedCards(aiOutputText.innerText);
                        }
                    }
                    aiStatusBadge.innerText = "Complete";
                    aiStatusBadge.className = "text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 ml-auto";
                } catch(e) {
                    aiOutputText.innerText = "Error: " + e.message;
                    aiStatusBadge.innerText = "Failed";
                    aiStatusBadge.className = "text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-400 ml-auto";
                }
            }

            """
        content = old_body_pattern.sub(new_body, content)

        # Also remove `let aiWorker = null;` at the top of script
        content = content.replace('let aiWorker = null;', '')
        
        with open('lessons.html', 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("Success")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
