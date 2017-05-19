# swagger_client.StoreNsApi

All URIs are relative to *https://localhost/*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_order**](StoreNsApi.md#delete_order) | **DELETE** /store_ns/orders/{order_id} | Delete an existing order
[**get_order**](StoreNsApi.md#get_order) | **GET** /store_ns/orders/{order_id} | Return an existing order
[**get_orders**](StoreNsApi.md#get_orders) | **GET** /store_ns/orders | Return the list of orders in the store
[**get_store**](StoreNsApi.md#get_store) | **GET** /store_ns/store | Returns a description of the store
[**post_orders**](StoreNsApi.md#post_orders) | **POST** /store_ns/orders | Create a new order


# **delete_order**
> delete_order(order_id)

Delete an existing order

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StoreNsApi()
order_id = 'order_id_example' # str | 

try: 
    # Delete an existing order
    api_instance.delete_order(order_id)
except ApiException as e:
    print("Exception when calling StoreNsApi->delete_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_order**
> Order get_order(order_id, x_fields=x_fields)

Return an existing order

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StoreNsApi()
order_id = 'order_id_example' # str | 
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    # Return an existing order
    api_response = api_instance.get_order(order_id, x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StoreNsApi->get_order: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **order_id** | **str**|  | 
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**Order**](Order.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_orders**
> list[Order] get_orders(x_fields=x_fields)

Return the list of orders in the store

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StoreNsApi()
x_fields = 'x_fields_example' # str | An optional fields mask (optional)

try: 
    # Return the list of orders in the store
    api_response = api_instance.get_orders(x_fields=x_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StoreNsApi->get_orders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **x_fields** | **str**| An optional fields mask | [optional] 

### Return type

[**list[Order]**](Order.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_store**
> get_store()

Returns a description of the store

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StoreNsApi()

try: 
    # Returns a description of the store
    api_instance.get_store()
except ApiException as e:
    print("Exception when calling StoreNsApi->get_store: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_orders**
> post_orders(payload)

Create a new order

### Example 
```python
from __future__ import print_statement
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.StoreNsApi()
payload = swagger_client.Order() # Order | 

try: 
    # Create a new order
    api_instance.post_orders(payload)
except ApiException as e:
    print("Exception when calling StoreNsApi->post_orders: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **payload** | [**Order**](Order.md)|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

