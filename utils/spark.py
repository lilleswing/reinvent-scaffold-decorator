"""
Spark util functions
"""

import pyspark.sql as ps


class SparkSessionSingleton:
    """Manages unique spark sessions for each app name."""

    SESSIONS = {}

    def __init__(self):
        raise NotImplementedError("SparkSessionSingleton is not instantiable.")

    @classmethod
    def get(cls, app_name, params_func=None):
        """
        Retrieves (or creates) a session with a given app name.
        """

        if app_name not in cls.SESSIONS:
            session = ps.SparkSession.builder \
                .appName(app_name)
            session.config('spark.driver.memory', "16G")
            session.config('spark.driver.maxResultSize', '2G')
            session.config('spark.executor.memory', '2G')
            if params_func:
                params_func(session)
            session = session.getOrCreate()
            context = session.sparkContext
            context.setLogLevel("ERROR")

            cls.SESSIONS[app_name] = (session, context)
        return cls.SESSIONS[app_name]

    @classmethod
    def cleanup(cls):
        """
        Closes all sessions.
        """
        for session, _ in cls.SESSIONS.values():
            session.close()
        cls.SESSIONS = {}
