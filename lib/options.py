import sys

options = {}

def getOption(name, default = None):
    if name in options:
        return options[name]

    return default

def formatMessage(type, message, file, line):
    output = [type, ": "] if type else []

    if file:
        output.append(file)

        if line:
            output.extend(["(", str(line), ")"])

        output.append(": ")

    output.append(message)

    if not message.endswith("\n"):
        output.append("\n")

    return "".join(output)

def info(message, file = None, line = None):
    if getOption('verbose', False):
        print formatMessage(None, message, file, line),

def warn(message, file = None, line = None):
    if not getOption('warning', False):
        return

    sys.stderr.write(formatMessage("warning", message, file, line))

    if getOption('fail-on-warning', False):
        sys.exit(1)

def error(message, file = None, line = None):
    sys.stderr.write(formatMessage("error", message, file, line))

    if not getOption('ignore-errors', False):
        sys.exit(1)

def fatal(message, file = None, line = None):
    sys.exit(formatMessage("fatal", message, file, line))

def takeAction(action):
    if getOption('noaction', False):
        print "Would " + action
        return False

    info("Will now " + action)
    return True
