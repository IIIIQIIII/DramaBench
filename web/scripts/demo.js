// DramaBench Interactive Demo
// Main JavaScript for demo functionality

const state = {
    apiKey: null,
    scripts: [],
    currentScript: null,
    promptTemplate: null,
    generatedContinuation: null,
    selectedModel: 'openai/gpt-5.2'
};

const OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions';
const STORAGE_KEY = 'dramabench_openrouter_api_key';

// ============================================================================
// Initialization
// ============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Initializing DramaBench Demo...');
    loadApiKey();
    await loadPromptTemplate();
    await loadScripts();
    console.log('Demo initialized');
});

// ============================================================================
// API Key Management
// ============================================================================
function loadApiKey() {
    const savedKey = localStorage.getItem(STORAGE_KEY);
    if (savedKey) {
        state.apiKey = savedKey;
        document.getElementById('api-key-input').value = savedKey;
        showStatus('api-status', 'API key loaded from storage', 'success');
        showMainDemo();
    }
}

function saveApiKey() {
    const input = document.getElementById('api-key-input');
    const key = input.value.trim();

    if (!key) {
        showStatus('api-status', 'Please enter an API key', 'error');
        return;
    }

    if (!key.startsWith('sk-or-v1-')) {
        showStatus('api-status', 'Invalid API key format. Should start with "sk-or-v1-"', 'error');
        return;
    }

    state.apiKey = key;
    localStorage.setItem(STORAGE_KEY, key);
    showStatus('api-status', 'API key saved successfully!', 'success');
    showMainDemo();
}

function clearApiKey() {
    state.apiKey = null;
    localStorage.removeItem(STORAGE_KEY);
    document.getElementById('api-key-input').value = '';
    showStatus('api-status', 'API key cleared', 'info');
    hideMainDemo();
}

function showMainDemo() {
    document.getElementById('main-demo').style.display = 'block';
}

function hideMainDemo() {
    document.getElementById('main-demo').style.display = 'none';
}

// ============================================================================
// Data Loading
// ============================================================================
async function loadPromptTemplate() {
    try {
        const response = await fetch('data/demo/drama_continuation_prompt_template.txt');
        state.promptTemplate = await response.text();
        console.log('Prompt template loaded');
    } catch (error) {
        console.error('Failed to load prompt template:', error);
        alert('Failed to load prompt template');
    }
}

async function loadScripts() {
    try {
        const response = await fetch('data/demo/dramabench_continuation_100.jsonl');
        const text = await response.text();
        state.scripts = text.trim().split('\n').map(line => JSON.parse(line));
        console.log(`Loaded ${state.scripts.length} scripts`);
        populateScriptSelect();
    } catch (error) {
        console.error('Failed to load scripts:', error);
        alert('Failed to load script dataset');
    }
}

function populateScriptSelect() {
    const select = document.getElementById('script-select');
    select.innerHTML = '<option value="">-- Select a script --</option>';
    state.scripts.forEach((script, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = `${script.id}: ${script.title}`;
        select.appendChild(option);
    });
}

// ============================================================================
// Script Selection
// ============================================================================
function selectScript(index) {
    if (index === '' || index < 0 || index >= state.scripts.length) {
        state.currentScript = null;
        clearScriptDisplay();
        return;
    }

    state.currentScript = state.scripts[index];
    displayScriptInfo();
    displayContext();
    enableGenerateButton();
    hideResults();
}

function selectRandomScript() {
    const randomIndex = Math.floor(Math.random() * state.scripts.length);
    document.getElementById('script-select').value = randomIndex;
    selectScript(randomIndex);
}

function displayScriptInfo() {
    const script = state.currentScript;
    const infoBox = document.getElementById('script-info');

    infoBox.querySelector('h3').textContent = script.title;
    infoBox.querySelector('p').textContent = script.description;

    const stats = script.stats;
    document.getElementById('script-stats').innerHTML = `
        <span>Total Lines: ${stats.total_lines}</span>
        <span>Context Lines: ${stats.context_lines}</span>
        <span>Continuation Lines: ${stats.continuation_lines}</span>
        <span>Split Ratio: ${stats.split_ratio}</span>
        <span>Split Type: ${stats.split_type}</span>
    `;
}

function displayContext() {
    document.getElementById('context-display').textContent = state.currentScript.context;
}

