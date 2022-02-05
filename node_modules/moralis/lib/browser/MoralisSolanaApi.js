"use strict";

var _Object$defineProperty = require("@babel/runtime-corejs3/core-js-stable/object/define-property");

var _interopRequireDefault = require("@babel/runtime-corejs3/helpers/interopRequireDefault");

_Object$defineProperty(exports, "__esModule", {
  value: true
});

exports.default = void 0;

var _regenerator = _interopRequireDefault(require("@babel/runtime-corejs3/regenerator"));

var _forEach = _interopRequireDefault(require("@babel/runtime-corejs3/core-js-stable/instance/for-each"));

var _keys = _interopRequireDefault(require("@babel/runtime-corejs3/core-js-stable/object/keys"));

var _filter = _interopRequireDefault(require("@babel/runtime-corejs3/core-js-stable/instance/filter"));

var _includes = _interopRequireDefault(require("@babel/runtime-corejs3/core-js-stable/instance/includes"));

var _asyncToGenerator2 = _interopRequireDefault(require("@babel/runtime-corejs3/helpers/asyncToGenerator"));

var _classCallCheck2 = _interopRequireDefault(require("@babel/runtime-corejs3/helpers/classCallCheck"));

var _createClass2 = _interopRequireDefault(require("@babel/runtime-corejs3/helpers/createClass"));

var _defineProperty2 = _interopRequireDefault(require("@babel/runtime-corejs3/helpers/defineProperty"));
/**
 * Automatically generated code, via genSolanaAPI.js
 * Do not modify manually
 */


var axios = require('axios');

