import requests
import json
from argparse import ArgumentParser


class WebPulsIR(object):

    def __init__(self):
        self.baseurl = "https://sitereview.bluecoat.com"
        self.session = requests.Session()
        self.session.get(self.baseurl)

    def reviewurl(self, url):
        classification = self.session.post(
            'https://sitereview.bluecoat.com/resource/lookup', json={'captcha': '', 'url': url})
        print classification.text

    def submiturl(self):
        submission = self.session.post('https://sitereview.bluecoat.com/resource/submitCategorization', json={
                                       "comments": "URL received in phishing email.",
                                       "email1": "information.security@uvmhealth.org",
                                       "email2": "",
                                       "partner": "bluecoatsg",
                                       "referrer": "",
                                       "sendEmail": True,
                                       "trackid": "",
                                       "cat1": 18,
                                       "cat2": None})
        print submission.text


def main(url):
    wpobj = WebPulsIR()
    wpobj.reviewurl(url)
    wpobj.submiturl()


if __name__ == "__main__":
    argobj = ArgumentParser()
    argobj.add_argument("url", help="Submit domain/URL to Symantec's Site Review")
    args = argobj.parse_args()

    main(args.url)
