"""
The click command line — ``sprezzature-ux-laws``.

The twin of ``sprezzature-ux-laws-audit`` (argparse): same flags, same
handler, the other parser. Both build the same argument vector and hand it to
the same ``main``, so a flag cannot exist on one front door and be missing
from the other.

There is one tool here, not four, so this is a single command rather than a
group — the dispatcher shape the larger packages in this suite use would be
one sub-command deep and would only make the thing harder to type.

Click is an extra (``[click]``), and the guarded import below is the reason
this package still installs into anything. The auditor has **no**
dependencies: standard library, milliseconds, no browser, which is what makes
it worth putting in a pre-commit hook. A twin that imported click at module
load would end that silently, because the failure arrives at the console
script rather than at the install.

Author
------
Warith HARCHAOUI <warithmetics@deraison.ai>
"""

from __future__ import annotations

import sys
from pathlib import Path

from sprezzature_ux_laws import LAWS

try:
    import click
except ImportError:  # pragma: no cover - exercised by a bare install

    def main(argv: list[str] | None = None) -> int:
        """Say which extra installs this command, and exit non-zero.

        The signature matches the real ``main`` exactly. Two conditional
        definitions that disagree are a trap: a caller who imports ``main``
        and passes an argv gets a TypeError on the machine where the extra is
        missing, and nowhere else.
        """
        del argv  # the message is the same whatever was asked for
        print(
            "sprezzature-ux-laws is the click front door, and click is an "
            "optional extra here:\n"
            "    pip install 'sprezzature-ux-laws[click]'\n"
            "The argparse front door, `sprezzature-ux-laws-audit`, needs "
            "nothing — this package has no base dependencies, which is what "
            "makes it cheap enough for a pre-commit hook.",
            file=sys.stderr,
        )
        return 1
else:
    from sprezzature_ux_laws_scripts.audit_laws_of_ux import main as _audit

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
    def main(  # type: ignore[misc]
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
