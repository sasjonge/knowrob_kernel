from ipykernel.kernelbase import Kernel
import json
import os
from knowrob import *

class KnowRobKernel(Kernel):
    implementation = 'KnowRob'
    implementation_version = '1.0'
    language = 'prolog'
    language_version = '0.1'
    language_info = {
        'name': 'prolog',  # This tells Jupyter to use the 'prolog' mode in CodeMirror
        'mimetype': 'text/x-prolog',  # Specify the MIME type for Prolog
        'file_extension': '.pl',  # Typical Prolog file extension
    }
    banner = "KnowRob Kernel"

    def __init__(self, **kwargs):
        print("Start Init")
        InitKnowRob()
        # Define the path to the default.json file
        file_path = os.path.expanduser("~/.knowrob/settings/default.json")
        # Check if the file exists
        if os.path.isfile(file_path):
            self.kb = KnowledgeBase(file_path)
            print("Loaded " + file_path)
        else:
            self.kb = KnowledgeBase("settings/mongolog.json")
            print("Loaded settings/mongolog.json")
        Kernel.__init__(self, **kwargs)

    def run_query(self, query_string, modalities=None):
            # Helper function to perform a query on a knowledge base
        # Load the settings
        if (not modalities):
            modalities = {
                "epistemicOperator": EpistemicOperator.KNOWLEDGE,
                "aboutAgentIRI": "",
                "confidence": 0.0,
                "temporalOperator": TemporalOperator.CURRENTLY,
                "minPastTimestamp": -1.0,
                "maxPastTimestamp": -1.0,
            }
        # Create a formula for the query
        phi = QueryParser.parse(query_string)
        print("parse")
        # Apply the modality
        mPhi = InterfaceUtils.applyModality(modalities, phi)
        print("applyModality")
        # Get Result Stream
        resultStream = self.kb.submitQuery(mPhi, QueryContext(QueryFlag.QUERY_FLAG_ALL_SOLUTIONS))
        print("submitQuery")
        resultQueue = resultStream.createQueue()
        # Get the result
        nextResult = resultQueue.pop_front()
        if isinstance(nextResult, AnswerNo):
            return "False"
        elif isinstance(nextResult, AnswerDontKnow):
            return "Don't Know"
        elif isinstance(nextResult, AnswerYes):
            toReturn = ""
            for substitution in nextResult.substitution():
                variable = substitution[1]
                term = substitution[2]
                toReturn = toReturn + str(variable) + " : " + str(term) + ";\n"
            return toReturn


    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        if code.startswith('%kr_load_setting'):
            # Extract the settings JSON string (which comes after the magic command) and sanitize it
            json_settings_str_help = code[len('%kr_load_setting'):].strip()
            json_settings_str = ''.join(c for c in json_settings_str_help if c.isprintable())

            # Parse the settings into a dictionary
            settings_dict = json.loads(json_settings_str)
            
            # Convert the dictionary to a JSON string and initialize the KnowledgeBase
            json_str = json.dumps(settings_dict)
            self.kb = KnowledgeBase(json_str)
            
            # Send confirmation message back to the notebook
            result = "Settings loaded and KnowledgeBase initialized successfully."
        else:
            # Handle queries
            result = self.run_query(code)
        
        if not silent:
            # Send back the result
            stream_content = {'name': 'stdout', 'text': result}
            self.send_response(self.iopub_socket, 'stream', stream_content)

        # Return the result in the format expected by Jupyter
        return {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
        }