from urllib.request import Request, urlopen
import json
import os


class Slack:
    def send_message_to_slack(self, title, text):
        number_of_messages = int(len(text)/1000)
        if number_of_messages==0:
            number_of_messages=1
        else:
            number_of_messages= number_of_messages + 1

        for i in range(number_of_messages):
            sub_text = text[i*1000:(i+1)*1000]

            app_name = os.environ.get('APPLICATION_NAME', 'AI Services API')
            post = {"blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "\n*Application Name:*:" + app_name + "\n*Title*:" + str(i+1) + "_" + title + "\n```" + str(sub_text) + "```"
                    }
                }
            ]
            }
            try:
                json_data = json.dumps(post)
                web_hook = os.environ.get('NOTIFICATION_SLACK_WEB_HOOK')
                print("web_hook:: ", web_hook.__str__())
                req = Request(web_hook.__str__(), data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'})
                resp = urlopen(req)
                print(resp)
            except Exception as em:
                print("EXCEPTION: " + str(em))