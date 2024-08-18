import shutil
from pathlib import Path
from app.redis_client import RedisConnection
from settings import PRELOAD_FOLDER, settings

redis_event_client = RedisConnection(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


def handle_expire_key(message):
    user_session_id = message["data"]
    delete_user_preload_folder(user_session_id)


def main():
    pubsub = redis_event_client.client.pubsub()
    pubsub.psubscribe(**{"__keyevent@0__:expired": handle_expire_key})
    thread = pubsub.run_in_thread(sleep_time=0.01)


def delete_user_preload_folder(user_session_id: str):
    path = Path(PRELOAD_FOLDER) / user_session_id
    shutil.rmtree(path)


if __name__ == "__main__":
    main()
