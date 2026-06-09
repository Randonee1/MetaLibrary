from __future__ import annotations

import argparse
import sys

from core import db
from core.items import add_item, get_item, item_path, list_items
from core.papers import PAPER_FIELDS, find_paper_by_url, get_paper, upsert_paper
from core.records import dump
from core.search import search_items


def print_result(data: object, as_json: bool) -> None:
    if as_json:
        print(dump(data))
        return
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                print("\t".join(str(row.get(key, "")) for key in row.keys()))
            else:
                print(row)
    elif isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    else:
        print(data)


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="print JSON output")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="library")
    add_common(parser)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="validate library health")

    db_parser = sub.add_parser("db", help="database commands")
    db_sub = db_parser.add_subparsers(dest="db_command", required=True)
    db_sub.add_parser("schema", help="print database schema")

    item = sub.add_parser("item", help="item (stored file) commands")
    item_sub = item.add_subparsers(dest="item_command", required=True)
    add = item_sub.add_parser("add", help="ingest a file as an item")
    add.add_argument("file")
    get = item_sub.add_parser("get", help="get an item and its paper record")
    get.add_argument("item_id")
    list_cmd = item_sub.add_parser("list", help="list items")
    list_cmd.add_argument("--limit", type=int, default=50)
    path_cmd = item_sub.add_parser("path", help="print an item's stored file path")
    path_cmd.add_argument("item_id")

    paper = sub.add_parser("paper", help="paper commands")
    paper_sub = paper.add_subparsers(dest="paper_command", required=True)
    paper_create = paper_sub.add_parser("create", help="create or update paper fields for an item")
    paper_create.add_argument("item_id")
    for field in PAPER_FIELDS:
        paper_create.add_argument("--" + field.replace("_", "-"), dest=field)
    paper_get = paper_sub.add_parser("get", help="get paper fields")
    paper_get.add_argument("item_id")
    paper_find = paper_sub.add_parser("find", help="find a paper by source URL (empty object if none)")
    paper_find.add_argument("--url", required=True)

    search = sub.add_parser("search", help="search items")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=50)

    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "check":
            db.ensure_schema()
            print("Library check passed")
            return 0
        if args.command == "db" and args.db_command == "schema":
            print(db.schema_for())
            return 0
        if args.command == "item":
            if args.item_command == "add":
                result = add_item(args.file)
            elif args.item_command == "get":
                result = get_item(args.item_id)
                if result is None:
                    raise ValueError(f"item not found: {args.item_id}")
            elif args.item_command == "path":
                path = item_path(args.item_id)
                if path is None:
                    raise ValueError(f"item not found: {args.item_id}")
                print(path)
                return 0
            else:
                result = list_items(args.limit)
            print_result(result, args.json)
            return 0
        if args.command == "paper":
            if args.paper_command == "create":
                fields = {field: getattr(args, field) for field in PAPER_FIELDS}
                result = upsert_paper(args.item_id, **fields)
            elif args.paper_command == "find":
                # Empty object (not an error) means "no such paper", so callers
                # can branch on the result without parsing stderr.
                result = find_paper_by_url(args.url) or {}
            else:
                result = get_paper(args.item_id)
                if result is None:
                    raise ValueError(f"paper not found: {args.item_id}")
            print_result(result, args.json)
            return 0
        if args.command == "search":
            print_result(search_items(args.query, args.limit), args.json)
            return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    parser.error("unhandled command")
    return 2


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
