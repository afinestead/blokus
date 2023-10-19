# BlokusApi.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createNewGameGameCreatePost**](DefaultApi.md#createNewGameGameCreatePost) | **POST** /game/create | Create New Game
[**gameStateStateGet**](DefaultApi.md#gameStateStateGet) | **GET** /state | Game State
[**getCurrentPlayerPlayerGet**](DefaultApi.md#getCurrentPlayerPlayerGet) | **GET** /player | Get Current Player
[**joinGameGameGameIdJoinPost**](DefaultApi.md#joinGameGameGameIdJoinPost) | **POST** /game/{game_id}/join | Join Game
[**placePiecePlacePut**](DefaultApi.md#placePiecePlacePut) | **PUT** /place | Place Piece
[**whoseTurnTurnGet**](DefaultApi.md#whoseTurnTurnGet) | **GET** /turn | Whose Turn



## createNewGameGameCreatePost

> GameID createNewGameGameCreatePost(gameConfig)

Create New Game

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let gameConfig = new BlokusApi.GameConfig(); // GameConfig | 
apiInstance.createNewGameGameCreatePost(gameConfig).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **gameConfig** | [**GameConfig**](GameConfig.md)|  | 

### Return type

[**GameID**](GameID.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## gameStateStateGet

> GameState gameStateStateGet(opts)

Game State

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let opts = {
  'tokenQuery': null, // Object | 
  'tokenHeader': null // Object | 
};
apiInstance.gameStateStateGet(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tokenQuery** | [**Object**](.md)|  | [optional] 
 **tokenHeader** | [**Object**](.md)|  | [optional] 

### Return type

[**GameState**](GameState.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## getCurrentPlayerPlayerGet

> PlayerProfile getCurrentPlayerPlayerGet(opts)

Get Current Player

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let opts = {
  'tokenQuery': null, // Object | 
  'tokenHeader': null // Object | 
};
apiInstance.getCurrentPlayerPlayerGet(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tokenQuery** | [**Object**](.md)|  | [optional] 
 **tokenHeader** | [**Object**](.md)|  | [optional] 

### Return type

[**PlayerProfile**](PlayerProfile.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## joinGameGameGameIdJoinPost

> AccessToken joinGameGameGameIdJoinPost(gameId)

Join Game

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let gameId = null; // Object | 
apiInstance.joinGameGameGameIdJoinPost(gameId).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **gameId** | [**Object**](.md)|  | 

### Return type

[**AccessToken**](AccessToken.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## placePiecePlacePut

> Object placePiecePlacePut(bodyPlacePiecePlacePut, opts)

Place Piece

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let bodyPlacePiecePlacePut = new BlokusApi.BodyPlacePiecePlacePut(); // BodyPlacePiecePlacePut | 
let opts = {
  'tokenQuery': null, // Object | 
  'tokenHeader': null // Object | 
};
apiInstance.placePiecePlacePut(bodyPlacePiecePlacePut, opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bodyPlacePiecePlacePut** | [**BodyPlacePiecePlacePut**](BodyPlacePiecePlacePut.md)|  | 
 **tokenQuery** | [**Object**](.md)|  | [optional] 
 **tokenHeader** | [**Object**](.md)|  | [optional] 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## whoseTurnTurnGet

> Object whoseTurnTurnGet(opts)

Whose Turn

### Example

```javascript
import BlokusApi from 'blokusApi';

let apiInstance = new BlokusApi.DefaultApi();
let opts = {
  'tokenQuery': null, // Object | 
  'tokenHeader': null // Object | 
};
apiInstance.whoseTurnTurnGet(opts).then((data) => {
  console.log('API called successfully. Returned data: ' + data);
}, (error) => {
  console.error(error);
});

```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tokenQuery** | [**Object**](.md)|  | [optional] 
 **tokenHeader** | [**Object**](.md)|  | [optional] 

### Return type

**Object**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json

