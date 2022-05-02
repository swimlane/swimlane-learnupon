import requests
import backoff
from learnupon.helpers import backoff_hdlr, fatal_code, giveup_handler
import os


class LearnUponRestAPI(object):
    def __init__(
        self,
        portal_url=os.environ.get("LEARNUPON_PORTAL_URL"),
        username=os.environ.get("LEARNUPON_ACCESS_KEY_ID"),
        password=os.environ.get("LEARNUPON_SECRET_KEY"),
        advanced_mode=False,
    ):
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({"Content-Type": "application/json"})
        self.base_url = os.path.join(portal_url, "api/v1/")
        if not self.base_url.endswith("/"):
            self.base_url += "/"
        self.last_exception = {}
        self.rate_limit_remaining_minute = None
        self.rate_limit_remaining_weekly = None
        self.last_status_code = None
        self.request_id = None
        self.current_page = None
        self.records_per_page = None
        self.has_next_page = False
        self.advanced_mode = advanced_mode
        self.test_auth()

    # backoff helps handle LearnUpon's rate limiting
    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_time=12,
        max_tries=8,
        on_backoff=backoff_hdlr,
        giveup=fatal_code,
        on_giveup=giveup_handler,
    )
    def request(self, method, endpoint, params={}, *args, **kwargs):
        endpoint = endpoint.lstrip("/")
        url = os.path.join(self.base_url, endpoint)
        response = self.session.request(
            method=method, url=url, params=params, *args, **kwargs
        )
        self.rate_limit_remaining_minute = response.headers[
            "X-LU-Rate-Limit-Remaining-Minute"
        ]
        self.rate_limit_remaining_weekly = response.headers[
            "X-LU-Rate-Limit-Remaining-Week"
        ]
        if self.advanced_mode:
            return response
        data = response.json()
        data["context"] = {}
        data["context"]["client"] = self
        data["context"]["response"] = response
        data["context"]["request_url"] = endpoint
        data["context"]["request_method"] = method
        if "X-Request-Id" in response.headers:
            data["context"]["request_id"] = response.headers["X-Request-Id"]
        if "LU-Has-Next-Page" in response.headers:
            data["context"]["has_next_page"] = (
                False if response.headers["LU-Has-Next-Page"] == "false" else True
            )
        if "LU-Records-Per-Page" in response.headers:
            data["context"]["records_per_page"] = int(
                response.headers["LU-Records-Per-Page"]
            )
        if "LU-Current-Page" in response.headers:
            data["context"]["current_page"] = int(response.headers["LU-Current-Page"])
        if "message" in data:
            self.last_exception = data
            self.last_status_code = response.status_code
            raise requests.exceptions.RequestException(response=response)
        else:
            response.raise_for_status()
            return LearnUponRestAPIResponse(data)

    def test_auth(self):
        test = self.request(method="get", endpoint="portals")
        if test["context"]["response"].status_code < 400:
            print("Successfully Authenticated")


class LearnUponRestAPIResponse(dict):
    def paginate(self, responsekey=None, *args, **kwargs):
        response = self["context"]["response"]
        params = {}
        old_params = list(
            x.split("=") for x in requests.utils.urlparse(response.url).query.split("&")
        )
        if len(str(old_params)) > 6:
            params = dict(old_params)
        if "params" in kwargs:
            for k, v in list(kwargs["params"]):
                params[k] = v
        if responsekey is None:
            responsekeys = list(self.keys())
            if "customDataFieldDefintions" in responsekeys:
                responsekeys.remove("customDataFieldDefintions")
            if "customDataFieldDefinitions" in responsekeys:
                responsekeys.remove("customDataFieldDefinitions")
            if "context" in responsekeys:
                responsekeys.remove("context")
            responsekey = responsekeys[0]
        output = self[responsekey]
        if "has_next_page" in self["context"]:
            if self["context"]["has_next_page"] is True:
                current_page = self["context"]["current_page"]
                next_page = current_page + 1
                endpoint = self["context"]["request_url"]
                method = self["context"]["request_method"]
                latest = LearnUponRestAPI.request(
                    self=self["context"]["client"],
                    method=method,
                    endpoint=endpoint,
                    params={"page": next_page},
                ).paginate(
                    responsekey=responsekey,
                )
                output += latest[responsekey]
        self[responsekey] = output
        self["context"]["has_next_page"] = False
        return self


# X-LU-Rate-Limit-Remaining-Minute': '299', 'X-LU-Rate-Limit-Remaining-Week': '359920', 'LU-Current-Page': '1', 'LU-Records-Per-Page': '499', 'LU-Has-Next-Page': 'true'
