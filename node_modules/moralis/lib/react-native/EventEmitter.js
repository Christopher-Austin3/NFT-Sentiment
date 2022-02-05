var EventEmitter = require('../../../react-native/Libraries/vendor/emitter/EventEmitter');

EventEmitter.prototype.on = EventEmitter.prototype.addListener;
module.exports = EventEmitter;