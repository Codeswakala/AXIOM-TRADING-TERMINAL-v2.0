import hashlib, os, sqlite3, subprocess, sys
BE = r"C:\Users\victo\.vscode\AXIOM\axiom\backend"
F, S = os.path.join(BE, "axiom_dev.db"), os.path.join(BE, "be10_int_scratch.db")

print("== R-0 FIELDED-FILE INTERROGATION (must be 0049/64/11) ==")
c = sqlite3.connect(f"file:{F}?mode=ro", uri=True)
rev = c.execute("SELECT version_num FROM alembic_version").fetchone()[0]
perms = c.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
cvs = c.execute("SELECT COUNT(*) FROM v2_computation_version").fetchone()[0]
print("fielded:", rev, perms, cvs)
assert (rev, perms, cvs) == ("20260905_0049", 64, 11), "FIELDED FILE TOUCHED - STOP, this is an incident"
print("fielded file: CLEAN, untouched")

print("\n== R-2 RE-CLONE SCRATCH FROM FIELDED ==")
import shutil; shutil.copyfile(F, S)
print("scratch sha:", hashlib.sha256(open(S, "rb").read()).hexdigest())

print("\n== R-3 APPLY 0050 ON SCRATCH (subprocess, output captured) ==")
env = dict(os.environ, AXIOM_DATABASE_URL=f"sqlite+aiosqlite:///{S.replace(os.sep, '/')}")
p = subprocess.run([sys.executable, "-m", "alembic", "upgrade", "head"],
                   cwd=BE, env=env, capture_output=True, text=True)
print(p.stdout); print(p.stderr, file=sys.stderr)
ups = [ln for ln in p.stdout.splitlines() if "Running upgrade" in ln]
print("UPGRADE LINES:", ups)
assert p.returncode == 0 and len(ups) == 1 and "20260905_0049 -> 20260908_0050" in ups[0], \
    "chain != exactly one 0049->0050 line - STOP"

print("\n== R-4 CENSUS (the B-3 tattoo, live) ==")
c = sqlite3.connect(f"file:{S}?mode=ro", uri=True)
trg = c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='trigger'").fetchone()[0]
prm = c.execute("SELECT COUNT(*) FROM v2_permission").fetchone()[0]
ap = c.execute("SELECT permission FROM v2_permission WHERE permission LIKE 'v2.account_context.%'").fetchall()
ace = c.execute("SELECT component, version, source_hash FROM v2_computation_version WHERE component='account_context_engine'").fetchall()
cvt = c.execute("SELECT COUNT(*) FROM v2_computation_version").fetchone()[0]
mrows = c.execute("SELECT source_symbol, instrument_id FROM v2_md_symbol_map WHERE source_id='exness_mt5_demo' ORDER BY source_symbol").fetchall()
srow = c.execute("SELECT source_id, kind FROM v2_md_source WHERE source_id='exness_mt5_demo'").fetchall()
print("triggers:", trg, "| permissions:", prm, "| acct-ctx:", ap)
print("compver ace:", ace, "| compver total:", cvt)
print("map rows:", mrows, "| count:", len(mrows)); print("source row:", srow)
SEAL = ["AUDUSDm","BTCUSDm","ETHUSDm","EURGBPm","EURUSDm","GBPUSDm","NZDUSDm",
        "SOLUSDm","USDCADm","USDCHFm","USDJPYm","XAUUSDm"]
assert {r[0] for r in mrows} == set(SEAL) and len(mrows) == 12, "sealed map mismatch - STOP"
assert (trg, prm, cvt) == (76, 65, 12), "census tattoo miss - STOP"
engsha = hashlib.sha256(open(os.path.join(BE, "app/v2/account_context/engine.py"), "rb").read()).hexdigest()
print("disk engine sha:", engsha)
print("compver source_hash == disk engine sha:", ace and ace[0][2] == engsha)

print("\n== R-6 DIGEST x3 ==")
try:
    import asyncio
    sys.path.insert(0, BE)
    os.environ["AXIOM_DATABASE_URL"] = f"sqlite+aiosqlite:///{S.replace(os.sep, '/')}"
    from app.db.session import get_db_session
    from app.v2.account_context.engine import compute_alignment
    async def go():
        ds = []
        async for s in get_db_session():
            for _ in range(3):
                r = await compute_alignment(s)
                ds.append(r.get("digest") if isinstance(r, dict) else getattr(r, "digest", str(r)))
        for d in ds: print("digest:", d)
        assert len(set(ds)) == 1, "digest not deterministic - STOP"
        print("3/3 digests identical")
    asyncio.run(go())
except Exception as e:
    print("R-6 EXC:", type(e).__name__, str(e)[:200], " - STOP, paste (name may differ; repaired from transcript)")

print("\n== REND ==")
