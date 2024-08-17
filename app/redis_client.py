import redis
from settings import settings


class RedisConnection:
    def __init__(self, host: str, port: int = 6379):
        self.host = host
        self.port = port
        self.client = self.__connect()

    def __connect(self):
        return redis.Redis(host=self.host, port=self.port, decode_responses=True)

    def make_record(self, user_session_id: str, data: dict, ttl: int = 3600):
        for key, value in data.items():
            self.client.hset(user_session_id, key, value)
        self.client.expire(user_session_id, ttl)

    def get_record(self, user_session_id: str) -> dict:
        return self.client.hgetall(user_session_id)

    def update_expire_time(self, user_session_id: str, ttl: int = 3600):
        self.client.expire(user_session_id, ttl)


redis_connection = RedisConnection(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
