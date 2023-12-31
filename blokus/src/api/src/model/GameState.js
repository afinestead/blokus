/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 *
 */

import ApiClient from '../ApiClient';


class GameState {
    
    constructor(status, turn) { 
        
        GameState.initialize(this, status, turn);
    }

    
    static initialize(obj, status, turn) { 
        obj['status'] = status;
        obj['turn'] = turn;
    }

    
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new GameState();

            if (data.hasOwnProperty('status')) {
                obj['status'] = ApiClient.convertToType(data['status'], Object);
            }
            if (data.hasOwnProperty('turn')) {
                obj['turn'] = ApiClient.convertToType(data['turn'], Object);
            }
        }
        return obj;
    }

    
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of GameState.RequiredProperties) {
            if (!data[property]) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }

        return true;
    }


}

GameState.RequiredProperties = ["status", "turn"];


GameState.prototype['status'] = undefined;


GameState.prototype['turn'] = undefined;






export default GameState;

