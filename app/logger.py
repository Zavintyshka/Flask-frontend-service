from logging import getLogger, FileHandler, StreamHandler, Formatter, INFO

flask_logger = getLogger("flask_logger")
flask_logger.setLevel(INFO)

output_formatter = Formatter("%(asctime)s - [%(levelname)s] - %(message)s")

console_handler = StreamHandler()
user_file_handler = FileHandler("./logs/user_logs.log")
file_file_handler = FileHandler("./logs/file_logs.log")

console_handler.setFormatter(output_formatter)
user_file_handler.setFormatter(output_formatter)
file_file_handler.setFormatter(output_formatter)

flask_logger.addHandler(console_handler)
flask_logger.addHandler(user_file_handler)
flask_logger.addHandler(file_file_handler)
