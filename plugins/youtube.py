from plugin_base import *

import logging
logging.basicConfig(format='\n%(asctime)s %(message)s', filename='../inzbot.log')

import re
import isodate
import requests

class YoutubePlugin(Plugin):

    @on_pubmsg
    @priority(80)
    def handle_line(self, bot, event):
        message = event.message
        youtube_links = ["youtube.com/watch?v=", "youtube.com/v/", "youtu.be/"]
        for link in youtube_links:
            index = message.find(link)
            if index == -1:
                continue
            after_main_link = message[index+len(link):]
            after_main_link = after_main_link.split(maxsplit=1)[0] # remove text after link
            video_id = re.split(r"\?|\.|&|=|/", after_main_link)[0]
            params = {
                "id": video_id,
                "key": bot.youtube_api_key,
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
                bot.message("adrian17: possible error, check it")
                return False
            bot.message("==== video: |{}| by {}, len: {} ====".format(video_title, video_author, str(duration)))
            return True