from ipykernel.kernelbase import Kernel
import json
from knowrob import *

class KnowRobKernel(Kernel):
    implementation = 'KnowRob'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'echo',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "KnowRob Kernel"

    def __init__(self, **kwargs):
        InitKnowRob()
        # Define the path to the default.json file
        file_path = os.path.expanduser("~/.knowrob/settings/default.json")
        # Check if the file exists
        if os.path.isfile(file_path):
            kb = KnowledgeBase(file_path)
        else:
            kb = KnowledgeBase("settings/mongolog.json")

    def run_query(query_string, modalities=None):
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
        # Apply the modality
        mPhi = InterfaceUtils.applyModality(modalities, phi)
        # Get Result Stream
        resultStream = kb.submitQuery(mPhi, QueryContext(QueryFlag.QUERY_FLAG_ALL_SOLUTIONS))
        resultQueue = resultStream.createQueue()
        # Get the result
        nextResult = resultQueue.pop_front()
        if isinstance(nextResult, AnswerNo):
            return "False"
        elif isinstance(nextResult, AnswerMaybe):
            return "Don't Know"
        elif isinstance(nextResult, AnswerNo):
            toReturn = ""
            for substitution in nextResult.substitution():
                variable = substitution[1]
                term = substitution[2]
                toReturn = toReturn + str(variable) + " : " + str(term) + ";\n"


    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        try:
            # Run the query with the provided code
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
        except Exception as e:
            # Handle exceptions and return an error message
            return {
                'status': 'error',
                'execution_count': self.execution_count,
                'ename': type(e).__name__,
                'evalue': str(e),
                'traceback': []
            }
