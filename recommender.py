import pandas as pd

from scoring import calculate_all_scores


def load_data():
    catalog = pd.read_csv(
        "data/01_product_catalog.csv"
    )

    specs = pd.read_csv(
        "data/02_specs.csv"
    )

    benchmark = pd.read_csv(
        "data/03_chipset_benchmark.csv"
    )

    data = catalog.merge(
        specs,
        on="product_id",
        how="inner"
    )

    data = data.merge(
        benchmark,
        left_on="chipset",
        right_on="chipset_name",
        how="left"
    )

    score_data = data.apply(
        lambda row: pd.Series(
            calculate_all_scores(row)
        ),
        axis=1
    )

    data = pd.concat(
        [data, score_data],
        axis=1
    )

    return data


def calculate_balanced_score(row):
    return (
        row["camera_score"]
        + row["gaming_score"]
        + row["battery_score"]
        + row["display_score"]
        + row["thin_light_score"]
    ) / 5


def calculate_new_value_score(row):
    price_million = row["price"] / 1000000

    if price_million <= 0:
        return 0

    raw_value = (
        row["balanced_score"]
        / price_million
    )

    # 12 điểm hiệu năng / 1 triệu
    # được coi là mức rất tốt
    value_score = raw_value / 12 * 100

    return round(
        min(value_score, 100),
        2
    )


def calculate_used_condition_score(row):
    battery_score = row[
        "battery_health_percent"
    ]

    exterior_mapping = {
        "like-new": 100,
        "good": 80,
        "fair": 60
    }

    exterior_score = exterior_mapping.get(
        row["exterior_condition"],
        60
    )

    warranty_score = (
        100
        if str(
            row["warranty_status"]
        ).lower() == "yes"
        else 0
    )

    score = (
        battery_score * 0.50
        + exterior_score * 0.30
        + warranty_score * 0.20
    )

    return round(score, 2)


def add_price_data(data, condition):
    if condition == "new":
        prices = pd.read_csv(
            "data/04a_price_new.csv"
        )

        prices["crawled_at"] = pd.to_datetime(
            prices["crawled_at"]
        )

        prices = prices.sort_values(
            "crawled_at"
        )

        prices = prices.drop_duplicates(
            "product_id",
            keep="last"
        )

        data = data.merge(
            prices,
            on="product_id",
            how="inner"
        )

        data = data[
            data["stock_status"]
            == "in_stock"
        ].copy()

        data["balanced_score"] = data.apply(
            calculate_balanced_score,
            axis=1
        )

        data["value_score"] = data.apply(
            calculate_new_value_score,
            axis=1
        )

    else:
        prices = pd.read_csv(
            "data/04b_price_used.csv"
        )

        prices["crawled_at"] = pd.to_datetime(
            prices["crawled_at"]
        )

        prices = prices.sort_values(
            "crawled_at"
        )

        prices = prices.drop_duplicates(
            "product_id",
            keep="last"
        )

        data = data.merge(
            prices,
            on="product_id",
            how="inner"
        )

        data["balanced_score"] = data.apply(
            calculate_balanced_score,
            axis=1
        )

        data[
            "condition_score"
        ] = data.apply(
            calculate_used_condition_score,
            axis=1
        )

        data[
            "base_value_score"
        ] = data.apply(
            calculate_new_value_score,
            axis=1
        )

        data["value_score"] = (
            data["base_value_score"] * 0.65
            + data["condition_score"] * 0.35
        )

    return data


def calculate_final_score(
    row,
    priorities
):
    score_mapping = {
        "camera": row["camera_score"],
        "gaming": row["gaming_score"],
        "battery": row["battery_score"],
        "display": row["display_score"],
        "thin_light": row[
            "thin_light_score"
        ]
    }

    if len(priorities) == 1:
        priority_score = score_mapping[
            priorities[0]
        ]

        final_score = (
            priority_score * 0.65
            + row["value_score"] * 0.20
            + row["balanced_score"] * 0.15
        )

    else:
        priority_1 = score_mapping[
            priorities[0]
        ]

        priority_2 = score_mapping[
            priorities[1]
        ]

        final_score = (
            priority_1 * 0.50
            + priority_2 * 0.30
            + row["value_score"] * 0.10
            + row["balanced_score"] * 0.10
        )

    return round(final_score, 2)


def generate_reason(row, priorities):
    reasons = []

    for priority in priorities:

        if priority == "gaming":
            reasons.append(
                f"Chip {row['chipset']} có "
                f"AnTuTu {int(row['antutu_score']):,}, "
                f"RAM {row['ram_gb']}GB và "
                f"màn hình {row['refresh_rate_hz']}Hz."
            )

        elif priority == "camera":
            if row["ois"] == 1:
                ois_text = "có OIS"
            else:
                ois_text = "không có OIS"

            reasons.append(
                f"Camera chính "
                f"{row['main_camera_mp']}MP, "
                f"{ois_text}, zoom quang "
                f"{row['optical_zoom_x']}x."
            )

        elif priority == "battery":
            reasons.append(
                f"Pin {row['battery_mah']}mAh, "
                f"sạc {row['charging_w']}W."
            )

        elif priority == "display":
            reasons.append(
                f"Màn hình {row['display_type']}, "
                f"{row['refresh_rate_hz']}Hz, "
                f"độ phân giải "
                f"{row['resolution_width']}x"
                f"{row['resolution_height']}."
            )

        elif priority == "thin_light":
            reasons.append(
                f"Khối lượng {row['weight_g']}g, "
                f"dày {row['thickness_mm']}mm."
            )

    return " ".join(reasons)


def recommend(
    min_budget,
    max_budget,
    condition,
    priorities,
    top_n=5
):
    data = load_data()

    data = add_price_data(
        data,
        condition
    )

    min_price = min_budget * 1000000
    max_price = max_budget * 1000000

    filtered = data[
        (data["price"] >= min_price)
        & (data["price"] <= max_price)
    ].copy()

    if filtered.empty:
        return filtered

    filtered[
        "final_score"
    ] = filtered.apply(
        lambda row: calculate_final_score(
            row,
            priorities
        ),
        axis=1
    )

    filtered[
        "reason"
    ] = filtered.apply(
        lambda row: generate_reason(
            row,
            priorities
        ),
        axis=1
    )

    filtered = filtered.sort_values(
        "final_score",
        ascending=False
    )

    return filtered.head(top_n)