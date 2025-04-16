from flask import Flask, render_template, request
from database import Database

app = Flask(__name__)
db = Database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/languages")
def languages():
    languages = db.list_languages()
    return render_template("languages.html", languages=languages)

@app.route("/tricks/<language>")
def tricks(language):
    data = db.load_language_tricks(language)
    if data:
        return render_template("tricks.html", data=data)
    return "Language not found", 404

@app.route("/tools")
def tools():
    tools = db.list_cybersecurity_tools()
    return render_template("tools.html", tools=tools)

@app.route("/guide/<tool>")
def guide(tool):
    data = db.load_cybersecurity_guide(tool)
    if data:
        return render_template("guide.html", data=data)
    return "Tool not found", 404

@app.route("/strategies")
def strategies():
    strategy_files = db.list_pentesting_files()
    return render_template("strategies.html", strategy_files=strategy_files)

@app.route("/strategy/<strategy_file>")
def strategy(strategy_file):
    data = db.load_pentesting_strategies(strategy_file)
    if data:
        return render_template("strategy.html", data=data)
    return "Strategy file not found", 404

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return render_template("search.html", query="", results={})
    results = db.search(query)
    return render_template("search.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
