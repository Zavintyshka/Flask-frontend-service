import shutil
from pathlib import Path
from app.redis_client import RedisConnection
from settings import PRELOAD_FOLDER

redis_event_client = RedisConnection(host="localhost", port=6379)


def handle_expire_key(message):
    user_session_id = message["data"]
    user_preload_folder = Path(PRELOAD_FOLDER) / user_session_id
    shutil.rmtree(user_preload_folder)


def main():
    pubsub = redis_event_client.client.pubsub()
    pubsub.psubscribe(**{"__keyevent@0__:expired": handle_expire_key})
    thread = pubsub.run_in_thread(sleep_time=0.01)


if __name__ == "__main__":
    main()
