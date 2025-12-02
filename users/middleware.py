import logging

logger= logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter =  logging.Formatter(fmt="%(asctime)s %(levelname)s; %(message)s")
handler.formatter = formatter
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class LoggingMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)
        
        # Code to be executed for each request/response after
        # the view is called.
        return response