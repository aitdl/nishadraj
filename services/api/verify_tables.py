import sqlalchemy as sa

engine = sa.create_engine("postgresql://app_user:localdev123@localhost:5433/prathamone_os")
inspector = sa.inspect(engine)
tables = inspector.get_table_names()
targets = ["users", "audit_logs"]

for t in targets:
    if t in tables:
        cols = [c["name"] for c in inspector.get_columns(t)]
        print(f"[OK] {t}: {cols}")
    else:
        print(f"[MISSING] {t}")
