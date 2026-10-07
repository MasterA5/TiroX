import { jest, describe, it, expect, beforeEach } from '@jest/globals';

jest.unstable_mockModule('../config/db.js', () => ({
  default: { query: jest.fn() }
}));

jest.unstable_mockModule('../models/User.js', () => ({
  default: {
    findByEmailOrUsername: jest.fn(),
    create: jest.fn(),
    findByEmail: jest.fn(),
    findById: jest.fn()
  }
}));

jest.unstable_mockModule('../models/Record.js', () => ({
  default: {
    binaryToUuid: jest.fn((buf) => {
      if (!buf) return null;
      const hex = buf.toString('hex');
      return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
    })
  }
}));

jest.unstable_mockModule('bcryptjs', () => ({
  default: {
    genSalt: jest.fn(),
    hash: jest.fn(),
    compare: jest.fn()
  }
}));

jest.unstable_mockModule('jsonwebtoken', () => ({
  default: {
    sign: jest.fn(() => 'mock-jwt-token'),
    verify: jest.fn(() => ({ id: '12345678-1234-1234-1234-123456789abc' }))
  }
}));

const { default: request } = await import('supertest');
const { default: User } = await import('../models/User.js');
const { default: Record } = await import('../models/Record.js');
const bcrypt = await import('bcryptjs');
const jwt = await import('jsonwebtoken');
const { default: app } = await import('../app.js');

describe('Auth Routes', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    jwt.default.sign.mockReturnValue('mock-jwt-token');
    jwt.default.verify.mockReturnValue({ id: '12345678-1234-1234-1234-123456789abc' });
  });

  describe('POST /api/auth/register', () => {
    it('deberia registrar un usuario nuevo exitosamente', async () => {
      User.findByEmailOrUsername.mockResolvedValue([]);
      bcrypt.default.genSalt.mockResolvedValue('salt');
      bcrypt.default.hash.mockResolvedValue('hashedPassword');
      User.create.mockResolvedValue('12345678-1234-1234-1234-123456789abc');

      const res = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'testuser',
          email: 'test@example.com',
          password: 'password123',
          first_name: 'Test',
          last_name: 'User',
          age: 15
        });

      expect(res.status).toBe(201);
      expect(res.body).toHaveProperty('token');
      expect(res.body.user).toHaveProperty('id');
      expect(res.body.user.username).toBe('testuser');
      expect(res.body.user.email).toBe('test@example.com');
      expect(res.body.user.first_name).toBe('Test');
      expect(res.body.user.last_name).toBe('User');
      expect(User.findByEmailOrUsername).toHaveBeenCalledTimes(1);
      expect(User.create).toHaveBeenCalledTimes(1);
    });

    it('deberia rechazar si el usuario o email ya existen', async () => {
      User.findByEmailOrUsername.mockResolvedValue([{ id: Buffer.from('abc', 'hex') }]);

      const res = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'existinguser',
          email: 'existing@example.com',
          password: 'password123',
          first_name: 'Existing',
          last_name: 'User',
          age: 14
        });

      expect(res.status).toBe(400);
      expect(res.body.message).toBe('User already exists');
      expect(User.findByEmailOrUsername).toHaveBeenCalledTimes(1);
      expect(User.create).not.toHaveBeenCalled();
    });

    it('deberia retornar 500 si hay un error del servidor', async () => {
      User.findByEmailOrUsername.mockRejectedValue(new Error('DB connection failed'));

      const res = await request(app)
        .post('/api/auth/register')
        .send({
          username: 'testuser',
          email: 'test@example.com',
          password: 'password123',
          first_name: 'Test',
          last_name: 'User',
          age: 15
        });

      expect(res.status).toBe(500);
      expect(res.body.message).toBe('Server error');
    });
  });

  describe('POST /api/auth/login', () => {
    it('deberia login exitoso con credenciales correctas', async () => {
      const fakeId = Buffer.from('12345678123456781234567812345678', 'hex');
      User.findByEmail.mockResolvedValue({
        id: fakeId,
        username: 'testuser',
        email: 'test@example.com',
        password: 'hashedPassword'
      });
      bcrypt.default.compare.mockResolvedValue(true);
      Record.binaryToUuid.mockReturnValue('12345678-1234-1234-1234-123456789abc');

      const res = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'test@example.com',
          password: 'password123'
        });

      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty('token');
      expect(res.body.user.username).toBe('testuser');
      expect(res.body.user.email).toBe('test@example.com');
    });

    it('deberia rechazar si el email no existe', async () => {
      User.findByEmail.mockResolvedValue(null);

      const res = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'noexist@example.com',
          password: 'password123'
        });

      expect(res.status).toBe(400);
      expect(res.body.message).toBe('Invalid credentials');
    });

    it('deberia rechazar si la password es incorrecta', async () => {
      const fakeId = Buffer.from('12345678123456781234567812345678', 'hex');
      User.findByEmail.mockResolvedValue({
        id: fakeId,
        username: 'testuser',
        email: 'test@example.com',
        password: 'hashedPassword'
      });
      bcrypt.default.compare.mockResolvedValue(false);

      const res = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'test@example.com',
          password: 'wrongpassword'
        });

      expect(res.status).toBe(400);
      expect(res.body.message).toBe('Invalid credentials');
    });

    it('deberia retornar 500 si hay un error del servidor', async () => {
      User.findByEmail.mockRejectedValue(new Error('DB error'));

      const res = await request(app)
        .post('/api/auth/login')
        .send({
          email: 'test@example.com',
          password: 'password123'
        });

      expect(res.status).toBe(500);
      expect(res.body.message).toBe('Server error');
    });
  });

  describe('GET /api/auth/me', () => {
    it('deberia retornar el usuario autenticado', async () => {
      User.findById.mockResolvedValue({
        id: '12345678-1234-1234-1234-123456789abc',
        username: 'testuser',
        email: 'test@example.com',
        first_name: 'Test',
        last_name: 'User',
        age: 15
      });

      const res = await request(app)
        .get('/api/auth/me')
        .set('Authorization', 'Bearer mock-jwt-token');

      expect(res.status).toBe(200);
      expect(res.body.user.username).toBe('testuser');
      expect(res.body.user.email).toBe('test@example.com');
      expect(res.body.user).not.toHaveProperty('password');
      expect(User.findById).toHaveBeenCalledWith('12345678-1234-1234-1234-123456789abc');
    });

    it('deberia rechazar si no hay token', async () => {
      const res = await request(app).get('/api/auth/me');

      expect(res.status).toBe(401);
      expect(User.findById).not.toHaveBeenCalled();
    });

    it('deberia rechazar si el token es invalido', async () => {
      jwt.default.verify.mockImplementation(() => { throw new Error('invalid'); });

      const res = await request(app)
        .get('/api/auth/me')
        .set('Authorization', 'Bearer invalid-token');

      expect(res.status).toBe(401);
      expect(User.findById).not.toHaveBeenCalled();
    });

    it('deberia retornar 404 si el usuario no existe', async () => {
      User.findById.mockResolvedValue(null);

      const res = await request(app)
        .get('/api/auth/me')
        .set('Authorization', 'Bearer mock-jwt-token');

      expect(res.status).toBe(404);
      expect(res.body.message).toBe('User not found');
    });
  });
});
