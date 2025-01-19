import psycopg2
import logging
class db():
    """Singleton для Posgresql"""
    __instance = None

    def __init__(self,HOST,PORT,USER,PASSWORD,DATABASE):
        if db.__instance is None:
            self.connection = psycopg2.connect(
                host=HOST,
                port=PORT,
                user=USER,
                password=PASSWORD,
                database=DATABASE
            )
            logging.info(f'Соединение установлено с базой {DATABASE}')
            db.__instance = self
        else:
            raise Exception("Этот класс является Singleton, используйте метод get_instance()")

    @staticmethod
    def get_instance():
        if not db.__instance:
            db()
        return db.__instance

    def execute(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()  # Подтверждаем изменения

    def fetchone(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполнение запроса
            return cursor.fetchone()[0] if cursor.rowcount > 0 else 0

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info('Соединение разорвано')
    def rollback(self):
        """Откат последней транзакции."""
        if self.connection:
            logging.info('Откат транзакции.')
            self.connection.rollback()
    def fetchall_with_headers(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)  # Выполнение запроса
            headers = [desc[0] for desc in cursor.description]  # Получение заголовков
            data = cursor.fetchall()  # Получение данных
        return [tuple(headers)]+ data  # Возвращаем заголовки и данные