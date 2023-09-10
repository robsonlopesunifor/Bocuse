class NonExistentPageFault(Exception):
    def __init__(self, error_message: str):
        self.STATUS_CODE = 400
        self.message = {"message": "O nome do titulo da pagina do fichario não existe.", "error": error_message}
        super().__init__(self.message, self.STATUS_CODE)
