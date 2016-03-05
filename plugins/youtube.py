from plugin_base import *

import logging
logging.basicConfig(format='\n%(asctime)s %(message)s', filename='../inzbot.log')

import isodate
import requests

class YoutubePlugin(Plugin):
    """Prints data about a YouTube video from its link."""

    @on_pubmsg
    @priority(80)
    @pattern(R"youtube\.com\/watch\?v=(?P<id>[-\w]+)")
    @pattern(R"youtube\.com\/v\/(?P<id>[-\w]+)")
    @pattern(R"youtu\.be\/(?P<id>[-\w]+)")
    def handle_line(self, bot, event):
        video_id = event.match.group("id")
        params = {
            "id": video_id,
            "key": bot.google_api_key,
            "part": "snippet,contentDetails",
            "fields": "items(snippet(title,channelTitle),contentDetails(duration))"
        }
        try:
            json = requests.get("https://www.googleapis.com/youtube/v3/videos", params=params).json()
            video_title = json["items"][0]["snippet"]["title"].strip()
            video_author = json["items"][0]["snippet"]["channelTitle"].strip()
            video_len = json["items"][0]["contentDetails"]["duration"]
            duration = isodate.parse_duration(video_len)
        except Exception:
            logging.exception("")
            bot.message("possible error, check it", target="adrian17")
            return False
        bot.message("=== video: |{}| by {}, len: {} ===".format(video_title, video_author, str(duration)))
        return True