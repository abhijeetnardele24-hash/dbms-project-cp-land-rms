"""
Generate architectural diagrams for IEEE research paper
Creates PNG images for system architecture, workflow, and database schema
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

# Set style
plt.style.use('default')
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 10

def create_system_architecture():
    """Create System Architecture Diagram (3-Tier)"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9.5, 'System Architecture - Three-Tier Model', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Presentation Layer
    presentation_box = FancyBboxPatch((0.5, 7), 9, 1.8, 
                                     boxstyle="round,pad=0.1", 
                                     edgecolor='#2E86AB', facecolor='#A7C6DA', linewidth=2)
    ax.add_patch(presentation_box)
    ax.text(5, 8.5, 'Presentation Layer (Frontend)', ha='center', fontsize=12, fontweight='bold')
    
    # Frontend components
    components = ['HTML5/CSS3/JS', 'Bootstrap 5', 'Leaflet.js (GIS)', 'Chart.js (Analytics)', 'AJAX/Fetch API']
    x_positions = np.linspace(1, 9, len(components))
    for i, (comp, x) in enumerate(zip(components, x_positions)):
        box = FancyBboxPatch((x-0.6, 7.2), 1.2, 0.4, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#1B4965', facecolor='white', linewidth=1)
        ax.add_patch(box)
        ax.text(x, 7.4, comp, ha='center', fontsize=8)
    
    # Arrow 1
    arrow1 = FancyArrowPatch((5, 7), (5, 6.2), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='#2E86AB')
    ax.add_patch(arrow1)
    ax.text(5.3, 6.6, 'HTTP/HTTPS', fontsize=8, style='italic')
    
    # Application Layer
    app_box = FancyBboxPatch((0.5, 4.2), 9, 1.8, 
                            boxstyle="round,pad=0.1", 
                            edgecolor='#4CAF50', facecolor='#C8E6C9', linewidth=2)
    ax.add_patch(app_box)
    ax.text(5, 5.7, 'Application Layer (Business Logic)', ha='center', fontsize=12, fontweight='bold')
    
    # Application components
    app_comps = ['Flask App', 'Auth Module', 'RBAC', 'File Handler', 'Notification Service']
    for i, (comp, x) in enumerate(zip(app_comps, x_positions)):
        box = FancyBboxPatch((x-0.6, 4.4), 1.2, 0.4, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#2E7D32', facecolor='white', linewidth=1)
        ax.add_patch(box)
        ax.text(x, 4.6, comp, ha='center', fontsize=8)
    
    # Routes
    routes = ['Admin Routes', 'Registrar Routes', 'Officer Routes', 'Citizen Routes', 'API Routes']
    for i, (route, x) in enumerate(zip(routes, x_positions)):
        box = FancyBboxPatch((x-0.6, 4.9), 1.2, 0.3, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#2E7D32', facecolor='#E8F5E9', linewidth=1)
        ax.add_patch(box)
        ax.text(x, 5.05, route, ha='center', fontsize=7)
    
    # Arrow 2
    arrow2 = FancyArrowPatch((5, 4.2), (5, 3.4), 
                            arrowstyle='->', mutation_scale=20, 
                            linewidth=2, color='#4CAF50')
    ax.add_patch(arrow2)
    ax.text(5.3, 3.8, 'SQL Queries', fontsize=8, style='italic')
    
    # Data Layer
    data_box = FancyBboxPatch((0.5, 1.4), 9, 1.8, 
                             boxstyle="round,pad=0.1", 
                             edgecolor='#F57C00', facecolor='#FFE0B2', linewidth=2)
    ax.add_patch(data_box)
    ax.text(5, 2.9, 'Data Layer (MySQL 8.0)', ha='center', fontsize=12, fontweight='bold')
    
    # Database components
    db_comps = ['Tables (13)', 'Stored Procedures', 'Triggers', 'Indexes', 'Views']
    for i, (comp, x) in enumerate(zip(db_comps, x_positions)):
        box = FancyBboxPatch((x-0.6, 1.6), 1.2, 0.4, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#E65100', facecolor='white', linewidth=1)
        ax.add_patch(box)
        ax.text(x, 1.8, comp, ha='center', fontsize=8)
    
    # Tables
    tables = ['users', 'properties', 'mutations', 'payments', 'documents', 'audit_logs']
    x_pos_tables = np.linspace(1.2, 8.8, len(tables))
    for comp, x in zip(tables, x_pos_tables):
        box = FancyBboxPatch((x-0.5, 2.15), 1, 0.25, 
                            boxstyle="round,pad=0.03", 
                            edgecolor='#E65100', facecolor='#FFF3E0', linewidth=1)
        ax.add_patch(box)
        ax.text(x, 2.27, comp, ha='center', fontsize=7)
    
    # External Services
    ext_box = FancyBboxPatch((0.5, 0.2), 4, 0.8, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#9C27B0', facecolor='#E1BEE7', linewidth=1.5)
    ax.add_patch(ext_box)
    ax.text(2.5, 0.7, 'External Services', ha='center', fontsize=10, fontweight='bold')
    ax.text(2.5, 0.4, 'Email • SMS • Payment Gateway', ha='center', fontsize=8)
    
    # Security Layer
    sec_box = FancyBboxPatch((5.5, 0.2), 4, 0.8, 
                            boxstyle="round,pad=0.05", 
                            edgecolor='#D32F2F', facecolor='#FFCDD2', linewidth=1.5)
    ax.add_patch(sec_box)
    ax.text(7.5, 0.7, 'Security Layer', ha='center', fontsize=10, fontweight='bold')
    ax.text(7.5, 0.4, 'CSRF • bcrypt • Session Mgmt', ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('system_architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ System Architecture diagram created: system_architecture.png")


def create_workflow_diagram():
    """Create Property Registration Workflow"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Property Registration Workflow', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Define roles and their x positions
    roles = ['Citizen', 'System', 'Registrar', 'Database']
    role_x = [2, 5, 8, 11]
    colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']
    
    # Draw swimlanes
    for i, (role, x, color) in enumerate(zip(roles, role_x, colors)):
        # Header
        header = FancyBboxPatch((x-1.2, 8.5), 2.4, 0.6, 
                               boxstyle="round,pad=0.05", 
                               edgecolor=color, facecolor=color, linewidth=2, alpha=0.7)
        ax.add_patch(header)
        ax.text(x, 8.8, role, ha='center', fontsize=11, fontweight='bold', color='white')
        
        # Lane
        lane = Rectangle((x-1.2, 0.5), 2.4, 8, 
                        edgecolor=color, facecolor='none', linewidth=1.5, linestyle='--', alpha=0.3)
        ax.add_patch(lane)
    
    # Workflow steps
    steps = [
        # (x, y, width, height, text, color)
        (2, 7.5, 2, 0.5, '1. Submit Property\nRegistration', '#2196F3'),
        (5, 7.2, 2, 0.5, '2. Validate Data\n& Upload Docs', '#4CAF50'),
        (11, 7.2, 2, 0.4, '3. Insert Property\nRecord', '#9C27B0'),
        (5, 6.5, 2, 0.5, '4. Generate\nApplication ID', '#4CAF50'),
        (2, 6.2, 2, 0.4, '5. Receive\nConfirmation', '#2196F3'),
        (8, 5.8, 2, 0.5, '6. Review\nApplication', '#FF9800'),
        (8, 5.1, 2, 0.4, 'Decision?', '#FFE082'),
        (8, 4.3, 1.8, 0.4, '7a. Approve &\nGenerate ULPIN', '#4CAF50'),
        (10.5, 4.3, 1.3, 0.4, '7b. Reject', '#F44336'),
        (11, 3.8, 2, 0.4, '8. Update Status\n& Records', '#9C27B0'),
        (5, 3.3, 2, 0.4, '9. Send\nNotification', '#4CAF50'),
        (2, 2.8, 2, 0.4, '10. Receive\nNotification', '#2196F3'),
        (8, 2.3, 2, 0.4, '11. Issue\nCertificate', '#FF9800'),
        (11, 1.8, 2, 0.4, '12. Log Audit\nTrail', '#9C27B0'),
    ]
    
    for x, y, w, h, text, color in steps:
        box = FancyBboxPatch((x-w/2, y), w, h, 
                            boxstyle="round,pad=0.05", 
                            edgecolor=color, facecolor=color, linewidth=2, alpha=0.8)
        ax.add_patch(box)
        ax.text(x, y+h/2, text, ha='center', va='center', fontsize=8, fontweight='bold', color='white')
    
    # Arrows connecting workflow
    arrows = [
        ((2, 7.5), (5, 7.4)),
        ((5, 7.2), (11, 7.3)),
        ((11, 7.2), (5, 6.7)),
        ((5, 6.5), (2, 6.4)),
        ((2, 6.2), (8, 6.05)),
        ((8, 5.8), (8, 5.3)),
        ((8, 5.1), (8, 4.7), 'Approved'),
        ((8.7, 5.1), (11, 4.5), 'Rejected'),
        ((8.9, 4.3), (11, 4.0)),
        ((11, 3.8), (5, 3.5)),
        ((5, 3.3), (2, 3.0)),
        ((8, 4.3), (8, 2.7)),
        ((8, 2.3), (11, 2.0)),
    ]
    
    for arrow_data in arrows:
        if len(arrow_data) == 3:
            start, end, label = arrow_data
            arrow = FancyArrowPatch(start, end, 
                                   arrowstyle='->', mutation_scale=15, 
                                   linewidth=1.5, color='#424242', linestyle='--')
            ax.add_patch(arrow)
            mid_x, mid_y = (start[0]+end[0])/2, (start[1]+end[1])/2
            ax.text(mid_x+0.2, mid_y+0.1, label, fontsize=7, style='italic', 
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        else:
            start, end = arrow_data
            arrow = FancyArrowPatch(start, end, 
                                   arrowstyle='->', mutation_scale=15, 
                                   linewidth=1.5, color='#424242')
            ax.add_patch(arrow)
    
    # Legend
    legend_y = 1.2
    ax.text(1, legend_y, 'Legend:', fontsize=9, fontweight='bold')
    legend_items = [
        ('User Action', '#2196F3'),
        ('System Process', '#4CAF50'),
        ('Officer Action', '#FF9800'),
        ('Database Operation', '#9C27B0')
    ]
    for i, (label, color) in enumerate(legend_items):
        box = Rectangle((1.5 + i*2.5, legend_y-0.15), 0.3, 0.3, 
                       facecolor=color, edgecolor='black', linewidth=1)
        ax.add_patch(box)
        ax.text(1.9 + i*2.5, legend_y, label, fontsize=8, va='center')
    
    plt.tight_layout()
    plt.savefig('workflow_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Workflow diagram created: workflow_diagram.png")


def create_database_er_diagram():
    """Create Entity-Relationship Diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Database Schema - Entity Relationship Diagram', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Define entities
    entities = {
        'users': (2, 7, ['id (PK)', 'email', 'password_hash', 'role', 'full_name', 'phone', 'is_active']),
        'properties': (7, 7, ['id (PK)', 'ulpin (UNIQUE)', 'survey_number', 'area', 'property_type', 'status', 'approved_by (FK)']),
        'ownerships': (12, 7, ['id (PK)', 'property_id (FK)', 'owner_id (FK)', 'ownership_type', 'share_percentage', 'start_date']),
        'mutations': (2, 4, ['id (PK)', 'mutation_number', 'property_id (FK)', 'requester_id (FK)', 'mutation_type', 'status', 'processed_by (FK)']),
        'payments': (7, 4, ['id (PK)', 'user_id (FK)', 'amount', 'payment_type', 'status', 'transaction_id', 'payment_date']),
        'documents': (12, 4, ['id (PK)', 'property_id (FK)', 'mutation_id (FK)', 'document_type', 'file_path', 'uploaded_at']),
        'audit_logs': (4.5, 1, ['id (PK)', 'user_id (FK)', 'action', 'entity_type', 'entity_id', 'timestamp', 'ip_address']),
        'notifications': (9.5, 1, ['id (PK)', 'user_id (FK)', 'title', 'message', 'notification_type', 'is_read', 'created_at']),
    }
    
    # Draw entities
    for entity, (x, y, attributes) in entities.items():
        # Entity box
        box_height = 0.3 + len(attributes) * 0.2
        entity_box = FancyBboxPatch((x-1, y-box_height), 2, box_height, 
                                   boxstyle="round,pad=0.05", 
                                   edgecolor='#1976D2', facecolor='#BBDEFB', linewidth=2)
        ax.add_patch(entity_box)
        
        # Entity name
        ax.text(x, y-0.15, entity.upper(), ha='center', fontsize=10, fontweight='bold')
        
        # Attributes
        for i, attr in enumerate(attributes):
            attr_y = y - 0.35 - i*0.2
            ax.text(x, attr_y, attr, ha='center', fontsize=7, family='monospace')
    
    # Relationships
    relationships = [
        # (from_entity, to_entity, label, style)
        ('users', 'properties', '1:N\napproves', 'dashed'),
        ('properties', 'ownerships', '1:N\nhas', 'solid'),
        ('users', 'ownerships', '1:N\nowns', 'solid'),
        ('properties', 'mutations', '1:N\nhas', 'solid'),
        ('users', 'mutations', '1:N\nrequests', 'dashed'),
        ('users', 'payments', '1:N\nmakes', 'solid'),
        ('properties', 'documents', '1:N\nhas', 'dashed'),
        ('mutations', 'documents', '1:N\nhas', 'dashed'),
        ('users', 'audit_logs', '1:N\nlogged', 'dotted'),
        ('users', 'notifications', '1:N\nreceives', 'solid'),
    ]
    
    for from_ent, to_ent, label, style in relationships:
        from_x, from_y, _ = entities[from_ent]
        to_x, to_y, _ = entities[to_ent]
        
        # Calculate connection points
        if from_x < to_x:
            start = (from_x + 1, from_y - 0.5)
            end = (to_x - 1, to_y - 0.5)
        elif from_x > to_x:
            start = (from_x - 1, from_y - 0.5)
            end = (to_x + 1, to_y - 0.5)
        else:
            start = (from_x, from_y - 1)
            end = (to_x, to_y + 0.3)
        
        arrow = FancyArrowPatch(start, end, 
                               arrowstyle='->', mutation_scale=15, 
                               linewidth=1.5, color='#424242', linestyle=style)
        ax.add_patch(arrow)
        
        # Label
        mid_x, mid_y = (start[0]+end[0])/2, (start[1]+end[1])/2
        ax.text(mid_x, mid_y, label, fontsize=7, ha='center', 
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='gray'))
    
    plt.tight_layout()
    plt.savefig('database_er_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Database ER diagram created: database_er_diagram.png")


def create_security_framework():
    """Create Security Framework Diagram"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.5, 'Multi-Layer Security Framework', 
            ha='center', fontsize=14, fontweight='bold')
    
    # Security layers (from outside to inside)
    layers = [
        (6, 4, 5, 2.5, 'Network Security\nHTTPS/TLS • Firewall • Rate Limiting', '#FFCDD2', '#D32F2F'),
        (6, 4, 4.2, 2, 'Application Security\nCSRF Protection • Input Validation • XSS Prevention', '#FFE0B2', '#F57C00'),
        (6, 4, 3.4, 1.5, 'Authentication & Authorization\nbcrypt Hashing • Session Management • RBAC', '#FFF9C4', '#F9A825'),
        (6, 4, 2.6, 1, 'Data Security\nSQL Injection Prevention • Parameterized Queries', '#C8E6C9', '#388E3C'),
        (6, 4, 1.8, 0.5, 'Audit & Monitoring\nComprehensive Logging • Anomaly Detection', '#BBDEFB', '#1976D2'),
    ]
    
    for x, y, w, h, text, facecolor, edgecolor in layers:
        ellipse = mpatches.Ellipse((x, y), w, h, 
                                  edgecolor=edgecolor, facecolor=facecolor, 
                                  linewidth=2.5, alpha=0.7)
        ax.add_patch(ellipse)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, 
               fontweight='bold', color='#212121')
    
    # Core
    core = mpatches.Circle((6, 4), 0.6, 
                          edgecolor='#4CAF50', facecolor='#A5D6A7', linewidth=3)
    ax.add_patch(core)
    ax.text(6, 4, 'Protected\nData', ha='center', va='center', 
           fontsize=10, fontweight='bold', color='#1B5E20')
    
    # Security features boxes
    features = [
        (1.5, 6.5, 'Password Security', ['bcrypt algorithm', 'Salt rounds: 12', 'Unique salts']),
        (10.5, 6.5, 'Session Security', ['Secure cookies', 'HTTPOnly flag', 'Session timeout']),
        (1.5, 1.5, 'RBAC Model', ['4 role types', 'Permission matrix', 'Hierarchical access']),
        (10.5, 1.5, 'Audit Logging', ['All operations', 'Immutable logs', 'Compliance ready']),
    ]
    
    for x, y, title, points in features:
        box = FancyBboxPatch((x-1, y-0.7), 2, 0.9, 
                            boxstyle="round,pad=0.08", 
                            edgecolor='#424242', facecolor='#E3F2FD', linewidth=2)
        ax.add_patch(box)
        ax.text(x, y+0.2, title, ha='center', fontsize=9, fontweight='bold')
        for i, point in enumerate(points):
            ax.text(x, y-0.1-i*0.2, f'• {point}', ha='center', fontsize=7)
    
    plt.tight_layout()
    plt.savefig('security_framework.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Security framework diagram created: security_framework.png")


def create_performance_comparison():
    """Create Performance Comparison Chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Query Response Time Comparison
    operations = ['Property\nSearch', 'Dashboard\nLoad', 'Complex\nJoin', 'Mutation\nProcess', 'Report\nGeneration']
    app_layer = [450, 820, 1200, 680, 1500]
    db_layer = [85, 150, 180, 95, 210]
    
    x = np.arange(len(operations))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, app_layer, width, label='Application Layer', 
                   color='#FF6B6B', edgecolor='black', linewidth=1.2)
    bars2 = ax1.bar(x + width/2, db_layer, width, label='Database Layer (Optimized)', 
                   color='#4ECDC4', edgecolor='black', linewidth=1.2)
    
    ax1.set_ylabel('Response Time (ms)', fontsize=11, fontweight='bold')
    ax1.set_title('Query Response Time Comparison', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(operations, fontsize=9)
    ax1.legend(fontsize=9)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}ms',
                    ha='center', va='bottom', fontsize=8, fontweight='bold')
    
    # Performance improvement percentage
    improvements = [((app-db)/app)*100 for app, db in zip(app_layer, db_layer)]
    colors = ['#FF6B6B' if imp < 70 else '#4ECDC4' if imp < 85 else '#95E1D3' 
             for imp in improvements]
    
    bars3 = ax2.barh(operations, improvements, color=colors, 
                    edgecolor='black', linewidth=1.2)
    ax2.set_xlabel('Performance Improvement (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Optimization Impact', fontsize=12, fontweight='bold')
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, imp) in enumerate(zip(bars3, improvements)):
        ax2.text(imp + 2, i, f'{imp:.1f}%', 
                va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✓ Performance comparison chart created: performance_comparison.png")


if __name__ == "__main__":
    print("Generating diagrams for IEEE research paper...\n")
    create_system_architecture()
    create_workflow_diagram()
    create_database_er_diagram()
    create_security_framework()
    create_performance_comparison()
    print("\n✓ All diagrams generated successfully!")
    print("\nGenerated files:")
    print("  1. system_architecture.png")
    print("  2. workflow_diagram.png")
    print("  3. database_er_diagram.png")
    print("  4. security_framework.png")
    print("  5. performance_comparison.png")
