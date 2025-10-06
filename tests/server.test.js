const request = require('supertest');
const { expect } = require('chai');
const app = require('../server'); // Make sure server.js exports app

describe('User Authentication & API', function () {
  it('Serve the login page', async function () {
    const res = await request(app).get('/login');
    expect(res.status).to.equal(200);
  });

  it('Sign up a new user and login', async function () {
    const username = `testuser_${Date.now()}`;
    const password = 'testpass';

    await request(app).post('/signup').send({ username, password });

    const login = await request(app).post('/login').send({ username, password });
    expect(login.body.success).to.be.true;
  });

  it('Reject chat if not logged in', async function () {
    const res = await request(app).post('/chat').send({ message: 'hello' });
    expect(res.status).to.equal(401);
  });
});
