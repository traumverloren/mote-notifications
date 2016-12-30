
import settings
import os
import time
import tweepy
import math
import random
import motephat as mote

from colorsys import hsv_to_rgb

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)
mote.set_brightness(0.1)

auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_SECRET'])

api = tweepy.API(auth)

speed = 1

class MoteLights():
    def rainbow_party(self):
        t_end = time.time() + 10

        while time.time() < t_end:
            h = time.time() * 50
            for channel in range(4):
                for pixel in range(16):
                    hue = (h + (channel * 64) + (pixel * 4)) % 360
                    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                    mote.set_pixel(channel + 1, pixel, r, g, b)
                mote.show()
                time.sleep(0.01)

        mote.clear()
        mote.show()

    def ocean_waves(self):
        t_end = time.time() + 10
        while time.time() < t_end:
            phase = 0

            for channel in range(4):
                for pixel in range(16):
                    hue_start = 160
                    hue_range = 80

                    h = (time.time() * speed) + (phase / 10.0)
                    h = math.sin(h) * (hue_range/2)
                    hue = hue_start + (hue_range/2) + h
                    hue %= 360

                    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                    mote.set_pixel(channel, pixel, r, g, b)

                    phase += 1

            mote.show()
            time.sleep(0.01)
            mote.clear()

        mote.clear()
        mote.show()

    def pink_waves(self):
        t_end = time.time() + 10
        while time.time() < t_end:
            phase = 0

            for channel in range(4):
                for pixel in range(16):
                    hue_start = 335
                    hue_range = 25

                    h = (time.time() * speed) + (phase / 10.0)
                    h = math.sin(h) * (hue_range/2)
                    hue = hue_start + (hue_range/2) + h
                    hue %= 360

                    r, g, b = [int(c * 255) for c in hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                    mote.set_pixel(channel, pixel, r, g, b)

                    phase += 1

            mote.show()
            time.sleep(0.01)
            mote.clear()

        mote.clear()
        mote.show()

class StephStreamListener(tweepy.StreamListener):
    lights = MoteLights()

    def on_connect(self):
        global lights
        lights.ocean_waves()

    # if a tweet is favorited, i'm followed or retweet is quoted, go pink
    def on_event(self, status):
        if status.event == 'favorite' or status.event == 'follow' or status.event == 'quoted_tweet':
            global lights
            lights.pink_waves()

    # if i get a reply to a tweet, do stuff
    def on_status(self, data):
        if data.in_reply_to_screen_name == "stephaniecodes":
            global lights
            lights.ocean_waves()

    # if I get a DM, go rainbow crazy
    def on_direct_message(self, data):
        global lights
        lights.rainbow_party()


    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StephStreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)

try:
    stream.userstream()
except KeyboardInterrupt:
    print "Exiting!"
    stream.disconnect()
    mote.clear()
    mote.show()
    sys.exit(0)
