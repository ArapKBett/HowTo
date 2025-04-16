import json
import os

class Database:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.languages_dir = os.path.join(data_dir, "languages")
        self.cybersecurity_dir = os.path.join(data_dir, "cybersecurity")
        self.pentesting_dir = os.path.join(data_dir, "pentesting")

    def load_language_tricks(self, language):
        file_path = os.path.join(self.languages_dir, f"{language.lower()}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return None

    def load_cybersecurity_guide(self, tool):
        file_path = os.path.join(self.cybersecurity_dir, f"{tool.lower()}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return None

    def load_pentesting_strategies(self, strategy_file):
        file_path = os.path.join(self.pentesting_dir, f"{strategy_file.lower()}.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        return None

    def list_languages(self):
        return [f.replace(".json", "") for f in os.listdir(self.languages_dir) if f.endswith(".json")]

    def list_cybersecurity_tools(self):
        return [f.replace(".json", "") for f in os.listdir(self.cybersecurity_dir) if f.endswith(".json")]

    def list_pentesting_files(self):
        return [f.replace(".json", "") for f in os.listdir(self.pentesting_dir) if f.endswith(".json")]

    def search(self, query):
        query = query.lower()
        results = {"tricks": [], "guides": [], "strategies": []}

        # Search language tricks
        for lang in self.list_languages():
            data = self.load_language_tricks(lang)
            if data:
                for trick in data["tricks"]:
                    if query in trick["title"].lower() or query in trick["description"].lower() or query in trick["code"].lower():
                        trick["language"] = data["name"]
                        results["tricks"].append(trick)

        # Search cybersecurity guides
        for tool in self.list_cybersecurity_tools():
            data = self.load_cybersecurity_guide(tool)
            if data:
                for guide in data["guides"]:
                    if query in guide["title"].lower() or query in guide["description"].lower() or query in guide["command"].lower() or query in guide["explanation"].lower():
                        guide["tool"] = data["name"]
                        results["guides"].append(guide)

        # Search pentesting strategies
        for strategy_file in self.list_pentesting_files():
            data = self.load_pentesting_strategies(strategy_file)
            if data:
                for strategy in data["strategies"]:
                    if query in strategy["title"].lower() or query in strategy["description"].lower() or any(query in step.lower() for step in strategy["steps"]):
                        results["strategies"].append(strategy)

        return results
