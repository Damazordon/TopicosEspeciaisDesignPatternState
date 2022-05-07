import abc
from abc import abstractmethod


# Classe abstrata (interface) que faz a função de State
# (...) significam o mesmo que pass e evitam a necessidade de implementação de cada metodo

class ShoppingOrderState:

    @abstractmethod
    def get_name(self):
        ...

    @abstractmethod
    def approve_payment(self):
        ...

    @abstractmethod
    def reject_payment(self):
        ...

    @abstractmethod
    def wait_payment(self):
        ...

    @abstractmethod
    def ship_order(self):
        ...


class ShoppingOrder:
    state: ShoppingOrderState

    def __init__(self):
        self.state = OrderPending(self)

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
        print("O estado do pedido agora é: ", self.get_state_name())

    def get_state_name(self):
        return self.state.get_name()

    def approve_payment(self):
        self.state.approve_payment()

    def wait_payment(self):
        self.state.wait_payment()

    def reject_payment(self):
        self.state.reject_payment()

    def ship_order(self):
        self.state.ship_order()


class OrderApproved(ShoppingOrderState):
    __name__ = 'Pedido Aprovado'
    order: ShoppingOrder

    def __init__(self, order):
        self.order = order

    def get_name(self):
        return self.__name__

    def approve_payment(self):
        print("O pedido já está no estado 'Pagamento Aprovado'.")

    def reject_payment(self):
        self.order.set_state(OrderRejected(self.order))

    def wait_payment(self):
        self.order.set_state(OrderPending(self.order))

    def ship_order(self):
        print("Enviando pedido para o cliente...")


class OrderRejected(ShoppingOrderState):
    __name__ = 'Pedido Rejeitado'
    order: ShoppingOrder

    def __init__(self, order):
        self.order = order

    def get_name(self):
        return self.__name__

    def approve_payment(self):
        print("Não é possível aprovar o pagamento pois o pedido foi recusado.")

    def reject_payment(self):
        print("Não é possível recusar o pagamento pois o pedido já está recusado.")

    def wait_payment(self):
        print("Não é possível mudar para pendente pois o pedido foi recusado.")

    def ship_order(self):
        print("Não é possível enviar o pedido com pagamento recusado")


class OrderPending(ShoppingOrderState):
    __name__ = 'Pedido Pendente'
    order: ShoppingOrder

    def __init__(self, order):
        self.order = order

    def get_name(self):
        return self.__name__

    def approve_payment(self):
        self.order.set_state(OrderApproved(self.order))

    def reject_payment(self):
        self.order.set_state(OrderRejected(self.order))

    def wait_payment(self):
        print("O pedido já está no estado 'Pagamento Pendente'.")

    def ship_order(self):
        print("Não é possível enviar o pedido com pagamento pendente")


class Main:
    order = ShoppingOrder()  # Estado do pedido começa como pendente

    # O fluxo abaixo aprova o pagamento e envia o pedido
    order.approve_payment()  # Muda o estado do pedido para aprovado
    order.ship_order()  # Envia o pedido para o cliente

    # O fluxo abaixo troca o estado para pendente e não deixa o pedido ser enviado
    order.wait_payment()  # Troca o estado para pendente novamente
    order.ship_order()  # Não deixa o pedido ser enviado caso esteja pendente

    # Rejeita o pedido
    order.reject_payment()

    # Após o pedido ser rejeitado não é possível alterar o estado
    order.approve_payment()
    order.wait_payment()
    order.reject_payment()
    order.ship_order()
