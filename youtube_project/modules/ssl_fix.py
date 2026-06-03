"""Patch ALL HTTP libraries to bypass broken SSL certs on this machine."""

import os
import ssl
import warnings

_PATCHED = False


def apply_ssl_fix() -> None:
    global _PATCHED
    if _PATCHED:
        return

    os.environ["DISABLE_SSL_VERIFY"] = "1"
    os.environ["PYTHONHTTPSVERIFY"] = "0"
    os.environ["CURL_CA_BUNDLE"] = ""
    os.environ["REQUESTS_CA_BUNDLE"] = ""

    try:
        import urllib3
        urllib3.disable_warnings()
    except Exception:
        pass

    warnings.filterwarnings("ignore")

    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except Exception:
        pass

    _patch_requests()
    _patch_urllib3()
    _PATCHED = True


def _patch_requests() -> None:
    import requests

    if getattr(requests.Session.request, "_ssl_patched", False):
        return

    _orig = requests.Session.request

    def _request(self, method, url, **kwargs):
        kwargs["verify"] = False
        return _orig(self, method, url, **kwargs)

    _request._ssl_patched = True
    requests.Session.request = _request

    for fn_name in ("request", "get", "post", "put", "delete", "head"):
        fn = getattr(requests, fn_name, None)
        if fn is None:
            continue

        def _wrap(original):
            def wrapper(*args, **kwargs):
                kwargs["verify"] = False
                return original(*args, **kwargs)
            return wrapper

        setattr(requests, fn_name, _wrap(fn))


def _patch_urllib3() -> None:
    try:
        import urllib3
        urllib3.disable_warnings()
        _orig = urllib3.PoolManager.__init__

        def _init(self, *args, **kwargs):
            kwargs["cert_reqs"] = ssl.CERT_NONE
            kwargs["assert_hostname"] = False
            _orig(self, *args, **kwargs)

        urllib3.PoolManager.__init__ = _init
    except Exception:
        pass
