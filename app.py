from flask import Flask, render_template, request, redirect, url_for, session
from LLM.VectorSearch import VectorSearch
from LLM.Chat import Chat
from uuid import uuid4

# In-memory store for session data to keep cookies small
SESSION_STORE = {}

app = Flask(__name__)
app.secret_key = 'change-me'

ROLE = """a geology data calatog experts for malaysia. \
                       ONLY USE THE DATA PROVIDED AND AVOID USE YOUR OWN KNOWLEDGE UNLESS ASKED BY USER. \
                       ENSURE AT THE BOTTOM OF YOUR RESPONSE ADD THE TITLE AND URL THAT YOU USE FOR REFERENCE. \
                       YOU ARE FOUND TO ALWAYS GET MIXED UP ON GEOGRAPHY LIKE SARAWAK IN PERAK. ENSURE YOU GOT THIS RIGHT WHEN GIVING ANSWER.\n                       """

def _init_store(sid):
    SESSION_STORE[sid] = {
        'history': [],
        'results': None,
        'last_answer': None
    }

def reset_session():
    sid = session.get('sid')
    if sid and sid in SESSION_STORE:
        del SESSION_STORE[sid]
    sid = str(uuid4())
    session['sid'] = sid
    _init_store(sid)

def _get_store():
    sid = session.get('sid')
    if not sid or sid not in SESSION_STORE:
        reset_session()
        sid = session['sid']
    return SESSION_STORE[sid]


@app.route('/', methods=['GET', 'POST'])
def index():
    store = _get_store()
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            vs = VectorSearch()
            results = vs.execute(query)
            results = [tuple(row) for row in results]
            store['results'] = results
            result_str = ""
            for res in results:
                result_str += (
                    f"title: {res[1]}author: {res[3]}url: {res[2]}"
                    f"abstract: {res[4]}\n"
                )
            prompt = (
                f"Based on the following data: {result_str} + summarize and answer the following query from the user: {query}"
            )
            chat = Chat()
            answer = chat.execute(prompt, ROLE)
            store['history'] = [('user', query), ('assistant', answer)]
            store['last_answer'] = answer
        return redirect(url_for('index'))
    return render_template(
        'index.html',
        results=store.get('results'),
        summary=store.get('last_answer'),
    )


@app.route('/chat', methods=['GET', 'POST'])
def chat_page():
    store = _get_store()
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form.get('query')
            if query:
                vs = VectorSearch()
                results = vs.execute(query)
                results = [tuple(row) for row in results]
                store['results'] = results
                result_str = ""
                for res in results:
                    result_str += (
                        f"title: {res[1]}author: {res[3]}url: {res[2]}"
                        f"abstract: {res[4]}\n"
                    )
                prompt = (
                    f"Based on the following data: {result_str} + summarize and answer the following query from the user: {query}"
                )
                chat = Chat()
                answer = chat.execute(prompt, ROLE)
                store['history'].append(('user', query))
                store['history'].append(('assistant', answer))
                store['last_answer'] = answer
        elif 'interrogate' in request.form:
            interrogation = request.form.get('interrogation')
            previous = store.get('last_answer')
            chat = Chat()
            answer = chat.execute(interrogation, ROLE, previous)
            store['history'].append(('user', interrogation))
            store['history'].append(('assistant', answer))
            store['last_answer'] = answer
        return redirect(url_for('chat_page'))
    return render_template(
        'chat.html',
        history=store.get('history'),
        results=store.get('results'),
    )

if __name__ == '__main__':
    app.run(debug=True)
