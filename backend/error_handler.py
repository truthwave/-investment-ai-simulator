import logging

class ErrorHandler:
    def handle_error(self, error):
        logging.error(f"エラー発生: {error}")
        return {"status": "エラー", "message": str(error)}
