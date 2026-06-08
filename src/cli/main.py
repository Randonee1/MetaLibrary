from __future__ import annotations

import argparse
import sys

from core import db
from core.items import create_item, get_item, list_items
from core.papers import PAPER_FIELDS, get_paper, upsert_paper
from core.records import dump
from core.search import search_items
from core.storage import add_attachment, attachment_path, list_attachments


def print_result(data: object, as_json: bool) -> None:
    if as_json:
        print(dump(data))
        return
    if isinstance(data, list):
        for row in data:
            if isinstance(row, dict):
                print("	".join(str(row.get(key, "")) for key in row.keys()))
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

    item = sub.add_parser("item", help="item commands")
    item_sub = item.add_subparsers(dest="item_command", required=True)
    create = item_sub.add_parser("create", help="create an item")
    create.add_argument("--type", required=True, dest="item_type")
    create.add_argument("--title", required=True)
    create.add_argument("--abstract")
    create.add_argument("--language")
    create.add_argument("--date")
    create.add_argument("--url")
    create.add_argument("--doi")
    create.add_argument("--isbn")
    get = item_sub.add_parser("get", help="get an item")
    get.add_argument("item_id")
    list_cmd = item_sub.add_parser("list", help="list items")
    list_cmd.add_argument("--limit", type=int, default=50)

    paper = sub.add_parser("paper", help="paper commands")
    paper_sub = paper.add_subparsers(dest="paper_command", required=True)
    paper_create = paper_sub.add_parser("create", help="create or update paper fields for an item")
    paper_create.add_argument("item_id")
    for field in PAPER_FIELDS:
        paper_create.add_argument("--" + field.replace("_", "-"), dest=field)
    paper_get = paper_sub.add_parser("get", help="get paper fields")
    paper_get.add_argument("item_id")

    attachment = sub.add_parser("attachment", help="attachment commands")
    attachment_sub = attachment.add_subparsers(dest="attachment_command", required=True)
    attachment_add = attachment_sub.add_parser("add", help="add a file attachment to an item")
    attachment_add.add_argument("item_id")
    attachment_add.add_argument("file")
    attachment_add.add_argument("--title")
    attachment_add.add_argument("--type", default="file", dest="attachment_type")
    attachment_list = attachment_sub.add_parser("list", help="list item attachments")
    attachment_list.add_argument("item_id")
    attachment_path_cmd = attachment_sub.add_parser("path", help="print an attachment file path")
    attachment_path_cmd.add_argument("attachment_id")

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
            if args.item_command == "create":
                result = create_item(
                    item_type=args.item_type,
                    title=args.title,
                    abstract=args.abstract,
                    language=args.language,
                    date=args.date,
                    url=args.url,
                    doi=args.doi,
                    isbn=args.isbn,
                )
            elif args.item_command == "get":
                result = get_item(args.item_id)
                if result is None:
                    raise ValueError(f"item not found: {args.item_id}")
            else:
                result = list_items(args.limit)
            print_result(result, args.json)
            return 0
        if args.command == "paper":
            if args.paper_command == "create":
                fields = {field: getattr(args, field) for field in PAPER_FIELDS}
                result = upsert_paper(args.item_id, **fields)
            else:
                result = get_paper(args.item_id)
                if result is None:
                    raise ValueError(f"paper not found: {args.item_id}")
            print_result(result, args.json)
            return 0
        if args.command == "attachment":
            if args.attachment_command == "add":
                result = add_attachment(
                    args.item_id,
                    args.file,
                    title=args.title,
                    attachment_type=args.attachment_type,
                )
                print_result(result, args.json)
                return 0
            if args.attachment_command == "list":
                print_result(list_attachments(args.item_id), args.json)
                return 0
            path = attachment_path(args.attachment_id)
            if path is None:
                raise ValueError(f"attachment not found: {args.attachment_id}")
            print(path)
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
