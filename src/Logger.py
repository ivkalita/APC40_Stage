# Set this variable to True, if you want to use logging
CUSTOM_DEBUG_LOGGING = False
# Change this path by your log file path
CUSTOM_LOG_FILE_PATH = "/Users/dev/ableton_log.txt"

def custom_log(msg):
	if CUSTOM_DEBUG_LOGGING == False:
		return
	my_log = open(CUSTOM_LOG_FILE_PATH, "a")
	print >>my_log, msg
	my_log.close()