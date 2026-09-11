import hashlib, os, sqlite3, subprocess, sys, re
BE = os.getcwd()
F = os.path.join(BE, "axiom_dev.db")
if not os.path.isfile(F):
    raise SystemExit("act runs from backend dir only - STOP")

print("== P-1 CORPUS GATE (REM-001 + supersession + REM-010, three layers) ==")
tx9  = open(r"..\docs\evidence\V2_BE-9_SOURCE_TRANSCRIPT.md",  encoding="utf-8").read()
tx10 = open(r"..\docs\evidence\V2_BE-10_SOURCE_TRANSCRIPT.md", encoding="utf-8").read()
re_pin = r"`([^`\n\|]+\.py)`\s*\|[^|\n]*\|[^|\n]*\|\s*`([0-9a-f]{64})`"
pins = dict(re.findall(re_pin, tx9))
SUPER = {"app/v2/broker_read/contract.py":  "f2862af9a7ad28e9b468b2d5b84c47e3a363227778cc3d449db785894f785176",
         "app/v2/broker_read/sync.py":      "d1e5d4b56c881db4547dcea88ea2e4f34e8642509916907c0a228f47714dfa09",
         "tests/test_v2_be9_boundaries.py": "9ba9fd8290d5861911582a5286752c7ed5aee71c06e56acb9f4ac4337355f91f",
         "tests/test_v2_be9_contract.py":   "12733c46f5fe495513fe2f44b66eadee5845abb35b03ca0b97bdc23131610d5e"}
pins.update(SUPER)
pins.update(re.findall(re_pin, tx10))
assert len(pins) == 32, f"pin inventory {len(pins)} != 32 - STOP"
bad = []
for rel, want in sorted(pins.items()):
    p = rel.replace("/", os.sep)
    layer = "SUPER" if rel in SUPER else ("NEW/REPL" if dict(re.findall(re_pin, tx10)).get(rel) == want else "REM001")
    if not os.path.isfile(p): bad.append(rel); print("MISSING", rel); continue
    got = hashlib.sha256(open(p, "rb").read()).hexdigest()
    if got != want: bad.append(rel); print("FAIL ", layer, rel, "got", got, "want", want)
print(f"{len(pins)-len(bad)}/{len(pins)} bodies pin-exact (three-layer)")
assert not bad, "corpus gate fail - STOP now"

print("\n== P-2 FRESH GATE (fielded file pre-act) ==")
print("gate sha BEFORE:", hashlib.sha256(open(F, "rb").read()).hexdigest())
c = sqlite3.connect(f"file:{F}?mode=ro", uri=True)
f2 = (c.execute("SELECT version_num FROM alembic_version").fetchone()[0],
      c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'").fetchone()[0],
      c.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0],
      c.execute("SELECT COUNT(*) FROM v2_computation_version").fetchone()[0])
print("rev/triggers/permissions/compver:", f2)
assert f2 == ("20260905_0049", 76, 64, 11), "gate census miss - STOP"

print("\n== P-3 APPLY 0050 ON THE FIELDED FILE ==")
env = dict(os.environ, AXIOM_DATABASE_URL=f"sqlite+aiosqlite:///{F.replace(os.sep, '/')}")
print("APPLY-TARGET =", env["AXIOM_DATABASE_URL"])
p = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"],
                   cwd=BE, env=env, capture_output=True, text=True)
both = p.stdout + "\n" + p.stderr
ups = [ln.strip() for ln in both.splitlines() if "Running upgrade" in ln]
print("UPGRADE LINES:", ups)
assert p.returncode == 0 and len(ups) == 1 and "20260905_0049 -> 20260908_0050" in ups[0], \
    "chain != exactly one 0049->0050 line - STOP"
print("apply: PASS")

print("\n== P-4 POST-VERIFY ==")
c = sqlite3.connect(f"file:{F}?mode=ro", uri=True)
trg = c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'").fetchone()[0]
prm = c.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
ap  = c.execute("SELECT permission FROM v2_permission WHERE permission='v2.account_context.read'").fetchall()
ace = c.execute("SELECT component, version, source_hash FROM v2_computation_version WHERE component='account_context_engine'").fetchall()
cvt = c.execute("SELECT COUNT(*) FROM v2_computation_version").fetchone()[0]
mrows = c.execute("SELECT source_symbol, instrument_id FROM v2_md_symbol_map WHERE source_id='exness_mt5_demo' ORDER BY source_symbol").fetchall()
srow = c.execute("SELECT source_id, kind, authority, active FROM v2_md_source WHERE source_id='exness_mt5_demo'").fetchall()
print("triggers:", trg, "| perms:", prm, "| acct-ctx:", ap)
print("ace:", ace, "| compver total:", cvt)
print("map rows:", mrows)
print("source row:", srow)
SEAL = ["AUDUSDm","BTCUSDm","ETHUSDm","EURGBPm","EURUSDm","GBPUSDm","NZDUSDm",
        "SOLUSDm","USDCADm","USDCHFm","USDJPYm","XAUUSDm"]
assert [r[0] for r in mrows] == SEAL and len(mrows) == 12, "sealed map mismatch - STOP"
assert (trg, prm, cvt) == (76, 65, 12), "census tattoo miss - STOP"
d = hashlib.sha256(); rel = "app/v2/account_context/engine.py"
d.update(rel.encode()); d.update(b"\x00")
d.update(open(os.path.join(BE, rel.replace("/", os.sep)), "rb").read()); d.update(b"\x00")
assert ace[0] == ("account_context_engine", "ace-1.0.0", d.hexdigest()), "compver row mismatch - STOP"
print("compver rolling-hash: VERIFIED (fielded, live)")
import asyncio
sys.path.insert(0, BE)
os.environ["AXIOM_DATABASE_URL"] = f"sqlite+aiosqlite:///{F.replace(os.sep, '/')}"
from app.db.session import get_db_session
from app.v2.account_context.engine import compute_alignment
async def go():
    ds = []
    async for s in get_db_session():
        for _ in range(3):
            r = await compute_alignment(s)
            ds.append(r.digest)
    for x in ds: print("digest:", x)
    assert len(set(ds)) == 1, "digest nondeterminism - STOP"
    print("3/3 digests identical")
asyncio.run(go())
print("FIELDED sha AFTER (expect != BEFORE):", hashlib.sha256(open(F, "rb").read()).hexdigest())
print("\n== P-4 COMPLETE ==")
