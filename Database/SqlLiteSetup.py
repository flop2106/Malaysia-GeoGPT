from sqlalchemy import text, create_engine
import utils.LoggerBaseUtil as LoggerBaseUtil
logger = LoggerBaseUtil.setup()
DATABASE_URL = 'sqlite:///GeoGPT.db'
engine = create_engine(DATABASE_URL)
#Base = declarative_base(engine)
def execute_sql(statement, parameters = None):
    with engine.connect() as connection:
        if parameters:
            result = connection.execute(statement, parameters)
        else:
            result = connection.execute(text(statement))
        if 'select' in str(statement).lower():
            result = result.fetchall()
        else:
            connection.commit()

    return result

def adding_item(table_name, keys, values):

    insert_item_statement = f"""
    INSERT INTO {table_name} ({keys})
    VALUES ({values})
    """
    execute_sql(insert_item_statement)
    print(f'New row inserted for {table_name}!')

def delete_item(table_name, condition):
    delete_item_statement = f"""
    DELETE FROM {table_name} WHERE {condition}
    """
    execute_sql(delete_item_statement)
    print(f'Rows deleted from {table_name}')

class PaperTable:

    @staticmethod
    def initialize_table():
        logger.info("Initialize Table listpaper")
        init_table_statement = """
                                CREATE TABLE IF NOT EXISTS listpaper (
                                paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                url TEXT,
                                authors TEXT,
                                abstract TEXT,
                               input_date DATE DEFAULT CURRENT_DATE
                               );
                          """
        execute_sql(init_table_statement)            
    @staticmethod
    def insert_paper(title, url, authors, abstract):
        adding_item("listpaper", "title, url, authors, abstract",f"'{title}','{url}','{authors}','{abstract}'")
    
    @staticmethod
    def get_paper_id():
        paper_id =  execute_sql(f"SELECT max(paper_id) FROM listpaper")
        
        return paper_id[0][0]

class EmbeddingsTable:
    @staticmethod
    def initialize_table():
        logger.info("Initialize Table embeddings")
        init_table_statement = """
                               CREATE TABLE IF NOT EXISTS embeddings (
                                   embeddings_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   embedding BLOB,
                                   paper_id INTEGER,
                                   FOREIGN KEY (paper_id) REFERENCES listpaper(paper_id)
                                   );
                               """
        execute_sql(init_table_statement)
    @staticmethod
    def insert_embeddings(paper_id, embedding):
        sql = text("INSERT INTO embeddings (embedding, paper_id) VALUES(:embedding, :paper_id)")
        execute_sql(sql, {"embedding": embedding.tobytes(), "paper_id": paper_id})

if __name__ == '__main__':
    execute_sql("SELECT * FROM embeddings LIMIT 5")