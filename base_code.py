from bs4 import BeautifulSoup
from urllib import request
import re

def analyse_a_question(url):
    """

    :param url: the url of the page to analyze. Example: https://www.xinli001.com//qa/100733774
    :return: a dictionary of the form:
        {
        'url':the url of the question
        'title': the title of the question
        'detail:' the detailed description of the question
        'answers':
            answer_no:
            {
                'reward': number of "赏"
                'like': number of "有用"
                'comment': number of "评论"
                'url': url of the answer
                'answer_html': answer in html format
                'answer_plain': answer in plain text format
            }
        }
    """
    try:
        output = {}
        output['answers'] = {}
        # Process the url
        html = request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        # Process the information of the question itself
        title = soup.select('.title span')[0].string
        detail = ''.join(str(soup.select('.content .text')[0]).split()[2:-1]).replace(r'<br/>', '\n')
        output['url'] = url
        output['title'] = title
        output['detail'] = detail
        # Determine page numbers
        pageNum = int(soup.select('.title strong')[0].string[:-3]) // 10 + 1
        # For each page, process each question
        output['answers'].update(analyse_a_question_page(html))
        for pageNum in range(2, pageNum + 1):
            url = r'https://www.xinli001.com//qa/100733774?page=' + str(pageNum)
            html = request.urlopen(url).read().decode('utf-8')
            try:
                output['answers'].update(analyse_a_question_page(html))
            except Exception as e:
                print(e)
        return output
    except Exception as e:
        print('Url Error: '+url+' Python recall: '+str(e))
        return None


def analyse_a_question_page(html):
    """
    :param html: the page of the question. Example: html = request.urlopen(https://www.xinli001.com//qa/100733774?page=3).read().decode('utf-8')
    :return: a dictionary of the form:
        {
            answer_no: string
            {
                'reward': number of "赏", int
                'like': number of "有用", int
                'comment': number of "评论", int
                'url': url of the answer
                'answer_html': answer in html format
                'answer_plain': answer in plain text format
            }
        }
    """
    output = {}
    soup = BeautifulSoup(html, "html.parser")
    answers = soup.select('li .label')
    for each_answer in answers:
        answer_soup = BeautifulSoup(str(each_answer), 'html.parser')
        if len(str(answer_soup.span.next_sibling.next_sibling).split()[-2]) < 10:
            reward = int(str(answer_soup.span.next_sibling.next_sibling).split()[-2])
        else:
            reward = 0
        like = int(answer_soup.select('.answer_zan font')[0].string)
        comment = int(answer_soup.select('.comment_num')[0].string)
        detail_url = answer_soup.select('.report_reply')[0].next_sibling.next_sibling['href']
        answer_no = detail_url.split('-')[-1]
        m_html = request.urlopen(detail_url).read().decode('utf-8') # the mobile site
        m_soup = BeautifulSoup(m_html, "html.parser")
        answer_html = str(m_soup.select('.ask_div_text')[0])
        answer_plain = re.sub(r'<br/>', '\n', answer_html)
        answer_plain = re.sub('<.{0,100}?>|\xa0','', answer_plain)
        #process output
        output[answer_no] = {}
        output[answer_no]['reward'] = reward
        output[answer_no]['like'] = like
        output[answer_no]['comment'] = comment
        output[answer_no]['url'] = detail_url
        output[answer_no]['answer_html'] = answer_html
        output[answer_no]['answer_plain'] = answer_plain
    return output


def traverse_n_questions(n):
    questions = {}
    for i in range(1, n+1):  # MAXIMUM for n: 1000 (1000 pages)
        page = questions_on_one_page(r'https://www.xinli001.com/qa?page=' + str(i))
        questions.update(page)
        print(str(i) + ' out of ' + str(n)+' questions processed')
    return questions


def questions_on_one_page(url):
    """
    :param url: the url of the page to analyze. Example: https://www.xinli001.com/qa?page=1
    :return: a dictionary of questions in the form:
            {
            'question_no': string
                {
                'title': the title of the question
                'url': the url of the question
                }
            }
    """
    html = request.urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    content = BeautifulSoup(str(soup.select('#main #left .content')), "html.parser")
    li = content.findAll('li')
    questions = {}

    for each_quest in li:
        for each in each_quest.children:
            try:
                title = str(each.p.a.next_sibling.next_sibling.span).split()[1]
                url = r'https://www.xinli001.com/' + str(each.p.a.next_sibling.next_sibling['href'].split('?')[0])
                no = url.split(r'/')[-1]
                questions[no] = {'title': title, 'url': url}
            except Exception as e:
                # print(e)
                pass
    return questions


if __name__ == '__main__':
    # print(traverse_500_questions())
    # print(questions_on_one_page('https://www.xinli001.com/qa'))
    print(analyse_a_question(r'https://www.xinli001.com//qa/100734469'))
