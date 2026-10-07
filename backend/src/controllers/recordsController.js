import Record from '../models/Record.js';

export const createRecord = async (req, res) => {
  const { hormone, result, notes } = req.body;

  if (!hormone || result === undefined || result === null || result === '') {
    return res.status(400).json({ message: 'Missing required fields' });
  }

  try {
    const record = await Record.create({
      userId: req.user.id,
      hormone,
      result,
      notes
    });
    res.status(201).json(record);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};

export const getMyRecords = async (req, res) => {
  try {
    const records = await Record.findByUserId(req.user.id);
    res.json(records);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};

export const getUserRecords = async (req, res) => {
  try {
    const records = await Record.findByUserId(req.params.userId);
    res.json(records);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};

export const getRecord = async (req, res) => {
  try {
    const record = await Record.findByIdAndUserId(req.params.id, req.user.id);
    if (!record) return res.status(404).json({ message: 'Record not found' });

    res.json(Record.formatRecord(record, req.user.id));
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};

export const updateRecord = async (req, res) => {
  const { hormone, result, notes } = req.body;

  if (!hormone || result === undefined || result === null || result === '') {
    return res.status(400).json({ message: 'Missing required fields' });
  }

  try {
    const updated = await Record.update(req.params.id, req.user.id, { hormone, result, notes });
    if (!updated) return res.status(404).json({ message: 'Record not found or not authorized' });

    res.json({ message: 'Record updated' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};

export const deleteRecord = async (req, res) => {
  try {
    const deleted = await Record.remove(req.params.id, req.user.id);
    if (!deleted) return res.status(404).json({ message: 'Record not found or not authorized' });

    res.json({ message: 'Record deleted' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};
