
import os
from neo4j import GraphDatabase


class Neo4jGraphService:

    def __init__(self):

        self.uri = os.getenv(
            "NEO4J_URI",
            "bolt://localhost:7687"
        )

        self.username = os.getenv(
            "NEO4J_USERNAME",
            "neo4j"
        )

        self.password = os.getenv(
            "NEO4J_PASSWORD",
            ""
        )

        self.database = os.getenv(
            "NEO4J_DATABASE",
            "neo4j"
        )

        self.driver = None

    def connect(self):

        try:

            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(
                    self.username,
                    self.password
                )
            )

            self.driver.verify_connectivity()

            return {
                "status": "connected",
                "uri": self.uri,
                "database": self.database
            }

        except Exception as e:

            self.driver = None

            return {
                "status": "not_connected",
                "uri": self.uri,
                "database": self.database,
                "reason": str(e)
            }

    def close(self):

        if self.driver is not None:
            self.driver.close()

    def run_query(self, query, parameters=None):

        if self.driver is None:
            result = self.connect()

            if result["status"] != "connected":
                return result

        try:

            with self.driver.session(
                database=self.database
            ) as session:

                records = session.run(
                    query,
                    parameters or {}
                )

                return {
                    "status": "success",
                    "records": [
                        record.data()
                        for record in records
                    ]
                }

        except Exception as e:

            return {
                "status": "query_failed",
                "reason": str(e)
            }

    def get_user_relationships(self, user_id):

        query = """
        MATCH (u:User {user_id: $user_id})-[r]-(entity)
        RETURN
            type(r) AS relationship,
            labels(entity) AS entity_type,
            entity
        """

        return self.run_query(
            query,
            {"user_id": user_id}
        )
