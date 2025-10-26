class ErrorResponse(Exception):
    def __init__(self, httpCode: int, message: str, error: any = None):
        # super serve para chamar o construtor da classe base (Exception)
        # ou seja, quando um Exception é criado, a mensagem é passada para o construtor da classe base
        # e é criado a mensagem personalizada
        
        super().__init__(message)
        self.__httpCode = httpCode
        self.__error = error
        
    # Getter para o código HTTP
    def httpCode(self) -> int:
        return self.__httpCode
    
    # Getter para o erro detalhado
    def error(self):
        return self.__error

    # Cria a representação em string do erro personalizado
    def __str__(self) -> str:
        return f"[{self.__httpCode}] {self.args[0]} | Detalhes: {self.__error}"