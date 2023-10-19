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

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD.
    define(['expect.js', process.cwd()+'/src/index'], factory);
  } else if (typeof module === 'object' && module.exports) {
    // CommonJS-like environments that support module.exports, like Node.
    factory(require('expect.js'), require(process.cwd()+'/src/index'));
  } else {
    // Browser globals (root is window)
    factory(root.expect, root.BlokusApi);
  }
}(this, function(expect, BlokusApi) {
  'use strict';

  var instance;

  beforeEach(function() {
    instance = new BlokusApi.DefaultApi();
  });

  var getProperty = function(object, getter, property) {
    // Use getter method if present; otherwise, get the property directly.
    if (typeof object[getter] === 'function')
      return object[getter]();
    else
      return object[property];
  }

  var setProperty = function(object, setter, property, value) {
    // Use setter method if present; otherwise, set the property directly.
    if (typeof object[setter] === 'function')
      object[setter](value);
    else
      object[property] = value;
  }

  describe('DefaultApi', function() {
    describe('createNewGameGameCreatePost', function() {
      it('should call createNewGameGameCreatePost successfully', function(done) {
        //uncomment below and update the code to test createNewGameGameCreatePost
        //instance.createNewGameGameCreatePost(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('gameStateStateGet', function() {
      it('should call gameStateStateGet successfully', function(done) {
        //uncomment below and update the code to test gameStateStateGet
        //instance.gameStateStateGet(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('getCurrentPlayerPlayerGet', function() {
      it('should call getCurrentPlayerPlayerGet successfully', function(done) {
        //uncomment below and update the code to test getCurrentPlayerPlayerGet
        //instance.getCurrentPlayerPlayerGet(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('joinGameGameGameIdJoinPost', function() {
      it('should call joinGameGameGameIdJoinPost successfully', function(done) {
        //uncomment below and update the code to test joinGameGameGameIdJoinPost
        //instance.joinGameGameGameIdJoinPost(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('placePiecePlacePut', function() {
      it('should call placePiecePlacePut successfully', function(done) {
        //uncomment below and update the code to test placePiecePlacePut
        //instance.placePiecePlacePut(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
    describe('whoseTurnTurnGet', function() {
      it('should call whoseTurnTurnGet successfully', function(done) {
        //uncomment below and update the code to test whoseTurnTurnGet
        //instance.whoseTurnTurnGet(function(error) {
        //  if (error) throw error;
        //expect().to.be();
        //});
        done();
      });
    });
  });

}));
