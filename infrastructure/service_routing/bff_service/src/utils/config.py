import os


class Config:

    # post and comment config
    _user_host, _user_port = os.getenv("USERSERVICE_HOST", "localhost"), os.getenv("USERSERVICE_PORT", 8082)
    _post_host, _post_port = os.getenv("POSTSERVICE_HOST", "localhost"), os.getenv("POSTSERVICE_PORT", 8081)
    _comment_host, _comment_port = os.getenv("COMMENTSERVICE_HOST", "localhost"), os.getenv("COMMENTSERVICE_PORT", 8080)

    post_url, comment_url = f"http://{_post_host}:{_post_port}/posts", f"http://{_comment_host}:{_comment_port}/comments"

    # user confi
    user_url = f"http://{_user_host}:{_user_port}/users"

    # service config
    host, port = os.getenv("HOST", "0.0.0.0"), int(os.getenv("PORT", 80))
