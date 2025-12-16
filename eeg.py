import time
from cortex2 import EmotivCortex2Client
from config import CORTEX_URL, CLIENT_ID, CLIENT_SECRET

class EmotivBCIClient:
    def __init__(self):
        self.client = EmotivCortex2Client(
            CORTEX_URL,
            client_id = CLIENT_ID,
            client_secret = CLIENT_SECRET,
            check_response = True,
            authenticate = True,
            debug = False, 
        )
        self.client.request_access()
        self.client.authenticate()

        self.client.query_headsets()
        self.client.connect_headset(0)
        self.client.create_session(0)

        self.client.subscribe(streams=['com'])

    def get_command(self):
        '''
        Returns (act, power) or (None, 0.0)
        Uses the background subscriber's data_streams instead of receive_data().
        '''

        if not self.client.data_streams:
            return None, 0.0
        
        session_streams = next(iter(self.client.data_streams.values()))

        com_deque = session_streams.get('com')
        if not com_deque or len(com_deque) == 0:
            return None, 0.0
        
        sample = com_deque[-1]
        com_values = sample.get("com")
        if not com_values or len(com_values) < 2:
            return None, 0.0

        act, power = com_values[0], com_values[1]

        # Sanity checks
        if not isinstance(act, str):
            return None, 0.0

        act = act.lower()
        if act == "neutral":
            return None, float(power)

        return act, float(power)
        
        # data = self.client.receive_data()
        # if not data:
        #     return None, 0.0
        
        # com_sample = data.get('com')
        # if not com_sample:
        #     return None, 0.0
        
        # act, power = com_sample[0]
        # if act.lower() == 'neutral':
        #     return None, power
        
        # return act.lower(), power