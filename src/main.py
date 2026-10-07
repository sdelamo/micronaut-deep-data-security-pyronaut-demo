"""Logging configuration.

Pyronaut routes Python's ``logging`` onto Logback, so this ``dictConfig``
configures the whole application, Micronaut's own loggers included. It is the
equivalent of the ``logback.xml`` in the Java version of this demo.
"""

from logback.config import dictConfig

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "format": "%cyan(%d{HH:mm:ss.SSS}) %gray([%thread]) %highlight(%-5level) %magenta(%logger{36}) - %msg"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "TRACE",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        # Shows the End User Security Context the OJDBC extension hands to Oracle JDBC.
        "io.micronaut.security.ojdbc.extensions": {"level": "DEBUG"},
        "io.netty.channel.DefaultChannelPipeline": {"level": "ERROR"},
        # Prints every query Micronaut Data executes.
        "io.micronaut.data.query": {"level": "TRACE"},
    },
}

dictConfig(LOGGING)
