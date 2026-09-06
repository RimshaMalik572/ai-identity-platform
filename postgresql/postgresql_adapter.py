
import os
import psycopg2
from psycopg2.extras import Json

class PostgreSQLAdapter:

    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = int(os.getenv("POSTGRES_PORT", "5432"))
        self.database = os.getenv("POSTGRES_DB", "ai_identity")
        self.user = os.getenv("POSTGRES_USER", "ai_identity_user")
        self.password = os.getenv("POSTGRES_PASSWORD", "")

    def connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def health_check(self):
        try:
            conn = self.connection()
            conn.close()
            return {
                "status": "connected",
                "database": self.database
            }
        except Exception as e:
            return {
                "status": "not_connected",
                "database": self.database,
                "reason": str(e)
            }

    def insert_verification(
        self,
        verification_id,
        user_id,
        verification_score,
        decision
    ):
        conn = self.connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO identity_verifications
                (verification_id, user_id, verification_score, decision)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    verification_id,
                    user_id,
                    verification_score,
                    decision
                )
            )

            conn.commit()

        finally:
            conn.close()
