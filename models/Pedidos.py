class Solicitacao:
    def __init__(self, filial, pedido, pedido_novo, item, descricao, motivo, obs, destino, regiao, arquivo):
        self.filial = filial # obrigatório
        self.pedido = pedido# obrigatório
        self.pedido_novo = pedido_novo
        self.item = item# obrigatório
        self.descricao = descricao# obrigatório
        self.motivo = motivo# obrigatório
        self.obs = obs# obrigatório
        self.destino = destino# obrigatório
        self.regiao = regiao# obrigatório
        self.arquivo = arquivo# obrigatório
    
    def validar(self):
        if self.pedido > 0 and self.item > 0 and self.descricao and self.destino != '' and self.motivo and self.obs and self.regiao and self.arquivo:
            return 'ok'
        else:
            return 'no'
              
    