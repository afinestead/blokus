# BlokusApi.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getPiecesPiecesGet**](DefaultApi.md#getPiecesPiecesGet) | **GET** /pieces | Get Pieces
[**placePiecePlacePut**](DefaultApi.md#placePiecePlacePut) | **PUT** /place | Place Piece
[**rootGet**](DefaultApi.md#rootGet) | **GET** / | Root
[**startGameStartPost**](DefaultApi.md#startGameStartPost) | **POST** /start | Start Game



## getPiecesPiecesGet

> Object getPiecesPiecesGet(degree)

Get Pieces

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let degree = null; // Object | 
apiInstance.getPiecesPiecesGet(degree).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **degree** | [**Object**](.md)|  | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## placePiecePlacePut

> Object placePiecePlacePut(bodyPlacePiecePlacePut)

Place Piece

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let bodyPlacePiecePlacePut = new BlokusApi.BodyPlacePiecePlacePut(); // BodyPlacePiecePlacePut | 
apiInstance.placePiecePlacePut(bodyPlacePiecePlacePut).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bodyPlacePiecePlacePut** | [**BodyPlacePiecePlacePut**](BodyPlacePiecePlacePut.md)|  | 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## rootGet

> Object rootGet()

Root

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
apiInstance.rootGet().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters

This endpoint does not need any parameter.

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## startGameStartPost

> Object startGameStartPost()

Start Game

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
apiInstance.startGameStartPost().then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters

This endpoint does not need any parameter.

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

