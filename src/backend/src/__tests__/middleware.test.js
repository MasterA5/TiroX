import { jest, describe, it, expect, beforeEach } from '@jest/globals';
import 'dotenv/config';

jest.unstable_mockModule('jsonwebtoken', () => ({
  default: {
    verify: jest.fn()
  }
}));

const jwt = await import('jsonwebtoken');
const { default: authMiddleware } = await import('../middleware/auth.js');

describe('Auth Middleware', () => {
  let mockReq;
  let mockRes;
  let mockNext;

  beforeEach(() => {
    jest.clearAllMocks();
    mockReq = { header: jest.fn() };
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn()
    };
    mockNext = jest.fn();
  });

  it('deberia dejar pasar si el token es valido', () => {
    jwt.default.verify.mockReturnValue({ id: 'test-user-id' });
    mockReq.header.mockReturnValue('Bearer valid-token');

    authMiddleware(mockReq, mockRes, mockNext);

    expect(mockNext).toHaveBeenCalled();
    expect(mockReq.user).toHaveProperty('id', 'test-user-id');
    expect(jwt.default.verify).toHaveBeenCalledWith('valid-token', process.env.JWT_SECRET);
  });

  it('deberia rechazar si no hay token', () => {
    mockReq.header.mockReturnValue(undefined);

    authMiddleware(mockReq, mockRes, mockNext);

    expect(mockRes.status).toHaveBeenCalledWith(401);
    expect(mockRes.json).toHaveBeenCalledWith({ message: 'No token, authorization denied' });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('deberia rechazar si el token es invalido', () => {
    jwt.default.verify.mockImplementation(() => { throw new Error('invalid token'); });
    mockReq.header.mockReturnValue('Bearer invalid-token-here');

    authMiddleware(mockReq, mockRes, mockNext);

    expect(mockRes.status).toHaveBeenCalledWith(401);
    expect(mockRes.json).toHaveBeenCalledWith({ message: 'Token is not valid' });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('deberia rechazar si el token esta expirado', () => {
    jwt.default.verify.mockImplementation(() => { throw new Error('jwt expired'); });
    mockReq.header.mockReturnValue('Bearer expired-token');

    authMiddleware(mockReq, mockRes, mockNext);

    expect(mockRes.status).toHaveBeenCalledWith(401);
    expect(mockRes.json).toHaveBeenCalledWith({ message: 'Token is not valid' });
    expect(mockNext).not.toHaveBeenCalled();
  });

  it('deberia manejar el header Authorization sin formato Bearer', () => {
    jwt.default.verify.mockImplementation(() => { throw new Error('invalid token'); });
    mockReq.header.mockReturnValue('just-a-token');

    authMiddleware(mockReq, mockRes, mockNext);

    expect(mockRes.status).toHaveBeenCalledWith(401);
    expect(mockRes.json).toHaveBeenCalledWith({ message: 'Token is not valid' });
  });
});
