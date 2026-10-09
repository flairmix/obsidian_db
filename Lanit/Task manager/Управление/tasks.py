"""SQLite is authoritative. Markdown and Canvas are generated projections."""
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from uuid import uuid4
import json
import re
import sqlite3
import yaml
from sqlalchemy import create_engine, select, event, delete
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session
from models import Base, Task, Dependency

FOLDERS = {'todo':'01 To Do', 'doing':'02 В работе', 'done':'03 Выполнено'}
LABELS = {'todo':'Запланировано','doing':'В работе','done':'Выполнено'}
PRIORITIES = ('Высокий', 'Средний', 'Низкий')

def day(value):
    if value in (None, ''): return None
    if isinstance(value, datetime): return value.date()
    return date.fromisoformat(str(value))

def now(): return datetime.now(timezone.utc).replace(tzinfo=None)

def frontmatter(path):
    text = path.read_text(encoding='utf-8-sig')
    lines = text.splitlines(keepends=True)
    if lines and lines[0].strip() == '---':
        for i in range(1,len(lines)):
            if lines[i].strip() == '---':
                meta = yaml.safe_load(''.join(lines[1:i])) or {}
                if not isinstance(meta,dict): raise ValueError(f'Некорректные свойства: {path}')
                return meta, ''.join(lines[i+1:])
    return {}, text

