import { v4 as uuidv4 } from 'uuid';
import db from '../config/db.js';

const uuidToBinary = (uuid) => Buffer.from(uuid.replace(/-/g, ''), 'hex');

const binaryToUuid = (buf) => {
  if (!buf) return null;
  const hex = buf.toString('hex');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
};

const formatRecord = (row, userId) => ({
  id: binaryToUuid(row.id),
  hormone: row.hormone,
  result: row.result !== undefined && row.result !== null ? Number(row.result) : row.result,
  notes: row.notes || null,
  created_at: row.created_at ? new Date(row.created_at).toISOString() : null,
  user_id: userId
});

const Record = {
  async create({ userId, hormone, result, notes }) {
    const id = uuidv4();
    const idBinary = uuidToBinary(id);
    const userBinary = uuidToBinary(userId);

    await db.query(
      'INSERT INTO registers (id, hormone, result, user_id, notes) VALUES (?, ?, ?, ?, ?)',
      [idBinary, hormone, result, userBinary, notes || null]
    );

    return {
      id,
      hormone,
      result: Number(result),
      notes: notes || null,
      created_at: new Date().toISOString(),
      user_id: userId
    };
  },

  async findByUserId(userId) {
    const userBinary = uuidToBinary(userId);
    const [rows] = await db.query(
      'SELECT * FROM registers WHERE user_id = ? ORDER BY created_at ASC',
      [userBinary]
    );
    return rows.map((r) => formatRecord(r, userId));
  },

  async findByIdAndUserId(id, userId) {
    const idBinary = uuidToBinary(id);
    const userBinary = uuidToBinary(userId);
    const [rows] = await db.query(
      'SELECT * FROM registers WHERE id = ? AND user_id = ?',
      [idBinary, userBinary]
    );
    return rows[0] || null;
  },

  async update(id, userId, { hormone, result, notes }) {
    const idBinary = uuidToBinary(id);
    const userBinary = uuidToBinary(userId);
    const [resultUpdate] = await db.query(
      'UPDATE registers SET hormone = ?, result = ?, notes = ? WHERE id = ? AND user_id = ?',
      [hormone, result, notes || null, idBinary, userBinary]
    );
    return resultUpdate.affectedRows > 0;
  },

  async remove(id, userId) {
    const idBinary = uuidToBinary(id);
    const userBinary = uuidToBinary(userId);
    const [result] = await db.query(
      'DELETE FROM registers WHERE id = ? AND user_id = ?',
      [idBinary, userBinary]
    );
    return result.affectedRows > 0;
  },

  binaryToUuid,
  formatRecord
};

export default Record;
