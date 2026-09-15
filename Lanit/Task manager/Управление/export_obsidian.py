from pathlib import Path
from datetime import date, datetime
from uuid import uuid4
import hashlib
import re
import math
import json
import os
import tempfile
import yaml
from tasks import FOLDERS, LABELS, frontmatter

def write(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(dir=path.parent,suffix='.tmp')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f: f.write(text)
        os.replace(name,path)
    finally:
        if os.path.exists(name): os.unlink(name)

def export(manager):
    # Canvas file paths and Obsidian links are relative to the vault,
    # while generated files remain inside the task manager directory.
    root = Path(manager.root).resolve()
    explicit = getattr(manager, "vault_root", None)
    if explicit is not None:
        vault = Path(explicit).expanduser().resolve()
    else:
        candidates = [p for p in [root, *root.parents] if (p / ".obsidian").is_dir()]
        if len(candidates) != 1:
            raise ValueError("Задайте manager.vault_root = Path(...): корень открытого хранилища Obsidian")
        vault = candidates[0]
    if not vault.is_dir() or not root.is_relative_to(vault):
        raise ValueError("Папка менеджера должна находиться внутри manager.vault_root")
    def vault_path(relative):
        return (root / relative).relative_to(vault).as_posix()
    rows=manager.tasks(); by_id={r['id']:r for r in rows}
    # Horizontal position is status; vertical position is creation date.
    statuses = ('todo', 'doing', 'done')
    column = {status: index for index, status in enumerate(statuses)}
    def creation_key(row):
        value = row.get('создано')
        if isinstance(value, datetime): value = value.date()
        if isinstance(value, str): value = date.fromisoformat(value)
        return (value is None, value or date.max, row['название'].casefold(), row['id'])
    groups = {status: sorted((r for r in rows if r['статус'] == status), key=creation_key)
              for status in statuses}
    for row in rows:
        if row['статус'] not in column: raise ValueError('Неизвестный статус задачи')
        if any(p not in by_id for p in row['зависит_от']):
            raise ValueError('Отсутствующая задача в зависимости')
    def filename(row):
        title = re.sub(r'[<>:"/\\|?*\[\]#^\x00-\x1f]', '_', row['название'])
        title = title.strip().rstrip('. ')[:120].rstrip('. ') or 'Задача'
        if title.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL',
                *[f'COM{i}' for i in range(1, 10)], *[f'LPT{i}' for i in range(1, 10)]}:
            title = '_' + title
        return title + '.md'
    paths = {r['id']: f"Задачи/{FOLDERS[r['статус']]}/{filename(r)}" for r in rows}
    used = set()
    for identifier, relative in paths.items():
        key = relative.casefold()
        if key in used:
            raise ValueError(f'Совпадают имена файлов: {relative}. Измените название одной задачи.')
        used.add(key)
        target = root / relative
        if target.exists():
            meta, _ = frontmatter(target)
            if meta.get('generated_by') != 'sqlite-task-manager' or str(meta.get('id')) != identifier:
                raise FileExistsError(f'Файл принадлежит другой заметке: {target}')
    links = {key: vault_path(value) for key, value in paths.items()}
    CARD_WIDTH = 360
    COLUMN_STEP = 460
    nodes = []
    for status, title in zip(statuses, ('TO DO', 'В РАБОТЕ', 'ВЫПОЛНЕНО')):
        nodes.append({'id':'header-'+status,'type':'text','x':column[status]*COLUMN_STEP,'y':-90,
                      'width':CARD_WIDTH,'height':60,
                      'text':f"**{title} · {len(groups[status])}**"})
    positions = {}
    for status in statuses:
        group = groups[status]
        cursor_y = 0
        for index,r in enumerate(group):
            path=manager.root/paths[r['id']]
            meta={'generated_by':'sqlite-task-manager','id':r['id'],'aliases':[r['название']],
                  'создано':r['создано'],'срок':r['срок'],'начать':r['начать'],'завершено':r['завершено'],
                  'приоритет':r['приоритет'],'проект':r['проект'],'статус':LABELS[r['статус']],
                  'оценка_ч':r['оценка_ч'],'зависит_от':[f"[[{links[p]}]]" for p in r['зависит_от']]}
            deps='\n'.join(f"- [[{links[p]}|{by_id[p]['название']}]]" for p in r['зависит_от']) or 'Нет'
            created=str(r['создано'] or 'не указана'); due=str(r['срок'] or 'не назначен')
            overdue=r['статус']!='done' and r['срок'] and r['срок']<date.today()
            info=('⚠ Просрочена' if overdue else '')
            blocked='Ожидает: '+', '.join(by_id[i]['название'] for i in r['блокируют']) if r['блокируют'] else 'Зависимости выполнены' if r['зависит_от'] else 'Нет зависимостей'
            body=(f"# {r['название']}\n\n**Появилась:** {created}  \n**Срок:** {due} {info}  \n"
                  f"**Статус:** {LABELS[r['статус']]} · **Приоритет:** {r['приоритет']}  \n"
                  f"**Проект:** {r['проект'] or '—'}\n\n{blocked}\n\n## Содержание\n{r['текст']}\n\n## Зависит от\n{deps}\n")
            content='---\n'+yaml.safe_dump(meta,allow_unicode=True,sort_keys=False)+'---\n'+body
            if path.exists() and frontmatter(path)[0].get('generated_by')!='sqlite-task-manager':
                raise FileExistsError(f'Экспорт не заменит стороннюю заметку: {path}')
            write(path,content)
            # A text node links to the note without embedding its full contents.
            title = re.sub(r'\s+', ' ', r['название']).strip()
            title = title.replace('|', '¦').replace('[', '(').replace(']', ')')
            def display_day(value):
                if not value: return '—'
                if isinstance(value, str): value = date.fromisoformat(value)
                return value.strftime('%d.%m.%Y')
            created = display_day(r['создано'])
            deadline = display_day(r['срок'])
            # Allow long titles to wrap; retain compact sizes for ordinary tasks.
            lines = max(1, math.ceil(len(title) / 30))
            height = max(160, 100 + lines * 25)
            positions[r['id']] = (column[status] * COLUMN_STEP, cursor_y)
            nodes.append({
                'id':r['id'], 'type':'text',
                'text':f"[[{links[r['id']]}|{title}]]\n\nСоздано: {created}\n\nДедлайн: {deadline}",
                'x':column[status]*COLUMN_STEP, 'y':cursor_y,
                'width':CARD_WIDTH, 'height':height,
                'color':{'todo':'4','doing':'3','done':'5'}[status],
            })
            cursor_y += height + 35
    # Remove only this exporter's old status copies, never legacy notes.
    for folder in FOLDERS.values():
        for path in (manager.root/'Задачи'/folder).glob('*.md'):
            meta,_=frontmatter(path)
            identifier=str(meta.get('id',''))
            if meta.get('generated_by')=='sqlite-task-manager' and identifier in paths:
                if path.relative_to(manager.root).as_posix()!=paths[identifier]: path.unlink()
    edges=[]
    for r in rows:
        for p in r['зависит_от']:
            ax, ay = positions[p]
            bx, by = positions[r['id']]
            if ax < bx: from_side, to_side = 'right', 'left'
            elif ax > bx: from_side, to_side = 'left', 'right'
            elif ay < by: from_side, to_side = 'bottom', 'top'
            else: from_side, to_side = 'top', 'bottom'
            edges.append({'id':hashlib.sha256((p+'>'+r['id']).encode()).hexdigest()[:16],
                          'fromNode':p,'fromSide':from_side,'toNode':r['id'],'toSide':to_side,
                          'toEnd':'arrow','label':'сначала выполнить'})
    write(manager.root/'Доска задач.canvas',json.dumps({'nodes':nodes,'edges':edges},ensure_ascii=False,indent=2))
    # Update only folder predicates in the existing generated Bases file.
    base_path = root / "Сроки.base"
    if base_path.exists():
        data = yaml.safe_load(base_path.read_text(encoding="utf-8"))
        def adjust(value):
            if isinstance(value, dict): return {k: adjust(v) for k, v in value.items()}
            if isinstance(value, list): return [adjust(v) for v in value]
            if isinstance(value, str):
                for relative in ["Задачи", *["Задачи/" + f for f in FOLDERS.values()]]:
                    value = value.replace('file.inFolder(' + json.dumps(relative, ensure_ascii=False) + ')',
                                          'file.inFolder(' + json.dumps(vault_path(relative), ensure_ascii=False) + ')')
            return value
        write(base_path, yaml.safe_dump(adjust(data), allow_unicode=True, sort_keys=False))
    return len(rows)
