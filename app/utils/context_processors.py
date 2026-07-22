from flask import request


def inject_globals():
    return {
        'current_path': request.path,
        'now': __import__('datetime').datetime.now(),
    }
