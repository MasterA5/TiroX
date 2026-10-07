import { jest, describe, it, expect, beforeEach, beforeAll } from '@jest/globals';

jest.unstable_mockModule('../config/db.js', () => ({
  default: { query: jest.fn() }
}));

jest.unstable_mockModule('../models/Record.js', () => ({
  default: {
    create: jest.fn(),
    findByUserId: jest.fn(),
    findByIdAndUserId: jest.fn(),
    update: jest.fn(),
    remove: jest.fn(),
    binaryToUuid: jest.fn((buf) => {
      if (!buf) return null;
      const hex = buf.toString('hex');
      return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
    }),
    formatRecord: jest.fn((row, userId) => ({
      id: 'aabbccdd-1122-3344-aabb-ccdd11223344',
      hormone: row.hormone,
      result: row.result,
      notes: row.notes || null,
      created_at: row.created_at ? new Date(row.created_at).toISOString() : null,
      user_id: userId
    }))
  }
}));

jest.unstable_mockModule('jsonwebtoken', () => ({
  default: {
    sign: jest.fn(() => 'mock-jwt-token'),
    verify: jest.fn(() => ({ id: 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee' }))
  }
}));

const { default: request } = await import('supertest');
const { default: Record } = await import('../models/Record.js');
const jwt = await import('jsonwebtoken');
const { default: app } = await import('../app.js');

describe('Records Routes', () => {
  const testUserId = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee';
  let token;

  beforeEach(() => {
    jest.clearAllMocks();
    jwt.default.sign.mockReturnValue('mock-jwt-token');
    jwt.default.verify.mockReturnValue({ id: testUserId });
    token = 'mock-jwt-token';
  });

  describe('POST /api/records', () => {
    it('deberia crear un registro exitosamente', async () => {
      Record.create.mockResolvedValue({
        id: 'record-uuid-1234-5678-9abc-def012345678',
        hormone: 'TSH',
        result: 4.50,
        notes: null,
        created_at: '2026-01-01T00:00:00.000Z',
        user_id: testUserId
      });

      const res = await request(app)
        .post('/api/records')
        .set('Authorization', `Bearer ${token}`)
        .send({ hormone: 'TSH', result: 4.50 });

      expect(res.status).toBe(201);
      expect(res.body.hormone).toBe('TSH');
      expect(res.body.result).toBe(4.50);
      expect(res.body.user_id).toBe(testUserId);
      expect(Record.create).toHaveBeenCalledWith({
        userId: testUserId,
        hormone: 'TSH',
        result: 4.50,
        notes: undefined
      });
    });

    it('deberia crear un registro con notas', async () => {
      Record.create.mockResolvedValue({
        id: 'record-uuid-1234-5678-9abc-def012345678',
        hormone: 'TSH',
        result: 4.5,
        notes: 'Ayuno previo',
        created_at: '2026-01-01T00:00:00.000Z',
        user_id: testUserId
      });

      const res = await request(app)
        .post('/api/records')
        .set('Authorization', `Bearer ${token}`)
        .send({ hormone: 'TSH', result: 4.50, notes: 'Ayuno previo' });

      expect(res.status).toBe(201);
      expect(Record.create).toHaveBeenCalledWith({
        userId: testUserId,
        hormone: 'TSH',
        result: 4.50,
        notes: 'Ayuno previo'
      });
    });

    it('deberia rechazar si faltan campos requeridos', async () => {
      const res = await request(app)
        .post('/api/records')
        .set('Authorization', `Bearer ${token}`)
        .send({ hormone: 'TSH' });

      expect(res.status).toBe(400);
      expect(res.body.message).toBe('Missing required fields');
      expect(Record.create).not.toHaveBeenCalled();
    });

    it('deberia rechazar si no hay token', async () => {
      const res = await request(app)
        .post('/api/records')
        .send({ hormone: 'TSH', result: 4.50 });

      expect(res.status).toBe(401);
      expect(res.body.message).toMatch(/no token/i);
    });

    it('deberia rechazar si el token es invalido', async () => {
      jwt.default.verify.mockImplementation(() => { throw new Error('invalid'); });

      const res = await request(app)
        .post('/api/records')
        .set('Authorization', 'Bearer invalid-token-here')
        .send({ hormone: 'TSH', result: 4.50 });

      expect(res.status).toBe(401);
      expect(res.body.message).toMatch(/token/i);
    });

    it('deberia retornar 500 si hay un error del servidor', async () => {
      Record.create.mockRejectedValue(new Error('DB error'));

      const res = await request(app)
        .post('/api/records')
        .set('Authorization', `Bearer ${token}`)
        .send({ hormone: 'T3', result: 1.20 });

      expect(res.status).toBe(500);
      expect(res.body.message).toBe('Server error');
    });
  });

  describe('GET /api/records', () => {
    it('deberia obtener todos los registros del usuario', async () => {
      Record.findByUserId.mockResolvedValue([
        { id: 'aabbccdd-1122-3344-aabb-ccdd11223344', hormone: 'TSH', result: 4.50, user_id: testUserId },
        { id: 'aabbccdd-1122-3344-aabb-ccdd11223344', hormone: 'T4', result: 8.20, user_id: testUserId }
      ]);

      const res = await request(app)
        .get('/api/records')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);
      expect(res.body.length).toBe(2);
      expect(res.body[0].hormone).toBe('TSH');
    });

    it('deberia retornar array vacio si no hay registros', async () => {
      Record.findByUserId.mockResolvedValue([]);

      const res = await request(app)
        .get('/api/records')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);
      expect(res.body.length).toBe(0);
    });

    it('deberia rechazar sin token', async () => {
      const res = await request(app).get('/api/records');
      expect(res.status).toBe(401);
    });
  });

  describe('GET /api/records/user/:userId', () => {
    it('deberia obtener los registros de un usuario especifico', async () => {
      const targetUserId = '11111111-2222-3333-4444-555555555555';
      Record.findByUserId.mockResolvedValue([
        { id: 'aabbccdd-1122-3344-aabb-ccdd11223344', hormone: 'TSH', result: 4.50, user_id: targetUserId },
        { id: 'aabbccdd-1122-3344-aabb-ccdd11223344', hormone: 'T4', result: 9.10, user_id: targetUserId }
      ]);

      const res = await request(app)
        .get(`/api/records/user/${targetUserId}`)
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);
      expect(res.body.length).toBe(2);
      expect(res.body[0].hormone).toBe('TSH');
    });

    it('deberia retornar array vacio si el usuario no tiene registros', async () => {
      Record.findByUserId.mockResolvedValue([]);

      const res = await request(app)
        .get('/api/records/user/11111111-2222-3333-4444-555555555555')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(Array.isArray(res.body)).toBe(true);
      expect(res.body.length).toBe(0);
    });

    it('deberia rechazar sin token', async () => {
      const res = await request(app).get('/api/records/user/11111111-2222-3333-4444-555555555555');
      expect(res.status).toBe(401);
    });
  });

  describe('GET /api/records/:id', () => {
    it('deberia obtener un registro especifico', async () => {
      Record.findByIdAndUserId.mockResolvedValue({ id: 'aabbccdd-1122-3344-aabb-ccdd11223344', hormone: 'TSH', result: 4.50 });
      Record.formatRecord.mockReturnValue({ id: 'aabbccdd-1122-3344-aabb-ccdd11223344', hormone: 'TSH', result: 4.50, user_id: testUserId });

      const res = await request(app)
        .get('/api/records/aabbccdd-1122-3344-aabb-ccdd11223344')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.hormone).toBe('TSH');
    });

    it('deberia retornar 404 si el registro no existe', async () => {
      Record.findByIdAndUserId.mockResolvedValue(null);

      const res = await request(app)
        .get('/api/records/00000000-0000-0000-0000-000000000000')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(404);
      expect(res.body.message).toBe('Record not found');
    });
  });

  describe('PUT /api/records/:id', () => {
    it('deberia actualizar un registro exitosamente', async () => {
      Record.update.mockResolvedValue(true);

      const res = await request(app)
        .put('/api/records/aabbccdd-1122-3344-aabb-ccdd11223344')
        .set('Authorization', `Bearer ${token}`)
        .send({ hormone: 'TSH Updated', result: 3.80 });

      expect(res.status).toBe(200);
      expect(res.body.message).toBe('Record updated');
    });

    it('deberia retornar 404 si el registro no existe o no pertenece al usuario', async () => {
      Record.update.mockResolvedValue(false);

      const res = await request(app)
        .put('/api/records/00000000-0000-0000-0000-000000000000')
        .set('Authorization', `Bearer ${token}`)
        .send({ hormone: 'TSH', result: 2.00 });

      expect(res.status).toBe(404);
      expect(res.body.message).toBe('Record not found or not authorized');
    });
  });

  describe('DELETE /api/records/:id', () => {
    it('deberia eliminar un registro exitosamente', async () => {
      Record.remove.mockResolvedValue(true);

      const res = await request(app)
        .delete('/api/records/aabbccdd-1122-3344-aabb-ccdd11223344')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(200);
      expect(res.body.message).toBe('Record deleted');
    });

    it('deberia retornar 404 si el registro no existe', async () => {
      Record.remove.mockResolvedValue(false);

      const res = await request(app)
        .delete('/api/records/00000000-0000-0000-0000-000000000000')
        .set('Authorization', `Bearer ${token}`);

      expect(res.status).toBe(404);
      expect(res.body.message).toBe('Record not found or not authorized');
    });
  });
});
