import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

# Set the style to match the reference
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'  # Using a cleaner font
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['axes.edgecolor'] = 'black'

# Data for the chart
models = ['GPT-4o-mini', 'GPT-4o', 'Claude 3.7', 'Qwen2.5VL-7B', 'SFT-Qwen2.5VL-3B', 'SFT-Qwen2.5VL-7B']
accuracy = [47.3, 54.6, 55.8, 36.8, 73.7, 80.1]
recall_high = [56.9, 43.5, 46.3, 19.5, 76.1, 76.0]
recall_low = [24.4, 72.2, 47.7, 23.5, 69.0, 77.0]

# Create figure with less height for more compact look
fig, ax = plt.subplots(figsize=(13, 7.5), facecolor='white')
ax.set_facecolor('white')

# Set the width of bars and positions
x = np.arange(len(models))
width = 0.25  # Slightly narrower bars

# Create bars with the specified colors - matching the second image style
rects1 = ax.bar(x - width, accuracy, width, label='Accuracy',
                color='#8CC572', edgecolor='none')
rects2 = ax.bar(x, recall_high, width, label='Recall HIGH',
                color='#87A4C7', edgecolor='none')
rects3 = ax.bar(x + width, recall_low, width, label='Recall LOW',
                color='#E4A2A2', edgecolor='none')

# Add value labels on bars with better spacing
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # Reduced vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold',
                    color='#2F2F2F')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

# Customize the plot with reduced margins
ax.set_ylabel('Score', fontsize=15, fontweight='normal', color='#333333')
ax.set_ylim(0, 100)
ax.set_xlim(-0.5, len(models) - 0.5)

# Set x-axis with slightly smaller font
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=13, color='#333333')

# Customize y-axis
ax.set_yticks(range(0, 101, 20))
ax.set_yticklabels([str(i) for i in range(0, 101, 20)], fontsize=11, color='#333333')

# Add horizontal grid lines with dashed style
ax.yaxis.grid(True, linestyle='--', color='#CCCCCC', alpha=0.7, linewidth=0.8)
ax.set_axisbelow(True)

# Customize legend - compact horizontal layout
legend = ax.legend(loc='upper center', fontsize=13, frameon=True,
                   fancybox=False, edgecolor='#CCCCCC', facecolor='white',
                   ncol=3, bbox_to_anchor=(0.5, 1.05),
                   columnspacing=2.0)  # Reduce space between legend items
legend.get_frame().set_linewidth(1.0)

# Remove all spines except bottom
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_color('#333333')
ax.spines['bottom'].set_color('#333333')

# Reduce padding for a more compact layout
plt.tight_layout(pad=0.5)
plt.subplots_adjust(top=0.93)  # Adjust top margin

# Save the figure with high quality
plt.savefig('multimodal_performance_compact.pdf', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.savefig('multimodal_performance_compact.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')

# Show the plot
plt.show()

# Create a more compact improvement chart
fig2, ax2 = plt.subplots(figsize=(9, 6.5), facecolor='white')
ax2.set_facecolor('white')

metrics = ['Accuracy', 'Recall HIGH', 'Recall LOW']
qwen_base = [36.8, 19.5, 23.5]
sft_7b = [80.1, 76.0, 77.0]
improvements = [sft_7b[i] - qwen_base[i] for i in range(len(metrics))]

x2 = np.arange(len(metrics))
width2 = 0.35

rects4 = ax2.bar(x2 - width2/2, qwen_base, width2, label='Qwen 7B (Base)',
                 color='#8CC572', edgecolor='none')
rects5 = ax2.bar(x2 + width2/2, sft_7b, width2, label='SFT 7B',
                 color='#87A4C7', edgecolor='none')

# Add value labels
def autolabel2(rects):
    for rect in rects:
        height = rect.get_height()
        ax2.annotate(f'{height:.1f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold',
                    color='#2F2F2F')

autolabel2(rects4)
autolabel2(rects5)

# Add improvement annotations with better positioning
for i, (base, sft, imp) in enumerate(zip(qwen_base, sft_7b, improvements)):
    ax2.annotate(f'+{imp:.1f}pp',
                xy=(x2[i] + width2/2, sft + 2),
                ha='center',
                fontsize=12,
                fontweight='bold',
                color='#4A7C4A')

ax2.set_ylabel('Score', fontsize=15, fontweight='normal', color='#333333')
ax2.set_title('Performance Improvement: Qwen 7B → SFT 7B',
              fontsize=17, fontweight='normal', pad=15, color='#333333')
ax2.set_xticks(x2)
ax2.set_xticklabels(metrics, fontsize=13, color='#333333')
ax2.set_ylim(0, 100)
ax2.set_xlim(-0.5, len(metrics) - 0.5)

# Add grid
ax2.yaxis.grid(True, linestyle='--', color='#CCCCCC', alpha=0.7, linewidth=0.8)
ax2.set_axisbelow(True)

# Customize legend - horizontal layout
legend2 = ax2.legend(fontsize=13, frameon=True, fancybox=False,
                     edgecolor='#CCCCCC', facecolor='white',
                     ncol=2, loc='upper center', bbox_to_anchor=(0.5, 1.05),
                     columnspacing=2.0)
legend2.get_frame().set_linewidth(1.0)

# Remove spines
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#333333')
ax2.spines['bottom'].set_color('#333333')

plt.tight_layout(pad=0.5)
plt.subplots_adjust(top=0.90)

# Save the improvement chart
plt.savefig('performance_improvement_compact.pdf', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
# plt.savefig('performance_improvement_compact.png', dpi=300, bbox_inches='tight',
#             facecolor='white', edgecolor='none')

plt.show()

print("Compact charts with improved fonts saved successfully!")
print("Files created:")
print("- multimodal_performance_compact.pdf")
print("- multimodal_performance_compact.png")
print("- performance_improvement_compact.pdf")
print("- performance_improvement_compact.png")