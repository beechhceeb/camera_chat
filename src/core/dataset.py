from config.settings import DB_PROMPT_SAVE_PATH

def format_inventory_context(df):
    # Select relevant columns
    cols = [
        "model_name",
        "brand",
        "primary_category",
        "product_type",
        "current_buy_price",
    ]
    df_sub = df[cols]

    # Create a string for each camera model
    lines = [
        f"{row['model_name']} ({row['brand']}, {row['primary_category']}, {row['product_type']}, £{row['current_buy_price']:.2f})"
        for _, row in df_sub.iterrows()
    ]

    # Join all lines into one context string
    inventory_context = "\n".join(lines)
    # save as txt
    with open(DB_PROMPT_SAVE_PATH, "w") as f:
        f.write(inventory_context)
    return inventory_context
