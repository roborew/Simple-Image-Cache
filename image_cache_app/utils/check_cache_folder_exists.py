import os


def check_cache_folder_exists(current_app):
    """
    Checks if the cache directory exists, and creates it if it doesn't.
    The cache directory path is retrieved from the application's configuration.
    """
    cache_dir = current_app.config["CACHE_DIR"]
    try:
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    except PermissionError:
        current_app.logger.error(
            f"Permission denied: Unable to create or access the directory {cache_dir}"
        )
        raise
    except Exception as e:
        current_app.logger.error(
            f"An error occurred while creating or accessing the directory {cache_dir}: {str(e)}"
        )
        raise
