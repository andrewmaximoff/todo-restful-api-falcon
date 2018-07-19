def serialize_to_json(req, resp, exception):
    representation = None

    preferred = req.client_prefers(('application/x-yaml',
                                    'application/json'))

    if preferred is not None:
        if preferred == 'application/json':
            representation = exception.to_json()
        else:
            representation = exception.to_xml()
        resp.body = representation
        resp.content_type = preferred

    resp.append_header('Vary', 'Accept')
