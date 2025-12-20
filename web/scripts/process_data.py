"""
Data Processing Script for DramaBench Web Demo
Extracts and converts data from drama-multi-dimension-analysis to web-friendly JSON
"""

import pandas as pd
import json
from pathlib import Path
from collections import defaultdict

# Paths
SOURCE_DIR = Path("/Users/jason/Projects/short_dataset/drama-multi-dimension-analysis/data")
OUTPUT_DIR = Path("/Users/jason/Projects/short_dataset/DramaBench/web/data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Model name mapping
MODEL_NAMES = {
    "claude-opus-4.5": "Claude Opus 4.5",
    "gpt-5.2": "GPT-5.2",
    "gemini-3-pro": "Gemini 3 Pro",
    "qwen3-max": "Qwen3-Max",
    "deepseek-v3.2": "DeepSeek V3.2",
    "minimax-m2": "MiniMax M2",
    "kimi-k2-thinking": "Kimi K2 Thinking",
    "glm-4.6": "GLM-4.6"
}

def process_leaderboard():
    """Process model rankings across all dimensions"""

    dimensions = [
        "format_standards",
        "narrative_efficiency",
        "character_consistency",
        "emotional_depth",
        "logic_consistency",
        "conflict_handling"
    ]

    leaderboard_data = []

    for dimension in dimensions:
        csv_path = SOURCE_DIR / "keep_clean" / f"{dimension}_metrics.csv"
        if not csv_path.exists():
            print(f"Warning: {csv_path} not found")
            continue

        df = pd.read_csv(csv_path)

        # Calculate average metrics per model
        model_stats = df.groupby('model').agg({
            'script_id': 'count'
        }).reset_index()

        # Get key metric based on dimension
        if dimension == "format_standards":
            model_perf = df.groupby('model')['format_error_rate'].mean()
        elif dimension == "narrative_efficiency":
            model_perf = df.groupby('model')['enr'].mean()
        elif dimension == "character_consistency":
            model_perf = df.groupby('model')['ooc_rate'].mean()
        elif dimension == "emotional_depth":
            model_perf = df.groupby('model')['emotional_depth_score'].mean()
        elif dimension == "logic_consistency":
            model_perf = df.groupby('model')['logic_break_rate'].mean()
        elif dimension == "conflict_handling":
            model_perf = df.groupby('model')['score_weight'].mean()

        for model, perf in model_perf.items():
            leaderboard_data.append({
                "model": MODEL_NAMES.get(model, model),
                "model_id": model,
                "dimension": dimension.replace('_', ' ').title(),
                "dimension_id": dimension,
                "score": float(perf),
                "samples": int(model_stats[model_stats['model'] == model]['script_id'].iloc[0])
            })

    # Calculate overall rankings
    overall_scores = defaultdict(list)
    for item in leaderboard_data:
        overall_scores[item['model']].append(item['score'])

    overall_rankings = []
    for model, scores in overall_scores.items():
        # Find model_id
        model_ids = [k for k, v in MODEL_NAMES.items() if v == model]
        model_id = model_ids[0] if model_ids else model.lower().replace(' ', '-')

        overall_rankings.append({
            "model": model,
            "model_id": model_id,
            "avg_score": sum(scores) / len(scores),
            "dimension_scores": dict(zip(
                [d.replace('_', ' ').title() for d in dimensions],
                scores[:len(dimensions)]
            ))
        })

    overall_rankings.sort(key=lambda x: x['avg_score'], reverse=True)

    # Add rankings
    for idx, item in enumerate(overall_rankings, 1):
        item['rank'] = idx

    output = {
        "last_updated": "2025-12-20",
        "total_scripts": 1103,
        "total_evaluations": 8824,
        "models_evaluated": 8,
        "dimensions": 6,
        "overall_rankings": overall_rankings,
        "dimension_details": leaderboard_data
    }

    with open(OUTPUT_DIR / "leaderboard.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Leaderboard data saved: {len(overall_rankings)} models")
    return output

def process_case_studies():
    """Process case studies data"""

    case_studies_path = SOURCE_DIR / "case_studies_error_analysis" / "case_studies" / "all_case_studies.json"

    if not case_studies_path.exists():
        print(f"Warning: {case_studies_path} not found")
        return None

    with open(case_studies_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)

    # Group by dimension
    dimension_cases = defaultdict(list)
    for case in cases:
        dim = case['dimension']
        dimension_cases[dim].append({
            "case_id": case['case_id'],
            "dimension": case['dimension'],
            "type": case['type'],
            "script_id": case['script_id'],
            "model": MODEL_NAMES.get(case['model'], case['model']),
            "model_id": case['model'],
            "rank": case.get('rank', 'N/A'),
            "metrics": case.get('metrics', {}),
            "context_excerpt": case.get('context_excerpt', '')[:500],
            "continuation_excerpt": case.get('continuation_excerpt', '')[:500],
            "analysis": case.get('analysis', {})
        })

    output = {
        "last_updated": "2025-12-20",
        "total_cases": len(cases),
        "dimensions": list(dimension_cases.keys()),
        "cases_by_dimension": dict(dimension_cases),
        "all_cases": cases[:30]  # Include first 30 full cases
    }

    with open(OUTPUT_DIR / "case_studies.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"✓ Case studies saved: {len(cases)} cases across {len(dimension_cases)} dimensions")
    return output

def process_statistics():
    """Process overall statistics"""

    stats = {
        "overview": {
            "total_scripts": 1103,
            "total_evaluations": 8824,
            "models_evaluated": 8,
            "dimensions": 6,
            "avg_script_length": 250,
            "evaluation_period": "2025-12-16 to 2025-12-20"
        },
        "dimensions": [
            {
                "id": "format_standards",
                "name": "Format Standards",
                "description": "Adherence to screenplay format (Fountain syntax)",
                "type": "rule-based",
                "key_metrics": ["Format Error Rate", "Novelization Index", "Dialogue-Action Ratio"]
            },
            {
                "id": "narrative_efficiency",
                "name": "Narrative Efficiency",
                "description": "Story progression effectiveness and pacing",
                "type": "llm-labeled",
                "key_metrics": ["Effective Narrative Rate", "Beats Per Page"]
            },
            {
                "id": "character_consistency",
                "name": "Character Consistency",
                "description": "Character voice and behavior consistency",
                "type": "llm-labeled",
                "key_metrics": ["Out-of-Character Rate", "Voice Distinctiveness"]
            },
            {
                "id": "emotional_depth",
                "name": "Emotional Depth",
                "description": "Emotional arc development and complexity",
                "type": "llm-labeled",
                "key_metrics": ["Arc Score", "Complexity Ratio"]
            },
            {
                "id": "logic_consistency",
                "name": "Logic Consistency",
                "description": "Factual coherence and logical continuity",
                "type": "llm-labeled",
                "key_metrics": ["Logic Break Rate", "Context Coherence"]
            },
            {
                "id": "conflict_handling",
                "name": "Conflict Handling",
                "description": "Conflict development and resolution quality",
                "type": "llm-labeled",
                "key_metrics": ["Conflict Score", "Drop Rate"]
            }
        ],
        "models": [
            {
                "id": "claude-opus-4.5",
                "name": "Claude Opus 4.5",
                "provider": "Anthropic",
                "description": "Latest Claude model with enhanced creative writing"
            },
            {
                "id": "gpt-5.2",
                "name": "GPT-5.2",
                "provider": "OpenAI",
                "description": "GPT-5 series with improved reasoning"
            },
            {
                "id": "gemini-3-pro",
                "name": "Gemini 3 Pro",
                "provider": "Google DeepMind",
                "description": "Gemini 3 generation flagship model"
            },
            {
                "id": "qwen3-max",
                "name": "Qwen3-Max",
                "provider": "Alibaba Cloud",
                "description": "Qwen 3 series maximum capability model"
            },
            {
                "id": "deepseek-v3.2",
                "name": "DeepSeek V3.2",
                "provider": "DeepSeek",
                "description": "DeepSeek V3 series with enhanced context"
            },
            {
                "id": "minimax-m2",
                "name": "MiniMax M2",
                "provider": "MiniMax",
                "description": "MiniMax M2 generation for coding and agents"
            },
            {
                "id": "kimi-k2-thinking",
                "name": "Kimi K2 Thinking",
                "provider": "Moonshot AI",
                "description": "1T parameter MoE with 256K context"
            },
            {
                "id": "glm-4.6",
                "name": "GLM-4.6",
                "provider": "Zhipu AI",
                "description": "ChatGLM 4 series latest version"
            }
        ]
    }

    with open(OUTPUT_DIR / "statistics.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

    print(f"✓ Statistics saved")
    return stats

def main():
    """Main processing function"""
    print("Starting data processing for DramaBench web demo...")
    print("=" * 60)

    # Process all data
    leaderboard = process_leaderboard()
    cases = process_case_studies()
    stats = process_statistics()

    print("=" * 60)
    print("✅ All data processed successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Files created:")
    print(f"  - leaderboard.json")
    print(f"  - case_studies.json")
    print(f"  - statistics.json")

if __name__ == "__main__":
    main()
