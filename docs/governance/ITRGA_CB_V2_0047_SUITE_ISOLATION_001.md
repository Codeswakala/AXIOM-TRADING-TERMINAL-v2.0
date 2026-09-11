=====================================================================
ITRGA CORRECTION BRIEF — SUITE ISOLATION DEFECT (TWO DEF-BE1-05 TESTS)
ITRGA-CB-V2-0047-SUITE-ISOLATION-001 · v1.0.0 · 2026-09-04 · TO: DA
CC: Operator · Re: ITRGA-ISS-V2-0047-PACKS-006 (resume stopped at B5)
=====================================================================

FINDING (severity: blocks the 0047 terminal act's suite gate; class:
TEST-ISOLATION DEFECT in PRE-BE-7 code; NOT a BE-7 regression; NOT an
instrument defect; NO schema or product behavior change involved)

  tests/test_v2_integration.py::test_v2_error_returns_structured_safe_contract
  tests/test_v2_integration.py::test_v2_internal_error_is_contained_and_safe
  FAIL with "assert 200 == 503/500" on the operator workstation
  (Windows, Python 3.14.7, venv pins), while PASSing (as 972/0) on the
  DA acceptance environment at the identical byte set.

ROOT CAUSE (line-exact; two independent proofs):
  backend/app/main.py in create_app():

      FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"
      ...
      if FRONTEND_DIST.is_dir() and (FRONTEND_DIST / "index.html").is_file():
          ...
          @application.get("/{full_path:path}", include_in_schema=False)
          async def spa_fallback(full_path: str) -> FileResponse:
              reserved = ("api", "docs", "redoc", "openapi.json", "health", "ready", "ws")
              first = full_path.split("/", 1)[0]
              if first in reserved:
                  return FileResponse(FRONTEND_DIST / "index.html")

  The SPA catch-all registers ONLY when frontend/dist/index.html exists
  (mandatory on the operator's real terminal workstation; absent on the
  acceptance/CI environment). The error_probe_client fixture
  (test_v2_integration.py L481-501) creates the app and adds the
  /api/v1/v2/_test/* routes AFTER create_app(). Starlette matches routes
  in registration order, so with the dist present the catch-all matches
  the probe path first; "api" is in the reserved set and index.html is
  served -> HTTP 200, and the raise never executes.

PROOF 1 (field): operator transcript 2026-09-04 11:29 UTC: both tests
  fail with 200 status; warnings preamble shows
  AXIOM_ALLOW_INSECURE_DEV=true active; zero AXIOM_* env overrides on
  the box.

PROOF 2 (minimal repro, ITRGA sandbox, same package family): a FastAPI
  app registering the identical dist-conditional catch-all BEFORE the
  probe route returns "200 + SPA HTML" on GET /api/v1/v2/_test/*; the
  same app WITHOUT the catch-all propagates the raise (500). Toggle is
  purely the presence of frontend/dist/index.html.

REQUIRED RESOLUTION (DA implements; ITRGA reviews full-depth):
  R-1. Repair test isolation so BOTH tests PASS DETERMINISTICALLY with
       frontend/dist/index.html present AND absent. Implement within
       the fixture scope in tests/test_v2_integration.py (e.g., neutralize
       any registered "spa_fallback" route for the fixture's app
       instance while documenting the conditional-registration law in a
       comment citing this brief). Do NOT change create_app() or the
       SPA fallback semantics (contracted product behavior for the
       terminal UI).
  R-2. Zero behavior change to the application code.
  R-3. Suite cardinality MUST remain exactly the BO floor: 972 tests
       collected, ALL passing, zero skipped-new.
  R-4. Deliver the corrected file to the Operator through the standard
       channel with its sha256 hash declared in the delivery note.
  R-5. ITRGA verifies the fix full-depth (diff + rerun proof), then
       re-issues the completion instruction for
       ITRGA_V2_0047_APPLY_RESUME_PACK_V1.ps1 (unchanged; pure-read) and
       ITRGA_V2_0047_VERIFY_PACK_V5.ps1 (edition 2).

STATE SAFETY WHILE THIS BRIEF RUNS:
  Working DB remains at 20260903_0047 (valid; witnessed); rollback
  anchor operator-evidence\BE-7\0047-ANCHOR-axiom_dev.bak intact; the
  resume/verify instruments are inert stopped states; no writes needed
  before the corrected test file lands.
=====================================================================