function clearScriptDisplay() {
    const infoBox = document.getElementById('script-info');
    infoBox.querySelector('h3').textContent = 'Select a script to begin';
    infoBox.querySelector('p').textContent = '';
    document.getElementById('script-stats').innerHTML = '';
    document.getElementById('context-display').innerHTML =
        '<p class="placeholder-text">Select a script to view context...</p>';
    disableGenerateButton();
}

function enableGenerateButton() {
    document.getElementById('generate-btn').disabled = false;
}

function disableGenerateButton() {
    document.getElementById('generate-btn').disabled = true;
}

// ============================================================================
// Generation
// ============================================================================
async function generateContinuation() {
    if (!state.apiKey) {
        showStatus('gen-status', 'Please configure your API key first', 'error');
        return;
    }

    if (!state.currentScript) {
        showStatus('gen-status', 'Please select a script first', 'error');
        return;
    }

    const selectedModelInput = document.querySelector('input[name="model"]:checked');
    state.selectedModel = selectedModelInput.value;

    disableGenerateButton();
    showStatus('gen-status', 'Generating continuation... This may take 30-60 seconds.', 'loading');

    try {
        const prompt = state.promptTemplate.replace('{{context}}', state.currentScript.context);

        const response = await fetch(OPENROUTER_API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${state.apiKey}`,
                'Content-Type': 'application/json',
                'HTTP-Referer': window.location.origin,
                'X-Title': 'DramaBench Interactive Demo'
            },
            body: JSON.stringify({
                model: state.selectedModel,
                messages: [{ role: 'user', content: prompt }],
                temperature: 0.7,
                max_tokens: 4000
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error?.message || `API request failed: ${response.status}`);
        }

        const data = await response.json();
        const generatedText = data.choices[0].message.content;
        state.generatedContinuation = extractContinuation(generatedText);

        showStatus('gen-status', 'Generation complete!', 'success');
        displayResults();

    } catch (error) {
        console.error('Generation error:', error);
        showStatus('gen-status', `Error: ${error.message}`, 'error');
    } finally {
        enableGenerateButton();
    }
}

function extractContinuation(text) {
    const match = text.match(/```continuation\s*([\s\S]*?)```/i);
    return match ? match[1].trim() : text.trim();
}

// ============================================================================
// Results Display
// ============================================================================
function displayResults() {
    document.getElementById('results-section').style.display = 'block';
    document.getElementById('model-name').textContent = getModelDisplayName(state.selectedModel);
    document.getElementById('gen-content').textContent = state.generatedContinuation;
    document.getElementById('gt-content').textContent = state.currentScript.continuation;
    document.getElementById('comp-gen').textContent = state.generatedContinuation;
    document.getElementById('comp-gt').textContent = state.currentScript.continuation;

    showGenerated();
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideResults() {
    document.getElementById('results-section').style.display = 'none';
}

function showGenerated() {
    setActiveToggle('show-gen-btn');
    document.getElementById('gen-result').style.display = 'block';
    document.getElementById('gt-result').style.display = 'none';
    document.getElementById('comp-view').style.display = 'none';
}

function showGroundTruth() {
    setActiveToggle('show-gt-btn');
    document.getElementById('gen-result').style.display = 'none';
    document.getElementById('gt-result').style.display = 'block';
    document.getElementById('comp-view').style.display = 'none';
}

function showComparison() {
    setActiveToggle('show-comp-btn');
    document.getElementById('gen-result').style.display = 'none';
    document.getElementById('gt-result').style.display = 'none';
    document.getElementById('comp-view').style.display = 'grid';
}

function setActiveToggle(buttonId) {
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(buttonId).classList.add('active');
}

// ============================================================================
// Utility Functions
// ============================================================================
function showStatus(elementId, message, type) {
    const el = document.getElementById(elementId);
    el.textContent = message;
    el.className = `status-msg ${type}`;
}

function getModelDisplayName(modelId) {
    const names = {
        'openai/gpt-5.2': 'GPT-5.2',
        'google/gemini-3-flash-preview': 'Gemini 3 Flash Preview',
        'z-ai/glm-4.7': 'GLM-4.7',
        'minimax/minimax-m2.1': 'MiniMax M2.1'
    };
    return names[modelId] || modelId;
}