class TaskManager:
    def __init__(self, root):
        self.root = Path(root).expanduser().resolve()
        if not self.root.is_dir(): raise ValueError('Папка менеджера не найдена')
        (self.root/'Данные').mkdir(exist_ok=True)
        self.db_path = self.root/'Данные/tasks.sqlite3'
        self.engine = create_engine(URL.create('sqlite',database=str(self.db_path)))
        @event.listens_for(self.engine, 'connect')
        def configure(dbapi_connection, record):
            dbapi_connection.execute('PRAGMA foreign_keys=ON')
        Base.metadata.create_all(self.engine)

    def _get(self, session, key):
        task = session.get(Task, str(key))
        if task: return task
        found = list(session.scalars(select(Task).where(Task.title == str(key))))
        if len(found)!=1: raise ValueError(f'Нужен точный ID или уникальное название: {key}')
        return found[0]

    def tasks(self, status=None):
        if status is not None and status not in FOLDERS: raise ValueError('Статус: todo / doing / done')
        with Session(self.engine) as s:
            all_tasks = {t.id:t for t in s.scalars(select(Task))}
            deps = list(s.scalars(select(Dependency)))
            rows=[]
            for t in all_tasks.values():
                if status and t.status!=status: continue
                prerequisites=[d.prerequisite_id for d in deps if d.dependent_id==t.id]
                blocked=[i for i in prerequisites if all_tasks[i].status!='done']
                rows.append({'id':t.id,'название':t.title,'статус':t.status,'создано':t.created_on,
                    'срок':t.due_on,'начать':t.start_on,'завершено':t.completed_on,
                    'приоритет':t.priority,'проект':t.project,'оценка_ч':t.estimate_hours,
                    'зависит_от':prerequisites,'блокируют':blocked,'текст':t.body})
            return sorted(rows,key=lambda r:(r['срок'] or date.max,r['название'],r['id']))

    def create(self, title, due=None, created=None, start=None, priority='Средний',
               project='Личное', estimate=None, description='', steps=None):
        title=str(title).strip()
        if not title: raise ValueError('Название не должно быть пустым')
        if priority not in PRIORITIES: raise ValueError('Неизвестный приоритет')
        if estimate is not None and (not isinstance(estimate,(int,float)) or estimate<0):
            raise ValueError('Оценка — неотрицательное число часов')
        identifier=uuid4().hex
        body=description+'\n\n## Подзадачи\n'+'\n'.join('- [ ] '+str(x) for x in (steps or []))+'\n'
        with Session(self.engine) as s, s.begin():
            if s.scalar(select(Task).where(Task.title==title)): raise ValueError('Название уже существует')
            s.add(Task(id=identifier,title=title,status='todo',created_on=day(created) or date.today(),
                       due_on=day(due),start_on=day(start),completed_on=None,updated_at=now(),
                       priority=priority,project=project,estimate_hours=estimate,body=body,extra={}))
        self.export()
        return identifier

    def update(self, task_id, **fields):
        mapping={'название':'title','создано':'created_on','срок':'due_on','начать':'start_on',
                 'приоритет':'priority','проект':'project','оценка_ч':'estimate_hours','текст':'body'}
        if set(fields)-set(mapping): raise ValueError(f'Допустимые поля: {list(mapping)}')
        with Session(self.engine) as s, s.begin():
            t=self._get(s,task_id)
            for key,value in fields.items():
                if key in {'создано','срок','начать'}: value=day(value)
                if key=='приоритет' and value not in PRIORITIES: raise ValueError('Неизвестный приоритет')
                if key=='название' and (not isinstance(value,str) or not value.strip()): raise ValueError('Пустое название')
                if key=='оценка_ч' and value is not None and (not isinstance(value,(int,float)) or value<0): raise ValueError('Неверная оценка')
                if key in {'название','проект','текст'} and not isinstance(value,str): raise ValueError('Ожидается текст')
                setattr(t,mapping[key],value)
            t.updated_at=now()
        self.export()

    def delete(self, task_id):
        """Удалить задачу, её зависимости и экспортированную заметку."""
        import hashlib

        # Сначала проверяем задачу и находим её заметки.
        with Session(self.engine) as s:
            task = self._get(s, task_id)
            identifier = task.id

        filename = hashlib.sha256(
            identifier.encode()
        ).hexdigest()[:16] + ".md"

        notes = []

        for folder in FOLDERS.values():
            path = self.root / "Задачи" / folder / filename

            if path.exists():
                meta, _ = frontmatter(path)

                if (
                    meta.get("generated_by") == "sqlite-task-manager"
                    and str(meta.get("id")) == identifier
                ):
                    notes.append(path)

        # Копия базы перед удалением.
        backup_path = self.backup()

        with Session(self.engine) as s, s.begin():
            task = self._get(s, identifier)

            s.execute(
                delete(Dependency).where(
                    (Dependency.prerequisite_id == identifier)
                    | (Dependency.dependent_id == identifier)
                )
            )

            s.delete(task)

        for path in notes:
            path.unlink(missing_ok=True)

        self.export()

        return {
            "deleted_id": identifier,
            "backup": str(backup_path),
        }


    def move(self, task_id, status):
        if status not in FOLDERS: raise ValueError('Статус: todo / doing / done')
        with Session(self.engine) as s, s.begin():
            t=self._get(s,task_id)
            deps=list(s.scalars(select(Dependency)))
            if status in {'doing','done'}:
                blockers=[s.get(Task,d.prerequisite_id).title for d in deps
                          if d.dependent_id==t.id and s.get(Task,d.prerequisite_id).status!='done']
                if blockers: raise ValueError('Сначала завершите: '+', '.join(blockers))
            if t.status=='done' and status!='done':
                active=[s.get(Task,d.dependent_id).title for d in deps
                        if d.prerequisite_id==t.id and s.get(Task,d.dependent_id).status!='todo']
                if active: raise ValueError('Сначала верните зависимые задачи в To Do: '+', '.join(active))
            t.status=status
            t.completed_on=(t.completed_on or date.today()) if status=='done' else None
            t.updated_at=now()
        self.export()

    def depend(self, task_id, prerequisite_id):
        """Б зависит от А: depend(Б, А), на холсте А → Б."""
        with Session(self.engine) as s, s.begin():
            b=self._get(s,task_id); a=self._get(s,prerequisite_id)
            if a.id==b.id: raise ValueError('Задача не может зависеть от себя')
            edges=[(d.prerequisite_id,d.dependent_id) for d in s.scalars(select(Dependency))]
            if (a.id,b.id) in edges: return
            todo=[b.id]; visited=set()
            while todo:
                node=todo.pop()
                if node==a.id: raise ValueError('Связь создаёт циклическую зависимость')
                if node in visited: continue
                visited.add(node); todo.extend(v for u,v in edges if u==node)
            if b.status!='todo' and a.status!='done': raise ValueError('Верните зависимую задачу в To Do перед добавлением блокировки')
            s.add(Dependency(prerequisite_id=a.id,dependent_id=b.id))
        self.export()

    def undepend(self, task_id, prerequisite_id):
        with Session(self.engine) as s, s.begin():
            b=self._get(s,task_id); a=self._get(s,prerequisite_id)
            s.execute(delete(Dependency).where(Dependency.prerequisite_id==a.id,Dependency.dependent_id==b.id))
        self.export()

    def due(self, days=7):
        if not isinstance(days,int) or days<1: raise ValueError('days >= 1')
        return [r for r in self.tasks() if r['статус']!='done' and r['срок'] and r['срок']<date.today()+timedelta(days=days)]

    def import_notes(self, source):
        """Одноразовый импорт старой папки Задачи. Исходники не меняются, повтор пропускается.
        Неизвестная дата появления остаётся пустой; дата файла не подменяет её.
        """
        source=Path(source).expanduser().resolve()
        if not source.is_dir(): raise ValueError('Исходная папка не найдена')
        count=0
        with Session(self.engine) as s, s.begin():
            for status,folder in FOLDERS.items():
                for path in sorted((source/folder).glob('*.md')):
                    meta,body=frontmatter(path)
                    if meta.get('generated_by')=='sqlite-task-manager': continue
                    key=str(path.resolve())
                    if s.scalar(select(Task).where(Task.source_key==key)): continue
                    identifier=str(meta.get('id') or uuid4().hex)
                    if s.get(Task,identifier): raise ValueError(f'Повтор ID: {path.name}')
                    priority=meta.get('приоритет') or 'Средний'
                    if priority not in PRIORITIES: priority='Средний'
                    s.add(Task(id=identifier,title=path.stem,status=status,created_on=day(meta.get('создано')),
                         due_on=day(meta.get('срок')),start_on=day(meta.get('начать')),
                         completed_on=day(meta.get('завершено')),updated_at=now(),priority=priority,
                         project=str(meta.get('проект') or ''),estimate_hours=meta.get('оценка_ч'),body=body,
                         extra=json.loads(json.dumps(meta,default=str)),source_key=key))
                    s.flush(); count+=1
        self.export()
        return count

    def backup(self):
        folder=self.root/'Резервные копии'; folder.mkdir(exist_ok=True)
        path=folder/(datetime.now().strftime('%Y%m%d-%H%M%S-')+uuid4().hex[:6]+'.sqlite3')
        with sqlite3.connect(self.db_path) as src, sqlite3.connect(path) as dst: src.backup(dst)
        return path

    def export(self):
        from export_obsidian import export
        return export(self)

    sync_board=export
