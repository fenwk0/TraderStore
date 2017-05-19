# swagger_client.BookNsApi

All URIs are relative to *https://localhost/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_book_active_bids_view**](BookNsApi.md#get_book_active_bids_view) | **GET** /book_ns/book/active_bids | 
[**get_book_active_offers_view**](BookNsApi.md#get_book_active_offers_view) | **GET** /book_ns/book/active_offers | 
[**get_book_order_view**](BookNsApi.md#get_book_order_view) | **GET** /book_ns/book/orders | Return the list of orders for the book
[**get_book_stats_view**](BookNsApi.md#get_book_stats_view) | **GET** /book_ns/book/stats | 
[**get_book_trade_view**](BookNsApi.md#get_book_trade_view) | **GET** /book_ns/book/trades | 
[**get_book_trader_order_view**](BookNsApi.md#get_book_trader_order_view) | **GET** /book_ns/book/traders/{trader}/orders | Return the list of orders for the book
[**get_book_view**](BookNsApi.md#get_book_view) | **GET** /book_ns/book | Returns a description of the book


# **get_book_active_bids_view**
> list[BookOrder] get_book_active_bids_view(x_fields=x_fields)



### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BookNsApi()
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    api_response = api_instance.get_book_active_bids_view(x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BookNsApi->get_book_active_bids_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**list[BookOrder]**](BookOrder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_book_active_offers_view**
> list[BookOrder] get_book_active_offers_view(x_fields=x_fields)



### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BookNsApi()
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    api_response = api_instance.get_book_active_offers_view(x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BookNsApi->get_book_active_offers_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**list[BookOrder]**](BookOrder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_book_order_view**
> list[BookOrder] get_book_order_view(x_fields=x_fields)

Return the list of orders for the book

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BookNsApi()
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    # Return the list of orders for the book
    api_response = api_instance.get_book_order_view(x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BookNsApi->get_book_order_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**list[BookOrder]**](BookOrder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_book_stats_view**
> Statistics get_book_stats_view(x_fields=x_fields)



### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BookNsApi()
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    api_response = api_instance.get_book_stats_view(x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BookNsApi->get_book_stats_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**Statistics**](Statistics.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_book_trade_view**
> list[Trade] get_book_trade_view(x_fields=x_fields)



### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BookNsApi()
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    api_response = api_instance.get_book_trade_view(x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BookNsApi->get_book_trade_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**list[Trade]**](Trade.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_book_trader_order_view**
> list[BookOrder] get_book_trader_order_view(trader, x_fields=x_fields)

Return the list of orders for the book

If trader is not None, return the list of orders for the given trader.

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BookNsApi()
trader = 'trader_example' # str | Trader name
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    # Return the list of orders for the book
    api_response = api_instance.get_book_trader_order_view(trader, x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BookNsApi->get_book_trader_order_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **trader** | **str**| Trader name | 
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**list[BookOrder]**](BookOrder.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_book_view**
> Book get_book_view(x_fields=x_fields)

Returns a description of the book

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.BookNsApi()
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    # Returns a description of the book
    api_response = api_instance.get_book_view(x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BookNsApi->get_book_view: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**Book**](Book.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

