import twitter
import requests


class ApiTwitterClient(twitter.Api):

    trends_available_url = "/trends/available.json"

    def __init__(self, consumerKey, consumerSecret, accessTokenKey, accessTokenSecret):
        self.consumerKey = consumerKey
        self.consumerSecret = consumerSecret
        self.accessTokenKey = accessTokenKey
        self.accessTokenSecret = accessTokenSecret
        self.all_countries = {}
        super().__init__(
            consumer_key=consumerKey,
            consumer_secret=consumerSecret,
            access_token_key=accessTokenKey,
            access_token_secret=accessTokenSecret)

    def getLatestTrends(self):
        current_trends = self.GetTrendsCurrent()
        return current_trends

    def getAvaiableTrends(self):
        url = '%s%s' % (self.base_url, self.trends_available_url)
        resp = self._RequestUrl(url, verb='GET')
        data = self._ParseAndCheckTwitter(resp.content.decode('utf-8'))

        for trend in data:
            print(trend)
            self.all_countries[trend['name']] = trend['woeid']
        return data

    def getTrendsFromPlace(self, place):
        woeid = self.all_countries.get(place.capitalize())
        if woeid is None:
            return None
        else:
            local_trends = self.GetTrendsWoeid(woeid)
            return local_trends

    @staticmethod
    def findCommonTrends(local_trends_dict, world_trends_dict):
        common_trend_names = []
        for local_tokens in local_trends_dict:
            local_trend_name = local_tokens['name']
            for world_tokens in world_trends_dict:
                world_trend_name = world_tokens['name']
                if local_trend_name.upper() == world_trend_name.upper():
                    common_trend_names.append(local_trend_name)
        return common_trend_names



