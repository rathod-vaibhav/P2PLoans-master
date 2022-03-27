import json
from datetime import datetime
from random import choice

import pymysql.cursors
import requests
from bs4 import BeautifulSoup
from flask import render_template, request, redirect, url_for

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoanApplicationDAO import LoanApplicationDAO
from project.com.dao.ScrapingDAO import ScrapingDAO
from project.com.vo.LoanApplicationVO import LoanApplicationVO
from project.com.vo.ScrapingVO import ScrapingVO


@app.route('/lender/insertScraping', methods=['GET'])
def lenderInsertScraping():
    try:
        if adminLoginSession() == 'lender':

            USER_AGENTS = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

            class InstagramScraper:
                def __init__(self, url, user_agents=None):
                    self.url = url
                    self.user_agents = user_agents

                def __random_agent(self):
                    if self.user_agents and isinstance(self.user_agents, list):
                        return choice(self.user_agents)
                    return choice(USER_AGENTS)

                def __request_url(self):
                    try:
                        response = requests.get(
                            self.url,
                            headers={'User-Agent': self.__random_agent()})
                        response.raise_for_status()
                    except requests.HTTPError:
                        raise requests.HTTPError('Received non-200 status code.')
                    except requests.RequestException:
                        raise requests.RequestException
                    else:
                        return response.text

                @staticmethod
                def extract_json(html):
                    soup = BeautifulSoup(html, 'html.parser')
                    body = soup.find('body')
                    script_tag = body.find('script')
                    raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
                    return json.loads(raw_string)

                def page_metrics(self):
                    results = {}
                    try:
                        response = self.__request_url()
                        json_data = self.extract_json(response)
                        metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
                    except Exception as e:
                        raise e
                    else:
                        for key, value in metrics.items():
                            if key != 'edge_owner_to_timeline_media':
                                if value and isinstance(value, dict):
                                    value = value['count']
                                    results[key] = value
                    return results

                def post_metrics(self):
                    results = []
                    try:
                        response = self.__request_url()
                        json_data = self.extract_json(response)
                        metrics = \
                            json_data['entry_data']['ProfilePage'][0]['graphql']['user'][
                                'edge_owner_to_timeline_media'][
                                'edges']
                    except Exception as e:
                        raise e
                    else:
                        for node in metrics:
                            node = node.get('node')
                            if node and isinstance(node, dict):
                                results.append(node)
                    return results

            url = request.args.get('borrowerSocialMediaLink')
            scrapingFrom_LoginId = request.args.get('loginId')

            instagram = InstagramScraper(url)
            post_metrics = instagram.post_metrics()
            print("<<<<<<<<<<<<<<<<,", post_metrics)

            print("------------------", instagram)

            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='root',
                                         db='pythondb',
                                         cursorclass=pymysql.cursors.DictCursor)

            update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            scrapingDAO = ScrapingDAO()

            for m in post_metrics:
                scrapingSocialId = str(m['id'])
                scrapingPostTime = datetime.fromtimestamp(m['taken_at_timestamp']).strftime('%Y-%m-%d %H:%M:%S')
                scrapingLike = int(m['edge_liked_by']['count'])
                scrapingComment = int(m['edge_media_to_comment']['count'])
                scrapingMedia = m['display_url']
                scrapingVideo = bool(m['is_video'])

                print(">>>>>>>>>>>>>>>>>>>")

                print("------------scrapingSocialId-----------", scrapingSocialId)
                print("------------scrapingPostTime----------", scrapingPostTime)
                print("------------scrapingLike-----------", scrapingLike)
                print("----------scrapingComment-----------", scrapingComment)
                print("-----------scrapingMedia----------", scrapingMedia)
                print("----------scrapingVideo------------", scrapingVideo)

                print(">>>>>>>>>>>>>>>>>>>")

                scrapingVO = ScrapingVO()

                scrapingVO.scrapingSocialId = scrapingSocialId
                scrapingVO.scrapingPostTime = scrapingPostTime
                scrapingVO.scrapingLike = scrapingLike
                scrapingVO.scrapingComment = scrapingComment
                scrapingVO.scrapingMedia = scrapingMedia
                scrapingVO.scrapingVideo = scrapingVideo
                scrapingVO.scrapingFrom_LoginId = scrapingFrom_LoginId

                scrapingDAO.insertScraping(scrapingVO)

            loanApplicationVO = LoanApplicationVO()
            loanApplicationDAO = LoanApplicationDAO()

            applicationId = request.args.get('applicationId')
            loanApplicationVO.scrapingStatus = 'viewed'
            loanApplicationVO.applicationId = applicationId
            loanApplicationDAO.insertScrapingStatus(loanApplicationVO)

            return redirect(url_for('lenderViewScraping', scrapingFrom_LoginId=scrapingFrom_LoginId))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/lender/viewScraping', methods=['GET'])
def lenderViewScraping():
    try:
        if adminLoginSession() == 'lender':

            scrapingDAO = ScrapingDAO()
            scrapingVO = ScrapingVO()

            scrapingFrom_LoginId = request.args.get('scrapingFrom_LoginId')
            scrapingVO.scrapingFrom_LoginId = scrapingFrom_LoginId

            scrapingVOList = scrapingDAO.viewScraping(scrapingVO)

            print("___________ scrapingVOList __________", scrapingVOList)

            return render_template('lender/viewScraping.html', scrapingVOList=scrapingVOList)

        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)
