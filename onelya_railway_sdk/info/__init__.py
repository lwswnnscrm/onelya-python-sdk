from datetime import datetime
from onelya_railway_sdk.utils import get_array, get_item, get_datetime
from onelya_railway_sdk.wrapper.requests import RequestWrapper
from onelya_railway_sdk.wrapper.types import OperationType, ProviderPaymentForm
from onelya_railway_sdk.wrapper import OrderCustomerInfo, RailwayFullOrderItemInfo, ShortOrderInfo

ORDER_INFO_METHOD = 'Order/V1/Info/OrderInfo'
ORDER_LIST_METHOD = 'Order/V1/Info/OrderList'


class Info(object):
    def __init__(self, session):
        self.__request_wrapper = RequestWrapper(session)

    def info(self, order_id: int=None, agent_reference_id: str=None):
        response = self.__request_wrapper.make_request(ORDER_INFO_METHOD, order_id=order_id,
                                                       agent_reference_id=agent_reference_id)
        return OrderInfo(response)

    def list(self, date: datetime=None, operation_type: OperationType=None,
             provider_payment_form: ProviderPaymentForm=None, is_externally_loaded: bool=None):
        response = self.__request_wrapper.make_request(ORDER_LIST_METHOD, date=date, operation_type=operation_type,
                                                       provider_payment_form=provider_payment_form,
                                                       is_externally_loaded=is_externally_loaded)
        return OrderList(response)


class OrderInfo(object):
    def __init__(self, json_data):
        self.order_customers = get_array(json_data.get('OrderCustomers', None), OrderCustomerInfo)
        self.order_items = get_array(json_data.get('OrderItems', None), RailwayFullOrderItemInfo)

        self.order_id = json_data.get('OrderId', None)
        self.amount = json_data.get('Amount', None)
        self.contact_phone = json_data.get('ContactPhone', None)
        self.contact_emails = json_data.get('ContactEmails', None)
        self.created = get_datetime(json_data.get('Created', None))
        self.confirmed = get_datetime(json_data.get('Confirmed', None))
        self.pos_sys_name = json_data.get('PosSysName', None)

        self.json_data = json_data


class OrderList(object):
    def __init__(self, json_data):
        self.orders = get_array(json_data.get('Orders', None), ShortOrderInfo)

        self.json_data = json_data