"""
The click command line — ``sprezzature-ux-laws``.

The twin of ``sprezzature-ux-laws-audit`` (argparse): same flags, same
handler, the other parser. Both build the same argument vector and hand it to
the same ``main``, so a flag cannot exist on one front door and be missing
from the other.

There is one tool here, not four, so this is a single command rather than a
group — the dispatcher shape the larger packages in this suite use would be
one sub-command deep and would only make the thing harder to type.

Click is the only parser here, and a base dependency rather than an extra:
this package carried no base dependencies at all, but with argparse removed
from the suite on 2026-10-25 no parser ships with Python, so an optional
click would mean an install whose own command does not run. The per-tool
script `sprezzature-ux-laws-audit` still needs nothing beyond it.


Author
------
Warith HARCHAOUI <warithmetics@deraison.ai>
"""

from __future__ import annotations

from pathlib import Path

import click
from sprezzature_ux_laws_scripts.audit_laws_of_ux import main as _audit

from sprezzature_ux_laws import LAWS


@click.command(
    name="sprezzature-ux-laws",
    context_settings={"help_option_names": ["-h", "--help"]},
    help=(
        "Static auditor for the canonical Laws of UX (Jon YABLONSKI, "
        "lawsofux.com): the fraction of each law that is decidable from "
        "the raw HTML text, with no browser and no human reviewer."
    ),
)
@click.version_option(package_name="sprezzature-ux-laws")
@click.argument(
    "targets",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--json",
    "json_",
    is_flag=True,
    default=False,
    help="Emit JSON instead of a text report.",
)
@click.option(
    "--strict",
    is_flag=True,
    default=False,
    help="Promote warnings to errors (any finding fails the run).",
)
@click.option(
    "--only",
    default="",
    help=(
        "Comma-separated subset of laws to run. Defaults to all. "
        f"Available: {','.join(sorted(LAWS))}."
    ),
)
@click.option("--ignore", default="", help="Comma-separated laws to skip.")
@click.option(
    "--fix",
    is_flag=True,
    default=False,
    help=(
        "Apply mechanical fixes in place for the laws that have a fixer. "
        "Idempotent. Combine with --dry-run to preview."
    ),
)
@click.option(
    "--dry-run",
    "dry_run",
    is_flag=True,
    default=False,
    help="With --fix, print what would change without touching the files.",
)
def main(
    targets: tuple[Path, ...],
    json_: bool,
    strict: bool,
    only: str,
    ignore: str,
    fix: bool,
    dry_run: bool,
) -> None:
    """Dispatch to the shared handler; propagate its exit code."""
    raise SystemExit(
        _audit(
            _as_argv(
                targets=targets,
                json_=json_,
                strict=strict,
                only=only,
                ignore=ignore,
                fix=fix,
                dry_run=dry_run,
            )
        )
    )


def _as_argv(
    *,
    targets: tuple[Path, ...],
    json_: bool,
    strict: bool,
    only: str,
    ignore: str,
    fix: bool,
    dry_run: bool,
) -> list[str]:
    """Rebuild the argument vector the argparse front door would parse.

    The shared ``main`` parses its own argv rather than taking a
    namespace, so the twin hands it one back. Reconstructing is uglier
    than calling a common handler — and it is what keeps there from being
    two code paths that can disagree about what a flag means.
    """
    argv: list[str] = [str(t) for t in targets]
    if json_:
        argv.append("--json")
    if strict:
        argv.append("--strict")
    if only:
        argv += ["--only", only]
    if ignore:
        argv += ["--ignore", ignore]
    if fix:
        argv.append("--fix")
    if dry_run:
        argv.append("--dry-run")
    return argv


if __name__ == "__main__":  # pragma: no cover
    main()
