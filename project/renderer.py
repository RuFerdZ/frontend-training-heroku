from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}

        if data is not None:
            if 'message' in data:
                response_data['message'] = data['message']

            if 'errors' in data:
                response_data['status'] = 'ERROR'
                response_data['errors'] = data['errors']
            else:
                response_data['status'] = 'OK'
                response_data['data'] = data

        elif renderer_context['response'].status_code == 204:
            response_data = None

        else:
            response_data['message'] = 'success'

        # call super to render the response
        response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)

        return response
