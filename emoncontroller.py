from pip._vendor import requests


class EmonController:
    debug = False

    emonUrl = ""
    apiKey = ""

    def __init__(self, emonurl, apikey):
        self.emonUrl = emonurl
        self.apiKey = apikey

    def create_payload(self, gastotal, energytotal):
        """
        :param gastotal:
        :param energytotal:
        :return:
        """

        if self.is_debug():
            node_id = 17
        else:
            node_id = 20

        params = '[[4,' + str(node_id) + ',' + str(gastotal) + ',' + str(energytotal) + ']]'
        return params

    def build_url(self, pay_load):
        print pay_load
        url = str(self.emonUrl) + '?' + 'apikey=' + self.apiKey + '&data=' + str(pay_load)
        return url

    @staticmethod
    def post_url_func(url):
        print requests.get(url=url)

    def set_debug(self, do_debug):
        do_debug = bool(do_debug)
        self.debug = do_debug

    def is_debug(self):
        return self.debug

    def upload_results(self, energy_total, gas_total, current_watts):
        if gas_total > 0 and energy_total > 0:
            payload = self.create_payload(gas_total, energy_total)

            post_url = self.build_url(payload)
            print post_url
            self.post_url_func(post_url)