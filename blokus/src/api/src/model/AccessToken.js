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


class AccessToken {
    
    constructor(accessToken) { 
        
        AccessToken.initialize(this, accessToken);
    }

    
    static initialize(obj, accessToken) { 
        obj['access_token'] = accessToken;
    }

    
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new AccessToken();

            if (data.hasOwnProperty('access_token')) {
                obj['access_token'] = ApiClient.convertToType(data['access_token'], Object);
            }
        }
        return obj;
    }

    
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of AccessToken.RequiredProperties) {
            if (!data[property]) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }

        return true;
    }


}

AccessToken.RequiredProperties = ["access_token"];


AccessToken.prototype['access_token'] = undefined;






export default AccessToken;

