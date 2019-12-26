import os
import sqlite3

db_filename = 'todo.db'
schema_filename = 'c:\\Users\\Anna\\Documents\\pj\\SQL_homework\\todo_schema.sql'

db_is_new = not os.path.exists(db_filename)

with sqlite3.connect(db_filename) as conn:
    if db_is_new:
        print('Creating schema')
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

        print('Schema Created Successfully')
        
        print('Inserting initial data')

        conn.executescript("""
        insert into spendings (category, amount, timedate)
        values ('Food', '250',
                '2019-11-30');

        insert into spendings (category, amount, timedate)
        values ('Credit', '150',
                '2019-11-30');  

        insert into spendings (category, amount, timedate)
        values ('Clothes', '100',
                '2019-11-30');     

        insert into subcategory (amount_spent, details, when_spent, category)
        values ('50', 'feast', '2019-11-26',
                'Food');

        insert into subcategory (amount_spent, details, when_spent, category)
        values ('40', 'grandmother', '2019-11-24',
                'Food');

        insert into subcategory (amount_spent, details, when_spent, category)
        values ('100', 'boots', '2019-11-28',
                'Clothes');
        """)

    else:
        print('Database exists, assume schema does, too.')

with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()

    cursor.execute("""
    select id, amount_spent, details, when_spent, category from subcategory
    where category = 'Food'
    """)

    for row in cursor.fetchall():
        subcategory_id, amount_spent, details, when_spent, category = row
        print('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
            subcategory_id, amount_spent, details, when_spent, category))

with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()

    cursor.execute("""
        select category, amount, timedate from spendings
        where category = 'Credit'
        """)
    category, amount, timedate = cursor.fetchone()

    print('\nSpendings for {} are {} due to {}'.format(
        category, amount, timedate))

with sqlite3.connect(db_filename) as conn:
    
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
    select id, amount_spent, details, when_spent, category from subcategory
    where category = 'Food' order by when_spent
    """)

    print('\nSpendings for food by data:')
    for row in cursor.fetchmany(5):
        print('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
            row['id'], row['amount_spent'], row['details'], row['when_spent'],
            row['category'],
        ))

with sqlite3.connect(db_filename) as conn:
    cursor = conn.cursor()
    query = "update subcategory set details = 'Products for grandmother' where id = :id"
    cursor.execute(query, {'id': subcategory_id})
  
    conn.row_factory = sqlite3.Row

    cursor.execute("""
    select id, amount_spent, details, when_spent, category from subcategory
    where category = 'Food'
    """)

    print('\nAmended spendings for food:')
    for row in cursor.fetchall():
        subcategory_id, amount_spent, details, when_spent, category = row
        print('{:2d} [{:d}] {:<25} [{:<8}] ({})'.format(
            subcategory_id, amount_spent, details, when_spent, category))