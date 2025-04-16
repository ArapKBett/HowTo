import json
import os
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, data_dir="data"):
        logger.debug(f"Initializing Database with data_dir: {data_dir}")
        self.data_dir = data_dir
        self.languages_dir = os.path.join(data_dir, "languages")
        self.cybersecurity_dir = os.path.join(data_dir, "cybersecurity")
        self.pentesting_dir = os.path.join(data_dir, "pentesting")
        
        # Verify directories exist
        for directory in [self.languages_dir, self.cybersecurity_dir, self.pentesting_dir]:
            if not os.path.exists(directory):
                logger.error(f"Directory not found: {directory}")
                raise FileNotFoundError(f"Directory not found: {directory}")

    def load_language_tricks(self, language):
        file_path = os.path.join(self.languages_dir, f"{language.lower()}.json")
        logger.debug(f"Loading language tricks from: {file_path}")
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return json.load(f)
            logger.warning(f"Language file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading language file {file_path}: {str(e)}")
            return None

    def load_cybersecurity_guide(self, tool):
        file_path = os.path.join(self.cybersecurity_dir, f"{tool.lower()}.json")
        logger.debug(f"Loading cybersecurity guide from: {file_path}")
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return json.load(f)
            logger.warning(f"Cybersecurity file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading cybersecurity file {file_path}: {str(e)}")
            return None

    def load_pentesting_strategies(self, strategy_file):
        file_path = os.path.join(self.pentesting_dir, f"{strategy_file.lower()}.json")
        logger.debug(f"Loading pentesting strategies from: {file_path}")
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return json.load(f)
            logger.warning(f"Pentesting file not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading pentesting file {file_path}: {str(e)}")
            return None

    def list_languages(self):
        logger.debug(f"Listing languages in: {self.languages_dir}")
        try:
            return [f.replace(".json", "") for f in os.listdir(self.languages_dir) if f.endswith(".json")]
        except Exception as e:
            logger.error(f"Error listing languages: {str(e)}")
            return []

    def list_cybersecurity_tools(self):
        logger.debug(f"Listing cybersecurity tools in: {self.cybersecurity_dir}")
        try:
            return [f.replace(".json", "") for f in os.listdir(self.cybersecurity_dir) if f.endswith(".json")]
        except Exception as e:
            logger.error(f"Error listing cybersecurity tools: {str(e)}")
            return []

    def list_pentesting_files(self):
        logger.debug(f"Listing pentesting files in: {self.pentesting_dir}")
        try:
            return [f.replace(".json", "") for f in os.listdir(self.pentesting_dir) if f.endswith(".json")]
        except Exception as e:
            logger.error(f"Error listing pentesting files: {str(e)}")
            return []

    def search(self, query):
        logger.debug(f"Searching for query: {query}")
        query = query.lower()
        results = {"tricks": [], "guides": [], "strategies": []}

        try:
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
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
        
        logger.debug(f"Search results: tricks={len(results['tricks'])}, guides={len(results['guides'])}, strategies={len(results['strategies'])}")
        return results
