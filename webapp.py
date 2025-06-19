from flask import Flask, render_template, request, redirect, url_for, session
from LLM.VectorSearch import VectorSearch
from LLM.Chat import Chat
from Database.SqlLiteSetup import get_all

app = Flask(__name__)
app.secret_key = 'change-me'

ROLE = """a geology data calatog experts for malaysia. \
                       ONLY USE THE DATA PROVIDED AND AVOID USE YOUR OWN KNOWLEDGE. \
                       ENSURE AT THE BOTTOM OF YOUR RESPONSE ADD THE TITLE AND URL THAT YOU USE FOR REFERENCE. \
                       YOU ARE FOUND TO ALWAYS GET MIXED UP ON GEOGRAPHY LIKE SARAWAK IN PERAK. ENSURE YOU GOT THIS RIGHT WHEN GIVING ANSWER.\n                       """

def reset_session():
    session['history'] = []
    session['result_ids'] = None
    session['last_answer'] = None


def fetch_results(ids):
    if not ids:
        return []
    condition = f"paper_id in ({','.join(map(str, ids))})"
    return get_all("listpaper", condition)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        reset_session()
    if request.method == 'POST':
        if 'reset' in request.form:
            reset_session()
            return redirect(url_for('index'))
        # follow-up question
        if session.get('result_ids') and 'interrogate' in request.form:
            interrogation = request.form.get('interrogation')
            previous = session.get('last_answer')
            chat = Chat()
            answer = chat.execute(interrogation, ROLE, previous)
            session['history'].append(('user', interrogation))
            session['history'].append(('assistant', answer))
            session['last_answer'] = answer
            return redirect(url_for('index'))
        # new query
        query = request.form.get('query')
        if query:
            vs = VectorSearch()
            results = vs.execute(query)
            session['result_ids'] = [row[0] for row in results]
            result_str = ""
            for res in results:
                result_str += (
                    f"title: {res[1]}author: {res[3]}url: {res[2]}"
                    f"abstract: {res[4]}\n"
                )
            prompt = f"Based on the following data: {result_str} + summarize and answer the following query from the user: {query}"
            chat = Chat()
            answer = chat.execute(prompt, ROLE)
            session['history'].append(('user', query))
            session['history'].append(('assistant', answer))
            session['last_answer'] = answer
            return redirect(url_for('index'))
    results = fetch_results(session.get('result_ids'))
    return render_template('index.html', history=session.get('history'), results=results)

if __name__ == '__main__':
    app.run(debug=True)
