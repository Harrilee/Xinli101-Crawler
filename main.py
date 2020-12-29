import base_code
import json
import time


def collect_questions(page_range):
    '''
    :param page_range: the range of pages you want to collect (max: 1000)
    :return: None
    '''
    questions = base_code.traverse_n_questions(page_range)
    json_file = json.dumps(questions)
    filename = 'Questions-' + str(page_range) + '_pages-' + time.strftime("%Y%m%d_%H-%M-%S", time.localtime()) + '.json'
    file = open(filename, 'w')
    file.write(json_file)
    file.close()
    print('Questions stored at: ' + filename)
    return filename


def process_answers(question_file):
    questions = json.loads(open(question_file).read())
    lenth = len(questions)
    i = 0 #number of questions processed
    k = 0 #number of times succeed
    for each in questions:
        i += 1
        response = base_code.analyse_a_question(questions[each]['url'])
        j = 1
        while response == None and j<=5: # Number of times retrying
            print('retrying...')
            time.sleep(1+j/2)
            j+=1
            response = base_code.analyse_a_question(questions[each]['url'])
        if j==5:
            j = 0
            continue
        j = 0
        json_file = json.dumps(response)
        filename = 'Answers-' + each+'-' + questions[each]['title'] + '_pages-' + time.strftime("%Y%m%d_%H-%M-%S",
                                                                                            time.localtime()) + '.json'
        file = open(filename, 'w')
        file.write(json_file)
        file.close()
        k+=1
        print(str(i) + ' out of ' + str(lenth) + ' questions processed. Success: '+ str(k)+'. '+ filename)



if __name__ == '__main__':
    # collect_questions(5)
    process_answers(collect_questions(5))
