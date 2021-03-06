# coding: utf-8

"""
    Market API

    A simple application exposing the Market to the web

    OpenAPI spec version: 1.0.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from pprint import pformat
from six import iteritems
import re


class Order(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, action=None, expiry=None, id=None, order_type=None, price=None, trader=None):
        """
        Order - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'action': 'str',
            'expiry': 'datetime',
            'id': 'str',
            'order_type': 'str',
            'price': 'float',
            'trader': 'str'
        }

        self.attribute_map = {
            'action': 'action',
            'expiry': 'expiry',
            'id': 'id',
            'order_type': 'order_type',
            'price': 'price',
            'trader': 'trader'
        }

        self._action = action
        self._expiry = expiry
        self._id = id
        self._order_type = order_type
        self._price = price
        self._trader = trader


    @property
    def action(self):
        """
        Gets the action of this Order.


        :return: The action of this Order.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this Order.


        :param action: The action of this Order.
        :type: str
        """
        allowed_values = ["sell", "buy"]
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"
                .format(action, allowed_values)
            )

        self._action = action

    @property
    def expiry(self):
        """
        Gets the expiry of this Order.


        :return: The expiry of this Order.
        :rtype: datetime
        """
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        """
        Sets the expiry of this Order.


        :param expiry: The expiry of this Order.
        :type: datetime
        """

        self._expiry = expiry

    @property
    def id(self):
        """
        Gets the id of this Order.


        :return: The id of this Order.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Order.


        :param id: The id of this Order.
        :type: str
        """

        self._id = id

    @property
    def order_type(self):
        """
        Gets the order_type of this Order.


        :return: The order_type of this Order.
        :rtype: str
        """
        return self._order_type

    @order_type.setter
    def order_type(self, order_type):
        """
        Sets the order_type of this Order.


        :param order_type: The order_type of this Order.
        :type: str
        """
        allowed_values = ["limit", "market"]
        if order_type not in allowed_values:
            raise ValueError(
                "Invalid value for `order_type` ({0}), must be one of {1}"
                .format(order_type, allowed_values)
            )

        self._order_type = order_type

    @property
    def price(self):
        """
        Gets the price of this Order.


        :return: The price of this Order.
        :rtype: float
        """
        return self._price

    @price.setter
    def price(self, price):
        """
        Sets the price of this Order.


        :param price: The price of this Order.
        :type: float
        """
        if price is None:
            raise ValueError("Invalid value for `price`, must not be `None`")

        self._price = price

    @property
    def trader(self):
        """
        Gets the trader of this Order.


        :return: The trader of this Order.
        :rtype: str
        """
        return self._trader

    @trader.setter
    def trader(self, trader):
        """
        Sets the trader of this Order.


        :param trader: The trader of this Order.
        :type: str
        """
        if trader is None:
            raise ValueError("Invalid value for `trader`, must not be `None`")

        self._trader = trader

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
