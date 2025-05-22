import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter, defaultdict


def analyze_annotations(json_file_path):
    """
    Analyze the annotation data from the JSON file.

    Args:
        json_file_path (str): Path to the JSON file containing annotations

    Returns:
        dict: Dictionary containing analysis results
    """
    # Load the annotation data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        annotations = json.load(f)

    # Count total annotations
    total_annotations = len(annotations)
    print(f"Total annotations: {total_annotations}")

    # Extract 'Annotation' and 'Your Review' values
    orig_annotations = [anno.get('Annotation', 'MISSING') for anno in annotations]
    reviews = [anno.get('Your Review', 'MISSING') for anno in annotations]

    # Replace NaN with 'MISSING'
    orig_annotations = ['MISSING' if pd.isna(a) or a is None else a for a in orig_annotations]
    reviews = ['MISSING' if pd.isna(r) or r is None else r for r in reviews]

    # Count occurrences of each label in both fields
    orig_count = Counter(orig_annotations)
    review_count = Counter(reviews)

    print("\n--- Original Annotation Distribution ---")
    for label, count in orig_count.items():
        percentage = (count / total_annotations) * 100
        print(f"{label}: {count} ({percentage:.2f}%)")

    print("\n--- Your Review Distribution ---")
    for label, count in review_count.items():
        percentage = (count / total_annotations) * 100
        print(f"{label}: {count} ({percentage:.2f}%)")

    # Find modified annotations
    modified = []
    for i, (orig, review) in enumerate(zip(orig_annotations, reviews)):
        if orig != review and orig != 'MISSING' and review != 'MISSING':
            modified.append((i, orig, review, annotations[i]))

    # Count modifications by type
    mod_patterns = defaultdict(int)
    for _, orig, review, _ in modified:
        mod_patterns[(orig, review)] += 1

    print(f"\n--- Modification Analysis ---")
    print(f"Total modified annotations: {len(modified)} ({(len(modified) / total_annotations) * 100:.2f}%)")

    print("\nModification patterns:")
    for (orig, review), count in sorted(mod_patterns.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(modified)) * 100
        print(f"{orig} → {review}: {count} ({percentage:.2f}%)")

    # Create a dataframe with website, annotation, review and reason for modified entries
    if modified:
        print("\nSample of modifications with reasons:")
        for i, (idx, orig, review, anno) in enumerate(modified[:5]):  # Display first 5 examples
            website = anno.get('website', 'N/A')
            reason = anno.get('Reason', 'No reason provided')
            print(f"\n{i + 1}. Website: {website}")
            print(f"   Original: {orig} → Modified: {review}")
            print(f"   Reason: {reason}")

    # Return analysis results for visualization
    return {
        'total': total_annotations,
        'orig_count': dict(orig_count),
        'review_count': dict(review_count),
        'modified': len(modified),
        'mod_patterns': dict(mod_patterns)
    }


def visualize_results(results):
    """
    Create visualizations of the analysis results.

    Args:
        results (dict): The analysis results
    """
    # Create a figure with multiple subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))

    # Plot original annotation distribution
    labels1 = list(results['orig_count'].keys())
    values1 = list(results['orig_count'].values())
    axs[0, 0].bar(labels1, values1, color='skyblue')
    axs[0, 0].set_title('Original Annotation Distribution')
    axs[0, 0].set_xlabel('Annotation')
    axs[0, 0].set_ylabel('Count')
    axs[0, 0].tick_params(axis='x', rotation=45)

    # Plot review distribution
    labels2 = list(results['review_count'].keys())
    values2 = list(results['review_count'].values())
    axs[0, 1].bar(labels2, values2, color='lightgreen')
    axs[0, 1].set_title('Your Review Distribution')
    axs[0, 1].set_xlabel('Review')
    axs[0, 1].set_ylabel('Count')
    axs[0, 1].tick_params(axis='x', rotation=45)

    # Plot modification patterns
    if results['mod_patterns']:
        labels3 = [f"{orig} → {rev}" for (orig, rev) in results['mod_patterns'].keys()]
        values3 = list(results['mod_patterns'].values())
        axs[1, 0].bar(labels3, values3, color='salmon')
        axs[1, 0].set_title('Modification Patterns')
        axs[1, 0].set_xlabel('Pattern')
        axs[1, 0].set_ylabel('Count')
        axs[1, 0].tick_params(axis='x', rotation=90)
    else:
        axs[1, 0].text(0.5, 0.5, "No modifications found", ha='center', va='center')
        axs[1, 0].set_title('Modification Patterns')

    # Pie chart for modified vs. unmodified
    modified = results['modified']
    unmodified = results['total'] - modified
    axs[1, 1].pie([unmodified, modified],
                  labels=['Unmodified', 'Modified'],
                  autopct='%1.1f%%',
                  colors=['lightgray', 'coral'],
                  startangle=90)
    axs[1, 1].set_title('Modified vs. Unmodified Annotations')

    plt.tight_layout()
    plt.savefig('annotation_analysis.png')
    plt.close()
    print("\nVisualization saved as 'annotation_analysis.png'")


def main():
    # Replace with the path to your JSON file
    json_file_path = "/reviewing/extract_reviewing_result/data/all_reviewed_annotation_4_15.json"

    print("Analyzing annotations...")
    results = analyze_annotations(json_file_path)

    print("\nCreating visualizations...")
    visualize_results(results)

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()