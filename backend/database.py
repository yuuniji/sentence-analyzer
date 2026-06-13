# backend/database.py
import aiosqlite
from pathlib import Path
from typing import Dict, Any

DB_PATH = Path("data/analyzer.db")

class HistoryDB:
    def __init__(self):
        # 确保 data 目录存在
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    async def _init_db(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS analysis_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sentence TEXT NOT NULL,
                    output TEXT NOT NULL,
                    mode TEXT NOT NULL DEFAULT 'standard',
                    model TEXT NOT NULL DEFAULT 'gemini-2.5-flash',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # 自动迁移：尝试添加 context 字段
            try:
                await db.execute('ALTER TABLE analysis_records ADD COLUMN context TEXT')
            except aiosqlite.OperationalError:
                pass # 字段可能已存在
            await db.commit()

    async def save(self, sentence: str, output: str, mode: str, context: str = None) -> int:
        await self._init_db()
        async with aiosqlite.connect(DB_PATH) as db:
            cursor = await db.execute(
                'INSERT INTO analysis_records (sentence, output, mode, context) VALUES (?, ?, ?, ?)',
                (sentence, output, mode, context)
            )
            await db.commit()
            return cursor.lastrowid

    async def list_records(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        await self._init_db()
        offset = (page - 1) * page_size
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            # 获取总数
            cursor = await db.execute('SELECT COUNT(*) as count FROM analysis_records')
            row = await cursor.fetchone()
            total = row['count']
            
            # 获取记录
            cursor = await db.execute(
                'SELECT * FROM analysis_records ORDER BY created_at DESC LIMIT ? OFFSET ?',
                (page_size, offset)
            )
            rows = await cursor.fetchall()
            records = [dict(row) for row in rows]
            
            return {
                "total": total,
                "page": page,
                "page_size": page_size,
                "records": records
            }

    async def delete_record(self, record_id: int):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('DELETE FROM analysis_records WHERE id = ?', (record_id,))
            await db.commit()
