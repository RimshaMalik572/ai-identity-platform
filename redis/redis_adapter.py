
import os
import json
import redis


class RedisAdapter:

    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", "6379"))
        self.db = int(os.getenv("REDIS_DB", "0"))

        self.client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            decode_responses=True
        )

    def health_check(self):

        try:
            response = self.client.ping()

            return {
                "status": "connected" if response else "not_connected",
                "host": self.host,
                "port": self.port
            }

        except Exception as e:

            return {
                "status": "not_connected",
                "host": self.host,
                "port": self.port,
                "reason": str(e)
            }

    def set_verification_result(
        self,
        user_id,
        result,
        ttl_seconds=3600
    ):

        key = f"identity:verification:{user_id}"

        self.client.setex(
            key,
            ttl_seconds,
            json.dumps(result)
        )

        return key

    def get_verification_result(self, user_id):

        key = f"identity:verification:{user_id}"

        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def set_trust_score(
        self,
        user_id,
        trust_score,
        risk_level,
        ttl_seconds=3600
    ):

        key = f"identity:trust:{user_id}"

        value = {
            "user_id": user_id,
            "trust_score": trust_score,
            "risk_level": risk_level
        }

        self.client.setex(
            key,
            ttl_seconds,
            json.dumps(value)
        )

        return key

    def get_trust_score(self, user_id):

        key = f"identity:trust:{user_id}"

        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)

    def set_risk_state(
        self,
        user_id,
        state,
        ttl_seconds=3600
    ):

        key = f"identity:risk:{user_id}"

        self.client.setex(
            key,
            ttl_seconds,
            json.dumps(state)
        )

        return key

    def get_risk_state(self, user_id):

        key = f"identity:risk:{user_id}"

        value = self.client.get(key)

        if value is None:
            return None

        return json.loads(value)
