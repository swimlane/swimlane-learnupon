def backoff_hdlr(details):
    """Prints backoff debug messages"""
    print(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target}".format(**details)
    )


def backoff_hdlr_with_args(details):
    """USE FOR DEBUGGING ONLY - Prints out all details about backoff events,
    including client object with credentials, to STDOUT
    """
    print(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target} with args {args} and kwargs "
        "{kwargs}".format(**details)
    )


def fatal_code(e):
    if "Number of requests has exceeded the 1 minute limit" in e.response.text:
        return False
    if 400 <= e.response.status_code < 500:
        return True


def giveup_handler(details):
    raise Exception(details["args"][0].last_exception)
