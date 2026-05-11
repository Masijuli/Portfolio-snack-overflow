BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "grocery_stores" (
  "store_id" integer,
  "store_name" text,
  "address" text,
  "open_time" time without time zone,
  "close_time" time without time zone,
  PRIMARY KEY ("store_id")
);

CREATE TABLE IF NOT EXISTS "recipe" (
  "recipe_id" integer,
  "recipe_name" text,
  "servings" integer,
  "instructions" text,
  PRIMARY KEY ("recipe_id")
);

CREATE TABLE IF NOT EXISTS "grocery_runs" (
  "run_id" integer,
  "store_id" integer,
  "bought_date" date,
  PRIMARY KEY ("run_id"),
  CONSTRAINT "FK_grocery_runs_store_id"
    FOREIGN KEY ("store_id")
      REFERENCES "grocery_stores"("store_id")
);

CREATE TABLE IF NOT EXISTS "grocery_list" (
  "grocery_list_id" integer,
  "list_name" text,
  PRIMARY KEY ("grocery_list_id")
);

CREATE TABLE IF NOT EXISTS "food_group" (
  "food_group_id" integer,
  "food_group_name" text,
  PRIMARY KEY ("food_group_id")
);

CREATE INDEX "AK" ON  "food_group" ("food_group_name");

CREATE TABLE IF NOT EXISTS "food" (
  "food_id" integer,
  "food_name" text,
  "food_group_id" integer,
  PRIMARY KEY ("food_id"),
  CONSTRAINT "FK_food_food_group_id"
    FOREIGN KEY ("food_group_id")
      REFERENCES "food_group"("food_group_id")
);

CREATE TABLE IF NOT EXISTS "units" (
  "unit_id" integer,
  "unit_name" text,
  "unit_type" text,
  PRIMARY KEY ("unit_id")
);

CREATE TABLE IF NOT EXISTS "grocery_list_items" (
  "grocery_list_item_id" integer,
  "grocery_list_id" integer,
  "food_id" integer,
  "notes" text,
  "auto_added" boolean,
  "quantity" numeric,
  "purchased" boolean,
  "unit_id" integer,
  PRIMARY KEY ("grocery_list_item_id"),
  CONSTRAINT "FK_grocery_list_items_grocery_list_id"
    FOREIGN KEY ("grocery_list_id")
      REFERENCES "grocery_list"("grocery_list_id"),
  CONSTRAINT "FK_grocery_list_items_food_id"
    FOREIGN KEY ("food_id")
      REFERENCES "food"("food_id"),
  CONSTRAINT "FK_grocery_list_items_unit_id"
    FOREIGN KEY ("unit_id")
      REFERENCES "units"("unit_id")
);

CREATE TABLE IF NOT EXISTS "ingredients" (
  "recipe_id" integer,
  "food_id" integer,
  "quantity" numeric,
  "unit_id" integer,
  PRIMARY KEY ("recipe_id", "food_id"),
  CONSTRAINT "FK_ingredients_food_id"
    FOREIGN KEY ("food_id")
      REFERENCES "food"("food_id"),
  CONSTRAINT "FK_ingredients_recipe_id"
    FOREIGN KEY ("recipe_id")
      REFERENCES "recipe"("recipe_id"),
  CONSTRAINT "FK_ingredients_unit_id"
    FOREIGN KEY ("unit_id")
      REFERENCES "units"("unit_id")
);

CREATE TABLE IF NOT EXISTS "usage_log" (
  "log_id" integer,
  "food_id" integer,
  "recipe_id" integer,
  "amount_used" numeric,
  "fully_depleted" boolean,
  "usage_date" date,
  "unit_id" integer,
  PRIMARY KEY ("log_id"),
  CONSTRAINT "FK_usage_log_recipe_id"
    FOREIGN KEY ("recipe_id")
      REFERENCES "recipe"("recipe_id"),
  CONSTRAINT "FK_usage_log_food_id"
    FOREIGN KEY ("food_id")
      REFERENCES "food"("food_id"),
  CONSTRAINT "FK_usage_log_unit_id"
    FOREIGN KEY ("unit_id")
      REFERENCES "units"("unit_id")
);

CREATE TABLE IF NOT EXISTS "storage" (
  "storage_id" integer,
  "location" text,
  "temperature" numeric,
  PRIMARY KEY ("storage_id")
);

CREATE TABLE IF NOT EXISTS "inventory" (
  "inventory_id" integer,
  "food_id" integer,
  "storage_id" integer,
  "run_id" integer,
  "purchase_price" numeric,
  "expiration_date" date,
  "opened_date" date,
  "quantity" numeric,
  "unit_id" integer,
  PRIMARY KEY ("inventory_id"),
  CONSTRAINT "FK_inventory_food_id"
    FOREIGN KEY ("food_id")
      REFERENCES "food"("food_id"),
  CONSTRAINT "FK_inventory_storage_id"
    FOREIGN KEY ("storage_id")
      REFERENCES "storage"("storage_id"),
  CONSTRAINT "FK_inventory_unit_id"
    FOREIGN KEY ("unit_id")
      REFERENCES "units"("unit_id"),
  CONSTRAINT "FK_inventory_run_id"
    FOREIGN KEY ("run_id")
      REFERENCES "grocery_runs"("run_id")
);

COMMIT TRANSACTION;
