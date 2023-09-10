from Bocuse.core.utils import return_message_error

def test_return_message_error():
    error = b"{'error':{'message':'mensagem de erro original'}}"
    error_message = return_message_error(error)
    return error_message == "mensagem de erro original"
