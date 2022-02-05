"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

function _defineProperty(obj, key, value) {
  if (key in obj) {
    Object.defineProperty(obj, key, {
      value: value,
      enumerable: true,
      configurable: true,
      writable: true
    });
  } else {
    obj[key] = value;
  }

  return obj;
}
/**
 * Automatically generated code, via genSolanaAPI.js
 * Do not modify manually
 */


const axios = require('axios');

class SolanaApi {
  // URL will be changed when api is deployed
  static initialize({
    apiKey,
    serverUrl,
    Moralis = null
  }) {
    if (!serverUrl && !apiKey) {
      throw new Error('SolanaApi.initialize failed: initialize with apiKey or serverUrl');
    }

    if (apiKey) this.apiKey = apiKey;
    if (serverUrl) this.serverUrl = serverUrl;
    this.Moralis = Moralis;
  }

  static getBody(params, bodyParams) {
    if (!params || !bodyParams || !bodyParams.length) {
      return undefined;
    }

    let body = {};
    bodyParams.forEach(({
      key,
      type,
      required
    }) => {
      if (params[key] === undefined) {
        if (required) throw new Error(`param ${key} is required!`);
      } else if (type === this.BodyParamTypes.setBody) {
        body = params[key];
      } else {
        body[key] = params[key];
      } // remove the param so it doesn't also get added as a query param


      delete params[key];
    });
    return body;
  }

  static getParameterizedUrl(url, params) {
    if (!Object.keys(params).length) return url; // find url params, they start with :

    const requiredParams = url.split('/').filter(s => s && s.includes(':'));
    if (!requiredParams.length) return url;
    let parameterizedUrl = url;
    requiredParams.forEach(p => {
      // strip the : and replace with param value
      const key = p.substr(1);
      const value = params[key];

      if (!value) {
        throw new Error(`required param ${key} not provided`);
      }

      parameterizedUrl = parameterizedUrl.replace(p, value); // remove required param from param list
      // so it doesn't become part of the query params

      delete params[key];
    });
    return parameterizedUrl;
  }

  static getErrorMessage(error, url) {
    var _error$response, _error$response$data;

    return (error === null || error === void 0 ? void 0 : (_error$response = error.response) === null || _error$response === void 0 ? void 0 : (_error$response$data = _error$response.data) === null || _error$response$data === void 0 ? void 0 : _error$response$data.message) || (error === null || error === void 0 ? void 0 : error.message) || (error === null || error === void 0 ? void 0 : error.toString()) || `Solana API error while calling ${url}`;
  }

  static async fetch({
    endpoint,
    params
  }) {
    const {
      method = 'GET',
      url,
      bodyParams
    } = endpoint;

    if (this.Moralis) {
      const {
        User
      } = this.Moralis;
      const user = User.current();

      if (!params.address) {
        if (user) {
          params.address = user.get('solAddress');
        }
      }
    }

    if (!params.network) params.network = 'mainnet';
    if (!params.responseType) params.responseType = 'native';

    if (!this.apiKey) {
      return this.apiCall(endpoint.name, params);
    }

    try {
      const parameterizedUrl = this.getParameterizedUrl(url, params);
      const body = this.getBody(params, bodyParams);
      const response = await axios(this.baseURL + parameterizedUrl, {
        params,
        method,
        body,
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
          'x-api-key': this.apiKey
        }
      }); // Perform type regularization before return depending on response type option

      return response.data;
    } catch (error) {
      const msg = this.getErrorMessage(error, url);
      throw new Error(msg);
    }
  }

  static async apiCall(name, options) {
    if (!this.serverUrl) {
      throw new Error('SolanaAPI not initialized, run Moralis.start() first');
    }

    try {
      const http = axios.create({
        baseURL: this.serverUrl
      });
      const response = await http.post(`/functions/sol-${name}`, options, {
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        }
      });
      return response.data.result;
    } catch (error) {
      var _error$response2, _error$response2$data;

      if ((_error$response2 = error.response) !== null && _error$response2 !== void 0 && (_error$response2$data = _error$response2.data) !== null && _error$response2$data !== void 0 && _error$response2$data.error) {
        throw new Error(error.response.data.error);
      }

      throw error;
    }
  }

}

_defineProperty(SolanaApi, "baseURL", 'https://solana-gateway.moralis.io');

_defineProperty(SolanaApi, "BodyParamTypes", {
  setBody: 'set body',
  property: 'property'
});

_defineProperty(SolanaApi, "account", {
  balance: async (options = {}) => SolanaApi.fetch({
    endpoint: {
      "method": "GET",
      "group": "account",
      "name": "balance",
      "url": "/account/:network/:address/balance"
    },
    params: options
  }),
  getSPL: async (options = {}) => SolanaApi.fetch({
    endpoint: {
      "method": "GET",
      "group": "account",
      "name": "getSPL",
      "url": "/account/:network/:address/tokens"
    },
    params: options
  }),
  getNFTs: async (options = {}) => SolanaApi.fetch({
    endpoint: {
      "method": "GET",
      "group": "account",
      "name": "getNFTs",
      "url": "/account/:network/:address/nft"
    },
    params: options
  }),
  getPortfolio: async (options = {}) => SolanaApi.fetch({
    endpoint: {
      "method": "GET",
      "group": "account",
      "name": "getPortfolio",
      "url": "/account/:network/:address/portfolio"
    },
    params: options
  })
});

_defineProperty(SolanaApi, "nft", {
  getNFTMetadata: async (options = {}) => SolanaApi.fetch({
    endpoint: {
      "method": "GET",
      "group": "nft",
      "name": "getNFTMetadata",
      "url": "/nft/:network/:address/metadata"
    },
    params: options
  })
});

var _default = SolanaApi;
exports.default = _default;