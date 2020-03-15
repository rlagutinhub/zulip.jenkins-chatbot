#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import dialogflow_v2 as dialogflow


class DialogFlow(object):

    def __init__(self, credentials, project_id, language_code, session_id):

        self.credentials = credentials
        self.project_id = project_id
        self.language_code = language_code
        self.session_id = session_id

        if os.path.exists(self.credentials) and os.path.isfile(self.credentials):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials

        else:
            print('Error:', self.credentials)
            sys.exit(1)

    def request_msg(self, msg=None):

        response = None

        if not msg:
            return False

        try:
            session_client = dialogflow.SessionsClient()
            session = session_client.session_path(self.project_id, self.session_id)
            text_input = dialogflow.types.TextInput(text=msg, language_code=self.language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)

            response = session_client.detect_intent(session=session, query_input=query_input)

        except:
            return False

        if response:

            # print("Query text:", response.query_result.query_text)
            # print("Detected intent:", response.query_result.intent.display_name)
            # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
            # print("Fulfillment text:", response.query_result.fulfillment_text)

            return {
                'query': response.query_result.query_text,
                'intent': response.query_result.intent.display_name,
                'confidence': response.query_result.intent_detection_confidence,
                'answer': response.query_result.fulfillment_text
            }


def main():

    pass


if __name__ == '__main__':

    sys.exit(main())
