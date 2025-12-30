# DramaBench Evaluation Prompts

This directory contains the LLM-based evaluation prompt templates used in the DramaBench framework for assessing drama script continuation quality.

## Overview

DramaBench uses a **hybrid evaluation system**:
- **Rule-based analysis** for Format Standards (not included here)
- **LLM-based labeling** for 5 content dimensions (prompts in this folder)

These prompts are designed to be filled with script context and continuation, then sent to an LLM (e.g., Claude Sonnet 4.5, GPT-4) to generate structured JSON analysis.

## Available Prompts

### 1. Narrative Efficiency (`narrative_efficiency_prompt.txt`)

**Purpose**: Evaluate how effectively the continuation advances the story and avoids narrative padding.

**Key Metrics**:
- Effective Narrative Rate (ENR)
- Beats Per Page
- Driver/Static/Redundant beat classification

**Output**: JSON with story beats, world state changes, and classifications.

**Use Case**: Determine if the continuation has meaningful plot progression or is filled with redundant descriptions.

---

### 2. Character Consistency (`character_consistency_prompt.txt`)

**Purpose**: Assess whether characters maintain their established personalities, speech patterns, and behaviors.

**Key Metrics**:
- Out-of-Character (OOC) Rate
- Voice Distinctiveness

**Output**: JSON with character persona profiles and dialogue line classifications (In-Character/Neutral/OOC).

**Use Case**: Identify if characters behave consistently with their established traits or suddenly act out of character.

---

### 3. Emotional Depth (`emotional_depth_prompt.txt`)

**Purpose**: Analyze the emotional arc and complexity of the protagonist's emotional journey.

**Key Metrics**:
- Emotional Arc Score (Shift vs Static)
- Complexity Ratio (mixed emotions)
- Valence and Arousal tracking

**Output**: JSON with opening/closing emotional states, arc type, and complex emotion moments.

**Use Case**: Evaluate if the continuation has meaningful emotional development or remains emotionally flat.

---

### 4. Logic Consistency (`logic_consistency_prompt.txt`)

**Purpose**: Verify factual coherence, continuity, and logical consistency with the context.

**Key Metrics**:
- Logic Break Rate
- Context Coherence

**Output**: JSON identifying logic breaks, contradictions, and unexplained changes.

**Use Case**: Detect plot holes, contradictions, or violations of established facts.

---

### 5. Conflict Handling (`conflict_handling_prompt.txt`)

**Purpose**: Evaluate how well the continuation develops, maintains, or resolves conflicts.

**Key Metrics**:
- Conflict Score
- Drop Rate (unresolved conflicts)

**Output**: JSON with conflict identification, development tracking, and resolution analysis.

**Use Case**: Assess if conflicts are properly developed or if they're dropped/resolved too easily.

---

### 6. Dialogue Quality (`dialogue_quality_prompt.txt`)

**Purpose**: Assess the quality of dialogue in terms of naturalness, purpose, and distinctiveness.

**Key Metrics**:
- Functional Dialogue Ratio
- Naturalistic Speech Patterns
- Character Voice Distinctiveness

**Output**: JSON with dialogue line analysis and quality classifications.

**Use Case**: Evaluate if dialogue sounds natural, serves narrative purposes, and differentiates characters.

---

## How to Use These Prompts

### Basic Usage

1. **Read the prompt template** (e.g., `narrative_efficiency_prompt.txt`)
2. **Replace placeholders** with actual data:
   - `{CONTEXT}` - Original script context
   - `{CONTINUATION}` - Generated continuation to evaluate
   - `{MODEL}` - Name of the model being evaluated
   - `{SCRIPT_ID}` - Unique identifier for the script
3. **Send to LLM** (recommended: Claude Sonnet 4.5, GPT-4, or similar)
4. **Parse JSON response** for structured metrics

### Example Workflow

```python
# Load prompt template
with open('prompts/narrative_efficiency_prompt.txt', 'r') as f:
    prompt_template = f.read()

# Fill in placeholders
prompt = prompt_template.replace('{CONTEXT}', script_context)
prompt = prompt.replace('{CONTINUATION}', generated_continuation)
prompt = prompt.replace('{MODEL}', 'GPT-4')
prompt = prompt.replace('{SCRIPT_ID}', 'script_001')

# Send to LLM
response = llm_api_call(prompt)

# Parse JSON output
evaluation = json.loads(response)
```

### Batch Evaluation

For evaluating multiple model outputs on the same script:

```python
models = ['GPT-4', 'Claude-Sonnet-4.5', 'Gemini-Pro']
dimensions = ['narrative_efficiency', 'character_consistency', 'emotional_depth',
              'logic_consistency', 'conflict_handling', 'dialogue_quality']

results = {}
for model in models:
    for dimension in dimensions:
        prompt_path = f'prompts/{dimension}_prompt.txt'
        # ... (fill template and evaluate)
        results[f'{model}_{dimension}'] = evaluation
```

## Output Format

All prompts return **structured JSON** with the following general pattern:

```json
{
  "script_id": "script_XXXX",
  "model": "model-name",
  "analysis": {
    // Dimension-specific analysis
  },
  "statistics": {
    // Calculated metrics
  }
}
```

## Quality Guidelines

**Best Practices**:
- Use the latest frontier LLMs (Claude Sonnet 4.5, GPT-4 Turbo, or better) for evaluation
- Maintain consistent LLM settings across evaluations (temperature, max tokens)
- Validate JSON output before processing
- Run multiple evaluations and aggregate for critical assessments

**Common Issues**:
- **Incomplete JSON**: Some LLMs may truncate output - increase max_tokens if needed
- **Schema violations**: Validate against expected JSON structure
- **Inconsistent standards**: Use the same evaluator LLM for all dimensions to maintain consistency

## Validation

The DramaBench paper validated these prompts through:
- **Statistical significance testing** (252 Mann-Whitney U tests)
- **Human-LLM agreement studies** (Cohen's Kappa, Pearson correlation)
- **Dimension independence analysis** (mean |r| = 0.020)

See the main README for detailed validation results.

## Citation

If you use these evaluation prompts, please cite the DramaBench paper:

```bibtex
@misc{ma2025dramabenchsixdimensionalevaluationframework,
  title={DramaBench: A Six-Dimensional Evaluation Framework for Drama Script Continuation},
  author={Shijian Ma and Yunqi Huang and Yan Lin},
  year={2025},
  eprint={2512.19012},
  archivePrefix={arXiv},
  primaryClass={cs.CL},
  url={https://arxiv.org/abs/2512.19012}
}
```

## License

MIT License - See parent LICENSE file for details.

---

**Last Updated**: 2025-12-30
**Version**: 1.0.0
**Contact**: mas8069@foxmail.com
