import requests
import json
from argparse import ArgumentParser
# from bs4 import BeautifulSoup


class WebPulsIR(object):
    # Phishing category is 18
    category = 18
    resultsrecip = 'information.security@uvmhealth.org'

    def __init__(self, baseurl='https://sitereview.bluecoat.com'):
        self.baseurl = baseurl
        self.session = requests.Session()
        self.session.get(self.baseurl)

    def reviewurl(self, url):
        classification = self.session.post(
            'https://sitereview.bluecoat.com/resource/lookup', json={
                'captcha': '', 'url': url})
        parsedclassification = json.loads(
            classification.content.decode("UTF-8"))
        reviewresult = "Results from WebPulse \n\n"
        reviewresult += "Category: " + parsedclassification[
            "categorization"][0]["name"] + "\n"
        reviewresult += "Date Reviewed: " + \
            parsedclassification[
                "translatedRateDates"][0]["text"][88:115] + "\n"
        reviewresult += "URL: " + parsedclassification["url"] + "\n"
        return reviewresult

    def submiturl(self, url):
        self.session.post('https://sitereview.bluecoat.com/resource/lookup',
                          json={'captcha': '', 'url': url})
        submission = self.session.post(
            'https://sitereview.bluecoat.com/resource/submitCategorization',
            json={
                "comments": "URL received in phishing email.",
                "email1": self.resultsrecip,
                "email2": "",
                "partner": "bluecoatsg",
                "referrer": "",
                "sendEmail": True,
                "trackid": "",
                "cat1": self.category,
                "cat2": None})
        parsedsubmission = json.loads(submission.content.decode("UTF-8"))
        return "Result from WebPulse:\n\n" + parsedsubmission['message']


def main(url, review=False, submit=False):
    if review is True and submit is True:
        wpobj = WebPulsIR()
        print(wpobj.reviewurl(url))
        print(wpobj.submiturl())
    elif review is True:
        wpobj = WebPulsIR()
        print(wpobj.reviewurl(url))
    elif submit is True:
        wpobj = WebPulsIR()
        wpobj.reviewurl(url)
        print(wpobj.submiturl())
    else:
        return "No switch specified."


if __name__ == "__main__":
    argobj = ArgumentParser()
    argobj.add_argument("-u", help="URL for WebPulse review/submission.")
    argobj.add_argument("-r", action='store_true',
                        help="Switch to specify review of URL to WebPulse.")
    argobj.add_argument("-s",
                        action='store_true',
                        help="Switch to specify submission of URL to WebPulse."
                        )
    args = argobj.parse_args()

    main(args.u, args.r, args.s)
