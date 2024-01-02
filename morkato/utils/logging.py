from typing import Any

import logging
import sys
import os

def is_docker() -> bool:
		path = '/proc/self/cgroup'
		return os.path.exists('/.dockerenv') or (os.path.isfile(path) and any('docker' in line for line in open(path)))


def stream_supports_colour(stream: Any) -> bool:
	if 'PYCHARM_HOSTED' in os.environ or os.environ.get('TERM_PROGRAM') == 'vscode':
		return True

	is_a_tty = hasattr(stream, 'isatty') and stream.isatty()
	if sys.platform != 'win32':
		return is_a_tty or is_docker()

	return is_a_tty and ('ANSICON' in os.environ or 'WT_SESSION' in os.environ)


class _ColourFormatter(logging.Formatter):

	LEVEL_COLOURS = [
		(logging.DEBUG, '\x1b[40;1m'),
		(logging.INFO, '\x1b[34;1m'),
		(logging.WARNING, '\x1b[33;1m'),
		(logging.ERROR, '\x1b[31m'),
		(logging.CRITICAL, '\x1b[41m'),
	]

	FORMATS = {
		level: logging.Formatter(
			f'\x1b[30;1m%(asctime)s\x1b[0m {colour}%(levelname)-8s\x1b[0m \x1b[35m%(name)s\x1b[0m %(message)s',
			'%Y-%m-%d %H:%M:%S',
		)
		for level, colour in LEVEL_COLOURS
	}

	def format(self, record):
		formatter = self.FORMATS.get(record.levelno)
		if formatter is None:
			formatter = self.FORMATS[logging.DEBUG]
		if record.exc_info:
			text = formatter.formatException(record.exc_info)
			record.exc_text = f'\x1b[31m{text}\x1b[0m'

		output = formatter.format(record)

		record.exc_text = None
		return output

def setup_logging(
	*,
	handler: logging.Handler = None,
	formatter: logging.Formatter = None,
	level: int = None,
	root: bool = False,
) -> None:
	if level is None:
		level = logging.INFO

	if handler is None:
		handler = logging.StreamHandler()

	if formatter is None:
		if isinstance(handler, logging.StreamHandler) and stream_supports_colour(handler.stream):
				formatter = _ColourFormatter()
		else:
			dt_fmt = '%Y-%m-%d %H:%M:%S'
			formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')

	if root:
		logger = logging.getLogger()
	else:
		library, _, _ = __name__.partition('.')
		logger = logging.getLogger(library)

	handler.setFormatter(formatter)
	logger.setLevel(level)
	logger.addHandler(handler)