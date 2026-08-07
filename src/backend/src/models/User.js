import { v4 as uuidv4 } from 'uuid';
import db from '../config/db.js';

const uuidToBinary = (uuid) => Buffer.from(uuid.replace(/-/g, ''), 'hex');

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
  }
};

export default User;
