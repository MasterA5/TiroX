import { Router } from 'express';
import auth from '../middleware/auth.js';
import {
  createRecord,
  getMyRecords,
  getUserRecords,
  getRecord,
  updateRecord,
  deleteRecord
} from '../controllers/recordsController.js';

const router = Router();

router.post('/', auth, createRecord);
router.get('/', auth, getMyRecords);
router.get('/user/:userId', auth, getUserRecords);
router.get('/:id', auth, getRecord);
router.put('/:id', auth, updateRecord);
router.delete('/:id', auth, deleteRecord);

export default router;
