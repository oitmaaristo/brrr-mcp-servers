#!/usr/bin/env python3
"""Flux kanban CLI. Usage:
  flux-tasks list [project] [--status=X]
  flux-tasks add <project> <title> [--status=planning|todo|in_progress|done] [--priority=0-3]
  flux-tasks update <id> --status=X
  flux-tasks comment <id> <msg>
  flux-tasks projects
  flux-tasks delete <id>
Env: FLUX_DATA (default /home/brrr/brrr-printer2/.flux/data.json), FLUX_AUTHOR (default claudia)
"""
import json, sys, os, uuid, datetime

DATA = os.environ.get("FLUX_DATA", "/home/brrr/brrr-printer2/.flux/data.json")

def load():
    with open(DATA) as f:
        return json.load(f)

def save(d):
    with open(DATA, "w") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

def uid():
    return uuid.uuid4().hex[:7]

def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

def main():
    args = sys.argv[1:]
    if not args or args[0] == "help":
        print(__doc__)
        return

    cmd = args[0]
    flags = {}
    for a in args:
        if a.startswith("--") and "=" in a:
            k, v = a.split("=", 1)
            flags[k.lstrip("-")] = v
    pos = [a for a in args[1:] if not a.startswith("--")]

    d = load()
    proj = {p["id"]: p["name"] for p in d["projects"]}
    pbn = {p["name"]: p["id"] for p in d["projects"]}

    if cmd == "projects":
        for p in d["projects"]:
            ts = [t for t in d["tasks"] if t["project_id"] == p["id"]]
            dn = sum(1 for t in ts if t["status"] == "done")
            print(f'  {p["id"]}  {p["name"]:20} ({dn}/{len(ts)} done)')

    elif cmd == "list":
        pf = pos[0] if pos else None
        sf = flags.get("status")
        for t in d["tasks"]:
            if pf and pf not in (t["project_id"], proj.get(t["project_id"], "")):
                continue
            if sf and t["status"] != sf:
                continue
            pn = proj.get(t["project_id"], "?")
            pri = t.get("priority", "-")
            s = t["status"]
            print(f'  [{s:12}] {t["id"]}  P{pri}  {t["title"]}  ({pn})')

    elif cmd == "add":
        if len(pos) < 2:
            print("Usage: flux-tasks add <project> <title>")
            return
        pid = pbn.get(pos[0], pos[0])
        if pid not in proj:
            print(f'Not found: {pos[0]}. Have: {", ".join(pbn.keys())}')
            return
        t = {
            "id": uid(),
            "title": " ".join(pos[1:]),
            "status": flags.get("status", "todo"),
            "depends_on": [],
            "comments": [],
            "project_id": pid,
            "priority": int(flags.get("priority", "2")),
            "created_at": now(),
            "updated_at": now(),
        }
        d["tasks"].append(t)
        save(d)
        print(f'  Created: {t["id"]} - {t["title"]} [{t["status"]}]')

    elif cmd == "update":
        if not pos:
            print("Usage: flux-tasks update <id> --status=X")
            return
        for t in d["tasks"]:
            if t["id"] == pos[0]:
                for k in ("status", "priority", "title"):
                    if k in flags:
                        t[k] = int(flags[k]) if k == "priority" else flags[k]
                t["updated_at"] = now()
                save(d)
                print(f'  Updated: {t["id"]} - {t["title"]} [{t["status"]}]')
                return
        print(f"Not found: {pos[0]}")

    elif cmd == "comment":
        if len(pos) < 2:
            print("Usage: flux-tasks comment <id> <msg>")
            return
        for t in d["tasks"]:
            if t["id"] == pos[0]:
                a = os.environ.get("FLUX_AUTHOR", "claudia")
                c = {"id": uid(), "body": " ".join(pos[1:]), "author": a, "created_at": now()}
                t["comments"].append(c)
                t["updated_at"] = now()
                save(d)
                print(f"  Comment added to {pos[0]}")
                return
        print(f"Not found: {pos[0]}")

    elif cmd == "delete":
        if not pos:
            print("Usage: flux-tasks delete <id>")
            return
        b = len(d["tasks"])
        d["tasks"] = [t for t in d["tasks"] if t["id"] != pos[0]]
        if len(d["tasks"]) < b:
            save(d)
            print(f"  Deleted: {pos[0]}")
        else:
            print(f"Not found: {pos[0]}")

    else:
        print(f"Unknown: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
