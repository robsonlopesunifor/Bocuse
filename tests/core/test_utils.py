from Bocuse.core.utils import returnMessageError

def test_return_message_error():
    error = b"{'error':{'message':'mensagem de erro original'}}"
    error_message = returnMessageError(error)
    return error_message == "mensagem de erro original"
