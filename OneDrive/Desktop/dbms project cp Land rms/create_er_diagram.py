import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.lines as mlines

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(20, 14))
ax.set_xlim(0, 20)
ax.set_ylim(0, 14)
ax.axis('off')

# Title
ax.text(10, 13.5, 'Land Registry Management System - Enhanced ER Diagram', 
        fontsize=20, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', edgecolor='black', linewidth=2))

# Color scheme
colors = {
    'core': '#E3F2FD',      # Light Blue - Core entities
    'master': '#FFF9C4',    # Light Yellow - Master data
    'transaction': '#F0F4C3', # Light Green - Transactions
    'support': '#FCE4EC'    # Light Pink - Support tables
}

# Define tables and their attributes
tables = {
    # Core Entities
    'users': {
        'pos': (1, 11),
        'color': colors['core'],
        'attrs': ['id (PK)', 'email', 'password_hash', 'full_name', 
                 'phone_number', 'role', 'is_active', 'created_at']
    },
    'properties': {
        'pos': (6, 11),
        'color': colors['core'],
        'attrs': ['id (PK)', 'ulpin (UNIQUE)', 'property_type', 'area', 
                 'market_value', 'survey_number', 'district', 'state',
                 'status', 'approved_by (FK)', 'created_at']
    },
    'owners': {
        'pos': (11, 11),
        'color': colors['core'],
        'attrs': ['id (PK)', 'user_id (FK)', 'full_name', 'aadhar_number',
                 'pan_number', 'phone_number', 'address', 'created_at']
    },
    'ownerships': {
        'pos': (16, 11),
        'color': colors['transaction'],
        'attrs': ['id (PK)', 'property_id (FK)', 'owner_id (FK)', 
                 'ownership_percentage', 'ownership_type', 'acquisition_date',
                 'acquisition_mode', 'is_current']
    },
    
    # Transaction Tables
    'mutations': {
        'pos': (1, 7.5),
        'color': colors['transaction'],
        'attrs': ['id (PK)', 'mutation_number', 'property_id (FK)', 
                 'mutation_type', 'previous_owner_id (FK)', 'new_owner_id (FK)',
                 'requester_id (FK)', 'status', 'total_fees', 'created_at']
    },
    'payments': {
        'pos': (6, 7.5),
        'color': colors['transaction'],
        'attrs': ['id (PK)', 'payment_reference', 'transaction_id', 
                 'user_id (FK)', 'property_id (FK)', 'mutation_id (FK)',
                 'payment_type', 'amount', 'status', 'payment_date']
    },
    'documents': {
        'pos': (11, 7.5),
        'color': colors['support'],
        'attrs': ['id (PK)', 'document_type_id (FK)', 'document_name', 
                 'file_path', 'entity_type', 'entity_id', 'uploaded_by (FK)',
                 'is_verified', 'uploaded_at']
    },
    
    # Support Tables
    'tax_assessments': {
        'pos': (16, 7.5),
        'color': colors['transaction'],
        'attrs': ['id (PK)', 'property_id (FK)', 'assessment_year', 
                 'assessed_value', 'tax_amount', 'status', 'due_date']
    },
    'notifications': {
        'pos': (1, 4),
        'color': colors['support'],
        'attrs': ['id (PK)', 'user_id (FK)', 'notification_type', 
                 'title', 'message', 'is_read', 'created_at']
    },
    'audit_logs': {
        'pos': (6, 4),
        'color': colors['support'],
        'attrs': ['id (PK)', 'user_id (FK)', 'action', 'entity_type', 
                 'entity_id', 'old_values', 'new_values', 'ip_address', 'timestamp']
    },
    
    # Master Data Tables
    'land_categories': {
        'pos': (11, 4),
        'color': colors['master'],
        'attrs': ['id (PK)', 'category_name', 'description', 'is_active']
    },
    'usage_types': {
        'pos': (13.5, 4),
        'color': colors['master'],
        'attrs': ['id (PK)', 'usage_type', 'description', 'is_active']
    },
    'document_types': {
        'pos': (16, 4),
        'color': colors['master'],
        'attrs': ['id (PK)', 'document_type', 'description', 'is_mandatory']
    }
}

# Draw tables
def draw_table(ax, name, pos, attrs, color):
    x, y = pos
    width = 3.5
    header_height = 0.4
    row_height = 0.25
    total_height = header_height + len(attrs) * row_height
    
    # Header
    header = FancyBboxPatch((x, y), width, header_height,
                           boxstyle="round,pad=0.05", 
                           facecolor='#1976D2', edgecolor='black', linewidth=2)
    ax.add_patch(header)
    ax.text(x + width/2, y + header_height/2, name.upper(), 
           fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    
    # Body
    body = FancyBboxPatch((x, y - total_height + header_height), width, total_height - header_height,
                         boxstyle="square,pad=0.05",
                         facecolor=color, edgecolor='black', linewidth=1.5)
    ax.add_patch(body)
    
    # Attributes
    for i, attr in enumerate(attrs):
        y_pos = y - (i + 1) * row_height + header_height/2
        fontweight = 'bold' if '(PK)' in attr or '(FK)' in attr else 'normal'
        fontsize = 8
        ax.text(x + 0.1, y_pos, attr, fontsize=fontsize, 
               fontweight=fontweight, va='center')

# Draw all tables
for table_name, table_info in tables.items():
    draw_table(ax, table_name, table_info['pos'], table_info['attrs'], table_info['color'])

# Define relationships with better positioning
relationships = [
    # Core relationships
    ('users', 'properties', '1:N\napproves', (3.5, 11.5), (6, 11.5), 'solid'),
    ('properties', 'ownerships', '1:N\nhas', (9.5, 11.5), (16, 11.5), 'solid'),
    ('owners', 'ownerships', '1:N\nbelongs', (14.5, 11.5), (16, 11.2), 'solid'),
    ('users', 'owners', '1:1\nlinks', (3.5, 11), (11, 11), 'dashed'),
    
    # Mutation relationships
    ('users', 'mutations', '1:N\nrequests', (2, 9.8), (2, 9), 'solid'),
    ('properties', 'mutations', '1:N\nhas', (7, 9.8), (3.5, 9), 'solid'),
    ('owners', 'mutations', '1:N\nprevious', (11.5, 9.8), (3.5, 8.5), 'dashed'),
    ('owners', 'mutations', '1:N\nnew', (12, 9.8), (4, 8.5), 'solid'),
    
    # Payment relationships
    ('users', 'payments', '1:N\nmakes', (2.5, 9.8), (6.5, 9), 'solid'),
    ('properties', 'payments', '1:N\nfor', (7.5, 9.8), (7.5, 9), 'dashed'),
    ('mutations', 'payments', '1:1\npays', (3.5, 7.5), (6, 7.8), 'dashed'),
    
    # Document relationships
    ('users', 'documents', '1:N\nuploads', (3, 9.5), (11.5, 9), 'solid'),
    ('documents', 'properties', 'N:1\nfor', (12, 9), (8, 10.5), 'dashed'),
    
    # Tax relationships
    ('properties', 'tax_assessments', '1:N\nassessed', (9.5, 11), (16.5, 9), 'solid'),
    
    # Notification & Audit
    ('users', 'notifications', '1:N\nreceives', (1.5, 9.8), (1.5, 5.5), 'dashed'),
    ('users', 'audit_logs', '1:N\nlogged', (2.5, 9.8), (6.5, 5.5), 'dashed'),
    
    # Master data
    ('land_categories', 'properties', '1:N\ncategory', (11.5, 5.5), (7, 9.8), 'dashed'),
    ('usage_types', 'properties', '1:N\nusage', (13.5, 5.5), (7.5, 9.8), 'dashed'),
    ('document_types', 'documents', '1:N\ntype', (16.5, 5.5), (12.5, 9), 'dashed'),
]

# Draw relationships
for rel in relationships:
    if len(rel) == 6:
        table1, table2, label, start, end, style = rel
        arrow = FancyArrowPatch(start, end,
                              connectionstyle="arc3,rad=0.1",
                              arrowstyle='->', mutation_scale=20,
                              linewidth=1.5 if style == 'solid' else 1,
                              linestyle=style, color='#424242')
        ax.add_patch(arrow)
        
        # Label
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        ax.text(mid_x, mid_y, label, fontsize=7, ha='center', 
               bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8))

# Legend
legend_x = 0.5
legend_y = 1.5
legend_items = [
    ('Core Entities', colors['core']),
    ('Master Data', colors['master']),
    ('Transactions', colors['transaction']),
    ('Support Tables', colors['support'])
]

ax.text(legend_x, legend_y + 0.8, 'Legend:', fontsize=10, fontweight='bold')
for i, (label, color) in enumerate(legend_items):
    y_pos = legend_y - i * 0.3
    rect = patches.Rectangle((legend_x, y_pos), 0.3, 0.2, 
                             facecolor=color, edgecolor='black', linewidth=1)
    ax.add_patch(rect)
    ax.text(legend_x + 0.4, y_pos + 0.1, label, fontsize=8, va='center')

# Add relationship legend
rel_legend_x = 3
ax.text(rel_legend_x, legend_y + 0.8, 'Relationships:', fontsize=10, fontweight='bold')
ax.plot([rel_legend_x, rel_legend_x + 0.5], [legend_y, legend_y], 'k-', linewidth=1.5)
ax.text(rel_legend_x + 0.6, legend_y, 'Mandatory (1:N, 1:1)', fontsize=8, va='center')
ax.plot([rel_legend_x, rel_legend_x + 0.5], [legend_y - 0.3, legend_y - 0.3], 'k--', linewidth=1)
ax.text(rel_legend_x + 0.6, legend_y - 0.3, 'Optional', fontsize=8, va='center')

# Add statistics box
stats_x = 0.5
stats_y = 0.3
stats_text = """Database Statistics:
• Total Tables: 15+ 
• Core Entities: 4
• Transaction Tables: 4
• Master Data: 3
• Support Tables: 4
• Normalization: 3NF
• Relationships: 20+"""

ax.text(stats_x, stats_y, stats_text, fontsize=9,
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8F5E9', 
                edgecolor='black', linewidth=1.5),
       verticalalignment='bottom', family='monospace')

# Add features box
features_x = 17
features_y = 0.3
features_text = """Key Features:
• ULPIN Generation
• RBAC (4 Roles)
• Joint Ownership
• Mutation Tracking
• Tax Assessment
• Audit Logging
• Document Mgmt"""

ax.text(features_x, features_y, features_text, fontsize=9,
       bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF3E0', 
                edgecolor='black', linewidth=1.5),
       verticalalignment='bottom', family='monospace')

plt.tight_layout()
plt.savefig('enhanced_er_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Enhanced ER diagram saved as 'enhanced_er_diagram.png'")
