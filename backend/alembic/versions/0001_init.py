from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("owner", sa.String(length=200), nullable=True),
        sa.Column("internet_exposed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("data_sensitivity", sa.String(length=20), nullable=False, server_default="low"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_unique_constraint("uq_applications_name", "applications", ["name"])

    op.create_table(
        "findings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id"), nullable=False),
        sa.Column("tool_source", sa.String(length=50), nullable=False),
        sa.Column("tool_name", sa.String(length=120), nullable=True),
        sa.Column("title", sa.String(length=300), nullable=False),
        sa.Column("normalized_type", sa.String(length=120), nullable=True),
        sa.Column("cwe", sa.String(length=50), nullable=True),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("cvss", sa.Float(), nullable=True),
        sa.Column("exploit_available", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("internet_exposed", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="open"),
        sa.Column("detected_at", sa.DateTime(), nullable=False),
        sa.Column("fixed_at", sa.DateTime(), nullable=True),
        sa.Column("external_id", sa.String(length=200), nullable=True),
        sa.Column("raw", sa.Text(), nullable=True),
    )
    op.create_index("ix_findings_app_status", "findings", ["application_id", "status"])

    op.create_table(
        "risk_scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("application_id", sa.Integer(), sa.ForeignKey("applications.id"), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=20), nullable=False),
        sa.Column("calculated_at", sa.DateTime(), nullable=False),
        sa.Column("open_critical", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("open_high", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("open_medium", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("open_low", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("mttr_days", sa.Float(), nullable=True),
    )
    op.create_index("ix_scores_app_time", "risk_scores", ["application_id", "calculated_at"])

def downgrade():
    op.drop_index("ix_scores_app_time", table_name="risk_scores")
    op.drop_table("risk_scores")
    op.drop_index("ix_findings_app_status", table_name="findings")
    op.drop_table("findings")
    op.drop_constraint("uq_applications_name", "applications", type_="unique")
    op.drop_table("applications")
