#!/usr/bin/env python3
"""
Test loading DramaBench dataset from Hugging Face Hub.

This script:
1. Loads the DramaBench dataset from HF
2. Analyzes dataset structure and statistics
3. Displays sample data
4. Validates data fields
"""

from datasets import load_dataset
import json
from pathlib import Path


def analyze_dataset():
    """Load and analyze DramaBench dataset."""

    print("=" * 80)
    print("DramaBench Dataset - Hugging Face Loading Test")
    print("=" * 80)

    # Load dataset
    print("\n📦 Loading dataset from Hugging Face Hub...")
    print("Repository: FutureMa/DramaBench")

    try:
        dataset = load_dataset("FutureMa/DramaBench", split="train")
        print(f"✅ Dataset loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return

    # Basic statistics
    print(f"\n📊 Dataset Statistics:")
    print(f"{'=' * 60}")
    print(f"Total samples: {len(dataset)}")
    print(f"Features: {list(dataset.features.keys())}")

    # Analyze field statistics
    print(f"\n📋 Field Statistics:")
    print(f"{'=' * 60}")

    # Context lengths
    context_lengths = [len(sample['context']) for sample in dataset]
    print(f"\nContext lengths:")
    print(f"  - Min: {min(context_lengths):,} chars")
    print(f"  - Max: {max(context_lengths):,} chars")
    print(f"  - Average: {sum(context_lengths) / len(context_lengths):,.0f} chars")

    # Continuation lengths
    continuation_lengths = [len(sample['continuation']) for sample in dataset]
    print(f"\nContinuation lengths:")
    print(f"  - Min: {min(continuation_lengths):,} chars")
    print(f"  - Max: {max(continuation_lengths):,} chars")
    print(f"  - Average: {sum(continuation_lengths) / len(continuation_lengths):,.0f} chars")

    # Split types
    split_types = [sample['stats']['split_type'] for sample in dataset]
    scene_boundary_count = split_types.count('scene_boundary')
    middle_count = split_types.count('middle')
    print(f"\nSplit types:")
    print(f"  - Scene boundary: {scene_boundary_count} ({scene_boundary_count/len(dataset)*100:.1f}%)")
    print(f"  - Middle: {middle_count} ({middle_count/len(dataset)*100:.1f}%)")

    # Sample IDs range
    ids = [sample['id'] for sample in dataset]
    print(f"\nSample IDs:")
    print(f"  - First: {min(ids)}")
    print(f"  - Last: {max(ids)}")
    print(f"  - Unique: {len(set(ids))}/{len(ids)}")

    # Display sample
    print(f"\n📝 Sample Data (First Entry):")
    print(f"{'=' * 60}")
    sample = dataset[0]
    print(f"ID: {sample['id']}")
    print(f"Title: {sample['title']}")
    print(f"Description: {sample['description'][:100]}...")
    print(f"\nContext preview (first 200 chars):")
    print(sample['context'][:200] + "...")
    print(f"\nContinuation preview (first 200 chars):")
    print(sample['continuation'][:200] + "...")
    print(f"\nStats:")
    print(json.dumps(sample['stats'], indent=2))

    # Validate required fields
    print(f"\n✅ Field Validation:")
    print(f"{'=' * 60}")
    required_fields = ['id', 'title', 'description', 'context', 'continuation', 'stats']
    for field in required_fields:
        all_present = all(field in sample for sample in dataset)
        status = "✅" if all_present else "❌"
        print(f"{status} {field}: Present in all samples")

    # Check for unexpected fields
    unexpected_fields = set()
    for sample in dataset:
        unexpected_fields.update(set(sample.keys()) - set(required_fields))

    if unexpected_fields:
        print(f"\n⚠️  Unexpected fields found: {unexpected_fields}")
    else:
        print(f"\n✅ No unexpected fields (clean dataset)")

    # Verify no full_script field
    has_full_script = any('full_script' in sample for sample in dataset)
    if has_full_script:
        print(f"❌ WARNING: 'full_script' field found (should be removed)")
    else:
        print(f"✅ 'full_script' field correctly removed")

    # Dataset size
    import sys
    dataset_size = sys.getsizeof(str(dataset))
    print(f"\n💾 Dataset Size:")
    print(f"{'=' * 60}")
    print(f"Approximate in-memory size: {dataset_size / 1024 / 1024:.2f} MB")

    # Usage example
    print(f"\n🔧 Usage Example:")
    print(f"{'=' * 60}")
    print("""
from datasets import load_dataset

# Load dataset
dataset = load_dataset("FutureMa/DramaBench", split="train")

# Access samples
sample = dataset[0]
print(sample['title'])
print(sample['context'])
print(sample['continuation'])

# Iterate
for sample in dataset:
    # Your processing code
    pass

# Convert to pandas
df = dataset.to_pandas()

# Filter by split type
scene_boundary_samples = dataset.filter(lambda x: x['stats']['split_type'] == 'scene_boundary')
""")

    print(f"\n{'=' * 80}")
    print(f"✅ Analysis complete!")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    analyze_dataset()
