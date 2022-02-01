'use strict';

const assert = require('assert');
const vsda = require('./index');

describe('vsda module', () => {
  it('has signer interface', () => {
    assert.strictEqual(typeof vsda.signer, 'function');
    assert.strictEqual(typeof Object.getOwnPropertyDescriptor(
      vsda.signer.prototype, 'sign').value, 'function');
  });

  it('has validator interface', () => {
    assert.strictEqual(typeof vsda.validator, 'function');
    assert.strictEqual(typeof Object.getOwnPropertyDescriptor(
      vsda.validator.prototype, 'createNewMessage').value, 'function');
    assert.strictEqual(typeof Object.getOwnPropertyDescriptor(
      vsda.validator.prototype, 'validate').value, 'function');
  });

  it('can sign with a valid string input', () => {
    const signer = new vsda.signer();
    const validator = new vsda.validator();
    const message = validator.createNewMessage("test");
    const signed_message = signer.sign(message);
    assert.strictEqual(validator.validate(signed_message), "ok");
  })

  it('throws for invalid input', () => {
    const signer = new vsda.signer();
    const validator = new vsda.validator();
    assert.throws(() => {
      validator.createNewMessage()
    }, "/^Error: Wrong number of arguments$/");
    assert.throws(() => {
      validator.createNewMessage(1)
    }, "/^Error: Wrong type of argment. Expects a string.$/");

    assert.throws(() => {
      validator.validate(1, 2)
    }, "/^Error: Wrong number of arguments$/");
    assert.throws(() => {
      validator.validate(1)
    }, "/^Error: Wrong type of argment. Expects a string.$/");

    assert.throws(() => {
      signer.sign("test1", "test2")
    }, "/^Error: Wrong number of arguments$/");
    assert.throws(() => {
      signer.sign(undefined)
    }, "/^Error: Wrong type of argment. Expects a string.$/");
  })
});