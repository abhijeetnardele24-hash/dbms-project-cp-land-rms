"""
Simple script to display all data from MySQL database
"""

import pymysql
from datetime import datetime

# Database connection
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='land_registry_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def print_separator(title):
    """Print a formatted separator with title"""
    print('\n' + '='*80)
    print(f' {title}')
    print('='*80)

def show_table_data(table_name, columns=None):
    """Show all data from a table"""
    print_separator(f'{table_name.upper()} TABLE')
    
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    print(f'\nTotal Records: {len(rows)}\n')
    
    if rows:
        for i, row in enumerate(rows, 1):
            print(f'Record #{i}:')
            for key, value in row.items():
                print(f'  {key}: {value}')
            print('-' * 80)
    else:
        print('No records found.')
    
    cursor.close()
    return len(rows)

def get_table_names():
    """Get all table names in the database"""
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [list(row.values())[0] for row in cursor.fetchall()]
    cursor.close()
    return tables

def main():
    try:
        print('\n')
        print('*' * 80)
        print(' LAND REGISTRY MANAGEMENT SYSTEM - COMPLETE DATABASE DUMP')
        print('*' * 80)
        
        # Get all tables
        tables = get_table_names()
        print(f'\nFound {len(tables)} tables in database')
        print('Tables:', ', '.join(tables))
        
        # Important tables to show first
        priority_tables = [
            'user',
            'owner', 
            'property',
            'ownership',
            'mutation',
            'payment',
            'notification',
            'document',
            'tax_assessment',
            'audit_log'
        ]
        
        # Show priority tables first
        for table in priority_tables:
            if table in tables:
                show_table_data(table)
                input(f'\nPress Enter to continue to next table...')
        
        # Show remaining tables
        remaining_tables = [t for t in tables if t not in priority_tables]
        if remaining_tables:
            print_separator('OTHER TABLES')
            print('\nRemaining tables:', ', '.join(remaining_tables))
            show_all = input('\nDo you want to see all remaining tables? (y/n): ')
            
            if show_all.lower() == 'y':
                for table in remaining_tables:
                    show_table_data(table)
                    input(f'\nPress Enter to continue...')
        
        print_separator('END OF DATA DUMP')
        print('\nAll data has been displayed!')
        
    except Exception as e:
        print(f'\nError: {e}')
    finally:
        conn.close()

if __name__ == '__main__':
    main()
