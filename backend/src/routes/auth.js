import { Router } from 'express';
import auth from '../middleware/auth.js';
import { register, login, me } from '../controllers/authController.js';

const router = Router();

router.post('/register', register);
router.post('/login', login);
router.get('/me', auth, me);

export default router;
