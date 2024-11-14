ALTER TABLE "attacks"
  ADD COLUMN "poison" attr_type
    NOT NULL
    DEFAULT 0;
ALTER TABLE "attacks"
  ADD COLUMN "poison_turn" attr_type
    NOT NULL
    DEFAULT 0;
ALTER TABLE "attacks"
  ADD COLUMN "burn" attr_type
    NOT NULL
    DEFAULT 0;
ALTER TABLE "attacks"
  ADD COLUMN "burn_turn" attr_type
    NOT NULL
    DEFAULT 0;
ALTER TABLE "attacks"
  ADD COLUMN "bleed" attr_type
    NOT NULL
    DEFAULT 0;
ALTER TABLE "attacks"
  ADD COLUMN "bleed_turn" attr_type
    NOT NULL
    DEFAULT 0;
ALTER TABLE "attacks"
  ADD COLUMN "stun" attr_type
    NOT NULL
    DEFAULT 0;