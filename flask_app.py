#!/usr/bin/python3
import requests
import operator
import json
import urllib

from flask import Flask, render_template, request

HEADERS = {'Authorization': 'Bearer a1c83e791bef890e41b476c6cba31669a09f71fa94d5d3b9d6845a6c1bf12721f4ac9d2d3c687043637451d35cafdf08643062acf3c4af5c6cbe8128836370ea','Content-Type':'application/json'}
BASE_URL = 'https://hackicims.com/api/v1/companies/'
WEIGHT_EXPERT = 5
WEIGHT_ADVANCED = 3
WEIGHT_BEGINNER = 1
MAX_LIST_LENGTH = 10

company_ids = {60,61,62,63,91,92,93,94}
data = {}

def update_data():
    for comp_id in company_ids:
        data[comp_id] = {}
        urlget = urllib.parse.quote(''.join([BASE_URL, str(comp_id)]), safe='/:')
        data[comp_id]['info'] = requests.get(urlget, headers=HEADERS).json()
        # data[comp_id]['info'].json()
        urlget = urllib.parse.quote(''.join([BASE_URL, str(comp_id), '/', 'applications']), safe='/:')
        data[comp_id]['applications'] = requests.get(urlget, headers=HEADERS).json()
        # data[comp_id]['applications'].json()
        urlget = urllib.parse.quote(''.join([BASE_URL, str(comp_id), '/', 'jobs']), safe='/:')
        data[comp_id]['jobs'] = requests.get(urlget, headers=HEADERS).json()
        # data[comp_id]['jobs'].json()
        urlget = urllib.parse.quote(''.join([BASE_URL, str(comp_id), '/', 'people']), safe='/:')
        data[comp_id]['people'] = requests.get(urlget, headers=HEADERS).json()
        # data[comp_id]['people'].json()


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    company_id = request.values.get('company_id')
    person_id = request.values.get('person_id')
    job_name = request.values.get('job_name')
    if company_id not in company_ids or person_id not in data[company_id]['people']['id'].values():
        body = '''Please enter a company ID and personal ID'''
        return render_template('home.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    if request.method == 'POST':
        body = ''
        if company_id in company_ids and person_id in data[company_id]['people']['id'].values():
            for person in data[company_id]['people']:
                if person['id'] == person_id:
                    body = json.dumps(person, indent=2)
        return render_template('home.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    else:
        body = ''
        if company_id in company_ids and person_id in data[company_id]['people']['id'].values():
            for person in data[company_id]['people']:
                if person['id'] == person_id:
                    body = json.dumps(person, indent=2)
        return render_template('home.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)


@app.route('/update/', methods=['GET', 'POST'])
def update():
    company_id = request.values.get('company_id')
    person_id = request.values.get('person_id')
    job_name = request.values.get('job_name')
    if company_id == 'None' or company_id == '' or person_id == 'None' or person_id == '':
        body = '''Please enter a company ID and personal ID'''
        return render_template('update.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    if request.method == 'POST':
        body = '''

        '''
        return render_template('update.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    else:
        body = '''

        '''
        return render_template('update.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)


@app.route('/job/', methods=['GET', 'POST'])
def job():
    company_id = request.values.get('company_id')
    person_id = request.values.get('person_id')
    job_name = request.values.get('job_name')
    if company_id == 'None' or company_id == '' or person_id == 'None' or person_id == '' or job_name == 'None' or job_name == '':
        body = '''Please enter a company ID, personal ID, and job name'''
        return render_template('job.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    if request.method == 'POST':
        comp_applicants_all = set()
        comp_applicants_accepted = set()
        comp_applicants_rejected = set()
        for comp_id in company_ids:
        # for each company_id
            job_ids = set()
            for job in data[comp_id]['jobs']:
                if job['title'] == job_name:
                    job_ids.add(job['id'])
            # get a set of all job ids with the same title as job_name
            # now we have a set of all jobIds for this company
            for application in data[comp_id]['applications']:
                if application['jobId'] in job_ids:
                # for each application with a jobId in our set
                    comp_applicants_all.add((comp_id, application['personId']))
                    # add personId to set of all applicants
                    if application['status'] == 'OFFER_ACCEPTED' or application['status'] == 'OFFER_REJECTED':
                    # # if status is OFFER_ACCEPTED or OFFER_REJECTED
                        comp_applicants_accepted.add((comp_id, application['personId']))
                        # add personId to set of accepted applicants
                    elif application['status'] == 'REJECTED':
                    # else if status is REJECTED
                        comp_applicants_rejected.add((comp_id, application['personId']))
                        # add personId to set of rejected applicants
        body = ''
        all_job_skills = {}
        all_job_skills_weighted = {}
        acc_job_skills = {}
        acc_job_skills_weighted = {}
        rej_job_skills = {}
        rej_job_skills_weighted = {}
        # credit to https://realpython.com/python-json/ for the idea
        for comp_applicant in comp_applicants_all:
            # get person in data with comp_id = comp_applicant[0] and people['id'] = comp_applicant[1]
            for person in data[comp_applicant[0]]['people']:
                if person['id'] == comp_applicant[1]:
                    for skill in person['skills']:
                        try:
                            all_job_skills[skill['name']] += 1
                            if skill['level'] == 'Expert':
                                all_job_skills_weighted[skill['name']] += WEIGHT_EXPERT
                            elif skill['level'] == 'Advanced':
                                all_job_skills_weighted[skill['name']] += WEIGHT_ADVANCED
                            elif skill['level'] == 'Beginner':
                                all_job_skills_weighted[skill['name']] += WEIGHT_BEGINNER
                        except KeyError:
                            all_job_skills[skill['name']] = 1
                            if skill['level'] == 'Expert':
                                all_job_skills_weighted[skill['name']] = WEIGHT_EXPERT
                            elif skill['level'] == 'Advanced':
                                all_job_skills_weighted[skill['name']] = WEIGHT_ADVANCED
                            elif skill['level'] == 'Beginner':
                                all_job_skills_weighted[skill['name']] = WEIGHT_BEGINNER
        for comp_applicant in comp_applicants_accepted:
            for person in data[comp_applicant[0]]['people']:
                if person['id'] == comp_applicant[1]:
                    for skill in person['skills']:
                        try:
                            acc_job_skills[skill['name']] += 1
                            if skill['level'] == 'Expert':
                                acc_job_skills_weighted[skill['name']] += WEIGHT_EXPERT
                            elif skill['level'] == 'Advanced':
                                acc_job_skills_weighted[skill['name']] += WEIGHT_ADVANCED
                            elif skill['level'] == 'Beginner':
                                acc_job_skills_weighted[skill['name']] += WEIGHT_BEGINNER
                        except KeyError:
                            acc_job_skills[skill['name']] = 1
                            if skill['level'] == 'Expert':
                                acc_job_skills_weighted[skill['name']] = WEIGHT_EXPERT
                            elif skill['level'] == 'Advanced':
                                acc_job_skills_weighted[skill['name']] = WEIGHT_ADVANCED
                            elif skill['level'] == 'Beginner':
                                acc_job_skills_weighted[skill['name']] = WEIGHT_BEGINNER
        for comp_applicant in comp_applicants_rejected:
            for person in data[comp_applicant[0]]['people']:
                if person['id'] == comp_applicant[1]:
                    for skill in person['skills']:
                        try:
                            rej_job_skills[skill['name']] += 1
                            if skill['level'] == 'Expert':
                                rej_job_skills_weighted[skill['name']] += WEIGHT_EXPERT
                            elif skill['level'] == 'Advanced':
                                rej_job_skills_weighted[skill['name']] += WEIGHT_ADVANCED
                            elif skill['level'] == 'Beginner':
                                rej_job_skills_weighted[skill['name']] += WEIGHT_BEGINNER
                        except KeyError:
                            rej_job_skills[skill['name']] = 1
                            if skill['level'] == 'Expert':
                                rej_job_skills_weighted[skill['name']] = WEIGHT_EXPERT
                            elif skill['level'] == 'Advanced':
                                rej_job_skills_weighted[skill['name']] = WEIGHT_ADVANCED
                            elif skill['level'] == 'Beginner':
                                rej_job_skills_weighted[skill['name']] = WEIGHT_BEGINNER
        all_skills_sorted = sorted(all_job_skills.items(), key=lambda skill: skill[1], reverse=True)
        all_skills_weighted_sorted = sorted(all_job_skills_weighted.items(), key=lambda skill: skill[1], reverse=True)
        acc_skills_sorted = sorted(acc_job_skills.items(), key=lambda skill: skill[1], reverse=True)
        acc_skills_weighted_sorted = sorted(acc_job_skills_weighted.items(), key=lambda skill: skill[1], reverse=True)
        rej_skills_sorted = sorted(rej_job_skills.items(), key=lambda skill: skill[1], reverse=True)
        rej_skills_weighted_sorted = sorted(rej_job_skills_weighted.items(), key=lambda skill: skill[1], reverse=True)
        body = ''.join([body, 'Most common skills for this job among ALL applicants: '])
        list_len = min(len(all_skills_sorted), MAX_LIST_LENGTH)
        for i in range(0, list_len):
            body = ' ~ '.join([body, all_skills_sorted[i][0]])
        body = ''.join([body, ' | | | ']);
        body = ''.join([body, 'Most common skills for this job among ALL applicants: (weighted by skill level) '])
        list_len = min(len(all_skills_weighted_sorted), MAX_LIST_LENGTH)
        for i in range(0, list_len):
            body = ' ~ '.join([body, all_skills_weighted_sorted[i][0]])
        body = ''.join([body, ' | | | ']);
        body = ''.join([body, 'Most common skills for this job among ACCEPTED applicants:'])
        list_len = min(len(acc_skills_sorted), MAX_LIST_LENGTH)
        for i in range(0, list_len):
            body = ' ~ '.join([body, acc_skills_sorted[i][0]])
        body = ''.join([body, ' | | | ']);
        body = ''.join([body, 'Most common skills for this job among ACCEPTED applicants: (weighted by skill level)'])
        list_len = min(len(acc_skills_weighted_sorted), MAX_LIST_LENGTH)
        for i in range(0, list_len):
            body = ' ~ '.join([body, acc_skills_weighted_sorted[i][0]])
        body = ''.join([body, ' | | | ']);
        body = ''.join([body, 'Most common skills for this job among REJECTED applicants:'])
        list_len = min(len(rej_skills_sorted), MAX_LIST_LENGTH)
        for i in range(0, list_len):
            body = '\n- '.join([body, rej_skills_sorted[i][0]])
        body = ''.join([body, ' | | | ']);
        body = ''.join([body, 'Most common skills for this job among REJECTED applicants: (weighted by skill level)'])
        list_len = min(len(rej_skills_weighted_sorted), MAX_LIST_LENGTH)
        for i in range(0, list_len):
            body = '\n- '.join([body, rej_skills_weighted_sorted[i][0]])
        # body = ''.join([body, '\n\n']);
        return render_template('job.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    else:
        body = '''

        '''
        return render_template('job.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)


@app.route('/skill/', methods=['GET', 'POST'])
def skill():
    company_id = request.values.get('company_id')
    person_id = request.values.get('person_id')
    job_name = request.values.get('job_name')
    if company_id == 'None' or company_id == '' or person_id == 'None' or person_id == '':
        body = '''Please enter a company ID and personal ID'''
        return render_template('skill.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    if request.method == 'POST':
        body = '''

        '''
        return render_template('skill.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)
    else:
        body = '''

        '''
        return render_template('skill.html', company_id=company_id, person_id=person_id, job_name=job_name, body=body)



if __name__ == '__main__':
    update_data()
    app.run(debug=True, port=5000) #run app in debug mode on port 5000






# https://scotch.io/bar-talk/processing-incoming-request-data-in-flask

# # http://127.0.0.1:5000/query-example?language=your_language_value_here
# @app.route('/query-example')
# def query_example():
#     language = request.args.get('language') #if key doesn't exist, returns None
#     return '''<h1>The language value is: {}</h1>'''.format(language)

# @app.route('/form-example', methods=['GET', 'POST']) #allow both GET and POST requests
# def form_example():
#     if request.method == 'POST': #this block is only entered when the form is submitted
#         language = request.form.get('language')
#         framework = request.form['framework']
#         return '''<h1>The language value is: {}</h1>
#                   <h1>The framework value is: {}</h1>'''.format(language, framework)
#     return '''<form method="POST">
#                   Language: <input type="text" name="language"><br>
#                   Framework: <input type="text" name="framework"><br>
#                   <input type="submit" value="Submit"><br>
#               </form>'''

# @app.route('/json-example', methods=['POST']) #GET requests will be blocked
# def json_example():
#     req_data = request.get_json()
#     language = req_data['language']
#     framework = req_data['framework']
#     python_version = req_data['version_info']['python'] #two keys are needed because of the nested object
#     example = req_data['examples'][0] #an index is needed because of the array
#     boolean_test = req_data['boolean_test']
#     return '''
#            The language value is: {}
#            The framework value is: {}
#            The Python version is: {}
#            The item at index 0 in the example list is: {}
#            The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)



# https://realpython.com/python-json/

# https://hackicims.com/dashboard
# https://hackicims.com/guide

# GET Request to get company information
# urlget = urllib.parse.quote(''.join(['https://hackicims.com/api/v1/companies/',company_id]))
# r = requests.get(urlget, headers=headers)
# Do something with r.json() or r.text
# Status codes can be checked with r.status_code

# POST Request to make a job post named Software Developer for company 'One Company'
# payload = json.JSONEncoder().encode({'title': 'Software Developer IV'})
# urlpost = urllib.parse.quote(''.join(['https://hackicims.com/api/v1/companies/',company_id,'jobs']))
# r = requests.post(urlpost, data=payload, headers=headers)
# Status codes can be checked with r.status_code

# company_ids = []

# response = requests.get("https://jsonplaceholder.typicode.com/todos")
# todos = json.loads(response.text)



