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
    instance = new BlokusApi.GameConfig();
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

  describe('GameConfig', function() {
    it('should create an instance of GameConfig', function() {
      // uncomment below and update the code to test GameConfig
      //var instance = new BlokusApi.GameConfig();
      //expect(instance).to.be.a(BlokusApi.GameConfig);
    });

    it('should have the property players (base name: "players")', function() {
      // uncomment below and update the code to test the property players
      //var instance = new BlokusApi.GameConfig();
      //expect(instance).to.be();
    });

    it('should have the property boardSize (base name: "board_size")', function() {
      // uncomment below and update the code to test the property boardSize
      //var instance = new BlokusApi.GameConfig();
      //expect(instance).to.be();
    });

    it('should have the property blockSize (base name: "block_size")', function() {
      // uncomment below and update the code to test the property blockSize
      //var instance = new BlokusApi.GameConfig();
      //expect(instance).to.be();
    });

  });

}));
