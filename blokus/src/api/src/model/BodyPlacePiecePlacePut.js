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
import Coordinate from './Coordinate';
import Piece from './Piece';
import PlayerProfile from './PlayerProfile';


class BodyPlacePiecePlacePut {
    
    constructor(player, piece, origin) { 
        
        BodyPlacePiecePlacePut.initialize(this, player, piece, origin);
    }

    
    static initialize(obj, player, piece, origin) { 
        obj['player'] = player;
        obj['piece'] = piece;
        obj['origin'] = origin;
    }

    
    static constructFromObject(data, obj) {
        if (data) {
            obj = obj || new BodyPlacePiecePlacePut();

            if (data.hasOwnProperty('player')) {
                obj['player'] = PlayerProfile.constructFromObject(data['player']);
            }
            if (data.hasOwnProperty('piece')) {
                obj['piece'] = Piece.constructFromObject(data['piece']);
            }
            if (data.hasOwnProperty('origin')) {
                obj['origin'] = Coordinate.constructFromObject(data['origin']);
            }
        }
        return obj;
    }

    
    static validateJSON(data) {
        // check to make sure all required properties are present in the JSON string
        for (const property of BodyPlacePiecePlacePut.RequiredProperties) {
            if (!data[property]) {
                throw new Error("The required field `" + property + "` is not found in the JSON data: " + JSON.stringify(data));
            }
        }
        // validate the optional field `player`
        if (data['player']) { // data not null
          PlayerProfile.validateJSON(data['player']);
        }
        // validate the optional field `piece`
        if (data['piece']) { // data not null
          Piece.validateJSON(data['piece']);
        }
        // validate the optional field `origin`
        if (data['origin']) { // data not null
          Coordinate.validateJSON(data['origin']);
        }

        return true;
    }


}

BodyPlacePiecePlacePut.RequiredProperties = ["player", "piece", "origin"];


BodyPlacePiecePlacePut.prototype['player'] = undefined;


BodyPlacePiecePlacePut.prototype['piece'] = undefined;


BodyPlacePiecePlacePut.prototype['origin'] = undefined;






export default BodyPlacePiecePlacePut;

