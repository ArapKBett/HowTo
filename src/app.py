import os
import logging
from flask import Flask, render_template, request
from database import Database

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
    logger.debug("Initializing Flask app")
    app = Flask(__name__)
    
    logger.debug("Initializing Database")
    db = Database()
    
    @app.route("/")
    def index():
        logger.debug("Serving index page")
        return render_template("index.html")

    @app.route("/languages")
    def languages():
        logger.debug("Serving languages page")
        languages = db.list_languages()
        return render_template("languages.html", languages=languages)

    @app.route("/tricks/<language>")
    def tricks(language):
        logger.debug(f"Serving tricks for language: {language}")
        data = db.load_language_tricks(language)
        if data:
            return render_template("tricks.html", data=data)
        logger.error(f"Language not found: {language}")
        return "Language not found", 404

    @app.route("/tools")
    def tools():
        logger.debug("Serving tools page")
        tools = db.list_cybersecurity_tools()
        return render_template("tools.html", tools=tools)

    @app.route("/guide/<tool>")
    def guide(tool):
        logger.debug(f"Serving guide for tool: {tool}")
        data = db.load_cybersecurity_guide(tool)
        if data:
            return render_template("guide.html", data=data)
        logger.error(f"Tool not found: {tool}")
        return "Tool not found", 404

    @app.route("/strategies")
    def strategies():
        logger.debug("Serving strategies page")
        strategy_files = db.list_pentesting_files()
        return render_template("strategies.html", strategy_files=strategy_files)

    @app.route("/strategy/<strategy_file>")
    def strategy(strategy_file):
        logger.debug(f"Serving strategy: {strategy_file}")
        data = db.load_pentesting_strategies(strategy_file)
        if data:
            return render_template("strategy.html", data=data)
        logger.error(f"Strategy file not found: {strategy_file}")
        return "Strategy file not found", 404

    @app.route("/search")
    def search():
        query = request.args.get("q", "")
        logger.debug(f"Processing search query: {query}")
        if not query:
            return render_template("search.html", query="", results={})
        results = db.search(query)
        return render_template("search.html", query=query, results=results)

except Exception as e:
    logger.error(f"Failed to initialize app: {str(e)}", exc_info=True)
    raise

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.debug(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_ENV") == "development")
