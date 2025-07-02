from flask import Flask, render_template, request, redirect, url_for, session
from LLM.VectorSearch import VectorSearch
from LLM.Chat import Chat

app = Flask(__name__)
app.secret_key = 'change-me'

ROLE = """a geology data calatog experts for malaysia. \
                       ONLY USE THE DATA PROVIDED AND AVOID USE YOUR OWN KNOWLEDGE UNLESS ASKED BY USER. \
                       ENSURE AT THE BOTTOM OF YOUR RESPONSE ADD THE TITLE AND URL THAT YOU USE FOR REFERENCE. \
                       YOU ARE FOUND TO ALWAYS GET MIXED UP ON GEOGRAPHY LIKE SARAWAK IN PERAK. ENSURE YOU GOT THIS RIGHT WHEN GIVING ANSWER.\n                       """



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            vs = VectorSearch()
            results = vs.execute(query)
            results = [list(row) for row in results]
            session['results'] = results
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
            session['history'] = [['user', query], ['assistant', answer]]
            session['last_answer'] = answer
            session['last_query'] = query

        return redirect(url_for('index'))
    return render_template(
        'index.html',
        results=session.get('results'),
        summary=session.get('last_answer'),
        query=session.get('last_query'),

    )


@app.route('/chat', methods=['GET', 'POST'])
def chat_page():
    if request.method == 'POST':
        if 'query' in request.form:
            query = request.form.get('query')
            if query:
                vs = VectorSearch()
                results = vs.execute(query)
                results = [list(row) for row in results]
                session['results'] = results
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
                history = session.get('history', [])
                history.append(['user', query])
                history.append(['assistant', answer])
                session['history'] = history
                session['last_answer'] = answer
        elif 'interrogate' in request.form:
            interrogation = request.form.get('interrogation')
            previous = session.get('last_answer')
            chat = Chat()
            answer = chat.execute(interrogation, ROLE, previous)
            history = session.get('history', [])
            history.append(['user', interrogation])
            history.append(['assistant', answer])
            session['history'] = history
            session['last_answer'] = answer
        return redirect(url_for('chat_page'))
    return render_template(
        'chat.html',
        history=session.get('history'),
        results=session.get('results'),
    )


if __name__ == '__main__':
    app.run(debug=True)