var SolanaApi = /*#__PURE__*/function () {
  function SolanaApi() {
    (0, _classCallCheck2.default)(this, SolanaApi);
  }

  (0, _createClass2.default)(SolanaApi, null, [{
    key: "initialize",
    value: // URL will be changed when api is deployed
    function (_ref) {
      var apiKey = _ref.apiKey,
          serverUrl = _ref.serverUrl,
          _ref$Moralis = _ref.Moralis,
          Moralis = _ref$Moralis === void 0 ? null : _ref$Moralis;

      if (!serverUrl && !apiKey) {
        throw new Error('SolanaApi.initialize failed: initialize with apiKey or serverUrl');
      }

      if (apiKey) this.apiKey = apiKey;
      if (serverUrl) this.serverUrl = serverUrl;
      this.Moralis = Moralis;
    }
  }, {
    key: "getBody",
    value: function (params, bodyParams) {
      var _this = this;

      if (!params || !bodyParams || !bodyParams.length) {
        return undefined;
      }

      var body = {};
      (0, _forEach.default)(bodyParams).call(bodyParams, function (_ref2) {
        var key = _ref2.key,
            type = _ref2.type,
            required = _ref2.required;

        if (params[key] === undefined) {
          if (required) throw new Error("param ".concat(key, " is required!"));
        } else if (type === _this.BodyParamTypes.setBody) {
          body = params[key];
        } else {
          body[key] = params[key];
        } // remove the param so it doesn't also get added as a query param


        delete params[key];
      });
      return body;
    }
  }, {
    key: "getParameterizedUrl",
    value: function (url, params) {
      var _context;

      if (!(0, _keys.default)(params).length) return url; // find url params, they start with :

      var requiredParams = (0, _filter.default)(_context = url.split('/')).call(_context, function (s) {
        return s && (0, _includes.default)(s).call(s, ':');
      });
      if (!requiredParams.length) return url;
      var parameterizedUrl = url;
      (0, _forEach.default)(requiredParams).call(requiredParams, function (p) {
        // strip the : and replace with param value
        var key = p.substr(1);
        var value = params[key];

        if (!value) {
          throw new Error("required param ".concat(key, " not provided"));
        }

        parameterizedUrl = parameterizedUrl.replace(p, value); // remove required param from param list
        // so it doesn't become part of the query params

        delete params[key];
      });
      return parameterizedUrl;
    }
  }, {
    key: "getErrorMessage",
    value: function (error, url) {
      var _error$response, _error$response$data;

      return (error === null || error === void 0 ? void 0 : (_error$response = error.response) === null || _error$response === void 0 ? void 0 : (_error$response$data = _error$response.data) === null || _error$response$data === void 0 ? void 0 : _error$response$data.message) || (error === null || error === void 0 ? void 0 : error.message) || (error === null || error === void 0 ? void 0 : error.toString()) || "Solana API error while calling ".concat(url);
    }
  }, {
    key: "fetch",
    value: function () {
      var _fetch = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee(_ref3) {
        var endpoint, params, _endpoint$method, method, url, bodyParams, User, user, parameterizedUrl, body, response, msg;

        return _regenerator.default.wrap(function (_context2) {
          while (1) {
            switch (_context2.prev = _context2.next) {
              case 0:
                endpoint = _ref3.endpoint, params = _ref3.params;
                _endpoint$method = endpoint.method, method = _endpoint$method === void 0 ? 'GET' : _endpoint$method, url = endpoint.url, bodyParams = endpoint.bodyParams;

                if (this.Moralis) {
                  User = this.Moralis.User;
                  user = User.current();

                  if (!params.address) {
                    if (user) {
                      params.address = user.get('solAddress');
                    }
                  }
                }

                if (!params.network) params.network = 'mainnet';
                if (!params.responseType) params.responseType = 'native';

                if (this.apiKey) {
                  _context2.next = 7;
                  break;
                }

                return _context2.abrupt("return", this.apiCall(endpoint.name, params));

              case 7:
                _context2.prev = 7;
                parameterizedUrl = this.getParameterizedUrl(url, params);
                body = this.getBody(params, bodyParams);
                _context2.next = 12;
                return axios(this.baseURL + parameterizedUrl, {
                  params: params,
                  method: method,
                  body: body,
                  headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json',
                    'x-api-key': this.apiKey
                  }
                });

              case 12:
                response = _context2.sent;
                return _context2.abrupt("return", response.data);

              case 16:
                _context2.prev = 16;
                _context2.t0 = _context2["catch"](7);
                msg = this.getErrorMessage(_context2.t0, url);
                throw new Error(msg);

              case 20:
              case "end":
                return _context2.stop();
            }
          }
        }, _callee, this, [[7, 16]]);
      }));

      return function () {
        return _fetch.apply(this, arguments);
      };
    }()
  }, {
    key: "apiCall",
    value: function () {
      var _apiCall = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee2(name, options) {
        var http, response, _error$response2, _error$response2$data;

        return _regenerator.default.wrap(function (_context3) {
          while (1) {
            switch (_context3.prev = _context3.next) {
              case 0:
                if (this.serverUrl) {
                  _context3.next = 2;
                  break;
                }

                throw new Error('SolanaAPI not initialized, run Moralis.start() first');

              case 2:
                _context3.prev = 2;
                http = axios.create({
                  baseURL: this.serverUrl
                });
                _context3.next = 6;
                return http.post("/functions/sol-".concat(name), options, {
                  headers: {
                    Accept: 'application/json',
                    'Content-Type': 'application/json'
                  }
                });

              case 6:
                response = _context3.sent;
                return _context3.abrupt("return", response.data.result);

              case 10:
                _context3.prev = 10;
                _context3.t0 = _context3["catch"](2);

                if (!((_error$response2 = _context3.t0.response) !== null && _error$response2 !== void 0 && (_error$response2$data = _error$response2.data) !== null && _error$response2$data !== void 0 && _error$response2$data.error)) {
                  _context3.next = 14;
                  break;
                }

                throw new Error(_context3.t0.response.data.error);

              case 14:
                throw _context3.t0;

              case 15:
              case "end":
                return _context3.stop();
            }
          }
        }, _callee2, this, [[2, 10]]);
      }));

      return function () {
        return _apiCall.apply(this, arguments);
      };
    }()
  }]);
  return SolanaApi;
}();

