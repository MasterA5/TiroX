import { v4 as uuidv4 } from 'uuid';
import db from '../config/db.js';

const uuidToBinary = (uuid) => Buffer.from(uuid.replace(/-/g, ''), 'hex');

const binaryToUuid = (buf) => {
  if (!buf) return null;
  const hex = buf.toString('hex');
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
};

const User = {
  async findByEmailOrUsername(email, username) {
    const [rows] = await db.query(
      'SELECT id FROM users WHERE email = ? OR username = ?',
      [email, username]
    );
    return rows;
  },

  async create({ username, email, password, first_name, last_name, age }) {
    const id = uuidv4();
    const idBinary = uuidToBinary(id);

    await db.query(
      'INSERT INTO users (id, username, email, password, first_name, last_name, age) VALUES (?, ?, ?, ?, ?, ?, ?)',
      [idBinary, username, email, password, first_name, last_name, age || null]
    );

    return id;
  },

  async findByEmail(email) {
    const [rows] = await db.query('SELECT * FROM users WHERE email = ?', [email]);
    return rows[0] || null;
  },

  async findById(id) {
    const idBinary = uuidToBinary(id);
    const [rows] = await db.query(
      'SELECT id, username, email, first_name, last_name, age FROM users WHERE id = ?',
      [idBinary]
    );
    const row = rows[0];
    if (!row) return null;

    return { ...row, id: binaryToUuid(row.id) };
  }
};

export default User;
