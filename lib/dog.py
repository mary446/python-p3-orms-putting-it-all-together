import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF  EXISTS dogs 
                
        """
        CURSOR.execute(sql)
    
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?) 
                
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid 
    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog
    @classmethod
    def new_from_db(cls, row):
        dog = cls(
            name = row[1], 
            breed = row[2],
            id = row[0]
            )
        return dog
    @classmethod
    def get_all(cls):
        sql = """
        SELECT *
        FROM dogs
        """
        all = CURSOR.execute(sql).fetchall()
        cls.all = [cls.new_from_db(row) for row in all]
        return cls.all
    @classmethod
    def find_by_name(cls, name):
        sql = """
        SELECT *
        FROM dogs
        WHERE name = ?
        LIMIT 1
        """
        dog = CURSOR.execute(sql, (name,)).fetchone()
        if not dog:
            return None
        return cls.new_from_db(dog)

    @classmethod
    def find_by_id(cls, id):
        sql = """
        SELECT *
        FROM dogs
        WHERE id = ?
        LIMIT 1
        """
        dog = CURSOR.execute(sql, (id,)).fetchone()
        if not dog:
            return None
        return cls.new_from_db(dog)

    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """
        dog = CURSOR.execute(sql, (name, breed)).fetchone()
        if not dog:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id = CURSOR.execute("SELECT last_insert_rowid() FROM dogs").fetchone()[0]
                # id=CURSOR.lastrowid  ##simpler way to express the above##
            )
        return cls.new_from_db(dog)
        
    def update(self):
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
    