(0, _defineProperty2.default)(SolanaApi, "baseURL", 'https://solana-gateway.moralis.io');
(0, _defineProperty2.default)(SolanaApi, "BodyParamTypes", {
  setBody: 'set body',
  property: 'property'
});
(0, _defineProperty2.default)(SolanaApi, "account", {
  balance: function () {
    var _balance = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee3() {
      var options,
          _args3 = arguments;
      return _regenerator.default.wrap(function (_context4) {
        while (1) {
          switch (_context4.prev = _context4.next) {
            case 0:
              options = _args3.length > 0 && _args3[0] !== undefined ? _args3[0] : {};
              return _context4.abrupt("return", SolanaApi.fetch({
                endpoint: {
                  "method": "GET",
                  "group": "account",
                  "name": "balance",
                  "url": "/account/:network/:address/balance"
                },
                params: options
              }));

            case 2:
            case "end":
              return _context4.stop();
          }
        }
      }, _callee3);
    }));

    return function () {
      return _balance.apply(this, arguments);
    };
  }(),
  getSPL: function () {
    var _getSPL = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee4() {
      var options,
          _args4 = arguments;
      return _regenerator.default.wrap(function (_context5) {
        while (1) {
          switch (_context5.prev = _context5.next) {
            case 0:
              options = _args4.length > 0 && _args4[0] !== undefined ? _args4[0] : {};
              return _context5.abrupt("return", SolanaApi.fetch({
                endpoint: {
                  "method": "GET",
                  "group": "account",
                  "name": "getSPL",
                  "url": "/account/:network/:address/tokens"
                },
                params: options
              }));

            case 2:
            case "end":
              return _context5.stop();
          }
        }
      }, _callee4);
    }));

    return function () {
      return _getSPL.apply(this, arguments);
    };
  }(),
  getNFTs: function () {
    var _getNFTs = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee5() {
      var options,
          _args5 = arguments;
      return _regenerator.default.wrap(function (_context6) {
        while (1) {
          switch (_context6.prev = _context6.next) {
            case 0:
              options = _args5.length > 0 && _args5[0] !== undefined ? _args5[0] : {};
              return _context6.abrupt("return", SolanaApi.fetch({
                endpoint: {
                  "method": "GET",
                  "group": "account",
                  "name": "getNFTs",
                  "url": "/account/:network/:address/nft"
                },
                params: options
              }));

            case 2:
            case "end":
              return _context6.stop();
          }
        }
      }, _callee5);
    }));

    return function () {
      return _getNFTs.apply(this, arguments);
    };
  }(),
  getPortfolio: function () {
    var _getPortfolio = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee6() {
      var options,
          _args6 = arguments;
      return _regenerator.default.wrap(function (_context7) {
        while (1) {
          switch (_context7.prev = _context7.next) {
            case 0:
              options = _args6.length > 0 && _args6[0] !== undefined ? _args6[0] : {};
              return _context7.abrupt("return", SolanaApi.fetch({
                endpoint: {
                  "method": "GET",
                  "group": "account",
                  "name": "getPortfolio",
                  "url": "/account/:network/:address/portfolio"
                },
                params: options
              }));

            case 2:
            case "end":
              return _context7.stop();
          }
        }
      }, _callee6);
    }));

    return function () {
      return _getPortfolio.apply(this, arguments);
    };
  }()
});
(0, _defineProperty2.default)(SolanaApi, "nft", {
  getNFTMetadata: function () {
    var _getNFTMetadata = (0, _asyncToGenerator2.default)( /*#__PURE__*/_regenerator.default.mark(function _callee7() {
      var options,
          _args7 = arguments;
      return _regenerator.default.wrap(function (_context8) {
        while (1) {
          switch (_context8.prev = _context8.next) {
            case 0:
              options = _args7.length > 0 && _args7[0] !== undefined ? _args7[0] : {};
              return _context8.abrupt("return", SolanaApi.fetch({
                endpoint: {
                  "method": "GET",
                  "group": "nft",
                  "name": "getNFTMetadata",
                  "url": "/nft/:network/:address/metadata"
                },
                params: options
              }));

            case 2:
            case "end":
              return _context8.stop();
          }
        }
      }, _callee7);
    }));

    return function () {
      return _getNFTMetadata.apply(this, arguments);
    };
  }()
});
var _default = SolanaApi;
exports.default = _default;